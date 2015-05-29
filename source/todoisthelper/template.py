'''
Created on May 7, 2015+

@author: TDARSEY
'''

from pytodoist import todoist
import templateparser


class ProjectTemplate(object):
    '''
    An abstract structure with predefined tasks for a todoist project.

    :ivar name: Name of the project to be created
    :ivar tasks: Ordered list of tasks to be mapped
    '''

    def __init__(self, tasks=[], attributes={}):
        self.tasks = tasks

        for argname, argvalue in attributes.iteritems():
            self.__setattr__(argname, argvalue)

    def addTask(self, content, indent, item_order=None):
        '''Add a task to the template.

        :param content:
        :type content: str
        :param item_order:
        :type item_order: int
        :param indent:
        :type indent: int
        '''

        new_task = templateparser.TemplateTask(content=content, indent=indent)

        if item_order is not None:
            self.tasks.insert(item_order, new_task)
        else:
            self.tasks.append(new_task)

    def createProject(self, user, parent_project=None):
        '''Create the templated project in todoist
        :param parent_project: Parent project's name
        :type parent_project: str
        '''
        indent = None
        order = None

        # TODO: Check to make sure we have all the requred parameters.

        # Find the correct placement under the parent project
        if parent_project is not None:
            indent = min(parent_project.indent + 1, 4)
            order = parent_project.item_order + 1

        # TODO: Check for existing project name

        # Get the root project
        new_project = user.add_project(
            name=self.name,
            color=None,
            indent=indent,
            order=order)

        # Add each task to our project with the proper indentation
        for task in self.tasks:
            new_task = new_project.add_task(content=task.content)
            new_task.indent = task.indent
            new_task.update()

    # format attributes on attribute access
    def formatAttributes(self):
        '''Loop through the templates attributes, conditionally
        replacing any occurences of bracketed placeholders with its
        corrisponding attribute.
        '''

        for key, value in self.__dict__.iteritems():
            if isinstance(value, str):
                try:
                    self.__setattr__(key, value.format(**self.__dict__))
                except KeyError as k:
                    # TODO: Make an actual warning
                    print "Key Error: no attribute \"{}\"" \
                        " not found in template parameters".format(k.message)

class TemplateFactory(object):
    '''Factory class for creating templates.
    '''

    @classmethod
    def loadFile(cls, filename, **kwargs):
        '''Load a template from a file.

        :param filename: The filename (including path) of the template.
        :type filename: str
        '''

        myfile = open(filename)
        template_string = myfile.read()
        myfile.close()

        return cls.load(template_string, **kwargs)

    @classmethod
    def load(cls, string, **kwargs):
        '''Load a template from a string.

        :param filename: The filename (including path) of the template.
        :type filename: str

        :return task:
        :rtype task: Task
        '''

        myparser = templateparser.Parser()
        return myparser.parse(string, **kwargs)
