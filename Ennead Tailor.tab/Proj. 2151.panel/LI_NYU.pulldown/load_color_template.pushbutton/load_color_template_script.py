#!/usr/bin/python
# -*- coding: utf-8 -*-


__doc__ = """Update color scheme with office template excel version
J:\\2151\\2_Master File\\B-70_Programming\\03_Colors\\Color Scheme_NYULI_Active.xls.
NOTE: excel should be saved with .xls instead of .xlsx format
Also note, the column header should be as such:
A: Department
B: Department Abbr.
C: Department Color

D: Program
E: Program Abbr.
F: Program Color

ANYTHING ELSE IN THE EXCEL FILE WILL BE IGNORED, including the hex code text on color cell and red, green, blue value number. 
Those manual color text cannot be trusted on the long run.
"""
__title__ = "Load Color Template"

# from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG
import EnneadTab
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
doc = __revit__.ActiveUIDocument.Document



EXCEL_PATH = "J:\\2151\\2_Master File\\B-70_Programming\\03_Colors\\Color Scheme_NYULI_Active.xls"
NAMING_MAP = {"department_color_map":"Primary_Department Category",
              "program_color_map":"Primary_Department Program Type"}


# NAMING_MAP = {"department_color_map":"test1",
#               "program_color_map":"test2"}

   
@EnneadTab.ERROR_HANDLE.try_catch_error
def load_color_template():
    
    # load data from color excel
    data = EnneadTab.COLOR.get_color_template_data(EXCEL_PATH)
    
    
    # for key, value in data.items():
        
    #     print ("\n\n\n{} :\n{} ".format(key, value))

    # return
 
    


    
    # update color scheme, create if not exist, update color if exist
    t = DB.Transaction(doc, "Update Color Scheme")
    t.Start()
    for key in NAMING_MAP.keys():
        update_color_scheme(data, lookup_key = key)
    t.Commit()
    
    EnneadTab.NOTIFICATION.messenger(main_text="Color Scheme Updated!")
    print ("\n\nDone!")

    EnneadTab.OUTPUT.display_output_on_browser()


def update_color_scheme(data, lookup_key):
    color_scheme = EnneadTab.REVIT.REVIT_SELECTION.get_color_scheme_by_name(NAMING_MAP[lookup_key])
    if not color_scheme:
        EnneadTab.NOTIFICATION.messenger(main_text="Color Scheme [{}] not found!\nCheck spelling".format(NAMING_MAP[lookup_key]))
        return
    
    output.print_md ("##Working on color scheme [{}]".format(color_scheme.Name))
    
    
    department_data = data[lookup_key]
    
    sample_entry = list(color_scheme.GetEntries())[0]
    storage_type = sample_entry.StorageType
    
    # print (sample_entry.GetStringValue ())
    # print (sample_entry.StorageType)
    
    current_entry_names = [x.GetStringValue() for x in color_scheme.GetEntries()]
    
    
    add_missing_entry(color_scheme, department_data, current_entry_names, storage_type)
    update_entry_color(color_scheme, department_data)

    
def markdown_text(text, colorRGB):
    return '<span style="color:rgb{};">{}</span>'.format(str(colorRGB),text)

    
    
def add_missing_entry(color_scheme, department_data, current_entry_names, storage_type):
    for department in department_data.keys():
        if department not in current_entry_names:
            entry = DB.ColorFillSchemeEntry (storage_type)
        
            entry.Color = EnneadTab.COLOR.tuple_to_color(department_data[department]["color"])
          
            entry.SetStringValue (department)
            entry.FillPatternId = EnneadTab.REVIT.REVIT_SELECTION.get_solid_fill_pattern_id(doc)
            color_scheme.AddEntry (entry)
            # print ("+++ entry [{}] added".format(department))
            output.print_md("**+++** entry [{}] added with **{}**".format(department, 
                                                              markdown_text("COLOR RGB={}".format(department_data[department]["color"]), department_data[department]["color"])))
        
    
    
def update_entry_color(color_scheme, department_data):
    for existing_entry in color_scheme.GetEntries():
        entry_title = existing_entry.GetStringValue ()
        existing_color = existing_entry.Color
        
        lookup_data = department_data.get(entry_title, None)
        if not lookup_data:
            # print ("??? entry [{}] in current area scheme not found template excel".format(entry_title))
            output.print_md("###  ??? entry [{}] in current area scheme not found template excel. Are you defining new entry?\nThis entry is skipped for now.".format(entry_title))
                                                             
            continue
        
        lookup_color = EnneadTab.COLOR.tuple_to_color(lookup_data["color"])
        
        if EnneadTab.COLOR.is_same_color(existing_color, lookup_color):
            continue
        
        old_color = (existing_entry.Color.Red, existing_entry.Color.Green, existing_entry.Color.Blue)
        existing_entry.Color = lookup_color
        color_scheme.UpdateEntry (existing_entry)
        output.print_md("**$$$** entry [{}] updated from **{}** to **{}**".format(entry_title, 
                                                                              markdown_text("OLD COLOR RGB={}".format(old_color), old_color),
                                                                              markdown_text("NEW COLOR RGB={}".format(lookup_data["color"]), lookup_data["color"])))
        


################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    load_color_template()
    ENNEAD_LOG.use_enneadtab(coin_change = 200, tool_used = __title__.replace("\n", " "), show_toast = True)









