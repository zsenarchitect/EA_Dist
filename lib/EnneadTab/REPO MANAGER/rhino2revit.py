

def main():
    try:
        import os
        # print (__file__)
        parent_folder = os.path.dirname(os.path.dirname(__file__))
        # print (parent_folder)
        
        
        import traceback
        import sys
        sys.path.append(parent_folder)
        # print (sys.path)
        
        import VERSION_CONTROL, NOTIFICATION
        VERSION_CONTROL._publish_ENNEAD_module_from_rhino()
        note = "Core Module:\nRHINO------->REVIT"
        NOTIFICATION.messenger(main_text=note)
        print (note)
    except:
        pass
        print (traceback.format_exc())
        

    


if __name__ == "__main__":
    main()