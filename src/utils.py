def append_to_internal_list(ifc_object, target_name: str, value):
    """Adds the specified value to a list type ifcopenshell object
       attribute. This is useful because it handles some of the
       necessary type checking.
       
       Parameters
       ==========
       
       ifc_object : ifcopenshell object
           ifcopenshell object with the list to append the value to
        
        target_name : str
            Name of the object property referencing the list to append
            the value to
        
        value : any
            Value to append"""
    
    target = list(getattr(ifc_object, target_name))
    if target:
        target.append(value)
        setattr(ifc_object, target_name, target)
    else:
        setattr(ifc_object, target_name, (value,))


def create_placement(file,
                     location: tuple,
                     direction: tuple,
                     axis: tuple = None,
                     placement_rel_to=None):
    """Create a 2D or 3D placement object.
    
       Parameters
       ==========
       
       file : ifcopenshell.file
           File to add the unit to
        
        location : tuple
            Origin point of the placement object
        
        direction : tuple
            Tuple to define the direction of the local x-axis
        
        axis : tuple, optional
            Tuple to define the direction of the local z-axis. If this
            is defined a 3D placement is created, otherwise a 2D
            placement is created.
        
        placement_rel_to : IfcAxis2Placement, optional
            IfcAxis2Placement to reference when creating the new
            placement. Defaults to the global coordinate system when
            not defined."""
    
    location = file.create_entity("IfcCartesianPoint", location)
    ref_direction = file.create_entity("IfcDirection", direction)
    if axis:
        relative_placement = file.create_entity(
            "IfcAxis2Placement2D",
            Location=location,
            RefDirection=file.create_entity("IfcDirection", direction))
    else:
        relative_placement = file.create_entity(
            "IfcAxis2Placement3D",
            Location=location,
            Axis=file.create_entity("IfcDirection", axis),
            RefDirection=ref_direction)
    placement = file.create_entity(
        "IfcLocalPlacement",
        PlacementRelTo=placement_rel_to,
        RelativePlacement=relative_placement)
    return placement


def reference_existing(file, kind: str, *args, **kwargs):
    """Searches for an instance of kind with the given values and
       and returns it. If an existing instance cannot be found a new
       one is created. This is to make it easier to 'reuse' non-rooted
       entities. Arguments are similar to file.create_entity."""
    ifc_list = file.by_type(kind)
    if not ifc_list:
        return file.create_entity(kind, *args, **kwargs)
    # Create a complete dict of values for the desired instance
    values_dict = vars(ifc_list[0])
    del values_dict["id"]
    del values_dict["type"]
    for key in values_dict.keys():
        values_dict.update({key: None})
    for i in range(len(args)):
        #This behavior may not be ideal since it is dict order dependant
        values_dict.update({list(values_dict.keys())[i]: args[i]})
    for key in kwargs.keys():
        values_dict.update({key: kwargs[key]})
    # Find an existing instance or create a new one if needed
    for i in range(len(ifc_list)):
        existing_dict = vars(ifc_list[i])
        del existing_dict["id"]
        del existing_dict["type"]
        if values_dict == existing_dict:
            return ifc_list[i]
    return file.create_entity(kind, **values_dict)