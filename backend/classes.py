# This draft is created to brainstorm about the potential 
# architecture of the final solution.

from abc import ABC, abstractmethod

# Scraper rack: Collect the date from the web, 
# clean, vectorize and store it.
class Scraper(ABC):
    @abstractmethod
    def method(self):
        pass

class Ingestion(Scraper):
    def __init__(self, source):
        self.source = source

    def method(self):
        return self.source

class Clean(Scraper):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def method(self):
        return self.source
    
class Vectorize(Scraper):
    def __init__(self):
        super().__init__()

class Store(Scraper):
    def __init__(self) -> None:
        super().__init__()