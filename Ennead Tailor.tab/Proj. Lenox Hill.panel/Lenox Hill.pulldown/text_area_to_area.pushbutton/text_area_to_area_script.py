#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Get the text type parameter value to area value by removing the 'SF' in the value and convert to float type"
__title__ = "Text Area --> Area"

# from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG
import EnneadTab
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
# uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = EnneadTab.REVIT.REVIT_APPLICATION.get_doc()
            
@EnneadTab.ERROR_HANDLE.try_catch_error
def text_area_to_area():
    for area in DB.FileredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Areas).WhereElementIsNotElementType().ToElements():
        bad_data = area.LookupParameter("Proposed Data_old").AsString().replace("SF", "")
        area.LookupParameter("Proposed Data").Set(float(bad_data))


################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    text_area_to_area()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)







