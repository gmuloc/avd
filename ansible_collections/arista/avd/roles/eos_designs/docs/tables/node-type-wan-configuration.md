<!--
  ~ Copyright (c) 2023 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->
=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>&lt;node_type_keys.key&gt;</samp>](## "<node_type_keys.key>") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;defaults</samp>](## "<node_type_keys.key>.defaults") | Dictionary |  |  |  | Define variables for all nodes of this type. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;transports</samp>](## "<node_type_keys.key>.defaults.transports") | List, items: Dictionary |  |  |  | List of WAN transports connected to the node |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.defaults.transports.[].name") | String | Required, Unique |  |  | Transport name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interfaces</samp>](## "<node_type_keys.key>.defaults.transports.[].interfaces") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.defaults.transports.[].interfaces.[].name") | String | Required, Unique |  |  | Interface to connect to the transport |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip_address</samp>](## "<node_type_keys.key>.defaults.transports.[].interfaces.[].ip_address") | String |  |  |  | The public IP for the transport on the node with mask.<br>If not set, default to "dhcp" |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;shutdown</samp>](## "<node_type_keys.key>.defaults.transports.[].interfaces.[].shutdown") | Boolean |  | `False` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ipsec_enabled</samp>](## "<node_type_keys.key>.defaults.transports.[].ipsec_enabled") | Boolean |  | `True` |  | Enable or disable IPSEC for a transport. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;wan_route_reflectors</samp>](## "<node_type_keys.key>.defaults.wan_route_reflectors") | List, items: String |  |  |  | List of inventory hostname acting as WAN route-reflectors. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "<node_type_keys.key>.defaults.wan_route_reflectors.[]") | String |  |  |  | Inventory_hostname_of_wan_route_reflectors. |
    | [<samp>&nbsp;&nbsp;node_groups</samp>](## "<node_type_keys.key>.node_groups") | List, items: Dictionary |  |  |  | Define variables related to all nodes part of this group. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;group</samp>](## "<node_type_keys.key>.node_groups.[].group") | String | Required, Unique |  |  | The Node Group Name is used for MLAG domain unless set with 'mlag_domain_id'.<br>The Node Group Name is also used for peer description on downstream switches' uplinks.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;nodes</samp>](## "<node_type_keys.key>.node_groups.[].nodes") | List, items: Dictionary |  |  |  | Define variables per node. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].name") | String | Required, Unique |  |  | The Node Name is used as "hostname". |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;transports</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports") | List, items: Dictionary |  |  |  | List of WAN transports connected to the node |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].name") | String | Required, Unique |  |  | Transport name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interfaces</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].interfaces") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].interfaces.[].name") | String | Required, Unique |  |  | Interface to connect to the transport |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip_address</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].interfaces.[].ip_address") | String |  |  |  | The public IP for the transport on the node with mask.<br>If not set, default to "dhcp" |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;shutdown</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].interfaces.[].shutdown") | Boolean |  | `False` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ipsec_enabled</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].transports.[].ipsec_enabled") | Boolean |  | `True` |  | Enable or disable IPSEC for a transport. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wan_route_reflectors</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].wan_route_reflectors") | List, items: String |  |  |  | List of inventory hostname acting as WAN route-reflectors. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "<node_type_keys.key>.node_groups.[].nodes.[].wan_route_reflectors.[]") | String |  |  |  | Inventory_hostname_of_wan_route_reflectors. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;transports</samp>](## "<node_type_keys.key>.node_groups.[].transports") | List, items: Dictionary |  |  |  | List of WAN transports connected to the node |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].name") | String | Required, Unique |  |  | Transport name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interfaces</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].interfaces") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].interfaces.[].name") | String | Required, Unique |  |  | Interface to connect to the transport |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip_address</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].interfaces.[].ip_address") | String |  |  |  | The public IP for the transport on the node with mask.<br>If not set, default to "dhcp" |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;shutdown</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].interfaces.[].shutdown") | Boolean |  | `False` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ipsec_enabled</samp>](## "<node_type_keys.key>.node_groups.[].transports.[].ipsec_enabled") | Boolean |  | `True` |  | Enable or disable IPSEC for a transport. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wan_route_reflectors</samp>](## "<node_type_keys.key>.node_groups.[].wan_route_reflectors") | List, items: String |  |  |  | List of inventory hostname acting as WAN route-reflectors. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "<node_type_keys.key>.node_groups.[].wan_route_reflectors.[]") | String |  |  |  | Inventory_hostname_of_wan_route_reflectors. |
    | [<samp>&nbsp;&nbsp;nodes</samp>](## "<node_type_keys.key>.nodes") | List, items: Dictionary |  |  |  | Define variables per node. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.nodes.[].name") | String | Required, Unique |  |  | The Node Name is used as "hostname". |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;transports</samp>](## "<node_type_keys.key>.nodes.[].transports") | List, items: Dictionary |  |  |  | List of WAN transports connected to the node |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.nodes.[].transports.[].name") | String | Required, Unique |  |  | Transport name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interfaces</samp>](## "<node_type_keys.key>.nodes.[].transports.[].interfaces") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "<node_type_keys.key>.nodes.[].transports.[].interfaces.[].name") | String | Required, Unique |  |  | Interface to connect to the transport |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip_address</samp>](## "<node_type_keys.key>.nodes.[].transports.[].interfaces.[].ip_address") | String |  |  |  | The public IP for the transport on the node with mask.<br>If not set, default to "dhcp" |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;shutdown</samp>](## "<node_type_keys.key>.nodes.[].transports.[].interfaces.[].shutdown") | Boolean |  | `False` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ipsec_enabled</samp>](## "<node_type_keys.key>.nodes.[].transports.[].ipsec_enabled") | Boolean |  | `True` |  | Enable or disable IPSEC for a transport. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wan_route_reflectors</samp>](## "<node_type_keys.key>.nodes.[].wan_route_reflectors") | List, items: String |  |  |  | List of inventory hostname acting as WAN route-reflectors. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "<node_type_keys.key>.nodes.[].wan_route_reflectors.[]") | String |  |  |  | Inventory_hostname_of_wan_route_reflectors. |

=== "YAML"

    ```yaml
    <node_type_keys.key>:

      # Define variables for all nodes of this type.
      defaults:

        # List of WAN transports connected to the node
        transports:

            # Transport name.
          - name: <str; required; unique>
            interfaces:

                # Interface to connect to the transport
              - name: <str; required; unique>

                # The public IP for the transport on the node with mask.
                # If not set, default to "dhcp"
                ip_address: <str>
                shutdown: <bool; default=False>

            # Enable or disable IPSEC for a transport.
            ipsec_enabled: <bool; default=True>

        # List of inventory hostname acting as WAN route-reflectors.
        wan_route_reflectors:

            # Inventory_hostname_of_wan_route_reflectors.
          - <str>

      # Define variables related to all nodes part of this group.
      node_groups:

          # The Node Group Name is used for MLAG domain unless set with 'mlag_domain_id'.
          # The Node Group Name is also used for peer description on downstream switches' uplinks.
        - group: <str; required; unique>

          # Define variables per node.
          nodes:

              # The Node Name is used as "hostname".
            - name: <str; required; unique>

              # List of WAN transports connected to the node
              transports:

                  # Transport name.
                - name: <str; required; unique>
                  interfaces:

                      # Interface to connect to the transport
                    - name: <str; required; unique>

                      # The public IP for the transport on the node with mask.
                      # If not set, default to "dhcp"
                      ip_address: <str>
                      shutdown: <bool; default=False>

                  # Enable or disable IPSEC for a transport.
                  ipsec_enabled: <bool; default=True>

              # List of inventory hostname acting as WAN route-reflectors.
              wan_route_reflectors:

                  # Inventory_hostname_of_wan_route_reflectors.
                - <str>

          # List of WAN transports connected to the node
          transports:

              # Transport name.
            - name: <str; required; unique>
              interfaces:

                  # Interface to connect to the transport
                - name: <str; required; unique>

                  # The public IP for the transport on the node with mask.
                  # If not set, default to "dhcp"
                  ip_address: <str>
                  shutdown: <bool; default=False>

              # Enable or disable IPSEC for a transport.
              ipsec_enabled: <bool; default=True>

          # List of inventory hostname acting as WAN route-reflectors.
          wan_route_reflectors:

              # Inventory_hostname_of_wan_route_reflectors.
            - <str>

      # Define variables per node.
      nodes:

          # The Node Name is used as "hostname".
        - name: <str; required; unique>

          # List of WAN transports connected to the node
          transports:

              # Transport name.
            - name: <str; required; unique>
              interfaces:

                  # Interface to connect to the transport
                - name: <str; required; unique>

                  # The public IP for the transport on the node with mask.
                  # If not set, default to "dhcp"
                  ip_address: <str>
                  shutdown: <bool; default=False>

              # Enable or disable IPSEC for a transport.
              ipsec_enabled: <bool; default=True>

          # List of inventory hostname acting as WAN route-reflectors.
          wan_route_reflectors:

              # Inventory_hostname_of_wan_route_reflectors.
            - <str>
    ```
