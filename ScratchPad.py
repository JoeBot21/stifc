# +
from typing import Optional

from rich import print

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.unit


# -

def add_derived_unit(ifcopenshell_file,
                     name: str,
                     unit_type: str,
                     elements: tuple):
    """Add a derived unit to the IFC file"""
    


# +
def get_units(file):
    """Returns a dictionary of units in the ifcopenshell.file object."""
    existing_units = {}
    for unit in file.by_type("IfcSIUnit"):
        if unit[2]:
            existing_units.update({unit[2]+unit[3]: unit})
        else:
            existing_units.update({unit[3]: unit})
    for unit in file.by_type("IfcConversionBasedUnit"):
        existing_units.update({unit[2]: unit})
    for unit in file.by_type("IfcDerivedUnit"):
        existing_units.update({unit[3]: unit})
    return existing_units

def add_si_unit(self, name: str, unit_type: str, prefix: str = ""):
    """Add a SI unit to the ifcopenshell.file object."""
    existing_units = self.get_units()
    if not existing_units.get(prefix+name, None):
        if not prefix:
            prefix = None
        self.file.create_entity("IfcSIUnit",
                                UnitType=unit_type,
                                Prefix=prefix,
                                Name=name)

def add_conversion_based_unit(self, name: str,
                              unit_type: str,
                              exponents: tuple,
                              conversion: float,
                              base: str):
    """Add a conversion based unit to the file"""
#    existing_units = 


# +
def initailize_project(name: str, schema: str = "IFC4"):
    ifcopenshell_file = ifcopenshell.api.project.create_file(schema)
    ifcopenshell.api.root.create_entity(
        ifcopenshell_file,
        ifc_class="IfcProject",
        name=name)
    return file(ifcopenshell_file)

def open(filename: str):
    ifcopenshell_file = ifcopenshell.open(filename)
    return file(ifcopenshell_file)


# -

model = ifcopenshell.open("TestModel.ifc")

print(get_units(model))
