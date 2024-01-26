# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ansible_collections.arista.avd.plugins.filter.convert_dicts import convert_dicts
from ansible_collections.arista.avd.plugins.filter.default import default
from ansible_collections.arista.avd.plugins.filter.natural_sort import natural_sort
from ansible_collections.arista.avd.plugins.filter.range_expand import range_expand
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdError, AristaAvdMissingVariableError
from ansible_collections.arista.avd.plugins.plugin_utils.merge import merge
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get, get_item, unique

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class FilteredTenantsMixin:
    """
    Mixin Class providing a subset of SharedUtils
    Class should only be used as Mixin to the SharedUtils class
    Using type-hint on self to get proper type-hints on attributes across all Mixins.
    """

    @cached_property
    def filtered_tenants(self: SharedUtils) -> list[dict]:
        """
        Return sorted tenants list from all network_services_keys and filtered based on filter_tenants.
        Keys of Tenant data model will be converted to lists.
        All sub data models like vrfs and l2vlans are also converted and filtered.
        """
        if not self.any_network_services:
            return []

        filtered_tenants = []
        filter_tenants = self.filter_tenants
        for network_services_key in self.network_services_keys:
            tenants = convert_dicts(get(self.hostvars, network_services_key["name"]), "name")
            for tenant in tenants:
                if tenant["name"] in filter_tenants or "all" in filter_tenants:
                    tenant["l2vlans"] = self.filtered_l2vlans(tenant)
                    tenant["vrfs"] = self.filtered_vrfs(tenant)
                    filtered_tenants.append(tenant)

        no_vrf_default = all(vrf["name"] != "default" for tenant in filtered_tenants for vrf in tenant["vrfs"])
        if self.wan_role is not None and no_vrf_default:
            filtered_tenants.append(
                {
                    "name": "WAN_DEFAULT",
                    "vrfs": [
                        {
                            "name": "default",
                            "vrf_id": 1,
                            "svis": [],
                            "l3_interfaces": [],
                            "bgp_peers": [],
                            "ipv6_static_routes": [],
                            "static_routes": [],
                            "loopbacks": [],
                            "additional_route_targets": [],
                        }
                    ],
                    "l2vlans": [],
                }
            )
        elif self.wan_role:
            # It is enough to check only the first occurence of default VRF as some other piece of code
            # checks that if the VRF is in multiple tenants, the configuration is consistent.
            for tenant in filtered_tenants:
                if (vrf_default := get_item(tenant["vrfs"], "name", "default")) is None:
                    continue
                if "evpn" in vrf_default.get("address_families", ["evpn"]):
                    if self.underlay_filter_peer_as:
                        raise AristaAvdError(
                            "WAN configuration requires EVPN to be enabled for VRF 'default'. Got 'address_families: {vrf_default['address_families']}."
                        )
                break

        return natural_sort(filtered_tenants, "name")

    def filtered_l2vlans(self: SharedUtils, tenant: dict) -> list[dict]:
        """
        Return sorted and filtered l2vlan list from given tenant.
        Filtering based on l2vlan tags.
        """
        if "l2vlans" not in tenant:
            return []

        l2vlans: list[dict] = natural_sort(convert_dicts(tenant["l2vlans"], "id"), "id")
        l2vlans = [
            l2vlan
            for l2vlan in l2vlans
            if self.is_accepted_vlan(l2vlan) and ("all" in self.filter_tags or set(l2vlan.get("tags", ["all"])).intersection(self.filter_tags))
        ]
        # Set tenant key on all l2vlans
        for l2vlan in l2vlans:
            l2vlan.update({"tenant": tenant["name"]})

        return l2vlans

    def is_accepted_vlan(self: SharedUtils, vlan: dict) -> bool:
        """
        Check if vlan is in accepted_vlans list
        If filter.only_vlans_in_use is True also check if vlan id or trunk group is assigned to connected endpoint
        """
        vlan_id = int(vlan["id"])

        if vlan_id not in self.accepted_vlans:
            return False

        if not self.filter_only_vlans_in_use:
            # No further filtering
            return True

        if vlan_id in self.endpoint_vlans:
            return True

        # Picking this up from facts so this would fail if accessed when shared_utils is run before facts
        # TODO see if this can be optimized
        endpoint_trunk_groups = set(self.get_switch_fact("endpoint_trunk_groups", required=False) or [])
        if self.enable_trunk_groups and vlan.get("trunk_groups") and endpoint_trunk_groups.intersection(vlan["trunk_groups"]):
            return True

        return False

    @cached_property
    def accepted_vlans(self: SharedUtils) -> list[int]:
        """
        The 'vlans' switch fact is a string representing a vlan range (ex. "1-200").
        For l2 switches return intersection of vlans from this switch and vlans from uplink switches.
        For anything else return the expanded vlans from this switch.
        """
        switch_vlans = self.get_switch_fact("vlans", required=False)
        if not switch_vlans:
            return []
        switch_vlans_list = range_expand(switch_vlans)
        accepted_vlans = [int(vlan) for vlan in switch_vlans_list]
        if self.uplink_type != "port-channel":
            return accepted_vlans

        uplink_switches = unique(self.uplink_switches)
        uplink_switches = [uplink_switch for uplink_switch in uplink_switches if uplink_switch in self.all_fabric_devices]
        for uplink_switch in uplink_switches:
            uplink_switch_facts = self.get_peer_facts(uplink_switch, required=True)
            uplink_switch_vlans = uplink_switch_facts.get("vlans", [])
            uplink_switch_vlans_list = range_expand(uplink_switch_vlans)
            uplink_switch_vlans_list = [int(vlan) for vlan in uplink_switch_vlans_list]
            accepted_vlans = [vlan for vlan in accepted_vlans if vlan in uplink_switch_vlans_list]

        return accepted_vlans

    def filtered_vrfs(self: SharedUtils, tenant: dict) -> list[dict]:
        """
        Return sorted and filtered vrf list from given tenant.
        Filtering based on svi tags, l3interfaces and filter.always_include_vrfs_in_tenants.
        Keys of VRF data model will be converted to lists.
        """
        filtered_vrfs = []

        always_include_vrfs_in_tenants = get(self.switch_data_combined, "filter.always_include_vrfs_in_tenants", default=[])

        vrfs: list[dict] = natural_sort(convert_dicts(tenant.get("vrfs", []), "name"), "name")
        for vrf in vrfs:
            # Storing tenant on VRF for use by child objects like SVIs
            vrf["tenant"] = tenant["name"]
            bgp_peers = natural_sort(convert_dicts(vrf.get("bgp_peers"), "ip_address"), "ip_address")
            vrf["bgp_peers"] = [bgp_peer for bgp_peer in bgp_peers if self.hostname in bgp_peer.get("nodes", [])]
            vrf["static_routes"] = [route for route in get(vrf, "static_routes", default=[]) if self.hostname in get(route, "nodes", default=[self.hostname])]
            vrf["ipv6_static_routes"] = [
                route for route in get(vrf, "ipv6_static_routes", default=[]) if self.hostname in get(route, "nodes", default=[self.hostname])
            ]
            vrf["svis"] = self.filtered_svis(vrf)
            vrf["l3_interfaces"] = [
                l3_interface
                for l3_interface in get(vrf, "l3_interfaces", default=[])
                if (
                    self.hostname in get(l3_interface, "nodes", default=[])
                    and l3_interface.get("ip_addresses") is not None
                    and l3_interface.get("interfaces") is not None
                )
            ]
            vrf["loopbacks"] = [loopback for loopback in get(vrf, "loopbacks", default=[]) if self.hostname == get(loopback, "node")]

            if self.vtep is True:
                evpn_l3_multicast_enabled = default(get(vrf, "evpn_l3_multicast.enabled"), get(tenant, "evpn_l3_multicast.enabled"))
                if evpn_l3_multicast_enabled is True and not self.evpn_multicast:
                    raise AristaAvdError(
                        f"'evpn_l3_multicast: true' under VRF {vrf['name']} or Tenant {tenant['name']}; this requires 'evpn_multicast' to also be set to true."
                    )

                if self.evpn_multicast:
                    vrf["_evpn_l3_multicast_enabled"] = evpn_l3_multicast_enabled

                    rps = []
                    for rp_entry in default(get(vrf, "pim_rp_addresses"), get(tenant, "pim_rp_addresses"), []):
                        if self.hostname in get(rp_entry, "nodes", default=[self.hostname]):
                            for rp_ip in get(
                                rp_entry,
                                "rps",
                                required=True,
                                org_key=f"pim_rp_addresses.rps under VRF '{vrf['name']}' in Tenant '{tenant['name']}'",
                            ):
                                rp_address = {"address": rp_ip}
                                if (rp_groups := get(rp_entry, "groups")) is not None:
                                    if (acl := rp_entry.get("access_list_name")) is not None:
                                        rp_address["access_lists"] = [acl]
                                    else:
                                        rp_address["groups"] = rp_groups

                                rps.append(rp_address)

                    if rps:
                        vrf["_pim_rp_addresses"] = rps

                    for evpn_peg in default(get(vrf, "evpn_l3_multicast.evpn_peg"), get(tenant, "evpn_l3_multicast.evpn_peg"), []):
                        if self.hostname in evpn_peg.get("nodes", [self.hostname]) and rps:
                            vrf["_evpn_l3_multicast_evpn_peg_transit"] = evpn_peg.get("transit")
                            break

            if (
                vrf["svis"]
                or vrf["l3_interfaces"]
                or vrf["loopbacks"]
                or "all" in always_include_vrfs_in_tenants
                or tenant["name"] in always_include_vrfs_in_tenants
            ):
                filtered_vrfs.append(vrf)

            vrf["additional_route_targets"] = [
                rt
                for rt in get(vrf, "additional_route_targets", default=[])
                if (
                    self.hostname in get(rt, "nodes", default=[self.hostname])
                    and rt.get("address_family") is not None
                    and rt.get("route_target") is not None
                    and rt.get("type") in ["import", "export"]
                )
            ]

        return filtered_vrfs

    @cached_property
    def svi_profiles(self: SharedUtils) -> list[dict]:
        """
        Return list of svi_profiles

        The key "nodes" is filtered to only contain one item with the relevant dict from "nodes" or {}
        """
        svi_profiles = convert_dicts(get(self.hostvars, "svi_profiles", default=[]), "profile")
        for svi_profile in svi_profiles:
            svi_profile["nodes"] = convert_dicts(svi_profile.get("nodes", []), "node")
            svi_profile["nodes"] = [get_item(svi_profile["nodes"], "node", self.hostname, default={})]

        return svi_profiles

    def get_merged_svi_config(self: SharedUtils, svi: dict) -> list[dict]:
        """
        Return structured config for one svi after inheritance

        Handle inheritance of node config as svi_profiles in two levels:

        First variables will be merged
        svi > svi_profile > svi_parent_profile --> svi_cfg
        &
        svi.nodes.<hostname> > svi_profile.nodes.<hostname> > svi_parent_profile.nodes.<hostname> --> svi_node_cfg

        Then svi is updated with the result of merging svi_node_cfg over svi_cfg
        svi_node_cfg > svi_cfg --> svi
        """
        svi_profile = {"nodes": [{}]}
        svi_parent_profile = {"nodes": [{}]}

        svi["nodes"] = convert_dicts(svi.get("nodes", []), "node")
        svi["nodes"] = [get_item(svi["nodes"], "node", self.hostname, default={})]

        if (svi_profile_name := svi.get("profile")) is not None:
            svi_profile = get_item(self.svi_profiles, "profile", svi_profile_name, default={})

        if (svi_parent_profile_name := svi_profile.get("parent_profile")) is not None:
            svi_parent_profile = get_item(self.svi_profiles, "profile", svi_parent_profile_name, default={})

        # deepmerge all levels of config - later vars override previous.
        # Using destructive_merge=False to avoid having references to profiles and other data.
        # Instead it will be doing deep copies inside merge.
        merged_svi = merge(
            svi_parent_profile,
            svi_profile,
            svi,
            svi_parent_profile["nodes"][0],
            svi_profile["nodes"][0],
            svi["nodes"][0],
            list_merge="replace",
            destructive_merge=False,
        )

        # Override structured configs since we don't want to deep-merge those
        merged_svi["structured_config"] = default(
            svi["nodes"][0].get("structured_config"),
            svi_profile["nodes"][0].get("structured_config"),
            svi_parent_profile["nodes"][0].get("structured_config"),
            svi.get("structured_config"),
            svi_profile.get("structured_config"),
            svi_parent_profile.get("structured_config"),
        )

        # Override bgp.structured configs since we don't want to deep-merge those
        merged_svi.setdefault("bgp", {})["structured_config"] = default(
            get(svi["nodes"][0], "bgp.structured_config"),
            get(svi_profile["nodes"][0], "bgp.structured_config"),
            get(svi_parent_profile["nodes"][0], "bgp.structured_config"),
            get(svi, "bgp.structured_config"),
            get(svi_profile, "bgp.structured_config"),
            get(svi_parent_profile, "bgp.structured_config"),
        )
        return merged_svi

    def filtered_svis(self: SharedUtils, vrf: dict) -> list[dict]:
        """
        Return sorted and filtered svi list from given tenant vrf.
        Filtering based on accepted vlans since eos_designs_facts already
        filtered that on tags and trunk_groups.
        """
        svis: list[dict] = natural_sort(convert_dicts(vrf.get("svis", []), "id"), "id")
        svis = [svi for svi in svis if self.is_accepted_vlan(svi)]

        # Handle svi_profile inheritance
        svis = [self.get_merged_svi_config(svi) for svi in svis]

        # Perform filtering on tags after merge of profiles, to support tags being set inside profiles.
        svis = [svi for svi in svis if "all" in self.filter_tags or set(svi.get("tags", ["all"])).intersection(self.filter_tags)]

        # Set tenant key on all SVIs
        for svi in svis:
            svi.update({"tenant": vrf["tenant"]})

        return svis

    @cached_property
    def endpoint_vlans(self: SharedUtils) -> list:
        endpoint_vlans = self.get_switch_fact("endpoint_vlans", required=False)
        if not endpoint_vlans:
            return []
        return [int(id) for id in range_expand(endpoint_vlans)]

    def get_vrf_id(self: SharedUtils, vrf, required: bool = True) -> int | None:
        vrf_id = default(vrf.get("vrf_id"), vrf.get("vrf_vni"))
        if vrf_id is None:
            if required:
                raise AristaAvdMissingVariableError(f"'vrf_id' or 'vrf_vni' for VRF '{vrf['name']} must be set.")
            return None
        return int(vrf_id)

    @cached_property
    def vrfs(self: SharedUtils) -> list:
        """
        Return the list of vrfs to be defined on this switch

        Ex. ["default", "prod"]
        """
        if not self.network_services_l3:
            return []

        vrfs = set()
        for tenant in self.filtered_tenants:
            for vrf in tenant["vrfs"]:
                vrfs.add(vrf["name"])

        return natural_sort(vrfs)
