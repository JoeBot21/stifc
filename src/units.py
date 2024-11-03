def get_units(file):
    """Returns a dictionary of units in the ifcopenshell.file object."""
    existing_units = {}
    for unit in file.by_type("IfcSIUnit"):
        if unit[2]:
            existing_units.update({unit[2]+unit[3]: unit})
        else:
            existing_units.update({unit[3]: unit})
    for unit in file.by_type("IfcConversionBasedUnit"):
        existing_units.update({unit[2]: unit})
    for unit in file.by_type("IfcDerivedUnit"):
        existing_units.update({unit[3]: unit})
    return existing_units

def find_dimensional_exponents(file, exponents: tuple):
    """Searches the file for a dimensional exponents entry that matches
       the provided dimensional exponents and returns an existing entry
       or creates and returns a new dimensional exponents entry. This
       may be replaced by utils.reference_existing in the future."""
    exponents_list = []
    ifc_exponents_list = file.by_type("IfcDimensionalExponents")
    for existing_exponents in ifc_exponents_list:
        exponents_list.append(tuple([x for x in existing_exponents]))
    for i in range(0, len(exponents_list)):
        if exponents == exponents_list[i]:
            return ifc_exponents_list[i]
    return file.create_entity("IfcDimensionalExponents", *exponents)

def add_si_unit(file, name: str, unit_type: str, prefix: str = ""):
    """Add a SI unit to the ifcopenshell.file object. IFC uses SI units
       by default and all conversion based and derived units ultimately
       reference the SI units.
    
       Parameters
       ==========
       
       file : ifcopenshell.file
           File to add the unit to
        
        name : str
            Name to assign to the unit Name field
        
        unit_type : str
            Type of unit. Should be an option from IfcUnitEnum.
        
        prefix : str, optional
            Metric prefix to use if applicable"""

    if not get_units(file).get(prefix+name, None):
        if not prefix:
            prefix = None
        file.create_entity("IfcSIUnit",
                            UnitType=unit_type,
                            Prefix=prefix,
                            Name=name)

def add_conversion_based_unit(file,
                              name: str,
                              unit_type: str,
                              exponents: tuple,
                              conversion: float,
                              base: str):
    """Add a conversion based unit to the ifcopenshell.file object.
       Conversion based units are non-SI units that can be converted
       directry back to a single previously defined SI unit.
    
       Parameters
       ==========
       
       file : ifcopenshell.file
           File to add the unit to
        
        name : str
            Name to assign to the unit Name field
        
        unit_type : str
            Type of unit. Should be an option from IfcUnitEnum.
        
        exponents : tuple
            Values to use for the dimensional exponents. Defines the
            dimensionality (length, mass, force, etc) of the unit.
        
        conversion : float
            Value used to convert from the SI base unit to the
            conversion based unit.
        
        base : str
            Name of the SI base unit"""

    existing_units = get_units(file)
    if not existing_units.get(name, None):
        exponents = find_dimensional_exponents(file, exponents)
        conversion_value = file.create_entity("Ifc"+unit_type[0:-4]+"Measure",
                                              conversion)
        ifc_measure_with = file.create_entity("IfcMeasureWithUnit",
                                              conversion_value,
                                              existing_units[base])
        file.create_entity("IfcConversionBasedUnit",
                           exponents,
                           unit_type,
                           name,
                           ifc_measure_with)

def add_derived_unit(file, name: str, unit_type: str, base_units: tuple):
    """Add a derived unit to the ifcopenshell.file object. Derived
       units are based on some combination of two or more previously
       defined units.

       Parameters
       ==========

       file : ifcopenshell.file
           File to add the unit to
        
        name : str
            Name to assign to the unit Name field
        
        unit_type : str
            Type of unit. Should be an option from IfcUnitEnum.
        
        base_units : tuple
            Tuple of tuples containing the units and their associated
            exponents used to derive the new unit."""
    existing_units = get_units(file)
    if not existing_units.get(name, None):
        derived_element_list = []
        for element in base_units:
            derived_element = file.create_entity("IfcDerivedUnitElement",
                                                 existing_units[element[0]],
                                                 element[1])
            derived_element_list.append(derived_element)
        file.create_entity("IfcDerivedUnit",
                           derived_element_list,
                           unit_type,
                           Name=name)