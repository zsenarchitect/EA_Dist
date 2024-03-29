"""Activates selection tool that picks a specific type of element.

Shift-Click:
Pick favorites from all available categories
"""
# pylint: disable=E0401,W0703,C0103
from collections import namedtuple

from pyrevit import revit, UI, DB
from pyrevit import forms
from pyrevit import script

__title__ = 'Preselection filter!!!!!!!!!!'



logger = script.get_logger()
my_config = script.get_config()


CategoryOption = namedtuple('CategoryOption', ['name', 'revit_cat'])


class PickByCategorySelectionFilter(UI.Selection.ISelectionFilter):
    """Selection filter implementation"""
    def __init__(self, category_opt):
        self.category_opt = category_opt

    def AllowElement(self, element):
        """Is element allowed to be selected?"""
        if element.Category \
                and self.category_opt.revit_cat.Id == element.Category.Id:
            return True
        else:
            return False

    def AllowReference(self, refer, point):  # pylint: disable=W0613
        """Not used for selection"""
        return False


def pick_by_category(category_opt):
    """Handle selection by category"""
    try:
        selection = revit.get_selection()
        msfilter = PickByCategorySelectionFilter(category_opt)
        selection_list = revit.pick_rectangle(pick_filter=msfilter)
        filtered_list = []
        for element in selection_list:
            filtered_list.append(element.Id)
        selection.set_to(filtered_list)
    except Exception as err:
        logger.debug(err)


# ask user to select a category to select by
if True:

    selected_category = DB.BuiltInCategory.OST_CurtainWallPanels

    if selected_category:
        selected_category_opt = \
            next(x for x in category_opts if x.name == selected_category)
        logger.debug(selected_category_opt)
        pick_by_category(selected_category_opt)
