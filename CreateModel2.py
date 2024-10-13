import ifcopenshell.api.project
import ifcopenshell.api.root
from rich import print

import units

model = ifcopenshell.api.project.create_file("IFC4X3")
project = ifcopenshell.api.root.create_entity(model,
                                              "IfcProject",
                                              name="00001-TestProject")

si_units = [
    ["METRE", "LENGTHUNIT"],
    ["SQUARE_METRE", "AREAUNIT"],
    ["NEWTON", "FORCEUNIT"],
    ["GRAM", "MASSUNIT"],
    ["RADIAN", "PLANEANGLEUNIT"],
    ["PASCAL", "PRESSUREUNIT"],
    ["CUBIC_METRE", "VOLUMEUNIT"]
]

for unit in si_units:
    units.add_si_unit(model, *unit)

conversion_based_units = [
    ["INCH^2", "AREAUNIT", (2, 0, 0, 0, 0, 0, 0), 0.0006452, "SQUARE_METRE"],
    ["LB", "FORCEUNIT", (1, 1, -2, 0, 0, 0, 0), 4.4482216153, "NEWTON"],
    ["INCH", "LENGTHUNIT", (1, 0, 0, 0, 0, 0, 0), 0.0254, "METRE"],
    ["LBM", "MASSUNIT", (0, 1, 0, 0, 0, 0, 0), 454, "GRAM"],
    ["DEGREE", "PLANEANGLEUNIT", (0, 0, 0, 0, 0, 0, 0), 0.017453293, "RADIAN"],
    ["LB/INCH^2 (PRESSURE)", "PRESSUREUNIT", (-1, 1, -2, 0, 0, 0, 0), 6894.7572932, "PASCAL"],
    ["INCH^3", "VOLUMEUNIT", (3, 0, 0, 0, 0, 0, 0), 0.00001639, "CUBIC_METRE"]
]

for unit in conversion_based_units:
    units.add_conversion_based_unit(model, *unit)

derived_units = [
    ["PLI", "LINEARFORCEUNIT", (("LB", 1), ("INCH", -1))],
    ["LBINCH/INCH", "LINEARMOMENTUNIT", (("LB", 1), ("INCH", 1), ("INCH", -1))],
    ["LB/INCH (LINEARSTIFFNESS)", "LINEARSTIFFNESSUNIT", (("LB", 1), ("INCH", -1))],
    ["LBM/INCH^3 (MASSDENSITY)", "MASSDENSITYUNIT", (("LBM", 1), ("INCH^3", -1))],
    ["LBM/INCH (MASSPERLENGTH)", "MASSPERLENGTHUNIT", (("LBM", 1), ("INCH", -1))],
    ["LB/INCH^2 (MODULUSOFELASTICITY)", "MODULUSOFELASTICITYUNIT", (("LB", 1), ("INCH^2", -1))],
    ["INCH^4 (MOMENTOFINERTIA)", "MOMENTOFINERTIAUNIT", (("INCH", 4),)],
    ["PSI", "PLANARFORCEUNIT", (("LB", 1), ("INCH^2", -1))],
    ["LBM/INCH^2 (ROTATIONALMASS)", "ROTATIONALMASSUNIT", (("LBM", 1), ("INCH^2", -1))],
    ["LBINCH/DEGREE (ROTATIONALSTIFFNESS)", "ROTATIONALSTIFFNESSUNIT", (("LB", 1), ("INCH", 1), ("DEGREE", -1))],
    ["INCH^5 (SECTIONAREAINTEGRAL)", "SECTIONAREAINTEGRALUNIT", (("INCH", 5),)],
    ["INCH^3 (SECTIONMODULUS)", "SECTIONMODULUSUNIT", (("INCH", 3),)],
    ["LB/INCH^2 (SHEARMODULUS)", "SHEARMODULUSUNIT", (("LB", 1), ("INCH^2", -1))]
]

for unit in derived_units:
    units.add_derived_unit(model, *unit)

ifc_units = units.get_units(model)
unit_assignment_list = [
    ifc_units["INCH"],
    ifc_units["LB"],
    ifc_units["INCH^2"],
    ifc_units["LBM"],
    ifc_units["DEGREE"],
    ifc_units["LB/INCH^2 (PRESSURE)"],
    ifc_units["INCH^3"],
    ifc_units["PLI"],
    ifc_units["LBINCH/INCH"],
    ifc_units["LB/INCH (LINEARSTIFFNESS)"],
    ifc_units["LBM/INCH^3 (MASSDENSITY)"],
    ifc_units["LBM/INCH (MASSPERLENGTH)"],
    ifc_units["LB/INCH^2 (MODULUSOFELASTICITY)"],
    ifc_units["INCH^4 (MOMENTOFINERTIA)"],
    ifc_units["PSI"],
    ifc_units["LBM/INCH^2 (ROTATIONALMASS)"],
    ifc_units["LBINCH/DEGREE (ROTATIONALSTIFFNESS)"],
    ifc_units["INCH^5 (SECTIONAREAINTEGRAL)"],
    ifc_units["INCH^3 (SECTIONMODULUS)"],
    ifc_units["LB/INCH^2 (SHEARMODULUS)"]
]

model.create_entity("IfcUnitAssignment", unit_assignment_list)

model.write("/home/joebot/git/stifc/AnnexE.ifc")