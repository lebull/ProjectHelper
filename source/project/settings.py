class Settings(object):
    PROJECT_DIRECTORY = "C:\\Users\\TDARSEY\\Desktop\\Personal Projects\\" \
                         "TodoistHelper\\Test"

    PROJECT_EXTENSION = ".pjc"

    @staticmethod
    def listSettings():
        return [attr for attr in vars(Settings)
                if not callable(getattr(Settings, attr))
                and not attr.startswith("__")]
