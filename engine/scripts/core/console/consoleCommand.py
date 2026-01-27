class ConsoleCommand:
    def __init__(self, callName:str, description:str=""):
        self.name = callName
        self.desc = description

    def execute(self, app, args:list[str]): # override this function
        pass