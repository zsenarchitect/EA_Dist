#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

try:
    import FOLDER
    import NOTIFICATION
    import SPEAK
    import ENVIRONMENT
    
except:
    from EnneadTab import FOLDER
    from EnneadTab import NOTIFICATION
    from EnneadTab import SPEAK
    from EnneadTab import ENVIRONMENT


def random_joke():
    import random
    joke_file = "{}\\FUN\\_dad_jokes.txt".format(ENVIRONMENT.CORE_MODULE_FOLDER_FOR_PUBLISHED_RHINO)
    with open(joke_file, "r") as f:
        lines = f.readlines()


    random.shuffle(lines)
    return lines[0].replace("\n", "")

def random_loading_message():
    """get some fun message for loading screen

    Returns:
        str: a random line of funny message
    """

    with open('{}\_loading_screen_message.txt'.format(FOLDER.get_folder_path_from_path(__file__)), "r") as f:
        lines = f.readlines()
    random.shuffle(lines)
    return lines[0].replace("\n", "")


def prank_popup(forced=False):
    
    if not forced and random.random() > 0.0001:
        return
    
    icon = '{}\prank\pornhub.png'.format(FOLDER.get_folder_path_from_path(__file__))
   
    NOTIFICATION.toast(sub_text="Please login again at www.pornhub.com",
                        main_text="4 videos failed to download.",
                        app_name="Chrome",
                        icon=icon,
                        force_toast=True)
    
    
def give_me_a_joke(talk = False, max_len = None):


    joke =  random_joke()
    if not max_len:
        import textwrap as TW
        wrapper = TW.TextWrapper(width = 70)
        temp = ""
        for line in wrapper.wrap(joke):
            temp += line + "\n"
        joke = temp


    if talk:
        SPEAK.speak(joke.replace("\n", " "))
    return joke.replace("\n", " ")


def validating_jokes():
    with open("_dad_jokes.txt", "r") as f:
    #import io
    #with io.open("dad_jokes.txt", encoding = "utf8") as f:
        lines = f.readlines()


    OUT = []
    for line in lines:
        #print "\n#######################"
        #print line
        if r"â€™" in line:
            print (line)
            print ("find a bad string" + "*" * 50)
            line = line.replace(r"â€™", r"\'")
        if r"â??" in line:
            print (line)
            print ("find a bad string" + "*" * 50)
            line = line.replace(r"â??", r"\"")
        if r".â" in line:
            print (line)
            print ("find a bad string" + "*" * 50)
            line = line.replace(r".â", r"\"")
        if line.endswith("?"):
            print ("find a questiong ending:" + "*" * 100)
            print (line)
        OUT.append(line)

    with open("dad_jokes.txt", "w") as f:
        f.writelines(OUT)





if __name__ == "__main__":
    # prank_popup(forced=True)
    print (random_loading_message())