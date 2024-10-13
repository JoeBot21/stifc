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

def find_dimensional_exponents(file, exponents: tuple):
    """Searches the file for a dimensional exponents entry that matches
       the provided dimensional exponents and returns an existing entry
       or creates and returns a new dimensional exponents entry."""
    exponents_list = []
    ifc_exponents_list = file.by_type("IfcDimensionalExponents")
    for existing_exponents in ifc_exponents_list:
        exponents_list.append((existing_exponents[0],
                               existing_exponents[1],
                               existing_exponents[2],
                               existing_exponents[3],
                               existing_exponents[4],
                               existing_exponents[5],
                               existing_exponents[6]))
    for i in range(0, len(exponents_list)):
        if exponents == exponents_list[i]:
            return ifc_exponents_list[i]
    return file.create_entity("IfcDimensionalExponents", *exponents)

def add_si_unit(file, name: str, unit_type: str, prefix: str = ""):
    """Add a SI unit to the ifcopenshell.file object."""
    if not get_units(file).get(prefix+name, None):
        if not prefix:
            prefix = None
        file.create_entity("IfcSIUnit",
                            UnitType=unit_type,
                            Prefix=prefix,
                            Name=name)

def add_conversion_based_unit(file,
                              name: str,
                              unit_type: str,
                              exponents: tuple,
                              conversion: float,
                              base: str):
    """Add a conversion based unit to the file"""
#    if not get_units(file).get(name, None):
#        exponents = 


# -

model = ifcopenshell.open("TestModel.ifc")

test_exponents = (4, 0, 0, 0, 0, 0, 0)
print(find_dimensional_exponents(model, test_exponents))

# +
exponents_list = []
for exponents in model.by_type("IfcDimensionalExponents"):
    current_exponents = (exponents[0],
                         exponents[1],
                         exponents[2],
                         exponents[3],
                         exponents[4],
                         exponents[5],
                         exponents[6])
    exponents_list.append(current_exponents)

print(exponents_list)
# -

print(model.by_type("IfcDimensionalExponents"))

print(get_units(model))
