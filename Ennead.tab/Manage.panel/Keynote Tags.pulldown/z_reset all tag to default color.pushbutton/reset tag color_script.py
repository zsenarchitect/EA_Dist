__doc__ = "Reset all keynote tag local override color to default. It might got its color from the other checking type button."
__title__ = "KeynoteTAG Reset Color"
__tip__ = True
import EA_UTILITY
import EnneadTab
from pyrevit import forms, DB, revit, script

uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = EnneadTab.REVIT.REVIT_APPLICATION.get_doc()


@EnneadTab.ERROR_HANDLE.try_catch_error
def main():
    key_note_tags = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_KeynoteTags).WhereElementIsNotElementType().ToElements()

    processed_element_count = 0
    with revit.Transaction("reset keynote tag"):
        for tag in key_note_tags:
            if EA_UTILITY.is_owned(tag):
                print ("---tag being owned, skip reset")
                continue
            view = revit.doc.GetElement(tag.OwnerViewId)
            if EA_UTILITY.is_owned(view):
                print ("---view [{}] being owned, skip reset".format(view.Name))
                continue
            OG_setting = DB.OverrideGraphicSettings()
            view.SetElementOverrides(tag.Id, OG_setting)
            processed_element_count += 1

    forms.alert("{} keynotes have been reset to default color.\n{} keynotes skipped due to ownership.\nSee output for details".format(processed_element_count, len(key_note_tags) - processed_element_count))
################## main code below #####################
if __name__ == "__main__":
        
    output = script.get_output()
    output.close_others()
    main()

