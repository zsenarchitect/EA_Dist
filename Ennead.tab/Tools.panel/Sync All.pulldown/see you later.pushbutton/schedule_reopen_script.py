

__title__ = "See You Again"
__doc__ = """Schedule current revit(s) to reopen as current files. 
You can set to reopen in a few minutes, or 8 am tomorrow, or next monday morning.

This si especially helpful for team taking long time to open files everyday."""


__tip__ = True
import EnneadTab
from pyrevit import forms, script
# import datetime
from datetime import datetime, timedelta
import time
# https://pypi.org/project/tkTimePicker/
# time picker

uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = EnneadTab.REVIT.REVIT_APPLICATION.get_doc()

@EnneadTab.ERROR_HANDLE.try_catch_error
def main():

    # get all open docs
    docs = EnneadTab.REVIT.REVIT_APPLICATION.get_application().Documents
    docs = [doc for doc in docs if not doc.IsLinked]
    docs = [doc.Title for doc in docs if not doc.IsFamilyDocument]

    data_file = "EA_SCHEDULE_OPENER.json"

    data = None
    if EnneadTab.FOLDER.is_file_exist_in_dump_folder(data_file):
        data = EnneadTab.DATA_FILE.read_json_as_dict_in_dump_folder(
            data_file, True)
        
    if data is None:
        data = dict()

    data["revit_version"] = EnneadTab.REVIT.REVIT_APPLICATION.get_application().VersionNumber
    recorded_docs = data.get("docs", [])
    for doc in docs:
        recorded_docs.append(doc)
    data["docs"] = list(set(recorded_docs))

    options = ["Tomorrow Morning 7am",
               "Tomorrow Morning 8am",
               "Tomorrow Morning 9am",
               "Next Monday Morning 7am",
               "In 5 Mins",               
               "In 2 Mins"]
    schedule_time = forms.ask_for_one_item(prompt="When to reopen current openned documents?",
                                  items = options,title = "EnneadTab See You Soon!",
                                  default = options[0])
    if schedule_time == options[0]:
        schedule_time = get_date(clock=7, is_tomorrow=True, is_next_week=False)
    elif schedule_time == options[1]:
        schedule_time = get_date(8,True, False)
    elif schedule_time == options[2]:
        schedule_time = get_date(9,True, False)
    elif schedule_time == options[3]:
        schedule_time = get_date(7, False, True)
    elif schedule_time == options[4]:
        schedule_time = datetime.now() + timedelta(minutes = 5.0)
    elif schedule_time == options[5]:
        schedule_time = datetime.now() + timedelta(minutes = 2.0)
    else:
        return
    data["open_time"] = schedule_time.isoformat()
    res = EnneadTab.DATA_FILE. save_dict_to_json_in_dump_folder(
        data, data_file, use_encode=True)
    # print (res)
    
    
    
    exe = r"L:\4b_Applied Computing\01_Revit\04_Tools\08_EA Extensions\Project Settings\Exe\SCHEDULE_OPENER_0.2\SCHEDULE_OPENER.EXE"
    EnneadTab.EXE.open_file_in_default_application(exe)
    
    if EnneadTab.USER.get_user_name() in ["paula.gronda"]:
        auto_clicker_exe = r"L:\4b_Applied Computing\01_Revit\04_Tools\08_EA Extensions\Project Settings\Exe\GENERAL_AUTO_CLICKER\GENERAL_AUTO_CLICKER.exe"
        EnneadTab.EXE.open_file_in_default_application(auto_clicker_exe)
    
    EnneadTab.REVIT.REVIT_APPLICATION.sync_and_close()
    
    import time
    time.sleep(5)
    EnneadTab.REVIT.REVIT_APPLICATION.sync_and_close()
    EnneadTab.REVIT.REVIT_APPLICATION.close_revit_app()
    EnneadTab.REVIT.REVIT_FORMS.notification(main_text = "There is nothing to see here. Close this revit.",
                                             sub_text = "Your scheduled reopen revit file will show up in new session.")



def get_date(clock,is_tomorrow, is_next_week):
    # Get the current date and time
    now = datetime.now()


    if is_next_week: 
        # Calculate the number of days until the next Monday
        days_until_next_monday = (7 - now.weekday()) % 7 or 7  # if today is Monday, then get the next Monday

        # Get the date for the next Monday
        target_day = now + timedelta(days=days_until_next_monday)

    if is_tomorrow:
        # Calculate tomorrow's date
        target_day = now + timedelta(days=1)

    # Get 7 a.m. of tomorrow's date
    return datetime(target_day.year, target_day.month, target_day.day, clock, 0)



######################################################
if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    main()
