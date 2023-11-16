<!--
  ~ Copyright (c) 2023 Arista Networks, Inc.
  ~ Use of this source code is governed by the Apache License 2.0
  ~ that can be found in the LICENSE file.
  -->
=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>autovpn</samp>](## "autovpn") | Dictionary |  |  |  | AUTOVPN configuration |
    | [<samp>&nbsp;&nbsp;control_plane</samp>](## "autovpn.control_plane") | Dictionary |  |  |  | Control Plan profile configuration. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;ike_policy_name</samp>](## "autovpn.control_plane.ike_policy_name") | String |  | `controlPlaneIkePolicy` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;sa_policy_name</samp>](## "autovpn.control_plane.sa_policy_name") | String |  | `controlPlaneSaPolicy` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;profile_name</samp>](## "autovpn.control_plane.profile_name") | String |  | `controlPlaneIpsecProfile` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;ipsec_key</samp>](## "autovpn.control_plane.ipsec_key") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;data_plane</samp>](## "autovpn.data_plane") | Dictionary |  |  |  | Data Plan profile configuration. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;ike_policy_name</samp>](## "autovpn.data_plane.ike_policy_name") | String |  | `dataPlaneIkePolicy` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;sa_policy_name</samp>](## "autovpn.data_plane.sa_policy_name") | String |  | `dataPlaneSaPolicy` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;profile_name</samp>](## "autovpn.data_plane.profile_name") | String |  | `dataPlaneIpsecProfile` |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;ipsec_key</samp>](## "autovpn.data_plane.ipsec_key") | String |  |  |  |  |
    | [<samp>sdwans_ites</samp>](## "sdwans_ites") | List, items: Dictionary |  |  |  | SD WAN Sites. |
    | [<samp>&nbsp;&nbsp;-&nbsp;name</samp>](## "sdwans_ites.[].name") | String | Required, Unique |  |  | SD-WAN site name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;id</samp>](## "sdwans_ites.[].id") | Integer |  |  | Min: 1<br>Max: 255 | SD-WAN site ID. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;role</samp>](## "sdwans_ites.[].role") | String | Required |  | Valid Values:<br>- <code>edge</code><br>- <code>pathfinder</code><br>- <code>transit region</code><br>- <code>transit zone</code> | Role name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;region</samp>](## "sdwans_ites.[].region") | Dictionary | Required |  |  | Region name and ID. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name</samp>](## "sdwans_ites.[].region.name") | String | Required |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id</samp>](## "sdwans_ites.[].region.id") | Integer | Required |  | Min: 1<br>Max: 255 |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;zone</samp>](## "sdwans_ites.[].zone") | Dictionary | Required |  |  | Zone name and ID. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name</samp>](## "sdwans_ites.[].zone.name") | String | Required |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id</samp>](## "sdwans_ites.[].zone.id") | Integer | Required |  | Min: 1<br>Max: 10000 |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;profile</samp>](## "sdwans_ites.[].profile") | String |  |  |  | Site Profile. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;transports</samp>](## "sdwans_ites.[].transports") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;name</samp>](## "sdwans_ites.[].transports.[].name") | String | Required, Unique |  |  | Transport name. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id</samp>](## "sdwans_ites.[].transports.[].id") | Integer |  |  |  | Path-group id (ovewrite the global one per site?) |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;ha</samp>](## "sdwans_ites.[].ha") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</samp>](## "sdwans_ites.[].ha.enabled") | Boolean |  |  |  | True if HA is enabled for this site False by defaut. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interface</samp>](## "sdwans_ites.[].ha.interface") | String | Required |  |  | HA peer interface. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;primary_transports</samp>](## "sdwans_ites.[].ha.primary_transports") | List, items: String |  |  |  | List of site transports connected to the primary router. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "sdwans_ites.[].ha.primary_transports.[]") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;secondary_transports</samp>](## "sdwans_ites.[].ha.secondary_transports") | List, items: String |  |  |  | List of site transports connected to the primary router. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&lt;str&gt;</samp>](## "sdwans_ites.[].ha.secondary_transports.[]") | String |  |  |  |  |
    | [<samp>transports</samp>](## "transports") | List, items: Dictionary |  |  |  | Transports definition used for WAN configuration |
    | [<samp>&nbsp;&nbsp;-&nbsp;name</samp>](## "transports.[].name") | String | Required, Unique |  |  | Transport name |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;description</samp>](## "transports.[].description") | String |  |  |  | A description for the transport - TODO maybe only for doc? |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;preference</samp>](## "transports.[].preference") | String |  |  | Valid Values:<br>- <code>always_use</code><br>- <code>backup</code><br>- <code>never_use</code> | TODO |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;path_group_id</samp>](## "transports.[].path_group_id") | String |  |  |  | Optional path_group_id. Auto generated if ommitted. |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;accessibility</samp>](## "transports.[].accessibility") | String |  |  | Valid Values:<br>- <code>public</code><br>- <code>private</code> | TODO |

=== "YAML"

    ```yaml
    # AUTOVPN configuration
    autovpn:

      # Control Plan profile configuration.
      control_plane:
        ike_policy_name: <str; default="controlPlaneIkePolicy">
        sa_policy_name: <str; default="controlPlaneSaPolicy">
        profile_name: <str; default="controlPlaneIpsecProfile">
        ipsec_key: <str>

      # Data Plan profile configuration.
      data_plane:
        ike_policy_name: <str; default="dataPlaneIkePolicy">
        sa_policy_name: <str; default="dataPlaneSaPolicy">
        profile_name: <str; default="dataPlaneIpsecProfile">
        ipsec_key: <str>

    # SD WAN Sites.
    sdwans_ites:

        # SD-WAN site name.
      - name: <str; required; unique>

        # SD-WAN site ID.
        id: <int; 1-255>

        # Role name.
        role: <str; "edge" | "pathfinder" | "transit region" | "transit zone"; required>

        # Region name and ID.
        region: # required
          name: <str; required>
          id: <int; 1-255; required>

        # Zone name and ID.
        zone: # required
          name: <str; required>
          id: <int; 1-10000; required>

        # Site Profile.
        profile: <str>
        transports:

            # Transport name.
          - name: <str; required; unique>

            # Path-group id (ovewrite the global one per site?)
            id: <int>
        ha:

          # True if HA is enabled for this site False by defaut.
          enabled: <bool>

          # HA peer interface.
          interface: <str; required>

          # List of site transports connected to the primary router.
          primary_transports:
            - <str>

          # List of site transports connected to the primary router.
          secondary_transports:
            - <str>

    # Transports definition used for WAN configuration
    transports:

        # Transport name
      - name: <str; required; unique>

        # A description for the transport - TODO maybe only for doc?
        description: <str>

        # TODO
        preference: <str; "always_use" | "backup" | "never_use">

        # Optional path_group_id. Auto generated if ommitted.
        path_group_id: <str>

        # TODO
        accessibility: <str; "public" | "private">
    ```
