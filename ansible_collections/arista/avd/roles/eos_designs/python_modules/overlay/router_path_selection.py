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

    @cached_property
    def router_path_selection(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        if not self.shared_utils.autovpn_role:
            return None

        local_transports = get(self.shared_utils.switch_data_combined, "transports", [])

        if not local_transports:
            return None

        router_path_selection = {}

        if self.shared_utils.autovpn_role == "server":
            router_path_selection["peer_dynamic_source"] = "stun"

        path_groups = []
        # TODO - need to have default value in one place only -> maybe facts / shared_utils ?
        ipsec_profile_name = get(self._hostvars, "autovpn.control_plane.profile_name", "controlPlaneIpsecProfile")

        for transport in local_transports:
            path_groups.append(
                {
                    "name": transport.get("name"),
                    "id": self._get_transport_id(transport),
                    "ipsec_profile": ipsec_profile_name,
                    "local_interfaces": self._get_local_interfaces(transport),
                    "dynamic_peers": self._get_dynamic_peers(),
                    "static_peers": self._get_static_peers(transport),
                }
            )

        if self.shared_utils.avt_role:
            site_info = self._wan_site_data
            # TODO maybe a flag to check if ha is enabled
            if get(site_info, "ha.enabled") is True:
                # TODO provide way to overrid LAN_HA name
                path_groups.append(
                    {
                        "name": "LAN_HA",
                        # TODO fake transport structure
                        "id": self._get_transport_id({"name": "LAN_HA"}),
                        "flow_assignment": "lan",
                        # TODO edit if this should be a list
                        "local_interfaces": [{"name": get(site_info, "ha.interface", required=True)}],
                        # TODO peer_static with local_peer
                    }
                )

        router_path_selection["path_groups"] = path_groups

        # TODO Load balance policy - for now one policy with all path_groups
        load_balance_policies = []
        if path_groups := [pg.get("name") for pg in path_groups]:
            load_balance_policies.append({"name": "LBPOLICY", "path_groups": path_groups})
        if load_balance_policies:
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
        # TODO this should be handled better
        if transport["name"] == "LAN_HA":
            return 65535

        wan_transports = get(self.shared_utils.switch_data_combined, "transports")
        wan_transport = get_item(wan_transports, "name", transport["name"], required=True)
        if (wan_transport_id := wan_transport.get("path_group_id")) is not None:
            return wan_transport_id

        # TODO avoid hard coded transports
        if transport["name"] == "MPLS-1":
            return 100
        if transport["name"] == "MPLS-2":
            return 200
        if transport["name"] == "INTERNET":
            return 300
        return 666

    def _get_local_interfaces(self, transport: dict) -> list | None:
        """
        Generate the router_path_selection.local_interfaces list

        For AUTOVPN clients, configure the stun server profiles as appropriate
        """
        local_interfaces = []
        for interface in transport.get("interfaces", []):
            local_interface = {"name": interface.get("name")}
            if self.shared_utils.autovpn_role == "client":
                stun_server_profiles = [
                    self._stun_server_profile_name(wrr, transport["name"]) for wrr in self._get_wan_route_reflector_with_transport(transport["name"])
                ]
                if stun_server_profiles:
                    local_interface["stun"] = {"server_profiles": stun_server_profiles}

            local_interfaces.append(local_interface)

        return local_interfaces

    def _get_wan_route_reflector_with_transport(self, transport_name: str) -> list:
        """
        Helper that retrieves the wan_route_reflector on which the transport is configured
        TODO: maybe move to utils
        """
        res = []
        for wan_route_reflector, data in self._wan_route_reflectors.items():
            if get_item(data.get("transports", []), "name", transport_name):
                res.append(wan_route_reflector)
        return res

    def _get_dynamic_peers(self) -> dict | None:
        """ """
        if self.shared_utils.autovpn_role != "client":
            return None
        return {"enabled": True}

    def _get_static_peers(self, transport: dict) -> list | None:
        """
        TODO
        """
        if self.shared_utils.autovpn_role != "client":
            return None
        static_peers = []
        for wan_route_reflector, data in self._wan_route_reflectors.items():
            # TODO GUARDS GUARDS!!
            # TODO make next logic nicer.. rendering only if transport is present on the remote RR
            if not (transport_data := get_item(data["transports"], "name", transport["name"], default={})):
                continue
            for interface in transport_data.get("interfaces", []):
                ipv4_addresses = []
                if (ip_address := interface.get("ip_address")) is not None:
                    # TODO - removing mask using split but maybe a helper is clearer
                    ipv4_addresses.append(ip_address.split("/")[0])
                static_peers.append(
                    {
                        "router_ip": data.get("router_id"),
                        "name": wan_route_reflector,
                        "ipv4_addresses": ipv4_addresses,
                    }
                )
        return static_peers
