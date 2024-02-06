
from pyrevit import  EXEC_PARAMS, script

import EnneadTab
from Autodesk.Revit import DB
from Autodesk.Revit import UI
args = EXEC_PARAMS.event_args
doc = args.ActiveDocument 
uiapp = UI.UIApplication(doc.Application)
# uiapp.PostCommand(args.CommandId)
import os


@EnneadTab.ERROR_HANDLE.try_catch_error_silently
def main():
    import imp
    module_name = "command-before-exec[ID_BUTTON_DELETE]"
    module_path = "{}\\{}.py".format(os.path.realpath(os.path.dirname(__file__)), module_name)
    module = imp.load_source(module_name, module_path)
    module.main()
    
############################
output = script.get_output()
output.close_others()


if __name__ == '__main__':
    main()