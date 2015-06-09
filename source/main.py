'''
Created on May 27, 2015

@author: TDARSEY
'''

from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label

from kivy.properties import ObjectProperty, ListProperty, StringProperty

# from kivy.uix.splitter import Splitter

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
            ProjectDetail:
                id: project_detail

<RootScreen>:
    StackLayout:
        RootActionBar:

        ScreenManager:
            MainScreen:
                id: main_screen
""")


class ProjectDetail(GridLayout):

    project = ObjectProperty()

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(ProjectDetail, self).__init__(**kwargs)
        self.bind(project=self.redraw)

    def redraw(self, *args):
        self.clear_widgets()

        if self.project:
            self.add_widget(Label(text="Name", halign='right'))
            self.add_widget(Label(text=self.project.name))

            for attr_key, attr_value in self.project.__dict__.iteritems():
                self.add_widget(Label(text=str(attr_key), halign='right'))
                self.add_widget(Label(text=str(attr_value)))

    def update(self, project):
        self.project = project
        self.redraw()


class ProjectsList(ListView):

    project_list = ListProperty([])

    def __init__(self, **kwargs):
        self.refreshData()
        super(ProjectsList, self).__init__(adapter=self.adapter, **kwargs)
        self.adapter.bind(on_selection_change=self._onSelectItem)

    def refreshData(self):

        self.project_list = ProjectFactory.getProjectsInPath(
            Settings.PROJECT_DIRECTORY)

        args_converter = lambda row_index, project: {'text': project.name,
                                                     'size_hint_y': None,
                                                     'height': 50}

        self.adapter = ListAdapter(data=self.project_list,
                                   args_converter=args_converter,
                                   cls=ListItemButton,
                                   selection_mode='single',
                                   allow_empty_selection=False)

    def _onSelectItem(self, adapter):
        '''Set the project detail to the selected project.'''
        project_index = adapter.selection[0].index
        project = self.project_list[project_index]

        self.parent.parent.parent.parent.ids.project_detail.update(project)

        # print
        # App.get_running_app().root.ids['main_screen'].ids['project_list'].ids['project_detail_splitter'].ids['project_detail'].update(project)


class RootScreen(BoxLayout):
    pass


class ProjectHelperApp(App):

    def build(self):
        return RootScreen()

if __name__ == "__main__":
    app = ProjectHelperApp().run()
