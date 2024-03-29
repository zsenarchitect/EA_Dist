#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import imp

import sys
import FOLDER
import ENVIRONMENT
import ERROR_HANDLE
import USER
import NOTIFICATION

#@ERROR_HANDLE.try_catch_error
def run_func_in_module(module_path, func_name, *args):
    """Run a specified function in a specified python file.

    Args:
        module_path (str): Path to the python file.
        func_name (str): Name of function to run.
        *args: Positional arguments to pass to the function.
    """
        
    module_name = FOLDER.get_file_name_from_path(module_path).replace(".py", "")
    ref_module = imp.load_source(module_name, module_path)
    func = getattr(ref_module, func_name, None) or getattr(ref_module, module_name, None)
    if func is None:
        NOTIFICATION.messenger(main_text="Oooops, cannot find the the source code.\nSen Zhang is no longer working for EnneadTab unluckly.")
    else:
        func(*args)


def run_Rhino_button(folder, file_name, func_name, *args):
    """Run a specified function in a specified file, for use with Rhino buttons.

    Args:
        folder (str): The folder name for the button script, in EnneadTab sources codes folder.
        file_name (str): The file name for the button script, without the .py extension.
        func_name (str): The function name to run in the button script. To run entire script, use "file_name".
        *args: Positional arguments to pass to the function.
    """


    root = ENVIRONMENT.get_EnneadTab_For_Rhino_root()
    module_path = "{}\Source Codes\{}\{}.py".format(root, folder, file_name)
    
    # add the folder of the module to the system path for referencing additional modules
    module_folder = os.path.dirname(module_path)
    if module_folder not in sys.path:
        sys.path.append(module_folder)

    run_func_in_module(module_path, func_name, *args)

@ERROR_HANDLE.try_catch_error_silently
def run_revit_script(script_subfolder_or_fullpath, func_name,*args,**kwargs):
    """_summary_

    Args:
        script_subfolder (str): such as 
            "XX.tab\\YY.panel\\ZZ.pulldown" or 
            "XX.tab\\YY.panel" or
            end with .py
        func_name (str): name of the func to run
    """
    
    folder_or_fullpath = "{}\\ENNEAD.extension\\{}".format(ENVIRONMENT.WORKING_FOLDER_FOR_REVIT, script_subfolder_or_fullpath)

    if script_subfolder_or_fullpath.endswith(".py"):
        full_file_path = folder_or_fullpath
    else:
        full_file_path = "{}\\{}.pushbutton\\{}_script.py".format(folder_or_fullpath, func_name, func_name)
    
    
    # if not USER.is_enneadtab_developer(): # wait until colin fix the bug
    if not USER.is_SZ():
        # NOTIFICATION.messenger(main_text = full_file_path)
        # print full_file_path
        full_file_path =  FOLDER.remap_filepath_to_folder(full_file_path)
        # print full_file_path
        # NOTIFICATION.duck_pop(main_text = full_file_path)
        
        
    if not os.path.exists(full_file_path):
        NOTIFICATION.messenger(main_text = "File not found: {}".format(full_file_path))
        return
    
    ref_module = imp.load_source("{}_script".format(func_name), full_file_path)

    getattr(ref_module, func_name)(*args, **kwargs)
    