import ifcopenshell.guid

from src.utils import *


class StructuralModel:
    """stifc StructuralModel object that holds an IFC structural
       analysis model and its rel assigns to group. Includes methods
       to make creating other structural analysis objects easier."""
    def __init__(self,
                 file,
                 project,
                 location: tuple = (0.0, 0.0, 0.0),
                 direction: tuple = (0.0, 0.0, 1.0),
                 axis: tuple = (1.0, 0.0, 0.0),
                 placement_rel_to = None,
                 **kwargs):
        self.file = file
        kwargs.update({"GlobalId": ifcopenshell.guid.new()})
        kwargs.update({"LoadedBy": ()})
        kwargs.update({"HasResults": ()})
        kwargs.update({"SharedPlacement": create_placement(
            self.file,
            location=location,
            direction=direction,
            axis=axis)})
        if not kwargs.get("OrientationOf2DPlane", None):
            kwargs.update({"OrientationOf2DPlane": kwargs["SharedPlacement"]})
        # Create analysis model
        self.IfcStructuralAnalysisModel = self.file.create_entity(
            "IfcStructuralAnalysisModel",
            **kwargs)
        # Relate analysis model upward into the project
        self.file.create_entity(
            "IfcRelDeclares",
            GlobalId=ifcopenshell.guid.new(),
            RelatingContext=project,
            RelatedDefinitions=(self.IfcStructuralAnalysisModel,))
        # Create relating object to hold items in the analysis model
        self.IfcRelAssignsToGroup = self.file.create_entity(
            "IfcRelAssignsToGroup",
            GlobalId=ifcopenshell.guid.new(),
            RelatedObjects=(),
            RelatingGroup=self.IfcStructuralAnalysisModel)
        

    def add_load_case(self,
                      ActionType: str,
                      ActionSource: str,
                      **kwargs):
        # Add load case
        IfcStructuralLoadCase = self.file.create_entity(
            "IfcStructuralLoadCase",
            GlobalId=ifcopenshell.guid.new(),
            Name=kwargs.get("Name", None),
            Description=kwargs.get("Description", None),
            PredefinedType=kwargs.get("PredefinedType", "LOAD_CASE"),
            ActionType=ActionType,
            ActionSource=ActionSource,
            Coefficient=kwargs.get("Coefficient", 1.0),
            Purpose=kwargs.get("Purpose", None),
            SelfWeightCoefficients=kwargs.get("SelfWeightCoefficients", (0.0, 0.0, 0.0)))
        load_case_list = list(self.IfcStructuralAnalysisModel.LoadedBy)
        if load_case_list:
            self.IfcStructuralAnalysisModel.LoadedBy = \
                tuple(load_case_list.append(IfcStructuralLoadCase))
        else:
            self.IfcStructuralAnalysisModel.LoadedBy = \
                (IfcStructuralLoadCase,)
        # Add load case result collector
        IfcStructuralResultGroup = self.file.create_entity(
            "IfcStructuralResultGroup",
            GlobalId=ifcopenshell.guid.new(),
            Name=kwargs.get("Name", None),
            Description=kwargs.get("Description", None),
            TheoryType=kwargs.get("TheoryType", "FIRST_ORDER_THEORY"),
            ResultForLoadGroup=IfcStructuralLoadCase,
            IsLinear=kwargs.get("IsLinear", True))
        results_list = list(self.IfcStructuralAnalysisModel.HasResults)
        if results_list:
            self.IfcStructuralAnalysisModel.HasResults = \
                tuple(results_list.append(IfcStructuralResultGroup))
        else:
            self.IfcStructuralAnalysisModel.HasResults = \
                (IfcStructuralResultGroup,)
        return IfcStructuralLoadCase

