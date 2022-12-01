from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import default, get

from .utils import UtilsMixin


class RouterIsisMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_isis(self) -> dict | None:
        """
        return structured config for router_isis
        """
        if self._underlay_router is not True:
            return None

        if self._underlay_routing_protocol not in ["isis", "isis-ldp", "isis-sr", "isis-sr-ldp"]:
            return None

        router_isis = {
            "instance": get(self._hostvars, "switch.isis_instance_name"),
            "log_adjacency_changes": True,
            "net": get(self._hostvars, "switch.isis_net"),
            "router_id": self._router_id,
            "is_type": get(self._hostvars, "switch.is_type"),
            "address_family": ["ipv4 unicast"],
            "isis_af_defaults": [f"maximum-paths {get(self._hostvars, 'isis_maximum_paths')}"],
        }

        # no passive interfaces
        no_passive_interfaces = []
        for link in self._underlay_links:
            if link["type"] == "underlay_p2p":
                no_passive_interfaces.append(link["interface"])
        if self._mlag_l3:
            mlag_l3_vlan = default(get(self._hostvars, "switch.mlag_peer_l3_vlan"), get(self._hostvars, "swicth.mlag_peer_vlan"))
            no_passive_interfaces.append(f"Vlan{mlag_l3_vlan}")
        if self._overlay_vtep is True:
            no_passive_interfaces.append(self._vtep_loopback)

        if self._underlay_routing_protocol in ["isis-ldp", "isis-sr-ldp"]:
            router_isis["mpls_ldp_sync_default"] = True

        # TI-LFA
        if get(self._hostvars, "isis_ti_lfa.enabled") is True:
            router_isis["timers"] = {
                "local_convergence": {
                    "delay": default(get(self._hostvars, "isis_ti_lfa.local_convergence_delay"), "10000"),
                    "protected_prefixes": True,
                }
            }
        ti_lfa_protection = get(self._hostvars, "isis_ti_lfa.protection")
        if ti_lfa_protection == "link":
            router_isis["isis_af_defaults"].append("fast-reroute ti-lfa mode link-protection")
        elif ti_lfa_protection == "node":
            router_isis["isis_af_defaults"].append("fast-reroute ti-lfa mode node-protection")

        # Overlay protocol
        if self._overlay_routing_protocol == "none":
            router_isis["redistribute_routes"] = [{"source_protocol": "connected"}]

        if self._underlay_routing_protocol in ["isis-sr", "isis-sr-ldp"]:
            router_isis["advertise"] = {
                "passive_only": default(get(self._hostvars, "isis_advertise_passive_only"), False),
            }
            # NOTE enabling IPv6 only in SR cases as per existing behavior
            # but this could probably be taken out
            if self._underlay_ipv6 is True:
                router_isis["address_family"].append("ipv6 unicast")
            router_isis["segment_routing_mpls"] = {"router_id": self._router_id, "enabled": True}

        return router_isis
