

import time

import USER

import TIME
import FOLDER
import USER
import DATA_FILE
import ENVIRONMENT
LOG_FILE_NAME = 'log_{}.json'.format(USER.USER_NAME)



from contextlib import contextmanager

@contextmanager
def log_usage(func,*args):
    t_start = time.time()
    res = func(*args)
    yield res
    t_end = time.time()
    duration = TIME.get_readable_time(t_end - t_start)
    with open(FOLDER.get_EA_dump_folder_file(LOG_FILE_NAME), "a") as f:
        f.writelines('\nRun at {}'.format(TIME.get_formatted_time(t_start)))
        f.writelines('\nDuration: {}'.format(duration))
        f.writelines('\nFunction name: {}'.format(func.__name__))
        f.writelines('\nArguments: {}'.format(args))
        f.writelines('\nResult: {}'.format(res))


# with log_usage(LOG_FILE_NAME) as f:
#     f.writelines('\nYang is writing!')


"""log and log is break down becasue rhino need a wrapper to direct run script directly
whereas revit need to look at local func run"""


@FOLDER.backup_data(LOG_FILE_NAME , "log")
def log(script_path, func_name_as_record):

    # for rhino many script have multiple title as mutiple aliasa , so in that case, only use the longest as recorder
    if isinstance(func_name_as_record, list):
        func_name_as_record = max(func_name_as_record, key=len)

        
    def decorator(func):
        def wrapper(*args, **kwargs):
            with DATA_FILE.update_data(LOG_FILE_NAME) as data:
                t_start = time.time()
                out = func(*args, **kwargs)
                t_end = time.time()

                data[TIME.get_formatted_current_time()] = {
                    "application":ENVIRONMENT.get_app_name(), 
                    "function_name": func_name_as_record.replace("\n", " "),
                    "arguments": args,
                    "result": str(out),
                    "script_path": script_path,
                    "duration": TIME.get_readable_time(t_end - t_start)
                    }

            return out
        return wrapper
    return decorator



def read_log(user_name = USER.USER_NAME):
    data = DATA_FILE.get_data(LOG_FILE_NAME)
    print ("Printing user log from <{}>".format(user_name))
    import pprint
    pprint.pprint(data, indent= 4)




def unit_test():
    pass



    
    
###########################################################
if __name__ == "__main__":
    unit_test()