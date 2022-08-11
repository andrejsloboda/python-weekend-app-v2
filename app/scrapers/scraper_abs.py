from abc import ABC, abstractmethod


class Scraper(ABC):

    @abstractmethod
    def get_locations(self):
        pass

    @abstractmethod
    def scrape(self):
        pass