#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Set the filled region border line to a specific line style"
__title__ = "Set FilledRegion\nBorder Style"

from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG
import EnneadTab
from EnneadTab.REVIT import REVIT_SELECTION
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


def set_filled_region_border_line():
    selection_ids = uidoc.Selection.GetElementIds ()
    selection = [doc.GetElement(x) for x in selection_ids]
    selection = filter(lambda x: type(x) == DB.FilledRegion, selection)

    if len(selection) == 0:
        print ("There is not any FilledRegion in the selection")
        return
    


    line_style = REVIT_SELECTION.pick_linestyle(doc, filledregion_friendly = True)
    if not line_style:
        print ("There is no line style selected")
        return
    


    t = DB.Transaction(doc, __title__)
    t.Start()
    for filled_region in selection:
        filled_region.SetLineStyleId(line_style.Id)

    t.Commit()

################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    set_filled_region_border_line()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)











