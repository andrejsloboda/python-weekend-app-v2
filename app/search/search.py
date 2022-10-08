import asyncio
from datetime import date
from app.database import database as db
from app.search.graph import Graph, BaseGraph
from app.scraper import scraper
from app.search import bfs


def search(origin: str, destination: str, departure_date: date):
    distinct_routes = db.get_distinct_routes_from_db()
    if distinct_routes:
        base_graph = BaseGraph(distinct_routes)
        base_routes = bfs.find_base_routes(base_graph, origin, destination)
        scraped_data = asyncio.run(scraper.scrape_base_routes(base_routes, departure_date))

        scraped_data_result = []
        for data in scraped_data:
            scraped_data_result.extend(data)

        graph = Graph(scraped_data_result)
        # routes = bfs.find_routes(graph, db.get_city_id(origin), db.get_city_id(destination))
        # routes = bfs.find_routes(graph, origin, destination)
        db.add_routes_to_db(scraped_data[0])
        # return routes
    else:
        # Here put logic to scrape simpe routes in case
        # there are no data in database
        pass



