# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get, get_item

from .utils import UtilsMixin


class RouterPathSelectionMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    # TODO - MUST NOT RELY ON TYPE -> need knobs in node type key

    @cached_property
    def router_path_selection(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        if not self.shared_utils.wan:
            return None

        router_path_selection = {}

        if self.shared_utils.type in ["pathfinders", "rr"]:
            router_path_selection["peer_dynamic_source"] = "stun"

        path_groups = []
        for transport in get(self.shared_utils.switch_data_combined, "transports", []):
            path_groups.append(
                {
                    "name": transport.get("name"),
                    "id": self._get_transport_id(transport),
                    # TODO CHANGE NEXT
                    "ipsec_profile": "AUTOVPNTUNNEL",
                    # TODO handle multiple interfaces
                    "local_interfaces": self._get_local_interfaces(transport),
                    "dynamic_peers": self._get_dynamic_peers(),
                    "static_peers": self._get_static_peers(transport),
                }
            )

        router_path_selection["path_groups"] = path_groups

        # TODO Load balance policy - for now one policy with all path_groups
        load_balance_policies = []
        load_balance_policies.append({"name": "LBPOLICY", "path_groups": [pg.get("name") for pg in path_groups]})
        router_path_selection["load_balance_policies"] = load_balance_policies

        # TODO DPS policies - for now adding one default one - MAYBE NEED TO REMOVED
        policies = [{"name": "dps-policy-default", "default_match": {"load_balance": "LBPOLICY"}}]
        router_path_selection["policies"] = policies

        # TODO - Adding default VRF here - check if it makes sense later
        vrfs = [{"name": "default", "path_selection_policy": "dps-policy-default"}]
        router_path_selection["vrfs"] = vrfs

        router_path_selection = {key: value for key, value in router_path_selection.items() if value is not None}
        return router_path_selection

    def _get_transport_id(self, transport: dict) -> int:
        """
        TODO - implement stuff from Venkit
        """
        # HACK
        if transport["name"] == "MPLS-1":
            return 100
        if transport["name"] == "MPLS-2":
            return 200
        if transport["name"] == "INTERNET":
            return 300
        return 666

    def _get_local_interfaces(self, transport: dict) -> dict | None:
        """
        TODO - handle multiples interfaces ?
        TODO - handle multiples stun profiles
        """
        local_interface = {"name": transport.get("interface")}
        if self.shared_utils.type not in ["pathfinders", "rr"]:
            # This MUST be made better
            for wan_route_reflector, data in self._wan_route_reflectors.items():
                for wr_transport in data.get("transports"):
                    router_transports_name = [wr_transport["name"] for transport in get(self.shared_utils.switch_data_combined, "transports", [])]
                    if transport["name"] not in router_transports_name:
                        continue
                    # This stun profile name should probably be a fact to avoid having it underlay/stun.py and here in
                    # for manageability
                    stun_profile_name = f"{wan_route_reflector}-{transport['name']}"
                    local_interface["stun"] = {"server_profiles": [stun_profile_name]}

        return [local_interface]

    def _get_dynamic_peers(self) -> dict | None:
        """ """
        if self.shared_utils.type not in ["transit", "edge"]:
            return None
        return {"enabled": True}

    def _get_static_peers(self, transport: dict) -> list | None:
        """
        TODO generate peer static config
        """
        if self.shared_utils.type not in ["transit", "edge"]:
            return None
        static_peers = []
        # TODO need some way to loop through rr/pathfinders transports public_ips
        # TODO - probably need to filter on public IPs as I guess not needed for MPLS -> ask
        for wan_route_reflector, data in self._wan_route_reflectors.items():
            # TODO GUARDS GUARDS!!
            # TODO make next logic nicer.. rendering only if transport is present on the remote RR
            if not (transport_data := get_item(data["transports"], "name", transport["name"], default={})):
                continue
            ipv4_addresses = [transport_data.get("public_ip")]
            static_peers.append(
                {
                    "router_ip": data.get("router_id"),
                    "name": wan_route_reflector,
                    "ipv4_addresses": ipv4_addresses,
                }
            )
        return static_peers
