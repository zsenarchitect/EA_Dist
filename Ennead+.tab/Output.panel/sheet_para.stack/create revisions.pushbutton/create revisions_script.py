#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Pick multiple open documents, and create new revision with the same \
revision name and revision date. Us e this to improve your consistency."
__title__ = "Create Revisions In Many Documents"

from pyrevit import forms #
from pyrevit import script #
# from pyrevit import revit #
import EA_UTILITY
import EnneadTab
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
doc = __revit__.ActiveUIDocument.Document

def create_revision(doc, description, revision_date):
    revision = DB.Revision.Create(doc)
    revision.Description = description
    revision.RevisionDate = revision_date

def main():
    docs = EA_UTILITY.select_top_level_docs()
    if docs is None:
        return

    description = forms.ask_for_string("Revision Name")
    revision_date = forms.ask_for_string("Revision Date")
    for doc in docs:
        t = DB.Transaction(doc, "create revisions")
        t.Start()
        create_revision(doc, description, revision_date)
        t.Commit()

    print "[{}] revision created for the document".format(description)
    for doc in docs:
        print "\n\t\t" + doc.Title



################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":

    main()
