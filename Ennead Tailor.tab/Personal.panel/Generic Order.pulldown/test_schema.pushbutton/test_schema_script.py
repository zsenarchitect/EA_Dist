#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Sen Zhang has not writed documentation for this tool, but he should!"
__title__ = "test_schema"

# from pyrevit import forms #

from pyrevit import script #

import ENNEAD_LOG
import EnneadTab
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
# uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = EnneadTab.REVIT.REVIT_APPLICATION.get_doc()


from EnneadTab.REVIT import REVIT_SCHEMA
from EnneadTab import NOTIFICATION

       
@EnneadTab.ERROR_HANDLE.try_catch_error
def test_schema():
    schema_name = "SampleSchema2"
    schema = REVIT_SCHEMA.get_schema_by_name(schema_name)
    if not schema:
        NOTIFICATION.messenger("need to make new schema")
        schema = REVIT_SCHEMA.create_schema(schema_name)



    t = DB.Transaction(doc, __title__)
    t.Start()
    grids = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
    for grid in grids:
        #REVIT_SCHEMA.update_schema_entity(schema, grid, "IsProtectedElement", True)
        REVIT_SCHEMA.update_schema_entity(schema, grid, "testtest", 12)



    t.Commit()



################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    test_schema()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)







