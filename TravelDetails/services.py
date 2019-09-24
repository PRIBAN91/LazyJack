from memoize import memoize


@memoize(timeout=60)
def determine_fastest_route(input_data):
    route_dict = create_route_dict(input_data["schedules"], input_data["prefered_time"])
    return {
        "flight_plan": find_fastest_route(input_data['trip_plan']['start_city'], input_data['trip_plan']['end_city'],
                                          input_data['prefered_time'], route_dict, set(), dict())}


def create_route_dict(schedules, preferred_time):
    route_dict = dict()
    for schedule in schedules:
        if schedule["departure"]["timestamp"] > preferred_time:
            if schedule["departure"]["city"] not in route_dict:
                route_dict[schedule["departure"]["city"]] = []
            route_dict[schedule["departure"]["city"]].append(
                {"departure_timestamp": schedule["departure"]["timestamp"], "destination": schedule["arrival"]["city"],
                 "arrival_timestamp": schedule["arrival"]["timestamp"]})
    return route_dict


def find_fastest_route(departure_city, arrival_city, departure_timestamp, route_dict, visited_cities, route_history):
    print("In fastest route")
    route_key = (departure_city, arrival_city, departure_timestamp)
    if route_key in route_history:
        return route_history[route_key]
    if departure_city == arrival_city:
        return [{"city": departure_city, "timestamp": departure_timestamp}]
    if departure_city in visited_cities:
        return None
    fastest_route = None
    for flight in route_dict[departure_city]:
        if flight['departure_timestamp'] >= departure_timestamp:
            visited_cities.add(departure_city)
            route = find_fastest_route(flight['destination'], arrival_city, flight['arrival_timestamp'], route_dict,
                                       visited_cities, route_history)
            if route and not fastest_route or route[len(route) - 1]['timestamp'] < \
                    fastest_route[len(fastest_route) - 1]['timestamp']:
                fastest_route = [{"city": departure_city, "timestamp": flight['departure_timestamp']}] + route
    route_history[route_key] = fastest_route
    return fastest_route
