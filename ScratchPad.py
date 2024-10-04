# +
from typing import Optional

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.unit


# -

class file:
    def __init__(self, ifcopenshell_file):
        self.file = ifcopenshell_file

    def add_unit(self, name, unit_type, )

    def write(self, filename: str):
        self.file.write(filename)


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

si_units = model.by_type("IfcSIUnit")
print(si_units[0][3])

model.create_entity("IfcSIUnit", "AREAUNIT", "SQUARE_METRE")


