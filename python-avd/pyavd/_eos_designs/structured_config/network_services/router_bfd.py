# Copyright (c) 2023-2026 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen

if TYPE_CHECKING:
    from . import AvdStructuredConfigNetworkServicesProtocol


class RouterBfdMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    def set_global_router_bfd_timers(self: AvdStructuredConfigNetworkServicesProtocol) -> None:
        """Set structured config for router_bfd."""
        if self.inputs.bfd_multihop:
            self.structured_config.router_bfd.multihop = self.inputs.bfd_multihop._cast_as(EosCliConfigGen.RouterBfd.Multihop, ignore_extra_keys=True)
