"""Module for searching for possible flights combinations in data.
"""
import json
from datetime import datetime

# internal
from constants import *


def search(dataset, orig, dest, bags) -> str:
    """Perform a search of possible flight combinations for selected route, based on other search parameters.

    Note: One possible optimization
    This same algorithm could be implemented using tree structure with arbitrary number of children, where every path
    from every leaf to root would be one possible route, therefore possible routes would not overlay themselves. This
    would slightly improve performance, but more important it would save a lot of memory. Code would also be nicer.
    Node's key would be an index into dataset as well. Python has no such built-in library. Luckily, because Python is
    dynamic, it is easy to implement, but for purpose of this project it would be overkill.

    :param dataset: Input data. Note: data should already be well-formatted. For more info check module `csv_handler`.
    :type dataset: list of lists of str
    :param orig: Airport code of requested origin.
    :type orig: str
    :param dest: Airport code of requested destination.
    :type dest: str
    :param bags: Number of requested bags.
    :type bags: int
    :return: Json formatted output of search.
    """

    # These variables save indexes of flights into dataset as list of lists of indexes (paths from orig to dest)
    # instead of whole records of dataset flights, to save memory, because number of items in `potential_routes` might
    # potentially grow large, larger than number of items in dataset, if large dataset is provided
    potential_routes = []
    found_routes = []

    # Initial search for flights starting in origin
    for flight_index, flight in enumerate(dataset):
        if flight[ORIGIN] == orig and int(flight[BAGS_ALLOWED]) >= bags:
            potential_routes.append([flight_index])

    # In this loop two important things happen. First, in first nested loop, is checked if any potential routes are
    # indeed already finishing in destination. If so, they are moved into found flights. Secondly, in second nested
    # loop, for every left potential flight is dataset iterated, trying to find and concatenate next flight with it.
    while potential_routes:
        for potential_route in list(potential_routes):
            if dataset[potential_route[-1]][DESTINATION] == dest:
                found_routes.append(potential_route)
                potential_routes.remove(potential_route)

        for potential_route in list(potential_routes):
            for flight_index, flight in enumerate(dataset):
                if flight[ORIGIN] == dataset[potential_route[-1]][DESTINATION]:
                    continue_flag = False
                    for index in potential_route:
                        if dataset[index][ORIGIN] == flight[DESTINATION]:  # repeated airport
                            continue_flag = True
                            break
                    if continue_flag:
                        continue

                    arrival = datetime.strptime(dataset[potential_route[-1]][ARRIVAL], '%Y-%m-%dT%H:%M:%S')
                    departure = datetime.strptime(flight[DEPARTURE], '%Y-%m-%dT%H:%M:%S')
                    delta_h = (departure - arrival).total_seconds() / 3600
                    if delta_h > 6.0 or delta_h < 1.0:
                        continue

                    if int(flight[BAGS_ALLOWED]) < bags:
                        continue

                    new_potential_route = potential_route.copy()
                    new_potential_route.append(flight_index)
                    potential_routes.append(new_potential_route)

            potential_routes.remove(potential_route)

    return _format_json(dataset, found_routes, bags, sort_by='total_price')


def _format_json(dataset, found_routes, bags_count, sort_by=None) -> str:
    """Formats found routes in form of indexes into json string.

    :param dataset: Input data. Note: data should already be well-formatted. For more info check module `csv_handler`.
    :type dataset: list of lists of str
    :param found_routes: Found possible routes to be formatted into json with dataset data.
    :type found_routes: list of lists of int
    :param bags_count: Number of requested bags.
    :type bags_count: int
    :param sort_by: Defaults to `None`. If `None`, returned json is not sorted in any kind. If 'total_price', returned
                    json trips (first level dictionaries in first array) are sorted by their total prices.
    :type sort_by: None or str
    :raise ValueError: If parameter sort_by is not supported.
    :return: Json formatted found routes.
    """
    if sort_by not in [None, 'total_price']:
        raise ValueError(f'illegal sort_by value: {sort_by}')

    data = []

    for found_route in found_routes:
        data.append({'flights': []})
        bags_allowed = float('inf')
        total_price = 0.0

        for index in found_route:
            if bags_allowed > int(dataset[index][BAGS_ALLOWED]):
                bags_allowed = int(dataset[index][BAGS_ALLOWED])
            total_price += float(dataset[index][BASE_PRICE]) + bags_count * float(dataset[index][BAG_PRICE])

            data[-1]['flights'].append({
                "flight_no": dataset[index][FLIGHT_NO],
                "origin": dataset[index][ORIGIN],
                "destination": dataset[index][DESTINATION],
                "departure": dataset[index][DEPARTURE],
                "arrival": dataset[index][ARRIVAL],
                "base_price": float(dataset[index][BASE_PRICE]),
                "bag_price": float(dataset[index][BAG_PRICE]),
                "bags_allowed": int(dataset[index][BAGS_ALLOWED])
            })

        data[-1]['bags_allowed'] = bags_allowed
        data[-1]['bags_count'] = int(bags_count)
        data[-1]['destination'] = dataset[found_route[-1]][DESTINATION]
        data[-1]['origin'] = dataset[found_route[0]][ORIGIN]
        data[-1]['total_price'] = total_price
        data[-1]['travel_time'] = str(datetime.strptime(dataset[found_route[-1]][ARRIVAL], '%Y-%m-%dT%H:%M:%S') -
                                      datetime.strptime(dataset[found_route[0]][DEPARTURE], '%Y-%m-%dT%H:%M:%S'))

    if sort_by:
        data = sorted(data, key=lambda d: d[sort_by])

    return json.dumps(data, indent=2)
