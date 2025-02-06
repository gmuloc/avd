# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen

if TYPE_CHECKING:
    from . import AvdStructuredConfigNetworkServicesProtocol


class RouterServiceInsertionMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    def set_router_service_insertion(self: AvdStructuredConfigNetworkServicesProtocol, connection: dict) -> dict | None:
        """
        Return structured config for router_service_insertion.

        Only used for CV Pathfinder edge routers today
        """
        service_connection = EosCliConfigGen.RouterServiceInsertion.ConnectionsItem(
            name=connection["name"],
            monitor_connectivity_host=connection["monitor_name"],
        )

        if connection["type"] == "tunnel":
            service_connection.tunnel_interface.primary = f"Tunnel{connection['tunnel_id']}"
        elif connection["type"] == "ethernet":
            service_connection.ethernet_interface._update(
                name=connection["source_interface"],
                next_hop=connection["next_hop"],
            )

        self.structured_config.router_service_insertion.connections.append(service_connection)

        # TODO: move it to do it once only
        self.structured_config.router_service_insertion.enabled = True
