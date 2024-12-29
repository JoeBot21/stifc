from stifc.ifc.ifc_utils import *

def set_node_fixities(file,
                      node,
                      *args,
                      **kwargs):
    """Assign restraints to a node. By default nodes are unrestrained.

       Parameters
       ==========

       file : ifcopenshell.file
           File containing the node

       node : IfcStructuralPointConnection
           Node to assing restraints to

        TranslationalStiffnessX : bool, optional
            Restraint against translation along the x-axis

        TranslationalStiffnessY : bool, optional
            Restraint against translation along the y-axis

        TranslationalStiffnessZ : bool, optional
            Restraint against translation along the z-axis

        RotationalStiffnessX : bool, optional
            Restraint against rotation about the x-axis

        RotationalStiffnessY : bool, optional
            Restraint against rotation about the y-axis

        RotationalStiffnessZ : bool, optional
            Restraint against rotation about the z-axis"""

    arg_order = [
        "TranslationalStiffnessX",
        "TranslationalStiffnessY",
        "TranslationalStiffnessZ",
        "RotationalStiffnessX",
        "RotationalStiffnessY",
        "RotationalStiffnessZ"]
    # Get existing boundary conditions. Default is unrestrained
    IfcBoundaryNodeCondition = node.AppliedCondition
    if not IfcBoundaryNodeCondition:
        default_values = {}
        for fixity in arg_order:
            default_values.update({
                fixity: file.create_entity("IfcBoolean", False)})
        IfcBoundaryNodeCondition = file.create_entity(
            "IfcBoundaryNodeCondition",
            **default_values)
        node.AppliedCondition = IfcBoundaryNodeCondition

    # Set boundary conditions
    for fixity in range(len(args)):
        setattr(IfcBoundaryNodeCondition,
                arg_order[fixity],
                file.create_entity("IfcBoolean", args[fixity]))
    for fixity in kwargs.keys():
        setattr(IfcBoundaryNodeCondition,
                fixity,
                file.create_entity("IfcBoolean", kwargs[fixity]))

