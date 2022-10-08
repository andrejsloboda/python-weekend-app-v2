import asyncio
import json
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Union, List
import aiohttp
from slugify import slugify
from app.settings import settings
from app.database.models import Route
from app.database import database
from app.scraper import FlixbusSearchResponse, FlixbusCity, RegiojetSearchResponse


class Scraper(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self.base_url: str
        self.locations_url: str

    @abstractmethod
    def get_location_id(self, session: aiohttp.ClientSession, location: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_search_data(self, session: aiohttp.ClientSession, origin: str, destination: str,
                        departure_date: date) -> Union[List[Route], None]:
        pass


class RegiojetScraper(Scraper):

    def __init__(self) -> None:
        self.locations_url = settings.regiojet_location_url
        self.base_url = settings.regiojet_base_url

    async def get_location_id(self, session: aiohttp.ClientSession, location: str) -> Union[str, None]:
        async with session.get(self.locations_url) as location_response:
            location_response = await location_response.json()
            for country in location_response:
                for city in country['cities']:
                    if city['name'] == location:
                        return city['id']
                    else:
                        for alias in city['aliases']:
                            if alias == location:
                                return city['id']

    async def get_search_data(self, session: aiohttp.ClientSession, origin: str, destination: str,
                              departure_date: date) -> Union[List[Route], None]:

        if departure_date >= datetime.today().date():

            # origin_id = database.get_city_id(origin)
            # destination_id = database.get_city_id(destination)

            search_params = {
                'tariffs': 'REGULAR',
                'toLocationType': 'CITY',
                'toLocationId': await self.get_location_id(session, destination),
                'fromLocationType': 'CITY',
                'fromLocationId': await self.get_location_id(session, origin),
                'departureDate': departure_date.strftime('%Y-%m-%d')
            }

            async with session.get(self.base_url, params=search_params) as response_raw:
                response = await response_raw.json()
                response = RegiojetSearchResponse(**response)

            routes = []
            for route in response.routes:
                if route.priceFrom > 0:
                    route = Route(
                        origin=slugify(origin),
                        destination=slugify(destination),
                        departure=datetime.fromisoformat(route.departureTime),
                        arrival=datetime.fromisoformat(route.arrivalTime),
                        carrier="REGIOJET",
                        vehicle_type=route.vehicleTypes.pop(),
                        price=route.priceFrom,
                        currency="EUR",
                        source_id=route.departureStationId,
                        destination_id=route.arrivalStationId,
                        free_seats=route.freeSeatsCount)
                    routes.append(route)
            return routes


class FlixbusScraper(Scraper):

    def __init__(self) -> None:
        self.base_url = settings.flixbus_base_url
        self.location_url = settings.flixbus_location_url

    async def get_location_id(self, session: aiohttp.ClientSession, location: str) -> Union[str, None]:

        location_params = {
            'q': location,
            'lang': 'en',
            'country': 'en',
            'flixbus_cities_only': 'false'
        }

        async with session.get(self.location_url, params=location_params) as location_response:
            response = await location_response.json()
            return FlixbusCity(**response[0]).id

    async def get_search_data(self, session: aiohttp.ClientSession, origin: str, destination: str,
                              departure_date: date) -> Union[List[Route], None]:
        if departure_date >= datetime.today().date():
            format_date_out = "%d.%m.%Y"
            departure_date_in = departure_date
            departure_date_out = datetime.strftime(departure_date_in, format_date_out)

            origin_id = database.get_city_id(origin)
            destination_id = database.get_city_id(destination)

            products = {
                "adult": 1,
                "children_0_5": 0,
                "bike_slot": 0
            }

            search_params = {
                'from_city_id': await self.get_location_id(session, origin),
                'to_city_id': await self.get_location_id(session, destination),
                'departure_date': departure_date_out,
                'products': json.dumps(products),
                'currency': 'EUR',
                'locale': 'en',
                'search_by': 'cities',
                'include_after_midnight_rides': 0
            }

            async with session.get(url=self.base_url, params=search_params) as response:
                response = await response.json()
                search_response = FlixbusSearchResponse(**response)

                routes = []
                for result in search_response.trips[0].results:
                    r = search_response.trips[0].results[result]
                    route = Route(
                        origin=origin_id,
                        destination=destination_id,
                        departure=datetime.fromisoformat(r['departure']['date']),
                        arrival=datetime.fromisoformat(r['arrival']['date']),
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


async def get_all_tasks(session, base_routes, departure_date):
    scrapers = [FlixbusScraper(), RegiojetScraper()]
    tasks = []
    for scraper in scrapers:
        for routes in base_routes:
            for route in routes:
                task = asyncio.create_task(scraper.get_search_data(session, route.origin.capitalize(),
                                                                   route.destination.capitalize(), departure_date))
                tasks.append(task)
    result = await asyncio.gather(*tasks)
    return result


async def scrape_base_routes(base_routes, departure_date):
    async with aiohttp.ClientSession() as session:
        return await get_all_tasks(session, base_routes, departure_date)
