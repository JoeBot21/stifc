# Imports
import ifcopenshell.api.aggregate as ifcAggregate
import ifcopenshell.api.context as ifcContext
import ifcopenshell.api.project as ifcProject
import ifcopenshell.api.pset as ifcPset
import ifcopenshell.api.root as ifcRoot
import ifcopenshell.api.unit as ifcUnit
import ifcopenshell.guid as ifcGuid

# Initialize the project
model = ifcProject.create_file("IFC4X3")
project = ifcRoot.create_entity(
    model,
    ifc_class="IfcProject",
    name="00000-TestProject")

# Add units
## Create the required SI units
SI_units = {
    "LENGTHUNIT": "METRE",
    "MASSUNIT": "GRAM",
    "TIMEUNIT": "SECOND",
    "THERMODYNAMICTEMPERATUREUNIT": "KELVIN",
    "PLANEANGLEUNIT": "RADIAN",
    "SOLIDANGLEUNIT": "STERADIAN",
    "FREQUENCYUNIT": "HERTZ",
    "FORCEUNIT": "NEWTON",
    "ENERGYUNIT": "JOULE",
    "POWERUNIT": "WATT",
    "PRESSUREUNIT": "PASCAL",
    "AREAUNIT": "SQUARE_METRE",
    "VOLUMEUNIT": "CUBIC_METRE"
}

ifc_unit = {}
for unit_type in SI_units.keys():
    name = SI_units[unit_type]
    unit = model.createIfcSIUnit(UnitType=unit_type, Name=name)
    ifc_unit.update({name: unit})

## Create the unit type exponents
unit_type_exponents = {
    "LENGTHUNIT": (1, 0, 0, 0, 0, 0, 0),
    "MASSUNIT": (0, 1, 0, 0, 0, 0, 0),
    "TIMEUNIT": (0, 0, 1, 0, 0, 0, 0),
    "THERMODYNAMICTEMPERATUREUNIT": (0, 0, 0, 0, 1, 0, 0),
    "AREAUNIT": (2, 0, 0, 0, 0, 0, 0),
    "VOLUMEUNIT": (3, 0, 0, 0 ,0, 0, 0),
    "FORCEUNIT": (1, 1, -2, 0, 0, 0, 0),
    "PRESSUREUNIT": (-1, 1, -2, 0, 0, 0, 0)
}

ifc_unit_exponents = {}
for unit_type in unit_type_exponents.keys():
    exponents = model.createIfcDimensionalExponents(
        *unit_type_exponents[unit_type])
    ifc_unit_exponents.update({unit_type: exponents})

## Create conversion based units
conversion_unit_list = [
    ("INCH", "LENGTHUNIT", 0.0254),
    ("FT", "LENGTHUNIT", 0.3048),
    ("SQ_IN", "AREAUNIT", 0.0006452),
    ("SQ_FT", "AREAUNIT", 0.09290304),
    ("CU_IN", "VOLUMEUNIT", 0.00001639),
    ("CU_FT", "VOLUMEUNIT", 0.02831684671168849),
    ("LB", "FORCEUNIT", 4.4482216153),
    ("KIP", "FORCEUNIT", 4448.2216153),
    ("PSI", "PRESSUREUNIT", 6894.7572932),
    ("PSF", "PRESSUREUNIT", 47.88025898),
    ("KSI", "PRESSUREUNIT", 6894757.2932),
    ("KSF", "PRESSUREUNIT", 47880.25898)
]

for new_unit in conversion_unit_list:
    metric_unit = ifc_unit[SI_units[new_unit[1]]]
    conversion_value = model.create_entity(
        "IfcReal",
        wrappedValue=new_unit[2])
    conversion = model.createIfcMeasureWithUnit(
        conversion_value,
        metric_unit)
    unit = model.createIfcConversionBasedUnit(
        Dimensions=ifc_unit_exponents[unit_type],
        UnitType=new_unit[1],
        Name=new_unit[0],
        ConversionFactor=conversion)
    ifc_unit.update({new_unit[0]: unit})

## Create derived units
derived_unit_list = [
    ("PLI", "LINEARFORCEUNIT", (("LB", 1), ("INCH", -1))),
    ("PLF", "LINEARFORCEUNIT", (("LB", 1), ("FT", -1))),
    ("KLI", "LINEARFORCEUNIT", (("KIP", 1), ("INCH", -1))),
    ("KLF", "LINEARFORCEUNIT", (("KIP", 1), ("FT", -1))),
    ("LB_IN", "TORQUEUNIT", (("LB", 1), ("INCH", 1))),
    ("LB_FT", "TORQUEUNIT", (("LB", 1), ("FT", 1))),
    ("KIP_IN", "TORQUEUNIT", (("KIP", 1), ("INCH", 1))),
    ("KIP_FT", "TORQUEUNIT", (("KIP", 1), ("FT", 1)))
]

for new_unit in derived_unit_list:
    derived_element_list = []
    for element in new_unit[2]:
        derived_element = model.createIfcDerivedUnitElement(
            ifc_unit[element[0]],
            element[1])
        derived_element_list.append(derived_element)
    unit = model.createIfcDerivedUnit(
        derived_element_list,
        new_unit[1],
        Name=new_unit[0])
    ifc_unit.update({new_unit[0]: unit})

## Set default units
default_unit_names = ["INCH", "LB"]

default_units = []
for unit in default_unit_names:
    default_units.append(ifc_unit[unit])

ifc_default_units = ifcUnit.assign_unit(model, default_units)


# Add contexts
model_parent = ifcContext.add_context(model, "Model")
plan_parent = ifcContext.add_context(model, "Plan")

subcontexts_list = {
    "model_body": (model, "Model", "Body", "MODEL_VIEW", model_parent),
    "model_axis": (model, "Model", "Axis", "GRAPH_VIEW", model_parent),
    "model_box": (model, "Model", "Box", "MODEL_VIEW", model_parent),
    "plan_body": (model, "Plan", "Body", "PLAN_VIEW", plan_parent),
    "plan_axis": (model, "Plan", "Axis", "GRAPH_VIEW", plan_parent),
    "plan_annotation": (model, "Plan", "Annotation", "PLAN_VIEW", plan_parent),
    "plan_elevation": (model, "Plan", "Annotation", "ELEVATION_VIEW", plan_parent),
    "plan_section": (model, "Plan", "Annotation", "SECTION_VIEW", plan_parent)
}

ifc_subcontexts = {}
for new_subcontext in subcontexts_list.keys():
    subcontext = ifcContext.add_context(*subcontexts_list[new_subcontext])
    ifc_subcontexts.update({new_subcontext: subcontext})


# Add site
site_origin = model.createIfcAxis2Placement3D(
    model.createIfcCartesianPoint((0.0, 0.0, 0.0)),
    model.createIfcDirection((0.0, 0.0, 1.0)),
    model.createIfcDirection((1.0, 0.0, 0.0)))
site_placement = model.createIfcLocalPlacement(RelativePlacement=site_origin)
site = model.createIfcSite(
    GlobalId=ifcGuid.new(),
    Name="PrimarySite",
    ObjectPlacement=site_placement)
ifcAggregate.assign_object(
    model,
    relating_object=project,
    products=[site])

# Add building
building_origin = model.createIfcAxis2Placement3D(
    model.createIfcCartesianPoint((0.0, 0.0, 0.0)),
    model.createIfcDirection((0.0, 0.0, 1.0)),
    model.createIfcDirection((1.0, 0.0, 0.0)))
building_placement = model.createIfcLocalPlacement(
    RelativePlacement=building_origin)
building = model.createIfcBuilding(
    GlobalId=ifcGuid.new(),
    Name="PrimaryBuilding",
    ObjectPlacement=building_placement)
ifcAggregate.assign_object(
    model,
    relating_object=site,
    products=[building])


# Add storeys
storey_list = [
    ("Storey_1", (0.0, 0.0, 0.0), {"EntranceLevel": True, "ElevationOfSSLRelative": 0}),
    ("Storey_2", (0.0, 0.0, 149.0), {"EntranceLevel": True, "ElevationOfSSLRelative": 147}),
    ("Storey_3", (0.0, 0.0, 294.0), {"EntranceLevel": False, "ElevationOfSSLRelative": 294})
]

ifc_storeys = []
for new_storey in storey_list:
    storey_origin = model.createIfcAxis2Placement3D(
    model.createIfcCartesianPoint(new_storey[1]),
    model.createIfcDirection((0.0, 0.0, 1.0)),
    model.createIfcDirection((1.0, 0.0, 0.0)))
    storey_placement = model.createIfcLocalPlacement(
        RelativePlacement=storey_origin)
    storey = model.createIfcBuildingStorey(
        GlobalId=ifcGuid.new(),
        Name=new_storey[0],
        ObjectPlacement=storey_placement)
    storey_pset = ifcPset.add_pset(
        model,
        product=storey,
        name="Pset_BuildingStoreyCommon")
    ifcPset.edit_pset(
        model,
        pset=storey_pset,
        properties=new_storey[2])
    ifc_storeys.append(storey)

ifcAggregate.assign_object(
    model,
    relating_object=building,
    products=ifc_storeys)


# Write model to file
model.write("C:\\Users\\JoeBears\\git\\IFC-Structural-Toolkit\\TestModel.ifc")




















