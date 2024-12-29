import pytest

import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.root

from stifc.ifc.structural_model import StructuralModel

def test_StructuralModel_init():
    file = ifcopenshell.api.project.create_file("IFC4X3")
    project = ifcopenshell.api.root.create_entity(
        file,
        "IfcProject",
        name="TestProject")
    result = StructuralModel(
        file,
        project,
        location=(1.0, 1.0, 1.0),
        Name="AnalysisModel",
        PredefinedType="LOADING_3D")
    assert len(file.by_type("IfcStructuralAnalysisModel"))
    assert result.IfcStructuralAnalysisModel.Name == "AnalysisModel"
    assert result.IfcStructuralAnalysisModel.PredefinedType == "LOADING_3D"
    assert result.IfcStructuralAnalysisModel.LoadedBy == ()
    assert result.IfcStructuralAnalysisModel.HasResults == ()
    assert len(file.by_type("IfcLocalPlacement")) == 1
    placement = result.IfcStructuralAnalysisModel.SharedPlacement
    assert placement.RelativePlacement.Location.Coordinates == (1.0, 1.0, 1.0)
    assert len(file.by_type("IfcRelDeclares")) == 1
    declares = file.by_type("IfcRelDeclares")[0]
    assert declares.RelatingContext == project
    assert declares.RelatedDefinitions == (result.IfcStructuralAnalysisModel,)
    assert len(file.by_type("IfcRelAssignsToGroup")) == 1
    assigns = result.IfcRelAssignsToGroup
    assert assigns.RelatedObjects == ()
    assert assigns.RelatingGroup == result.IfcStructuralAnalysisModel

class TestStructuralModel:
    def setup_method(self, method):
        self.file = ifcopenshell.api.project.create_file("IFC4X3")
        self.project = ifcopenshell.api.root.create_entity(
            self.file,
            "IfcProject",
            name="TestProject")
        self.parent_context = ifcopenshell.api.context.add_context(
            self.file,
            "Model")
        self.context = ifcopenshell.api.context.add_context(
            self.file,
            "Model",
            "Body",
            "MODEL_VIEW",
            self.parent_context)
        self.model = StructuralModel(
            self.file,
            self.project,
            Name="AnalysisModel",
            PredefinedType="LOADING_3D")

    def test_add_load_case(self):
        result = self.model.add_load_case(
            "VARIABLE_Q",
            "LIVE_LOAD_Q",
            Name="TestCase")
        assert result.Name == "TestCase"
        assert result.ActionType == "VARIABLE_Q"
        assert result.ActionSource == "LIVE_LOAD_Q"
        assert self.model.IfcStructuralAnalysisModel.LoadedBy[0] == result
        assert len(self.file.by_type("IfcStructuralResultGroup")) == 1
        results_group = self.file.by_type("IfcStructuralResultGroup")[0]
        assert self.model.IfcStructuralAnalysisModel.HasResults[0] == results_group
        assert results_group.Name == "TestCase"
        assert results_group.ResultForLoadGroup == result

    def test_add_node(self):
        result = self.model.add_node((0.0, 0.0, 0.0))
        assert result.Name == "node_0"
        assert result.ObjectPlacement.RelativePlacement.Location.Coordinates == (0.0, 0.0, 0.0)
        assert self.model.nodes["node_0"] == result
        assert self.model.IfcRelAssignsToGroup.RelatedObjects[0] == result
        assert result.Representation.Name == "node_0"
        assert result.Representation.Representations[0].Items[0].VertexGeometry == result.ObjectPlacement.RelativePlacement.Location
