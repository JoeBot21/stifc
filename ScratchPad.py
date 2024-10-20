# +
from rich import print

import ifcopenshell
import ifcopenshell.guid

from utils import *
# -

model = ifcopenshell.open("AnnexE.ifc")

# # Add load case
# The IFC standard has an IfcStructuralLoadCase store information about
# the action (loads) on the structure and an associated
# IfcStructuralResultGroup store the results of the actions.
# It might be good to create a stifc.create_load_case function that
# creates both of these simultaneously and adds them to the structural
# analysis model.

load_case = model.create_entity(
    type="IfcStructuralLoadCase",
    GlobalId=ifcopenshell.guid.new(),
    Name="LoadCase1",
    Description="description text",
    PredefinedType="LOAD_CASE",
    ActionType="VARIABLE_Q",
    ActionSource="LIVE_LOAD_Q",
    Coefficient=1,
    SelfWeightCoefficients=(0.0, 0.0, 0.0))

load_case_results = model.create_entity(
    type="IfcStructuralResultGroup",
    GlobalId=ifcopenshell.guid.new(),
    Name="LoadCase1",
    Description="description text",
    TheoryType="FIRST_ORDER_THEORY",
    ResultForLoadGroup=load_case,
    IsLinear=True)

# # Add structural analysis model

origin = model.create_entity("IfcAxis2Placement3D",
             model.create_entity("IfcCartesianPoint", (0.0, 0.0, 0.0)),
             model.create_entity("IfcDirection", (0.0, 0.0, 1.0)),
             model.create_entity("IfcDirection", (1.0, 0.0, 0.0)))
origin_placement = model.create_entity("IfcLocalPlacement",
                                       RelativePlacement=origin)

analysis_model = model.create_entity(
    type="IfcStructuralAnalysisModel",
    GlobalId=ifcopenshell.guid.new(),
    Name="AnalysisModel",
    Description="description text",
    PredefinedType="LOADING_3D",
    OrientationOf2DPlane=origin,
    LoadedBy=(load_case,),
    HasResults=(load_case_results,),
    SharedPlacement=origin_placement)

model.create_entity(
    type="IfcRelDeclares",
    GlobalId=ifcopenshell.guid.new(),
    Name="AnalysisModelRelation",
    Description="description text",
    RelatingContext=model.by_type("IfcProject")[0],
    RelatedDefinitions=(analysis_model,))

# # Add structural member



# +
#model.write("C:/Users/JoeBears/git/stifc/AnnexE1.ifc")
