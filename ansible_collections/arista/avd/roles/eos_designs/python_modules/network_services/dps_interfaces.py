# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from .utils import UtilsMixin


class DpsInterfacesMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    # Set type hints for Attributes of the main class as needed
    _hostvars: dict
    _filtered_tenants: list[dict]

    @cached_property
    def dps_interfaces(self) -> dict | None:
        """
        Returns structured config for dps_interfaces

        Only used for WAN devices
        """
        if not self.shared_utils.autovpn_role:
            return None

        dps1 = {"name": "Dps1"}

        # Trailblazer default, may need to change
        if self.shared_utils.avt_role:
            # TODO what IP to use?
            dps1["tcp_mss_ceiling"] = {"ipv4": 1000}
            # TODO - even for virtual devices?
            dps1["flow_tracker"] = {"hardware": "flowTracker"}

        return [dps1]
