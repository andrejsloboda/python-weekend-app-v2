import asyncio
from datetime import date
from app.database import database as db
from app.search.graph import Graph, BaseGraph
from app.scraper import scraper
from app.search import bfs


def search(origin: str, destination: str, departure_date: date):
    data = db.get_data_from_db(departure_date)
    if data:
        graph = Graph(data)
        routes = bfs.find_routes(graph, origin, destination)
        return routes
    else:
        distinct_routes = db.get_distinct_routes_from_db()
        base_graph = BaseGraph(distinct_routes)
        base_routes = bfs.find_base_routes(base_graph, origin, destination)
        scraped_data = asyncio.run(scraper.scrape_base_routes(base_routes, departure_date))

        for data in scraped_data:
            if not db.is_in_db(origin, destination, departure_date):
                db.add_routes_to_db(data)

        data_from_db = db.get_data_from_db(departure_date)
        graph = Graph(data_from_db)
        routes = bfs.find_routes(graph, origin, destination)
        return routes




