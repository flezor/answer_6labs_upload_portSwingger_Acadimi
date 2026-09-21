from abc import ABC, abstractmethod
class Strategy(ABC):
    name = "base"
    @abstractmethod
    def run(self, session, csrf, config, logger):
        raise NotImplementedError
