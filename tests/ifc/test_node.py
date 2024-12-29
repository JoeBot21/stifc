import pytest

import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.root

from stifc.ifc.structural_model import StructuralModel
from stifc.ifc import node

class TestNode:
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
            Name="AnalysisMode",
            PredefinedType="LOADING_3D")
        self.node = self.model.add_node((0.0, 0.0, 0.0))

    def test_set_node_fixities_1(self):
        node.set_node_fixities(
            self.file,
            self.node,
            True, True, True,
            RotationalStiffnessZ=True)
        assert len(self.file.by_type("IfcBoundaryNodeCondition")) == 1
        result = self.file.by_type("IfcBoundaryNodeCondition")[0]
        assert self.node.AppliedCondition == result
        assert result.TranslationalStiffnessX.wrappedValue == True
        assert result.TranslationalStiffnessY.wrappedValue == True
        assert result.TranslationalStiffnessZ.wrappedValue == True
        assert result.RotationalStiffnessX.wrappedValue == False
        assert result.RotationalStiffnessY.wrappedValue == False
        assert result.RotationalStiffnessZ.wrappedValue == True

    def test_set_node_fixities_2(self):
        node.set_node_fixities(
            self.file,
            self.node,
            True, True, True, True, True, True)
        node.set_node_fixities(
            self.file,
            self.node,
            False, False, False, False, False, False)
        assert len(self.file.by_type("IfcBoundaryNodeCondition")) == 1
        result = self.file.by_type("IfcBoundaryNodeCondition")[0]
        assert self.node.AppliedCondition == result
        assert result.TranslationalStiffnessX.wrappedValue == False
        assert result.TranslationalStiffnessY.wrappedValue == False
        assert result.TranslationalStiffnessZ.wrappedValue == False
        assert result.RotationalStiffnessX.wrappedValue == False
        assert result.RotationalStiffnessY.wrappedValue == False
        assert result.RotationalStiffnessZ.wrappedValue == False
