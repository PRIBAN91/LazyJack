from memoize import memoize
from Utility.Graph import Graph
from django.conf import settings


# @memoize(timeout=settings.FETCH_PLANS_CACHE_TTL)
def determine_fastest_route(input_data):
    preferred_time = input_data["prefered_time"]
    start_city = input_data["trip_plan"]["start_city"]
    end_city = input_data["trip_plan"]["end_city"]
    flight_dict, place_set = dict(), set()
    for flight_schedule in input_data["schedules"]:
        if flight_schedule["departure"]["timestamp"] > preferred_time:
            flight_dict[(flight_schedule["departure"]["city"], flight_schedule["arrival"]["city"])] = \
                (flight_schedule["departure"]["timestamp"], flight_schedule["arrival"]["timestamp"])
            place_set.add(flight_schedule["departure"]["city"])
            place_set.add(flight_schedule["arrival"]["city"])
    return create_adjacency_matrix(place_set, flight_dict, start_city, end_city)


def create_adjacency_matrix(place_set, flight_dict, start_city, end_city):
    v_total, max_index = len(place_set), 1
    place_indices = {start_city: 0, end_city: v_total - 1}
    matrix = [[0 for i in range(v_total)] for j in range(v_total)]
    for place in place_set:
        if place not in place_indices:
            place_indices[place] = max_index
            max_index += 1
    for k, v in flight_dict.items():
        matrix[place_indices[k[0]]][place_indices[k[1]]] = v[1] - v[0]
    return final_result_json(v_total, matrix, place_indices, flight_dict, start_city)


def final_result_json(v_total, matrix, place_indices, flight_dict, start_city):
    g = Graph(v_total, matrix)
    parent = g.dijkstra(0)
    place_list = [0] * v_total
    for k, v in place_indices.items():
        place_list[v] = k
    idx = v_total - 1
    flight_plan = []
    while parent[idx] != -1:
        flight_plan.append(
            {"city": place_list[idx], "timestamp": flight_dict[(place_list[parent[idx]], place_list[idx])][1]})
        idx = parent[idx]
    flight_plan.append(
        {"city": start_city, "timestamp": flight_dict[(start_city, flight_plan[len(flight_plan) - 1]["city"])][0]})
    flight_plan.reverse()
    return {"flight_plan": flight_plan}
