# Copyright (c) 2026 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import Any, ClassVar

import pytest

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen
from pyavd._eos_designs.schema import EosDesigns
from pyavd._schema.models.avd_indexed_list import AvdIndexedList
from pyavd._schema.models.avd_list import AvdList
from pyavd._schema.models.avd_model import AvdModel


class SourceChild(AvdModel):
    _fields: ClassVar[dict] = {"enabled": {"type": bool, "default": True}, "always": {"type": bool}}


class TargetChild(AvdModel):
    _fields: ClassVar[dict] = {"enabled": {"type": bool}, "always": {"type": bool}}


class SourceList(AvdList):
    _item_type = SourceChild


class TargetList(AvdList):
    _item_type = TargetChild


class SourceIndexedItem(AvdModel):
    _fields: ClassVar[dict] = {"name": {"type": str}, "enabled": {"type": bool, "default": True}}


class TargetIndexedItem(AvdModel):
    _fields: ClassVar[dict] = {"name": {"type": str}, "enabled": {"type": bool}}


class SourceIndexedList(AvdIndexedList):
    _item_type = SourceIndexedItem
    _primary_key = "name"


class TargetIndexedList(AvdIndexedList):
    _item_type = TargetIndexedItem
    _primary_key = "name"


class SourceModel(AvdModel):
    _fields: ClassVar[dict] = {
        "name": {"type": str},
        "direct_default": {"type": bool, "default": True},
        "missing_from_target": {"type": str, "default": "ignored"},
        "child": {"type": SourceChild},
        "list_items": {"type": SourceList},
        "indexed_items": {"type": SourceIndexedList},
        "no_default_child": {"type": SourceChild},
        "no_default_list": {"type": SourceList},
        "no_default_dict": {"type": dict},
        "no_default_string": {"type": str},
        "any_field": {"type": Any},
    }


class TargetModel(AvdModel):
    _fields: ClassVar[dict] = {
        "name": {"type": str},
        "direct_default": {"type": bool},
        "child": {"type": TargetChild},
        "list_items": {"type": TargetList},
        "indexed_items": {"type": TargetIndexedList},
        "no_default_child": {"type": TargetChild},
        "no_default_list": {"type": TargetList},
        "no_default_dict": {"type": dict},
        "no_default_string": {"type": str},
        "any_field": {"type": Any},
    }


def test_cast_as_default_behavior_is_unchanged() -> None:
    source = SourceModel(name="test")

    target = source._cast_as(TargetModel, ignore_extra_keys=True)

    assert target._dump() == {"name": "test"}


def test_cast_as_includes_direct_explicit_source_defaults() -> None:
    source = SourceModel(name="test")

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"name": "test", "direct_default": True}


def test_cast_as_does_not_create_absent_nested_objects_from_child_defaults() -> None:
    source = SourceModel(name="test")

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert "child" not in target._dump()
    assert "no_default_child" not in target._dump()


def test_cast_as_includes_child_defaults_when_nested_object_is_present() -> None:
    source = SourceModel(name="test", child=SourceChild())

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"name": "test", "direct_default": True, "child": {"enabled": True}}


def test_cast_as_does_not_materialize_source_defaults() -> None:
    source = SourceModel(child=SourceChild())

    source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert "direct_default" not in source.__dict__
    assert "enabled" not in source.child.__dict__


def test_cast_as_does_not_include_defaults_for_null_objects() -> None:
    source = SourceModel(child=SourceChild._from_null())

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target.child._created_from_null is True
    assert "enabled" not in target.child.__dict__
    assert target._dump() == {"direct_default": True, "child": None}


def test_cast_as_include_default_values_honors_ignore_extra_keys() -> None:
    source = SourceModel()

    with pytest.raises(TypeError, match="missing_from_target"):
        source._cast_as(TargetModel, include_default_values=True)

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)
    assert "missing_from_target" not in target._dump()


def test_cast_as_does_not_include_default_default_values() -> None:
    source = SourceModel()

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"direct_default": True}


def test_cast_as_include_default_values_recurses_into_list_items() -> None:
    source = SourceModel(list_items=SourceList([SourceChild()]))

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"direct_default": True, "list_items": [{"enabled": True}]}


def test_cast_as_include_default_values_recurses_into_indexed_list_items() -> None:
    source = SourceModel(indexed_items=SourceIndexedList([SourceIndexedItem(name="item1")]))

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"direct_default": True, "indexed_items": [{"name": "item1", "enabled": True}]}


def test_cast_as_include_default_values_handles_any_fields() -> None:
    source = SourceModel(any_field={"key": "value"})

    target = source._cast_as(TargetModel, ignore_extra_keys=True, include_default_values=True)

    assert target._dump() == {"direct_default": True, "any_field": {"key": "value"}}


def test_cast_as_include_default_values_for_network_services_bgp_peer_default_originate() -> None:
    source_type = EosDesigns._DynamicKeys.DynamicNetworkServicesItem.NetworkServicesItem.VrfsItem.BgpPeersItem

    absent_default_originate = source_type(ip_address="192.0.2.1")
    target = absent_default_originate._cast_as(EosCliConfigGen.RouterBgp.VrfsItem.NeighborsItem, ignore_extra_keys=True, include_default_values=True)
    assert target._dump() == {"ip_address": "192.0.2.1"}

    present_default_originate = source_type(ip_address="192.0.2.1", default_originate=source_type.DefaultOriginate(always=True))
    target = present_default_originate._cast_as(EosCliConfigGen.RouterBgp.VrfsItem.NeighborsItem, ignore_extra_keys=True, include_default_values=True)
    assert target._dump() == {"ip_address": "192.0.2.1", "default_originate": {"enabled": True, "always": True}}

    disabled_default_originate = source_type(ip_address="192.0.2.1", default_originate=source_type.DefaultOriginate(enabled=False, always=True))
    target = disabled_default_originate._cast_as(EosCliConfigGen.RouterBgp.VrfsItem.NeighborsItem, ignore_extra_keys=True, include_default_values=True)
    assert target._dump() == {"ip_address": "192.0.2.1", "default_originate": {"enabled": False, "always": True}}
