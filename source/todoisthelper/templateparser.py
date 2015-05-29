'''
Created on May 8, 2015

@author: TDARSEY
'''

import logging
from collections import namedtuple

import template



TemplateTask = namedtuple('TemplateTask', ['content', 'indent'])


class Parser(object):
    '''
    classdocs
    '''

    # TODO: set attributes from a parameter.
    def parse(self, string, **kwargs):
        '''
        :return ProjectTemplate
        '''
        self.attributes = {"name": "(No name)",
                           "tabsize": "4"}
        self.attributes.update(**kwargs)

        self.tasklist = []

        for line in string.split("\n"):
            self._processLine(line)

        return template.ProjectTemplate(tasks=self.tasklist,
                                        attributes=self.attributes)

    def _processLine(self, line):
        '''Process one line of a template file

        :param line: a line of the template file
        :type line: string
        '''

        stripped_line = line.lstrip()

        # Ignore if the first characters of a string are '//'
        if(stripped_line == "" or stripped_line.startswith(TOKEN.COMMENT)):
            return

        # Process parameter
        if(stripped_line.startswith(TOKEN.ATTRIBUTE)):
            self._processAttribute(line)
            return

        # Process attribute
        if(stripped_line.startswith(TOKEN.COMMENT)):
            self._processAttribute(line)
            return

        # Process a single task
        self.tasklist.append(self._processTask(line))

    def _processTask(self, line):
        '''Process an attribute in the template file.

        :param line: a line of the template file
        :type line: string
        '''
        # Replace any tabs with spaces

        stripped_line = line.lstrip()

        tabsize = int(self.attributes['tabsize'])

        line = line.replace('\t', ' ' * tabsize)
        indent_size = (len(line) - len(stripped_line)) // tabsize
        indent_size += 1  # Add one to have 1 the lowest indent
        indent_size = min(max(indent_size, 1), 4)
        task_name = stripped_line

        return TemplateTask(content=task_name,
                            indent=indent_size)

    def _processAttribute(self, line):
        '''Process an attribute in the template file.

        :param line: a line of the template file
        :type line: string
        '''
        line = line[1:]  # strip off '@'
        attribute, value = line.split(" ", 1)

        self.attributes[attribute] = value

        # TODO:If an attribute exists, set it.
        # Otherwise, throw a warning.


class TOKEN:
    COMMENT = "//"
    ATTRIBUTE = "@"

if __name__ == "__main__":

    stuff = \
"""
@tabsize 4
@params item, description, changenumber
@name {item} {description} {changenumber}

Task
    Subtask
        SubSubTask
NextTask
"""
    myparser = Parser()
    template = myparser.parse(stuff)
    print template.name

