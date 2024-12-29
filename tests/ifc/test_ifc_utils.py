import pytest

import ifcopenshell.api.project
import ifcopenshell.guid

from stifc.ifc import ifc_utils

def test_append_to_internal_list_1():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    model = file.create_entity(
        "IfcStructuralAnalysisModel",
        GlobalId=ifcopenshell.guid.new())
    load_case = file.create_entity(
        "IfcStructuralLoadCase",
        GlobalId=ifcopenshell.guid.new())
    ifc_utils.append_to_internal_list(model, "LoadedBy", load_case)
    assert model.LoadedBy == (load_case,)

def test_append_to_internal_list_2():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    model = file.create_entity(
        "IfcStructuralAnalysisModel",
        GlobalId=ifcopenshell.guid.new(),
        LoadedBy=())
    load_case = file.create_entity(
        "IfcStructuralLoadCase",
        GlobalId=ifcopenshell.guid.new())
    ifc_utils.append_to_internal_list(model, "LoadedBy", load_case)
    assert model.LoadedBy == (load_case,)

def test_append_to_internal_list_3():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    load_case_1 = file.create_entity(
        "IfcStructuralLoadCase",
        GlobalId=ifcopenshell.guid.new())
    model = file.create_entity(
        "IfcStructuralAnalysisModel",
        GlobalId=ifcopenshell.guid.new(),
        LoadedBy=(load_case_1,))
    load_case_2 = file.create_entity(
        "IfcStructuralLoadCase",
        GlobalId=ifcopenshell.guid.new())
    ifc_utils.append_to_internal_list(model, "LoadedBy", load_case_2)
    assert model.LoadedBy == (load_case_1, load_case_2)

def test_create_placement_1():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    result = ifc_utils.create_placement(
        file,
        location=(0.0, 0.0, 0.0),
        direction=(0.0, 0.0, 1.0),
        axis=(1.0, 0.0, 0.0)).RelativePlacement
    assert len(file.by_type("IfcLocalPlacement")) == 1
    assert len(file.by_type("IfcAxis2Placement3D")) == 1
    assert len(file.by_type("IfcDirection")) == 2
    assert len(file.by_type("IfcCartesianPoint")) == 1
    assert result.Location.Coordinates == (0.0, 0.0, 0.0)
    assert result.Axis.DirectionRatios == (1.0, 0.0, 0.0)
    assert result.RefDirection.DirectionRatios == (0.0, 0.0, 1.0)

def test_create_placement_2():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    result = ifc_utils.create_placement(
        file,
        location=(0.0, 0.0, 0.0),
        direction=(0.0, 0.0, 1.0)).RelativePlacement
    assert len(file.by_type("IfcLocalPlacement")) == 1
    assert len(file.by_type("IfcAxis2Placement2D")) == 1
    assert len(file.by_type("IfcDirection")) == 1
    assert len(file.by_type("IfcCartesianPoint")) == 1
    assert result.Location.Coordinates == (0.0, 0.0, 0.0)
    assert result.RefDirection.DirectionRatios == (0.0, 0.0, 1.0)

def test_create_placement_3():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    point = ifc_utils.create_placement(
        file,
        location=(0.0, 0.0, 0.0),
        direction=(0.0, 0.0, 1.0),
        axis=(1.0, 0.0, 0.0))
    result = ifc_utils.create_placement(
        file,
        location=(1.0, 0.0, 0.0),
        direction=(0.0, 0.0, 1.0),
        axis=(1.0, 0.0, 0.0),
        placement_rel_to=point)
    assert result.PlacementRelTo == point

def test_reference_existing_1():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    result = ifc_utils.reference_existing(
        file,
        "IfcDimensionalExponents",
        1, 0, 0, 0, 0, 0, 0)
    assert len(file.by_type("IfcDimensionalExponents")) == 1
    assert result.LengthExponent == 1
    assert result.MassExponent == 0
    assert result.TimeExponent == 0
    assert result.ElectricCurrentExponent == 0
    assert result.ThermodynamicTemperatureExponent == 0
    assert result.AmountOfSubstanceExponent == 0
    assert result.LuminousIntensityExponent == 0

def test_reference_existing_2():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    _ = ifc_utils.reference_existing(
        file,
        "IfcDimensionalExponents",
        1, 0, 0, 0, 0, 0, 0)
    result = ifc_utils.reference_existing(
        file,
        "IfcDimensionalExponents",
        1, 1, -2, 0, 0, 0, 0)
    assert len(file.by_type("IfcDimensionalExponents")) == 2
    assert result.LengthExponent == 1
    assert result.MassExponent == 1
    assert result.TimeExponent == -2
    assert result.ElectricCurrentExponent == 0
    assert result.ThermodynamicTemperatureExponent == 0
    assert result.AmountOfSubstanceExponent == 0
    assert result.LuminousIntensityExponent == 0

def test_reference_existing_3():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    _ = ifc_utils.reference_existing(
        file,
        "IfcDimensionalExponents",
        1, 0, 0, 0, 0, 0, 0)
    results = ifc_utils.reference_existing(
        file,
        "IfcDimensionalExponents",
        1, 0, 0, 0, 0, 0, 0)
    assert len(file.by_type("IfcDimensionalExponents")) == 1
