class Usecase:
    def __init__(self, file, **settings):
        self.file = file
        self.settings = {"actor": None}
        for key, value in settings.items():
            self.settings[key] = value

    def execute(self):
        self.file.remove(self.settings["actor"])
