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
