# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

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

        if not self.shared_utils.autovpn_role:
            return None

        stun = {}
        if self.shared_utils.autovpn_role == "server":
            local_interfaces = []
            for transport in get(self.shared_utils.switch_data_combined, "transports", []):
                local_interfaces.extend([interface["name"] for interface in transport.get("interfaces", [])])
            stun["server"] = {"local_interfaces": local_interfaces}

        if self.shared_utils.autovpn_role == "client":
            server_profiles = []

            # TODO - do we need a helper for this if reused multiple places
            local_transports = [transport["name"] for transport in get(self.shared_utils.switch_data_combined, "transports", [])]

            for wan_route_reflector, data in self._wan_route_reflectors.items():
                for transport in data.get("transports", []):
                    if transport["name"] not in local_transports:
                        continue

                    ipv4_addresses = []

                    for interface in transport.get("interfaces", []):
                        if (ip_address := interface.get("ip_address")) is not None:
                            # TODO - removing mask using split but maybe a helper is clearer
                            ipv4_addresses.append(ip_address.split("/")[0])
                    # TODO - does it need to be sorted ?
                    for index, ip_address in enumerate(ipv4_addresses, start=1):
                        server_profiles.append(
                            {
                                "name": self._stun_server_profile_name(wan_route_reflector, transport["name"], index),
                                "ip_address": ip_address,
                            }
                        )
            stun["client"] = {"server_profiles": server_profiles}

        return stun
