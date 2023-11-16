# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from ipaddress import ip_interface
from re import findall
from typing import TYPE_CHECKING

from ansible_collections.arista.avd.plugins.filter.range_expand import range_expand
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdError, AristaAvdMissingVariableError
from ansible_collections.arista.avd.plugins.plugin_utils.utils import default, get

if TYPE_CHECKING:
    from ansible_collections.arista.avd.plugins.plugin_utils.eos_designs_facts import EosDesignsFacts

    from .shared_utils import SharedUtils


class SdwanMixin:
    """
    Mixin Class providing a subset of SharedUtils
    Class should only be used as Mixin to the SharedUtils class
    Using type-hint on self to get proper type-hints on attributes across all Mixins.
    """

    @cached_property
    def sdwan(self.SharedUtils) -> bool:
        return self.shared_utils.avt_role is not None

    @cached_property
    def sdwan_site_name(self.SharedUtils) -> str | None:
        if not self.sdwan:
            return None
        return get(self.shared_utils.switch_data_combined, "wan_site", required=True)

    @cached_property
    def sdwan_site(self.SharedUtils) -> bool:
        if not self.sdwan:
            return False
        sites = get(self._hostvars, "sdwan_sites", required=True)
        return get_item(sites, "name", self.sdwan_site_name)

    @cached_property
    def sdwan_ha(self.SharedUtils) -> bool:
        return get(self.sdwan_site, "ha.enabled", False)

    @cached_property
    def sdwan_ha_interface(self: SharedUtils) -> str:
        # TODO
        return "Ethernet4"

    @cached_property
    def sdwan_ha_peer(self: SharedUtils) -> str | None:
        if not self.sdwan_ha:
            return None
        if self.switch_data_node_group_nodes[0]["name"] == self.hostname:
            return self.switch_data_node_group_nodes[1]["name"]
        elif self.switch_data_node_group_nodes[1]["name"] == self.hostname:
            return self.switch_data_node_group_nodes[0]["name"]

        raise AristaAvdError("Unable to find SDWAN HA peer within same node group")

    @cached_property
    def sdwan_ha_peer_router_id(self: SharedUtils) -> str:
        return self.get_sdwan_peer_fact("router_id")

    @cached_property
    def sdwan_ha_peer_ip_addresses(self: SharedUtils) -> list:
        return self.get_sdwan_peer_fact("ipv4_addresses")

    # TODO can the two function be reused with MLAG
    def get_sdwan_peer_fact(self: SharedUtils, key, required=True):
        return get(self.mlag_peer_facts, key, required=required, org_key=f"avd_switch_facts.({self.sdwan_peer}).switch.{key}")

    @cached_property
    def sdwan_peer_facts(self: SharedUtils) -> EosDesignsFacts | dict:
        return self.get_peer_facts(self.sdwan_peer, required=True)
