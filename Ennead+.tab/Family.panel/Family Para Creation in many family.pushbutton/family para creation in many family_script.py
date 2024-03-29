__doc__ = "Help you get started with many family by adding many useful parameter quickly."
__title__ = "Family Parameter\nCreation In Many Families"

from pyrevit import forms, script
import EA_UTILITY
import EnneadTab
from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document
import re

def ft_to_mm(dist):
    return (dist/3.28084)*1000
def mm_to_ft(dist):
    return (dist/1000)*3.28084

def add_yes_no(docs):
    add_yes_no_type_para(docs, name = "no", tooltip = "You can use this in your formula:\nif(condition,yes,no)",default_value = False, default_formula = "1>2")
    add_yes_no_type_para(docs, name = "yes", tooltip = "You can use this in your formula:\nif(condition,yes,no)",default_value = False, default_formula = "not(no)")





def add_yes_no_type_para(doc, name, tooltip = "Generated by EnneadTab para creater", default_value = False, default_formula = ""):
    #print "%%%%"
    #print doc
    if type(doc) is list:
        for item_doc in doc:
            add_yes_no_type_para(item_doc, name, tooltip, default_value, default_formula)
        return

    family_manager = doc.FamilyManager
    if default_value != False:
        default_value = eval(default_value)


    para_name = name


    try:
        para_group = DB.BuiltInParameterGroup.PG_GENERAL
        para_type = DB.ParameterType.YesNo
    #  since 2023, ParameterType property is no longer valid.
    except:
        para_group = DB.GroupTypeId.General 
        para_type = EnneadTab.REVIT.REVIT_UNIT.lookup_unit_spec_id("yesno")
    is_instance = True


    t = DB.Transaction(doc, "Add parameter")
    t.Start()

    try:
        para = family_manager.AddParameter(para_name,\
                                        para_group,\
                                        para_type,\
                                        is_instance)
        try:
            family_manager.Set(para, default_value)
        except:
            print "cannot set default value"
        if default_formula != "":
            try:
                family_manager.SetFormula(para, default_formula)
            except:
                print "cannot set formula"
        family_manager.SetDescription(para, tooltip)

        LOG = "\n<{}> added as Yes/No parameter in [{}], default as {}".format(name, doc.Title, default_value)
        if default_formula != "":
            LOG += ", formula as {}".format(default_formula)
        print LOG
    except Exception as e:
        EA_UTILITY.dialogue(main_text = "<{}> parameter cannot be created becasue {}.".format(para_name, e))
    t.Commit()

def add_dim_type_para(doc, name, tooltip = "", default_value = 1, default_formula = None):
    if type(doc) is list:
        for item_doc in doc:
            add_dim_type_para(item_doc, name, tooltip, default_value, default_formula)
        return


    family_manager = doc.FamilyManager
    para_name = name
    try:
        para_group = DB.BuiltInParameterGroup.PG_ADSK_MODEL_PROPERTIES
        para_type = DB.ParameterType.Length
    #  since 2023, ParameterType property is no longer valid.
    except:
        para_group = DB.GroupTypeId.AdskModelProperties 
        para_type = EnneadTab.REVIT.REVIT_UNIT.lookup_unit_spec_id("length")
    is_instance = True
    t = DB.Transaction(doc, "Add parameter")
    t.Start()
    try:
        para = family_manager.AddParameter(para_name,\
                                        para_group,\
                                        para_type,\
                                        is_instance)

        try:
            family_manager.Set(para, default_value)
        except:
            pass
        if not default_formula:
            try:
                family_manager.SetFormula(para, default_formula)
            except:
                pass

        family_manager.SetDescription(para, tooltip)

        LOG = "\n<{}> added as Length parameter in [{}], default as {}".format(name, doc.Title, default_value)
        if default_formula != "":
            LOG += ", formula as {}".format(default_formula)
        print LOG
    except Exception as e:
        EA_UTILITY.dialogue(main_text = "<{}> parameter cannot be created becasue {}.".format(para_name, e))

    t.Commit()





def create_paras():


    working_docs = EnneadTab.REVIT.REVIT_APPLICATION.select_family_docs(select_multiple = True, including_current_doc = True)
    if not working_docs:
        return
    print "Working on those families:"
    for doc in working_docs:
        print "- " + doc.Title
    print "#"*50
    while True:
        if not pick_para(working_docs):
            EnneadTab.SOUNDS.play_sound()
            return




def pick_para(working_docs):
    options = ["---End Tool Now---",\
                "YesNo--> Yes/No",\
                "YesNo--> <Type In><Default False>",\
                "YesNo--> <Type In><Default Value><Default Formula>",\
                "Length--> <Type In><Default Value>",\
                "Length--> FRW mullion_H",\
                "Length--> Spandrel_H",
                "YesNo--> is_start",\
                "YesNo--> is_end",\
                "YesNo--> is_corner",\
                "YesNo--> is_top",\
                "YesNo--> is_bm",\
                "YesNo--> is_terrace",\
                "YesNo--> is_ground",\
                "YesNo--> is_operable",\
                "YesNo--> is_louver",\
                "YesNo--> is_louver upper",\
                "YesNo--> is_louver lower",\
                "YesNo--> is_FRW",\
                "YesNo--> is_full clear",\
                "YesNo--> is_double pane clear",\
                "YesNo--> is_double pane spandrel",\
                "YesNo--> is_full spandrel",\
                "YesNo--> is_door",\
                "YesNo--> is_louver lower",\
                "YesNo--> is_louver upper",\
                "YesNo--> show_mullion FRW",\
                "YesNo--> show_coping",\
                "YesNo--> show_backpan",\
                "YesNo--> show_louver",\
                "YesNo--> show_glass vision",\
                "YesNo--> show_glass spandrel",\
                "YesNo--> show_railing",\
                "YesNo--> show_mullion spandrel"]

    sel = forms.SelectFromList.show(options,
                                    multiselect = False,
                                    title = "Let's do those action to the family.",
                                    button_name= "Let's go!"
                                    )

    if sel == None or sel == options[0]:
        return False


    #

    process_docs(working_docs, sel)
    EnneadTab.SOUNDS.play_sound("sound effect_popup msg3.wav")
    return True

def process_docs(docs, selection):
    """
    if doc.IsFamilyDocument != True:
        EA_UTILITY.dialogue(main_text = "This tool is only appliable when you are in family document.")
        return False
    """
    #print revit.doc.Title

    #print family_manager




    para_name = selection.split("--> ")[-1]
    para_type = selection.split("--> ")[0]

    if para_type == "YesNo":
        if "Yes/No" in para_name:

            add_yes_no(docs)
            return True

        if "<Type In><Default False>" in para_name:
            template_string = "Type in para name here."

            user_input = forms.ask_for_string(default = template_string, prompt="Type below the name of the parameter\nleave it blank if you want to exit.", title="Name and default value of the parameter", width = 1000)
            template_string = user_input
            if not user_input or user_input == "" or len(user_input) == 0:
                return False
            para_name = user_input


            add_yes_no_type_para(docs, para_name)
            return True




        if "<Type In><Default Value><Default Formula>" in para_name:
            template_string = "<Para><True/False><No_Formula>"
            while True:
                user_input = forms.ask_for_string(default = template_string, prompt="Type below the name of the parameter\nleave it blank if you want to exit.", title="Name, default T/F and formula of the parameter", width = 1000)
                template_string = user_input
                if not user_input or user_input == "" or len(user_input) == 0:
                    return False
                try:
                    match = re.search(r"<(.+)><(.+)><(.+)>", user_input)
                    para_name, default_value, default_formula = match.group(1), match.group(2), match.group(3)
                    #print para_name, default_value, default_formula
                    if default_value not in ["True", "False"]:
                        EA_UTILITY.dialogue(main_text = "Default_Value need to be either 'True' or 'False'")
                        continue
                    if default_formula == "No_Formula":
                        default_formula = ""
                    break
                except Exception as e:
                    print str(e)

            add_yes_no_type_para(docs, para_name, default_value = default_value, default_formula = default_formula)
            return True


        add_yes_no_type_para(docs, para_name)
        return True


    elif para_type == "Length":

        if "<Type In><Default Value>" in para_name:
            template_string = "<Para><Default_Length_in_Ft>"
            while True:
                user_input = forms.ask_for_string(default = template_string, prompt="Type below the name of the parameter,\nleave it blank if you want to exit.", title="Name and default length of the parameter", width = 1000)
                template_string = user_input
                if not user_input or user_input == "" or len(user_input) == 0:
                    return False
                try:
                    match = re.search(r"<(.+)><(.+)>", user_input)
                    para_name, default_value = match.group(1), match.group(2)

                    default_value = float(default_value)
                    break
                except Exception as e:
                    print str(e)

            add_dim_type_para(docs, para_name, default_value = default_value)
            return True

        add_dim_type_para(docs, para_name)
        return True


    return True



################## main code below #####################
output = script.get_output()
output.close_others()
if __name__ == "__main__":
    create_paras()
    import ENNEAD_LOG
    ENNEAD_LOG.use_enneadtab(coin_change = 30, tool_used = "Family para creation in many docs.", show_toast = True)
