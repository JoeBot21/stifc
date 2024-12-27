# +
from rich import print

import ifcopenshell
import ifcopenshell.guid

from stifc.ifc.ifc_utils import *
from stifc.ifc.node import set_node_fixities
from stifc.ifc.structural_model import StructuralModel
# -

model = ifcopenshell.open("models/AnnexE.ifc")

analysis_model = StructuralModel(
    model,
    model.by_type("IfcProject")[0],
    Name="AnalysisModel",
    Description="Main 3D analysis model",
    PredefinedType="LOADING_3D")

analysis_model.add_load_case(
    "VARIABLE_Q",
    "LIVE_LOAD_Q",
    Name="TestCase",
    Description="Load case for testing")

# +
node_list = [
    ("node_1", (0.0, 0.0, 0.0)),
    ("node_2", (0.0, 0.0, 120.0)),
    ("node_3", (192.0, 0.0, 0.0)),
    ("node_4", (192.0, 0.0, 120.0))
]

# Create nodes
nodes = {}
for node in node_list:
    nodes.update({node[0]: analysis_model.add_node(node[1], Name=node[0])})

# Fix nodes 1 and 3
for node in ["node_1", "node_3"]:
    set_node_fixities(model, nodes[node], True, True, True, True, True, True)
# -

# model.write("C:/Users/JoeBears/git/stifc/models/AnnexE1.ifc")
model.write("/home/joebot/git/stifc/models/AnnexE1.ifc")

# # Add structural member

point_1 = reference_existing(
    model,
    "IfcVertexPoint",
    reference_existing(model, "IfcCartesianPoint", (0.0, 0.0, 0.0)))
point_2 = reference_existing(
    model,
    "IfcVertexPoint",
    reference_existing(model, "IfcCartesianPoint", (0.0, 0.0, 120.0)))

edge = reference_existing(
    model,
    "IfcEdge",
    point_1,
    point_2)

model_context = model.by_id(73)
print(model_context)

topology_representation = reference_existing(
    model,
    "IfcTopologyRepresentation",
    ContextOfItems=model_context,
    RepresentationIdentifier="Reference",
    RepresentationType="Edge",
    Items=(edge,))

definition_shape = reference_existing(
    model,
    "IfcProductDefinitionShape",
    Name="DefinitionShapeName",
    Description="description text",
    Representations=(topology_representation,))

direction = reference_existing(model, "IfcDirection", (1.0, 0.0, 0.0))

model.create_entity(
    type="IfcStructuralCurveMember",
    GlobalId=ifcopenshell.guid.new(),
    Name="LeftColumn",
    Description="description text",
    Representation=definition_shape,
    PredefinedType="RIGID_JOINED_MEMBER",
    Axis=direction)

#model.write("C:/Users/JoeBears/git/stifc/AnnexE1.ifc")
model.write("/home/joebot/git/stifc/AnnexE1.ifc")
