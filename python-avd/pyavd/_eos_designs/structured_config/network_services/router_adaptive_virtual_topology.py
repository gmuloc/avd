# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen
from pyavd._eos_designs.structured_config.structured_config_generator import structured_config_contributor
from pyavd._errors import AristaAvdInvalidInputsError
from pyavd._utils import get, get_item

if TYPE_CHECKING:
    from . import AvdStructuredConfigNetworkServicesProtocol


class RouterAdaptiveVirtualTopologyMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    @structured_config_contributor
    def router_adaptive_virtual_topology(self: AvdStructuredConfigNetworkServicesProtocol) -> None:
        """Set structured config for profiles, policies and VRFs for router adaptive-virtual-topology (AVT)."""
        if not self.shared_utils.is_cv_pathfinder_router:
            return

        self._cv_pathfinder_wan_vrfs()

    def _cv_pathfinder_wan_vrfs(self: AvdStructuredConfigNetworkServicesProtocol) -> None:
        """Set the of WAN VRFs based on filtered tenants and the AVT."""
        # For CV Pathfinder, it is required to go through all the AVT profiles in the policy to assign an ID.
        for vrf in self._filtered_wan_vrfs:
            wan_vrf = EosCliConfigGen.RouterAdaptiveVirtualTopology.VrfsItem(
                name=vrf.name,
                policy=f"{vrf.policy}-WITH-CP" if vrf.name == "default" else vrf.policy,
            )

            # Need to allocate an ID for each profile in the policy, for now picked up from the input.
            if wan_vrf.policy not in self.inputs.wan_virtual_topologies.policies:
                msg = f"The policy {wan_vrf.policy} used in vrf {wan_vrf.name} is not configured under 'wan_virtual_topologies.policies'."
                raise AristaAvdInvalidInputsError(msg)

            policy = get_item(self._filtered_wan_policies, "name", wan_vrf.policy)

            for match in policy.get("matches", []):
                wan_vrf.profiles.append_new(
                    name=get(match, "avt_profile", required=True),
                    id=get(match, "id", required=True),
                )
            if (default_match := policy.get("default_match")) is not None:
                wan_vrf.profiles.append_new(
                    name=get(default_match, "avt_profile", required=True),
                    id=get(default_match, "id", required=True),
                )

            self.structured_config.router_adaptive_virtual_topology.vrfs.append(wan_vrf)
