'''
Created on May 27, 2015

@author: TDARSEY
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter

from kivy.uix.splitter import Splitter

from project.project import Project, ProjectFactory
from project.settings import Settings


Builder.load_string("""

<RootActionBar@ActionBar>:
    pos_hint: {'top':1}
    ActionView:
        use_separator: True
        ActionPrevious:
            title: 'Back'
        ActionOverflow:
        ActionButton:
            text: 'New Project'
        ActionButton:
            text: 'Settings'

<MainScreen@Screen>
    BoxLayout:
        id: project_list

        TabbedPanel:
            do_default_tab: False
            tab_width: sp(80)

            TabbedPanelItem:
                text: 'Active'
                ProjectsList:

            TabbedPanelItem:
                text: 'Hold'
                ProjectsList:

            TabbedPanelItem:
                text: 'Complete'
                RstDocument:
                    text:
                        '\\n'.join(("Hello world", "-----------",
                        "You are in the third tab."))

        Splitter:
            BoxLayout:
                id: project_detail
                Button:
                    text: 'Project Detail'

<RootScreen>:
    StackLayout:
        RootActionBar:

        ScreenManager:
            MainScreen:
                id: main_screen


""")

projects = ProjectFactory.getProjectsInPath(Settings.PROJECT_DIRECTORY)


class ProjectsList(ListView):
    def __init__(self, **kwargs):
            self.refreshData()
            #super(ProjectsList, self).__init__(adapter=self.adapter, **kwargs)
            self.adapter.bind(on_selected_item = self._onSelectItem)

    def refreshData(self):

        args_converter = lambda row_index, project: {'text': project.name,
                                                     'size_hint_y': None,
                                                     'height': 50}

        self.adapter = ListAdapter(data=projects,
                                   args_converter=args_converter,
                                   cls=ListItemButton,
                                   selection_mode='single',
                                   allow_empty_selection=False)

    def _onSelectItem(self, **kwargs):
        print self.adapter

    def onSelectProject(self, project):
        '''Set the project detail to the selected project.'''


class RootScreen(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return RootScreen()

if __name__ == "__main__":
    app = MyApp().run()
