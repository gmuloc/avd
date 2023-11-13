# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

from .utils import UtilsMixin


class RouterPathSelectionMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_path_selection(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        if not self.shared_utils.autovpn_role:
            return None

        if not self.shared_utils.network_services_l3:
            return None

        # TODO make this better
        local_transports = get(self.shared_utils.switch_data_combined, "transports", [])
        if not local_transports:
            return None

        router_path_selection = {}

        for tenant in self._filtered_tenants:
            for vrf in tenant["vrfs"]:
                vrf_name = vrf.get("name")
                policy_name = f"dps-policy-{vrf_name}"

                # TODO DPS policies - for now adding one default one - MAYBE NEED TO REMOVED
                policies = [{"name": policy_name, "default_match": {"load_balance": "LBPOLICY"}}]
                router_path_selection["policies"] = policies

                # TODO - Adding default VRF here - check if it makes sense later
                vrfs = [{"name": vrf_name, "path_selection_policy": policy_name}]
                router_path_selection["vrfs"] = vrfs

        # TODO maybe strip empty
        return router_path_selection
