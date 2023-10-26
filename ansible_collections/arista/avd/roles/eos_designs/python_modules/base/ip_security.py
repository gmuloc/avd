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
        if self.shared_utils.wan is False:
            return None

        autovpn = get(self._hostvars, "autovpn", required=True)

        ip_security = {
            "ike_policies": self._ike_policies(),
            "sa_policies": self._sa_policies(),
            "profiles": self._profiles(autovpn),
            "key_controller": self._key_controller(),
        }

        return strip_null_from_data(ip_security)

    def _ike_policies(self) -> dict | None:
        """
        Return the IKE policies

        TODO: allow for configurable name
        """
        return [
            {
                "name": "IKEAUTOVPN",
                "local_id": self.shared_utils.router_id,
            }
        ]

    def _sa_policies(self) -> dict | None:
        """
        Return the SA policies

        TODO: allow for configurable name
        """
        return [{"name": "SAAUTOVPN"}]

    def _profiles(self, autovpn: dict) -> dict | None:
        """
        Return the required IPSec Profiles

        TODO: return data plane profile for WAN
        TODO: allow for configurable name
        """
        return [
            {
                "name": "AUTOVPNTUNNEL",
                "ike_policy": "IKEAUTOVPN",
                "sa_policy": "SAAUTOVPN",
                "connection": "start",
                "shared_key": get(autovpn, "control_plane.ipsec_key", required=True),
                "dpd": {"interval": 10, "time": 50, "action": "clear"},
                "mode": "transport",
            }
        ]

    def _key_controller(self) -> dict | None:
        """
        Return a key_controller structure if the device is not a RR or pathfinder

        TODO: allow for configurable name
        """
        # TODO try to avoid using hostvars
        if self.shared_utils.type not in ["edge", "transit"]:
            return None

        return {"profile": "AUTOVPNTUNNEL"}
