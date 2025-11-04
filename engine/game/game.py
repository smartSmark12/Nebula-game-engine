from scripts.core.mainEngine import MainEngine

class MainGame:
    def __init__(self, appInstance):
        self.app = appInstance

    def on_start(self):
        print("hello world from MainGame! on start")

    def on_frame(self):
        pass