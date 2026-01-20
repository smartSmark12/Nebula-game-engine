class ReactionListener:
    def __init__(self, triggerFunction):
        self.triggerFunction = triggerFunction

    def trigger(self):
        try:
            self.triggerFunction()
        
        except Exception as e:
            print(f"{__name__}: reaction function failed to trigger! :3 ({e})")