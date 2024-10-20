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
        self.analysis_model = self.file.create_entity(
            "IfcStructuralAnalysisModel",
            **kwargs)
        # Relate analysis model upward into the project
        self.file.create_entity(
            "IfcRelDeclares",
            GlobalId=ifcopenshell.guid.new(),
            RelatingContext=project,
            RelatedDefinitions=(self.analysis_model,))
        # Create relating object to hold items in the analysis model
        self.holds = self.file.create_entity(
            "IfcRelAssignsToGroup",
            GlobalId=ifcopenshell.guid.new(),
            RelatedObjects=(),
            RelatingGroup=self.analysis_model)
        

    def add_node(self, 