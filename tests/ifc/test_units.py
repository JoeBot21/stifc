import pytest

import ifcopenshell.api.project

from stifc.ifc import units

def test_add_si_unit_1():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "METRE", "LENGTHUNIT")
    assert len(file.by_type("IfcSIUnit")) == 1
    result = file.by_type("IfcSIUnit")[0]
    assert result.UnitType == "LENGTHUNIT"
    assert result.Prefix == None
    assert result.Name == "METRE"
    assert result.Dimensions.LengthExponent == 1
    assert result.Dimensions.MassExponent == 0
    assert result.Dimensions.TimeExponent == 0
    assert result.Dimensions.ElectricCurrentExponent == 0
    assert result.Dimensions.ThermodynamicTemperatureExponent == 0
    assert result.Dimensions.AmountOfSubstanceExponent == 0
    assert result.Dimensions.LuminousIntensityExponent == 0

def test_add_si_unit_2():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "NEWTON", "FORCEUNIT", "KILO")
    assert len(file.by_type("IfcSIUnit")) == 1
    result = file.by_type("IfcSIUnit")[0]
    assert result.UnitType == "FORCEUNIT"
    assert result.Prefix == "KILO"
    assert result.Name == "NEWTON"
    assert result.Dimensions.LengthExponent == 1
    assert result.Dimensions.MassExponent == 1
    assert result.Dimensions.TimeExponent == -2
    assert result.Dimensions.ElectricCurrentExponent == 0
    assert result.Dimensions.ThermodynamicTemperatureExponent == 0
    assert result.Dimensions.AmountOfSubstanceExponent == 0
    assert result.Dimensions.LuminousIntensityExponent == 0

def test_add_si_unit_3():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "GRAM", "MASSUNIT")
    units.add_si_unit(file, "GRAM", "MASSUNIT")
    assert len(file.by_type("IfcSIUnit")) == 1

def test_add_si_unit_4():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "GRAM", "MASSUNIT")
    units.add_si_unit(file, "GRAM", "MASSUNIT", "KILO")
    assert len(file.by_type("IfcSIUnit")) == 2
    assert file.by_type("IfcSIUnit")[0].Prefix == None
    assert file.by_type("IfcSIUnit")[1].Prefix == "KILO"

def test_add_conversion_based_unit_1():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "METRE", "LENGTHUNIT")
    units.add_conversion_based_unit(
        file,
        "INCH",
        "LENGTHUNIT",
        (1, 0, 0, 0, 0, 0, 0),
        0.0254,
        "METRE")
    assert len(file.by_type("IfcConversionBasedUnit")) == 1
    result = file.by_type("IfcConversionBasedUnit")[0]
    assert result.UnitType == "LENGTHUNIT"
    assert result.Name == "INCH"
    assert len(file.by_type("IfcDimensionalExponents")) == 1
    assert result.Dimensions.LengthExponent == 1
    assert result.Dimensions.MassExponent == 0
    assert result.Dimensions.TimeExponent == 0
    assert result.Dimensions.ElectricCurrentExponent == 0
    assert result.Dimensions.ThermodynamicTemperatureExponent == 0
    assert result.Dimensions.AmountOfSubstanceExponent == 0
    assert result.Dimensions.LuminousIntensityExponent == 0
    assert len(file.by_type("IfcMeasureWithUnit")) == 1
    assert result.ConversionFactor.ValueComponent.wrappedValue == 0.0254
    assert result.ConversionFactor.UnitComponent.Name == "METRE"

def test_add_conversion_based_unit_2():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "METRE", "LENGTHUNIT")
    units.add_conversion_based_unit(
        file,
        "INCH",
        "LENGTHUNIT",
        (1, 0, 0, 0, 0, 0, 0),
        0.0254,
        "METRE")
    units.add_conversion_based_unit(
        file,
        "INCH",
        "LENGTHUNIT",
        (1, 0, 0, 0, 0, 0, 0),
        0.0254,
        "METRE")
    assert len(file.by_type("IfcConversionBasedUnit")) == 1
    assert len(file.by_type("IfcDimensionalExponents")) == 1
    assert len(file.by_type("IfcMeasureWithUnit")) == 1

def test_add_derived_unit():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    units.add_si_unit(file, "METRE", "LENGTHUNIT")
