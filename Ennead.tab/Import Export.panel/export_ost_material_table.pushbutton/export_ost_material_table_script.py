#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = """Export the OST and material table so it can be used in Rhino import when using 'map Revit SubC'.

With this tool, the layer in Rhino can be assigned with similar Revit material based on layer names.
If you have not done already, you can update dwg export layer mapping with EnneadTab first so each SubCategory in object style table become something rhino layer can match.
"""
__title__ = "Export SubCategory\nMaterial Table"
__tip__ = True
# from pyrevit import forms #
import pprint
from pyrevit import script #

import ENNEAD_LOG
from  EnneadTab import NOTIFICATION, DATA_FILE
from EnneadTab.REVIT import REVIT_APPLICATION

from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
uidoc = REVIT_APPLICATION.get_uidoc()
doc = REVIT_APPLICATION.get_doc()


class Solution:
    def __init__(self):
        self.table = dict()
        
    def process_category(self, category):
        if "Imports in Families" in category.Name or ".dwg" in category.Name.lower():
            return
        if category.Parent:
            if "Imports in Families" in category.Parent.Name or ".dwg" in category.Parent.Name.lower():
                return    

        if category.Material is None:
            # self.table[layer_name] = material_data
            return
        
        
        if category.Parent:
            layer_name = "{}_{}".format(category.Parent.Name, category.Name)
        else:
            layer_name = "{}".format(category.Name)
            


        material_data = dict()
        material = category.Material
        material_data["shading"] = {"name": material.Name,
                                    "color": {"red": int(material.Color.Red), "green": int(material.Color.Green), "blue": int(material.Color.Blue)},                      
                                    "transparency": material.Transparency,
                                    "glossy": material.Shininess ,
                                    "smoothness": material.Smoothness}
        
        apperance_asset = doc.GetElement(material.AppearanceAssetId)
        # print apperance_asset
        # for para in apperance_asset.Parameters:
        #     print para.Definition.Name
        # material_data["appearance"] = {"name": apperance_asset.Name,
        #                                "color": apperance_asset.Color.ToArgb(), 
        #                                 "transparency": apperance_asset.Transparency}
        
        # print (material_data)
        self.table[layer_name] = material_data
        
        
    def export_ost_material_table(self):
        
        categories = doc.Settings.Categories
        for i, category in enumerate(categories):

            self.process_category(category)
            
            for sub_c in category.SubCategories:
                self.process_category(sub_c)
        

        DATA_FILE.pretty_print_dict (self.table)
        # pprint.pprint(self.table, indent=4)
        DATA_FILE.save_dict_to_json_in_dump_folder(self.table, "SUBC_MATERIAL_TABLE.json", use_encode = True)
        NOTIFICATION.messenger(main_text="Export done, now swicth to 'map Revit SubC' in Rhino")
################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    Solution().export_ost_material_table()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)








