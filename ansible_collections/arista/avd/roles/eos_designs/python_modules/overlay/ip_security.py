# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.strip_empties import strip_null_from_data
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

from .utils import UtilsMixin


class IPSecMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def ip_security(self) -> dict | None:
        """
        ip_security set based on autovpn_ipsec data_model
        """
        if not self.shared_utils.autovpn_role:
            return None

        autovpn = get(self._hostvars, "autovpn", required=True)

        ike_policies = []
        sa_policies = []
        profiles = []

        ip_security = {"ike_policies": ike_policies, "sa_policies": sa_policies, "profiles": profiles}

        if (data_plane := get(autovpn, "data_plane", None)) is not None:
            ike_policy_name = get(data_plane, "ike_policy_name", "dataPlaneIkePolicy")
            sa_policy_name = get(data_plane, "sa_policy_name", "dataPlaneSaPolicy")
            profile_name = get(data_plane, "profile_name", "dataPlaneIpsecProfile")
            key = get(data_plane, "ipsec_key", required=True)

            ike_policies.append(self._ike_policy(ike_policy_name))
            sa_policies.append(self._sa_policy(sa_policy_name))
            profiles.append(self._profile(profile_name, ike_policy_name, sa_policy_name, key))

            # For data plane, adding this
            ip_security["key_controller"] = self._key_controller(profile_name)

        if (control_plane := get(autovpn, "control_plane", None)) is not None:
            ike_policy_name = get(control_plane, "ike_policy_name", "controlPlaneIkePolicy")
            sa_policy_name = get(control_plane, "sa_policy_name", "controlPlaneSaPolicy")
            profile_name = get(control_plane, "profile_name", "controlPlaneIpsecProfile")
            key = get(control_plane, "ipsec_key", required=True)

            ike_policies.append(self._ike_policy(ike_policy_name))
            sa_policies.append(self._sa_policy(sa_policy_name))
            profiles.append(self._profile(profile_name, ike_policy_name, sa_policy_name, key))

            if not ip_security.get("key_controller"):
                # If there is not data plane IPSec profile, use the control plane one for key controller
                ip_security["key_controller"] = self._key_controller(profile_name)

        return strip_null_from_data(ip_security)

    def _ike_policy(self, name: str) -> dict | None:
        """
        Return an IKE policy
        """
        return {
            "name": name,
            "local_id": self.shared_utils.router_id,
        }

    def _sa_policy(self, name: str) -> dict | None:
        """
        Return an SA policy
        """
        return {"name": name}

    def _profile(self, profile_name: str, ike_policy_name: str, sa_policy_name: str, key: str) -> dict | None:
        """
        Return one IPsec Profile
        """
        return {
            "name": profile_name,
            "ike_policy": ike_policy_name,
            "sa_policy": sa_policy_name,
            "connection": "start",
            "shared_key": key,
            "dpd": {"interval": 10, "time": 50, "action": "clear"},
            "mode": "transport",
        }

    def _key_controller(self, profile_name: str) -> dict | None:
        """
        Return a key_controller structure if the device is not a RR or pathfinder
        """
        if self.shared_utils.autovpn_role != "client":
            return None

        return {"profile": profile_name}
