# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.filter.natural_sort import natural_sort
from ansible_collections.arista.avd.plugins.filter.range_expand import range_expand
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get, get_item

from .utils import UtilsMixin


class StunMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def stun(self) -> dict | None:
        """
        Return structured config for stun
        """

        if not self.shared_utils.wan:
            return None

        if self.shared_utils.type in ["edge", "transit"]:
            server_profiles = []
            # TODO need some way to loop through rr/pathfinders transports public_ips
            # TODO - probably need to filter on public IPs as I guess not needed for MPLS -> ask
            for wan_route_reflector, data in self._wan_route_reflectors.items():
                # TODO GUARDS GUARDS!!
                for transport in data.get("transports"):
                    server_profiles.append(
                        {
                            "name": f"{wan_route_reflector}-{transport['name']}",
                            "ip_address": transport["public_ip"],
                        }
                    )
            return {"client": {"server_profiles": server_profiles}}
        elif self.shared_utils.type in ["pathfinders", "rr"]:
            local_interfaces = [transport.get("interface") for transport in get(self.shared_utils.switch_data_combined, "transports", [])]
            return {"server": {"local_interfaces": local_interfaces}}
