from datetime import datetime
from TravelDetails.Graph import Graph


def determine_fastest_route(input_data):
    preferred_time = input_data["prefered_time"]
    start_city = input_data["trip_plan"]["start_city"]
    end_city = input_data["trip_plan"]["end_city"]
    flight_dict, place_set = dict(), set()
    for flight_schedule in input_data["schedules"]:
        if flight_schedule["departure"]["timestamp"] > preferred_time:
            save_departure_arrival_data(flight_schedule, flight_dict, start_city, preferred_time)
            place_set.add(flight_schedule["departure"]["city"])
            place_set.add(flight_schedule["arrival"]["city"])
    # print(flight_dict)
    print(place_set)
    create_adjacency_matrix(place_set, flight_dict, start_city, end_city, preferred_time)
    # print(preferred_time)


def save_departure_arrival_data(flight_schedule, flight_dict, start_city, preferred_time):
    if flight_schedule["departure"]["city"] == start_city:
        flight_dict[(flight_schedule["departure"]["city"], flight_schedule["arrival"]["city"])] = \
            (preferred_time, flight_schedule["arrival"]["timestamp"])
    else:
        flight_dict[(flight_schedule["departure"]["city"], flight_schedule["arrival"]["city"])] = \
            (flight_schedule["departure"]["timestamp"], flight_schedule["arrival"]["timestamp"])


def create_adjacency_matrix(place_set, flight_dict, start_city, end_city, preferred_time):
    v_total, max_index = len(place_set), 1
    place_indices = {start_city: 0, end_city: v_total - 1}
    matrix = [[0 for i in range(v_total)] for j in range(v_total)]
    for place in place_set:
        if place not in place_indices:
            place_indices[place] = max_index
            max_index += 1
    # print(place_indices)
    for k, v in flight_dict.items():
        matrix[place_indices[k[0]]][place_indices[k[1]]] = v[1] - v[0]
    # print(matrix)
    # v_total = len(flight_dict) + 1
    # max_index = 1
    # matrix = [[0 for i in range(v_total)] for j in range(v_total)]
    # dest_indices = {start_city: 0, end_city: v_total - 1}
    # for k, v in flight_dict[start_city].items():
    #     dest_indices[k] = max_index
    #     max_index += 1
    #     matrix[0][dest_indices[k]] = v - preferred_time
    # for k in flight_dict:
    #     if k not in dest_indices:
    #         dest_indices[k] = max_index
    #         max_index += 1
    # for k, v in flight_dict.items():
    #     if k != start_city:
    #         for k1, v1 in v.items():
    #             matrix[dest_indices[k]][dest_indices[k1]] = v1 - preferred_time
    # print(matrix)


def final_result_json(v_total, matrix, place_indices):
    g = Graph(v_total, matrix)
    parents = g.dijkstra(0)
