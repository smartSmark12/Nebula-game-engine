from scripts.core.reactions.reactionProvider import ReactionProvider
from scripts.core.reactions.reactionListener import ReactionListener

class ReactionService:
    def __init__(self, appInstance):
        self.app = appInstance

        self.providers:dict[str,ReactionProvider] = {}

    def add_provider(self, providerName:str, provider:ReactionProvider):
        self.providers[providerName] = provider

    def remove_provider(self, providerName:str):
        if providerName in self.providers:
            return self.providers.pop(providerName)
        else:
            print(f"{__name__}: no ReactionProvider with the name {providerName} found; did not remove")

    def get_provider(self, providerName:str):
        if providerName in self.providers:
            return self.providers[providerName]
        else:
            print(f"{__name__}: no ReactionProvider with the name {providerName} found")
            return None

    def trigger_provider(self, providerName:str):
        if providerName in self.providers:
            self.providers[providerName].trigger()
        else:
            print(f"{__name__}: no ReactionProvider with the name {providerName} found; did not trigger")