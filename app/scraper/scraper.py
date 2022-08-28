import json
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Union, List

import requests
from slugify import slugify

# from ..settings import settings
from .schemas import FlixbusSearchResponse, FlixbusCity, Route, RegiojetSearchResponse


class Scraper(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self.base_url: str
        self.locations_url: str

    @abstractmethod
    def get_location_id(self, location: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_search_data(self, origin: str, destination: str, departure_date: date) -> Union[List[Route], None]:
        pass


class RegiojetScraper(Scraper):

    def __init__(self) -> None:
        # self.locations_url = settings.regiojet_locations_url
        # self.base_url = settings.regiojet_base_url
        self.locations_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
        self.base_url = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple'

    def get_location_id(self, location: str) -> Union[str, None]:
        try:
            locations_response = requests.get(self.locations_url).json()

        except requests.RequestException as e:
            print(e)
            return None

        finally:
            for country in locations_response:
                for city in country['cities']:
                    if city['name'] == location:
                        return city['id']
                    else:
                        for alias in city['aliases']:
                            if alias == location:
                                return city['id']

    def get_search_data(self, origin: str, destination: str, departure_date: date) -> Union[List[Route], None]:
        if departure_date >= datetime.today().date():

            search_params = {
                'tariffs': 'REGULAR',
                'toLocationType': 'CITY',
                'toLocationId': self.get_location_id(destination),
                'fromLocationType': 'CITY',
                'fromLocationId': self.get_location_id(origin),
                'departureDate': departure_date
            }

            try:
                response = RegiojetSearchResponse(**requests.get(self.base_url, params=search_params).json())

            except requests.RequestException as e:
                print(e)
                return []

            finally:
                routes = []

                for route in response.routes:
                    if route.priceFrom > 0:
                        route = Route(
                            origin=slugify(origin),
                            destination=slugify(destination),
                            departure=route.departureTime,
                            arrival=route.arrivalTime,
                            carrier="REGIOJET",
                            vehicle_type=route.vehicleTypes.pop(),
                            price=route.priceFrom,
                            currency="EUR",
                            source_id=route.departureStationId,
                            destination_id=route.arrivalStationId,
                            free_seats=route.freeSeatsCount)
                        routes.append(route)
                return routes
        else:
            return None


class FlixbusScraper(Scraper):

    def __init__(self) -> None:
        self.base_url = 'https://global.api.flixbus.com/search/service/v4/search'
        self.location_url = 'https://global.api.flixbus.com/search/autocomplete/cities'

    def get_location_id(self, location: str) -> Union[str, None]:

        location_params = {
            'q': location,
            'lang': 'en',
            'country': 'en',
            'flixbus_cities_only': 'false'
        }

        try:
            location_response_raw = requests.get(url=self.location_url, params=location_params)

        except requests.exceptions.RequestException as e:
            print(e)
            return None

        finally:
            return FlixbusCity(**location_response_raw.json()[0]).id

    def get_search_data(self, origin: str, destination: str, departure_date: date) -> Union[List[Route], None]:
        if departure_date >= datetime.today().date():
            format_date_out = "%d.%m.%Y"
            departure_date_in = departure_date
            departure_date_out = datetime.strftime(departure_date_in, format_date_out)

            products = {
                "adult": 1,
                "children_0_5": 0,
                "bike_slot": 0
            }

            search_params = {
                'from_city_id': self.get_location_id(origin),
                'to_city_id': self.get_location_id(destination),
                'departure_date': departure_date_out,
                'products': json.dumps(products),
                'currency': 'EUR',
                'locale': 'en',
                'search_by': 'cities',
                'include_after_midnight_rides': 0
            }

            try:
                search_response_raw = requests.get(url=self.base_url, params=search_params)

            except requests.RequestException as e:
                print(e)
                return []

            finally:
                search_response = FlixbusSearchResponse(**search_response_raw.json())
                print(type(search_response.trips[0].departure_city_id), type(search_response.trips[0].departure_city_id))
                routes = []
                for result in search_response.trips[0].results:
                    r = search_response.trips[0].results[result]
                    route = Route(
                        origin=slugify(origin),
                        destination=slugify(destination),
                        departure=r['departure']['date'],
                        arrival=r['arrival']['date'],
                        carrier='FLIXBUS',
                        price=r['price']['total'],
                        vehicle_type=search_response.trips[0].means_of_transport[0],
                        currency='EUR',
                        source_id=search_response.trips[0].departure_city_id,
                        destination_id=search_response.trips[0].departure_city_id,
                        free_seats=0)
                    routes.append(route)
                return routes
        else:
            return None


def scrape(origin: str, destination: str, departure_date: date) -> Union[List[Route], None]:
    scrapers = [FlixbusScraper(), RegiojetScraper()]
    scraped_data = []
    for scraper in scrapers:
        scraped_data.extend(scraper.get_search_data(origin, destination, departure_date))
    return scraped_data

