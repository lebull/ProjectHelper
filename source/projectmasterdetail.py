'''
Created on May 27, 2015

@author: TDARSEY
'''

from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.widget import Widget
from kivy.uix.rst import RstDocument
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.screenmanager import Screen

from kivy.properties import ObjectProperty, ListProperty, StringProperty

# from kivy.uix.splitter import Splitter

from project.project import Project, ProjectFactory
from project.settings import Settings


Builder.load_string("""

<ProjectMasterDetail@Screen>
    on_pre_enter: self.refreshAllData()


    BoxLayout:
        BoxLayout:
            id: project_list_wrapper
            orientation: 'vertical'
            size_hint_x: None
            width: sp(250)

            ProjectList:
                id:project_list_view

            BoxLayout:
                size_hint_y: None
                height: sp(40)

                Button:
                    text: "+"

                Button:
                    text: "Refresh"
                    on_press: root.ids.project_list_view.refreshList()

        BoxLayout:
            orientation: 'vertical'
            ProjectDetailRST:
                id: project_detail
            BoxLayout:
                size_hint_y: None
                height: sp(40)
                Button:
                    text: "Add/Edit Value"
""")


class ProjectDetailRST(RstDocument):

    project = ObjectProperty()

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(ProjectDetailRST, self).__init__(**kwargs)
        self.bind(project=self.redraw)

    def redraw(self, *args):
        self.text = self.project.getRST()

    def update(self, project):
        self.project = project
        self.redraw()


class ProjectList(ListView):

    projects = ListProperty([])

    def __init__(self, **kwargs):
        self.refreshList()
        super(ProjectList, self).__init__(adapter=self.adapter, **kwargs)
        # self.bind(project_list=self.refreshList)

    def refreshList(self):

        if self.parent:
            App.get_running_app().root.refreshProjectList()
            self.projects = self.parent.parent.parent.project_list
        else:
            self.projects = []

        args_converter = lambda row_index, project: {'text': project.name,
                                                     'size_hint_y': None,
                                                     'height': 50}

        self.adapter = ListAdapter(data=self.projects,
                                   args_converter=args_converter,
                                   cls=ListItemButton,
                                   selection_mode='single',
                                   allow_empty_selection=False)

        self.adapter.bind(on_selection_change=self._onSelectItem)

    def _onSelectItem(self, adapter):
        '''Set the project detail to the selected project.'''
        project_index = adapter.selection[0].index
        project = self.projects[project_index]

        self.parent.parent.parent.ids.project_detail.update(
            project)


class ProjectMasterDetail(Screen):

    project_list = ListProperty()

    def refreshProjectList(self):
        self.project_list = ProjectFactory.getProjectsInPath(
            Settings.PROJECT_DIRECTORY)

    def refreshAllData(self):
        self.refreshProjectList()
        self.ids.project_list_view.refreshList()
        print "Load"

    def build(self, **kwargs):
        self.refreshProjectList()
        return super(ProjectMasterDetail, self).build(**kwargs)

# Factory.register(ProjectMasterDetail)

if __name__ == "__main__":

    class ProjectHelperApp(App):

        def on_start(self):
            self.root.refreshProjectList()

        def build(self):
            return ProjectMasterDetail()

    app = ProjectHelperApp().run()
