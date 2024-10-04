import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.unit


class TestClass(ifcopenshell.file):
    def __init__(
        self,
        f: Optional[ifcopenshell.ifcopenshell_wrapper.file] = None,
        schema: Optional[str] = None,
        schema_version: Optional[tuple[int, int, int, int]] = None,
    ):
        super().__init__(f=f, schema=schema, schema_version=schema_version)


model = TestC


