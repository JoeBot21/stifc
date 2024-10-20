import ifcopenshell.guid

class StructuralModel:
    def __init__(self,
                 file,
                 project,
                 location: tuple = (0.0, 0.0, 0.0),
                 direction: tuple = ((0.0, 0.0, 1.0), (1.0, 0.0, 0.0)),
                 placement_rel_to = None,
                 **kwargs):
        self.file = file
        kwargs.update({"GlobalId": ifcopenshell.guid.new()})
        kwargs.update({"LoadedBy": ()})
        kwargs.update({"HasResults": ()})
        # Create placement object for analysis model
        kwargs.update({"SharedPlacement": file.create_entity(
            "IfcLocalPlacement",
            PlacementRelTo=placement_rel_to,
            RelativePlacement=file.create_entity(
                "IfcAxis2Placement3D",
                Location=file.create_entity("IfcCartesianPoint", location),
                Axis=file.create_entity("IfcDirection", direction[0]),
                RefDirection=file.create_entity("IfcDirection", direction[1])
            ))})
        if not kwargs.get("OrientationOf2DPlane", None):
            kwargs.update({"OrientationOf2DPlane": kwargs["SharedPlacement"]})
        # Create analysis model
        self.analysis_model = file.create_entity(
            "IfcStructuralAnalysisModel",
            **kwargs)
        # Relate analysis model upward into the project
        file.create_entity(
            "IfcRelDeclares",
            GlobalId=ifcopenshell.guid.new(),
            RelatingContext=project,
            RelatedDefinitions=(self.analysis_model,))
        # Create relating object to hold items in the analysis model
        self.holds = file.create_entity(
            "IfcRelAssignsToGroup",
            GlobalId=ifcopenshell.guid.new(),
            RelatedObjects=(),
            RelatingGroup=self.analysis_model)
        
        