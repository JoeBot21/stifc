def make_numbered_name(iterable, base_string: str):
    """Create a new generic name given a set of items and a base string

       Parameters
       ==========

       iterable : iterable of str
           Iterable of names to generate the new name for

       base_string : str
           Base string to add a number to when making the name"""
    numbered_names = [x for x in iterable if base_string in x
                      and x.lstrip(base_string).isdigit()]
    try:
        number = max([int(x.lstrip(base_string)) for x in numbered_names])
    except:
        number = -1
    name = base_string+str(number+1)
    return name
