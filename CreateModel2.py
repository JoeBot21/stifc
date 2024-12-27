import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.root
import ifcopenshell.api.unit
from rich import print

import units

model = ifcopenshell.api.project.create_file("IFC4X3")
project = ifcopenshell.api.root.create_entity(model,
                                              "IfcProject",
                                              name="00001-TestProject")

# Add units
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

unit_assignment_list = ["INCH", "LB", "INCH^2", "LBM", "DEGREE",
    "LB/INCH^2 (PRESSURE)", "INCH^3", "PLI", "LBINCH/INCH",
    "LB/INCH (LINEARSTIFFNESS)", "LBM/INCH^3 (MASSDENSITY)",
    "LBM/INCH (MASSPERLENGTH)", "LB/INCH^2 (MODULUSOFELASTICITY)",
    "INCH^4 (MOMENTOFINERTIA)", "PSI", "LBM/INCH^2 (ROTATIONALMASS)",
    "LBINCH/DEGREE (ROTATIONALSTIFFNESS)", "INCH^5 (SECTIONAREAINTEGRAL)",
    "INCH^3 (SECTIONMODULUS)", "LB/INCH^2 (SHEARMODULUS)"]
ifc_units = units.get_units(model)
ifc_unit_assignment_list = [ifc_units[name] for name in unit_assignment_list]
ifcopenshell.api.unit.assign_unit(model, ifc_unit_assignment_list)

# Add contexts
model_parent = ifcopenshell.api.context.add_context(model, "Model")
plan_parent = ifcopenshell.api.context.add_context(model, "Plan")

subcontexts_list = [
    (model, "Model", "Body", "MODEL_VIEW", model_parent),
    (model, "Model", "Axis", "GRAPH_VIEW", model_parent),
    (model, "Model", "Box", "MODEL_VIEW", model_parent),
    (model, "Plan", "Body", "PLAN_VIEW", plan_parent),
    (model, "Plan", "Axis", "GRAPH_VIEW", plan_parent),
    (model, "Plan", "Annotation", "PLAN_VIEW", plan_parent),
    (model, "Plan", "Annotation", "ELEVATION_VIEW", plan_parent),
    (model, "Plan", "Annotation", "SECTION_VIEW", plan_parent)
]

ifc_subcontexts = {}
for new_subcontext in subcontexts_list:
    ifcopenshell.api.context.add_context(*new_subcontext)

# Write model
model.write("C:/Users/JoeBears/git/stifc/AnnexE.ifc")
