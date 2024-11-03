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
        """Create the stifc StructuralModel object.

           Parameters
           ==========
           
           file : ifcopenshell.file
               File to add the structural model to
            
            project : IfcProject
                IfcProject to relate the structural model up into
            
            location : tuple, optional
                Location of origin used when placing the structural
                model. Defaults to the origin point referenced for
                the placement or the global origin.
            
            direction : tuple, optional
                Direction of the x-axis of the structural model.
                Defaults to the x-axis referenced for the placement or
                the global x-axis.
            
            axis : tuple, optional
                Direction of the z-axis of the structural model.
                Defaults to the z-axis referenced for the placement or
                the global z-axis.
            
            placement_rel_to : IfcAxis2Placement, optional
                IfcAxis2Placement to reference when creating the new
                placement. Defaults to the global coordinate system when
                not defined.
            
            Name : str, optional
                Name to assign to the IfcStructuralAnalysisModel Name
                field
            
            Description : str, optional
                Text to add to the IfcStructuralAnalysisModel
                Description field
            
            PredefinedType : str, optional
                Loading type from IfcAnalysisModelTypeEnum
            
            OrientationOf2DPlane : IfcAxis2Placement3D, optional
                IFC 3D axis placement used to define the orientation of
                the 2D plane in a 3D structural model."""

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
        # Set default representation context to add elements to.
        # This currently just grabs the main 3D context.
        for context in self.file.by_type("IfcGeometricRepresentationContext",
                                     include_subtypes=False):
            if context.CoordinateSpaceDimension == 3:
                self.context = context
        

    def add_load_case(self,
                      ActionType: str,
                      ActionSource: str,
                      **kwargs):
        """Adds a load case and associated results group to the analysis
           model.
           
           Parameters
           ==========
           
           ActionType : str
               Type from IfcActionTypeEnum that defines the nature of
               the loading
            
            ActionSource : str
                Type from IfcActionSourceTypeEnum that defines the cause
                of the loading
            
            Name : str, optional
                Name to assign to the IfcStructuralAnalysisModel Name
                field
            
            Description : str, optional
                Text to add to the IfcStructuralAnalysisModel
                Description field"""

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
            load_case_list.append(IfcStructuralLoadCase)
            self.IfcStructuralAnalysisModel.LoadedBy = tuple(load_case_list)
        else:
            self.IfcStructuralAnalysisModel.LoadedBy = (IfcStructuralLoadCase,)
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
            results_list.append(IfcStructuralResultGroup)
            self.IfcStructuralAnalysisModel.HasResults = tuple(results_list)
        else:
            self.IfcStructuralAnalysisModel.HasResults = (IfcStructuralResultGroup,)
        return IfcStructuralLoadCase


    def add_node(self, Coordinates: tuple, **kwargs):
        """Add a node to the structural analysis model.
        
           Parameters
           ==========
           
           location : tuple
               Location of the node
            
            Name : str, optional
                Name to assign to the IfcStructuralAnalysisModel Name
                field
            
            Description : str, optional
                Text to add to the IfcStructuralAnalysisModel
                Description field"""

        IfcCartesianPoint = self.file.create_entity(
            "IfcCartesianPoint",
            Coordinates=Coordinates)
        IfcVertexPoint = self.file.create_entity(
            "IfcVertexPoint",
            VertexGeometry=IfcCartesianPoint)
        IfcTopologyRepresentation = self.file.create_entity(
            "IfcTopologyRepresentation",
            ContextOfItems=self.context,
            RepresentationIdentifier="Node",
            RepresentationType="Vertex",
            Items=(IfcVertexPoint,))
        IfcProductDefinitionShape = self.file.create_entity(
            "IfcProductDefinitionShape",
            Name=kwargs.get("Name", None),
            Description=kwargs.get("Description", None),
            Representations=(IfcTopologyRepresentation,))
        IfcLocalPlacement = self.file.create_entity(
            "IfcLocalPlacement",
            RelativePlacement=self.file.create_entity(
                "IfcAxis2Placement3D",
                Location=IfcCartesianPoint,
                Axis=self.file.create_entity(
                    "IfcDirection",
                    (1.0, 0.0, 0.0)),
                RefDirection=self.file.create_entity(
                    "IfcDirection",
                    (0.0, 0.0, 1.0))))
        node = self.file.create_entity(
            "IfcStructuralPointConnection",
            GlobalId=ifcopenshell.guid.new(),
            Name=kwargs.get("Name", None),
            Description=kwargs.get("Description", None),
            ObjectPlacement=IfcLocalPlacement,
            Representation=IfcProductDefinitionShape)
        element_list = list(self.IfcRelAssignsToGroup.RelatedObjects)
        if element_list:
            element_list.append(node)
            self.IfcRelAssignsToGroup.RelatedObjects = tuple(element_list)
        else:
            self.IfcRelAssignsToGroup.RelatedObjects = (node,)
        return node
        
            
                 