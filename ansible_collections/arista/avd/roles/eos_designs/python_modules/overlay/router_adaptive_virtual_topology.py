# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get, get_item

from .utils import UtilsMixin


class RouterAdaptiveVirtualTopologyMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_adaptive_virtual_topology(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        # TODO could be an issue between transit / edge / .. site -> turning a site transit should be easier
        #     than
        if not self.shared_utils.avt_role:
            return None

        router_adaptive_virtual_topology = {}

        sites = get(self._hostvars, "sdwan_sites", required=True)
        dev_site = get(self.shared_utils.switch_data_combined, "wan_site", required=True)
        # or should we look for IP
        site = get_item(sites, "name", dev_site)

        router_adaptive_virtual_topology["topology_role"] = self.shared_utils.avt_role
        router_adaptive_virtual_topology["region"] = get(site, "region", required=True)
        router_adaptive_virtual_topology["zone"] = get(site, "zone", required=True)
        router_adaptive_virtual_topology["site"] = {"name": dev_site, "id": get(site, "id", required=True)}

        # TODO - handle Policy/Profile/VRF here

        return router_adaptive_virtual_topology
