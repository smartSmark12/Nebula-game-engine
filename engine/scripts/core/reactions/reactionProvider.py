from scripts.core.reactions.reactionListener import ReactionListener

class ReactionProvider:
    def __init__(self):
        self.listeners:list[ReactionListener] = []

    def add_listener(self, listener:ReactionListener):
        self.listeners.append(listener)

        return len(self.listeners) - 1 # a "way" to get the last added index
    
    def remove_listener(self, listenerIndex:int):
        if listenerIndex > 0 and listenerIndex < len(self.listeners) - 1:
            return self.listeners.pop(listenerIndex)
        
        else:
            print(f"{__name__}: cannot find a ReactionListener at index {listenerIndex}")

    def trigger(self):
        for listener in self.listeners:
            listener.trigger()