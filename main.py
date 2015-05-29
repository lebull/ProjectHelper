'''
Created on May 11, 2015

TODO:

Save a file template
    Save properties in a .tdh file
Archive projects
GUI

@author: TDARSEY
'''
from pytodoist import todoist

from todoisthelper.template import TemplateFactory


TEMPLATE_FILE = "C:\\Users\\TDARSEY\\Desktop\\Personal Projects\\" \
                "TodoistHelper\\templates\\template.txt"

parent_project_NAME = "Test"

API_KEY = "c37ac7d6aaf139372705b239f73855c29728e088"

if __name__ == '__main__':

    params = {}
    params['icode'] = raw_input("Inventory Code: ")
    params['program_name'] = raw_input("Program Name: ")
    params['crnum'] = raw_input("Change Request Number: ")
    params['desc'] = raw_input("Change Description: ")

    my_template = TemplateFactory.loadFile(TEMPLATE_FILE, **params)

    my_template.formatAttributes()

    user = todoist.login_with_api_token(API_KEY)
    parent_project = user.get_project(parent_project_NAME)
    my_template.createProject(user = user,
                              parent_project = parent_project)

    print "Project Created"
