# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ansible_collections.arista.avd.plugins.filter.range_expand import range_expand
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdError, AristaAvdMissingVariableError
from ansible_collections.arista.avd.plugins.plugin_utils.utils import default, get, get_item

if TYPE_CHECKING:
    from ansible_collections.arista.avd.plugins.plugin_utils.eos_designs_facts import EosDesignsFacts

    from .shared_utils import EosDesignsFacts


class SdwanMixin:
    """
    Mixin Class providing a subset of EosDesignsFacts
    Class should only be used as Mixin to the EosDesignsFacts class
    Using type-hint on self to get proper type-hints on attributes across all Mixins.
    """

    @cached_property
    def sdwan_ha_interface(self: EosDesignsFacts) -> str | None:
        if not self.shared_utils.sdwan_ha:
            return None
        return self.shared_utils.sdwan_ha_interface

    @cached_property
    def sdwan_ha_peer(self: EosDesignsFacts) -> str | None:
        if not self.shared_utils.sdwan_ha:
            return None
        return self.shared_utils.sdwan_ha_peer

    @cached_property
    def sdwan_ha_router_id(self: EosDesignsFacts) -> str | None:
        if not self.shared_utils.sdwan_ha:
            return None
        return self.shared_utils.sdwan_ha_router_id

    @cached_property
    def sdwan_ha_ip_addresses(self: EosDesignsFacts) -> list | None:
        if not self.shared_utils.sdwan_ha:
            return None
        return self.shared_utils.sdwan_ha_ip_addresses
