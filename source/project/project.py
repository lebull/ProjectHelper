'''
Created on May 11, 2015

@author: TDARSEY
'''

import os.path
import json
import fnmatch

from settings import Settings

class Project(object):
    '''classdocs
    '''

    def __init__(self, **kwargs):
        '''Constructor
        '''
        self.other_attributes = {}

        self.name = ""

        self.inventory_code = ""
        self.program_name = ""
        self.functional_counterpart = ""
        self.change_description = ""
        self.production_date = None

        self.transports = []
        self.questions = []

        self.todoist_project = None
        self.status = "Active"

        # If a kwarg is not a class variable, set it in other_attributes.
        for key, value in kwargs.iteritems():
            if key in self.__dict__.keys():
                self.__dict__[key] = value
            else:
                self.other_attributes[key] = value

    def getFilepath(self, status=None):
        if status is None:
            status = self.status

        target_dir = os.path.join(Settings.PROJECT_DIRECTORY,
                                  self.status)

        filepath = os.path.join(target_dir,
                                self.name + Settings.PROJECT_EXTENSION
                                )

        filepath = os.path.normpath(filepath)

        return filepath

    def save(self, status=None):
        '''Save a project.  The subdirectory that the project will be saved in
        depends on the status.
        '''
        if(status is None):
            status = self.status
        else:
            self.status = status

        filepath = self.getFilepath(status)

        # The target directory.  We need to make sure this exists before saving
        # the file.

        target_dir = os.path.dirname(filepath)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Ex. PROJECT_DIRECTORY/Active/myPrjoect.PROJECT_EXTENSION

        fp = open(filepath, 'w')
        json.dump(self.__dict__, fp, indent=4)
        fp.close()

        return filepath

    def move(self, to_status, from_status=None):
        # Try to delete the existing project.
        try:
            from_filepath = self.getFilepath(from_status)
            os.remove(from_filepath)
        except:
            # Save the new project
            print "Throw a real error! " \
                "But there was a problem moving the project"
        else:
            self.save(status=to_status)

    def __str__(self):
        return json.dumps(self.__dict__,
                          default=lambda o: o.__dict__,
                          indent=4)
    def getRST(self):
        return_string = ""
        for key, value in self.__dict__.iteritems():
            return_string += "\n -{} {}".format(key, value) 
        return return_string

class ProjectFactory(object):
    '''classdocs
    '''

    @staticmethod
    def loadProject(filepath):
        '''
        '''

        myfile = open(filepath, 'r')
        new_project_dict = json.load(myfile)
        myfile.close()

        new_project = Project()
        new_project.__dict__ = new_project_dict
        return new_project

    @staticmethod
    def listProjectsInPath(path):
        '''
        Based on SE answer provided by Nadia Alramli
        http://stackoverflow.com/questions/1724693/find-a-file-in-python
        '''
        pattern = "*" + Settings.PROJECT_EXTENSION

        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    @classmethod
    def getProjectsInPath(cls, path):
        projects = []
        paths = cls.listProjectsInPath(path)
        for filepath in paths:
            projects.append(cls.loadProject(filepath))
        return projects

    @staticmethod
    def findProject(attributes={}):
        '''
        '''

# class ProjectEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Project):
#             return obj.__dict__
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)

# TODO: JsonEncoder, JsonDecoder

if __name__ == "__main__":

    for project in ProjectFactory.getProjectsInPath(Settings.PROJECT_DIRECTORY):
        print project.__getattr__("name")

#     print Settings.listSettings()
#     myproject = Project(name="Test Project",
#                         program_name="Test",
#                         inventory_code="10150",
#                         color="green")
# 
#     myproject.save("Active")
#     myproject.move(to_status="Hold")


#     myproject = ProjectFactory.loadProject("C:\\Users\\TDARSEY\\Desktop\\Personal Projects\\TodoistHelper\\Test\\Hold\\Test Project.pjc")
#     print myproject