
import os
import sys
root_folder = os.path.abspath((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root_folder)
import ENVIRONMENT_CONSTANTS
if ENVIRONMENT_CONSTANTS.is_Rhino_environment():
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

def set_doc_to_rhinodoc():
    sc.doc = Rhino.RhinoDoc.ActiveDoc

def set_doc_to_ghdoc(ghdoc):
    sc.doc = ghdoc


class AccessRhinoDoc():
    """Simplifies switching backa dn forth between Rhino and Grasshopper documents. 
    by setting to RhinoDoc.ActiveDoc and ghdoc before and after the context.
    Automatically rolls back if exception is raised.

    >>> with AccessRhinoDoc():
    >>>     wall.DoSomething()

    """
    def __init__(self, ghdoc):
        self.ghdoc = ghdoc

    def __enter__(self):
        set_doc_to_rhinodoc()
        return self

    def __exit__(self, exception, exception_value, traceback):
        set_doc_to_ghdoc(self.ghdoc)