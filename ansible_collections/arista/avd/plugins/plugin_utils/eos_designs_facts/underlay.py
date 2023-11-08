# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

if TYPE_CHECKING:
    from .eos_designs_facts import EosDesignsFacts


class UnderlayMixin:
    """
    Mixin Class used to generate some of the EosDesignsFacts.
    Class should only be used as Mixin to the EosDesignsFacts class
    Using type-hint on self to get proper type-hints on attributes across all Mixins.
    """

    @cached_property
    def wan_route_reflectors(self: EosDesignsFacts) -> list:
        """
        Exposed in avd_switch_facts

        For edge and transit routers , the default value for WAN Route Reflectors is the list of rr and pathfinders nodes
        For all other node types, there is no default.
        """
        if not self.shared_utils.underlay_router:
            return []

        if self.shared_utils.autovpn_role == "client":
            return get(self.shared_utils.switch_data_combined, "wan_route_reflectors")

        return []

    @cached_property
    def wan_transports(self: EosDesignsFacts) -> list:
        """
        Exposed in avd_switch_facts

        """
        # TODO - is it used anywhere?
        if not self.shared_utils.underlay_router:
            return []

        if self.shared_utils.autovpn_role == "server":
            return get(self.shared_utils.switch_data_combined, "transports")

        return []
