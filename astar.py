import argparse
import heapq
import csvToObj
import webbrowser
import folium
from geopy import distance as geopy_distance

penalty = 60


def astar(graph, start, goal, start_time, heuristic):
    front = [(start_time, start)]
    came_from = {start: (None, None, None, None, None)}
    cost_so_far = {start: start_time}

    while front:
        _, current = heapq.heappop(front)

        if current == goal:
            break

        if current not in graph.graph_dict:
            continue

        for neighbor in graph.graph_dict[current]:

            new_cost = neighbor[2]
            if neighbor[1] < cost_so_far[current]:
                new_cost = new_cost + 24 * 60
            while 0 > new_cost - cost_so_far[current]:
                new_cost = new_cost + 60 * 24

            if neighbor[3] not in cost_so_far or new_cost < cost_so_far[neighbor[3]]:
                cost_so_far[neighbor[3]] = new_cost
                priority = new_cost - cost_so_far[current] + heuristic(neighbor, graph.graph_dict[goal][0])
                heapq.heappush(front, (priority, neighbor[3]))
                came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8], neighbor[4], \
                    neighbor[5], neighbor[6], neighbor[7]

    path = [(goal, None, None, None, None)]
    current = came_from[goal]
    while current[0] != start:
        path.append(current)
        current = came_from[current[0]]
    path.append(current)
    path.reverse()

    return start_time, cost_so_far[goal], path


# line, departure_time, arrival_time, end_stop, start_stop_lat,start_stop_lon, end_stop_lat, end_stop_lon, id

def astar_multi_come_from(graph, start, goal, start_time):
    front = [(start_time, start)]
    came_from = {(start, "None"): (None, None, None, None, None)}
    cost_so_far = {(start, "None"): start_time}
    lowes_cost_so_far = {start: start_time}
    lines_from_start = set()
    end = False

    while front:
        _, current = heapq.heappop(front)

        if current == goal:
            for line in lines_from_start:
                if (goal, line) in cost_so_far:
                    end = True

            if end:
                break

        if current not in graph.graph_dict:
            continue

        for neighbor in graph.graph_dict[current]:

            if current == start:
                lines_from_start.add(neighbor[0])

            new_cost = neighbor[2]

            if (current, neighbor[0]) not in cost_so_far:
                cost = lowes_cost_so_far[current]
            else:
                cost = cost_so_far[(current, neighbor[0])]

            if neighbor[1] < cost:
                new_cost = new_cost + 24 * 60
            while 0 > new_cost - cost:
                new_cost = new_cost + 60 * 24

            if (neighbor[3], neighbor[0]) not in cost_so_far or new_cost < cost_so_far[neighbor[3], neighbor[0]]:
                cost_so_far[(neighbor[3], neighbor[0])] = new_cost
                came_from[(neighbor[3], neighbor[0])] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8], \
                    neighbor[4], \
                    neighbor[5], neighbor[6], neighbor[7]

                priority = new_cost - cost + lowest_stop_heuristic(neighbor,
                                                                   graph.graph_dict[goal][0],
                                                                   came_from[(neighbor[3], neighbor[0])][3])
                heapq.heappush(front, (priority, neighbor[3]))

                if neighbor[3] not in lowes_cost_so_far or new_cost < lowes_cost_so_far[neighbor[3]]:
                    lowes_cost_so_far[neighbor[3]] = new_cost

    line = None
    for line_from_start in lines_from_start:
        if (goal, line_from_start) in cost_so_far and (line == None or cost_so_far[goal, line_from_start] < cost_line):
            line = line_from_start
            cost_line = cost_so_far[goal, line_from_start]

    path = [(goal, None, None, None, None)]
    current = came_from[goal, line]
    while current[0] != start:
        path.append(current)
        if current[0] == start:
            current = came_from[(current[0], None)]
        else:
            current = came_from[current[0], line]
    path.append(current)
    path.reverse()

    return start_time, cost_so_far[goal, line], path


# def astar_proba_mocy_godzina_23(graph, start, goal, start_time):
#     front = [(start_time, start, 0)]
#     came_from = {start: (None, None, None, None, None)}
#     cost_so_far = {start: (start_time, 0)}
#
#     while front:
#         _, current, line_switch = heapq.heappop(front)
#
#         if current == goal:
#             break
#
#         if current not in graph.graph_dict:
#             continue
#
#         for neighbor in graph.graph_dict[current]:
#
#             new_cost = neighbor[2]
#             if neighbor[1] < cost_so_far[current][0]:
#                 new_cost = new_cost + 24 * 60
#             while 0 > new_cost - cost_so_far[current][0]:
#                 new_cost = new_cost + 60 * 24
#
#             new_line_switch = line_switch
#             if came_from[current][3] is not None and neighbor[0] != came_from[current][3]:
#                 new_line_switch = new_line_switch + 1
#
#             if neighbor[3] not in cost_so_far or new_cost - (cost_so_far[neighbor[3]][1] - new_line_switch) * penalty < \
#                     cost_so_far[neighbor[3]][0]:
#
#                 if neighbor[3] not in cost_so_far or cost_so_far[neighbor[3]][1] > new_line_switch:
#                     cost_so_far[neighbor[3]] = (new_cost, new_line_switch)
#                     came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8]
#                 # cost_so_far[neighbor[3]] = (new_cost,new_line_switch)
#                 priority = new_cost - cost_so_far[current][0] + lowest_stop_heuristic(neighbor,
#                                                                                       graph.graph_dict[goal][0],
#                                                                                       came_from[current][3])
#                 heapq.heappush(front, (priority, neighbor[3], new_line_switch))
#                 # came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8]
#
#     path = [(goal, None, None, None, None)]
#     current = came_from[goal]
#     while current[0] != start:
#         path.append(current)
#         current = came_from[current[0]]
#     path.append(current)
#     path.reverse()
#
#     return start_time, cost_so_far[goal][0], path
#
#
# def astar_lower_line_switch(graph, start, goal, start_time):
#     front = [(start_time, start)]
#     came_from = {start: (None, None, None, None, None)}
#     cost_so_far = {start: (start_time, start_time)}
#
#     while front:
#         _, current = heapq.heappop(front)
#
#         if current == goal:
#             break
#
#         if current not in graph.graph_dict:
#             continue
#
#         for neighbor in graph.graph_dict[current]:
#
#             weight = neighbor[2]
#             if neighbor[1] < cost_so_far[current][0]:
#                 weight = weight + 24 * 60
#             while 0 > weight - cost_so_far[current][0]:
#                 weight = weight + 60 * 24
#             weight = weight - cost_so_far[current][0]
#             new_cost = cost_so_far[current][0] + weight + lowest_stop_heuristic(neighbor, graph.graph_dict[goal][0],
#                                                                                 came_from[current][3])
#
#             # if (neighbor[3] == "poczta główna".upper()):
#             #     print("elo")
#
#             # priority = new_cost + lowest_stop_heuristic(neighbor, graph.graph_dict[goal][0],
#             #                                             came_from[current][3])  # test
#
#             # if neighbor[3] not in cost_so_far or priority < cost_so_far[neighbor[3]]:  # test
#             if neighbor[3] not in cost_so_far or new_cost < cost_so_far[neighbor[3]][1]:  # test
#                 # if neighbor[3] not in cost_so_far or weight < cost_so_far[neighbor[3]][0]:
#                 cost_so_far[neighbor[3]] = (weight, new_cost)  # test
#                 came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8]  # orgin
#                 # if neighbor[3] not in cost_so_far or new_cost < cost_so_far[neighbor[3]]:  # orgin
#                 #     cost_so_far[neighbor[3]] = new_cost
#                 # cost_so_far[neighbor[3]] = new_cost#orgin
#                 priority = new_cost + lowest_time_heuristic(neighbor, graph.graph_dict[goal][0], )  # orgin
#                 # cost_so_far[neighbor[3]] = (cost_so_far[neighbor[3]][0],new_cost)  # test
#                 heapq.heappush(front, (priority, neighbor[3]))  # orgin
#
#     path = [(goal, None, None, None, None)]
#     current = came_from[goal]
#     while current[0] != start:
#         path.append(current)
#         current = came_from[current[0]]
#     path.append(current)
#     path.reverse()
#
#     return start_time, cost_so_far[goal], path


def manhattan_distance(current_stop, goal_stop):
    distanceX = geopy_distance.distance((current_stop[6], goal_stop[5]), (goal_stop[4], goal_stop[5])).meters
    distanceY = geopy_distance.distance((goal_stop[4], current_stop[7]), (goal_stop[4], goal_stop[5])).meters

    return distanceX + distanceY


def euclidean_distance(current_stop, goal_stop):
    distance = geopy_distance.distance((current_stop[6], current_stop[7]), (goal_stop[4], goal_stop[5])).meters
    return distance


def euclidean_distance_cord(start_lat, start_lot, goal_lat, goal_lot):
    distance = geopy_distance.distance((start_lat, start_lot), (goal_lat, goal_lot)).meters
    return distance


def meters_to_min(meters):
    min = meters // 300
    return min


def lowest_time_heuristic_manhattan(current_stop, goal_stop):
    return meters_to_min(manhattan_distance(current_stop, goal_stop))


def lowest_time_heuristic_avg_manhattan_euclidean(current_stop, goal_stop):
    return meters_to_min(
        (manhattan_distance(current_stop, goal_stop) + euclidean_distance(current_stop, goal_stop)) / 2)


def lowest_stop_heuristic(current_stop, goal_stop, line):
    heuristic = lowest_time_heuristic_manhattan(current_stop, goal_stop)

    if line is None or current_stop[0] == line:
        return heuristic
    else:
        return penalty + heuristic


def circle_heuristic(current_stop, goal_stop):
    center = (51.110114, 17.031977)

    if (current_stop[3] == goal_stop[3]):
        return 0

    min = 1 + meters_to_min(euclidean_distance_cord(center[0], center[1], goal_stop[6], goal_stop[7])
                            - euclidean_distance_cord(center[0], center[1], goal_stop[4],goal_stop[5]))
    return min


def print_astar(start_time, end_time, path):
    print(start_time + " -----> " + end_time, end="\n")

    last_stop = path[0]
    last_line = ""
    for stop in path[:-1]:

        if last_line != stop[3] and last_line != "":
            print(" ---> " + stop[0], end="")

            hour = last_stop[1] // 60
            minute = last_stop[1] % 60
            print(" ---> " + f"{hour:02d}:{minute:02d}:00", end="")
        if last_line != stop[3]:
            last_line = stop[3]
            hour = stop[2] // 60
            minute = stop[2] % 60
            print()
            print(f"LINE : {last_line}")
            print(f"{hour:02d}:{minute:02d}:00", end="")
            print(" ---> " + stop[0], end="")
        else:
            print(" ---> " + stop[0], end="")

        last_stop = stop
        last_line = stop[3]

    print(" ---> " + path[-1][0], end="")
    hour = last_stop[1] // 60
    minute = last_stop[1] % 60
    print(" ---> " + f"{hour:02d}:{minute:02d}:00")

    print_path_on_map(path)


def minute_after_midnight_to_str(time):
    hour = (time // 60) % 24
    minute = time % 60
    return f"{hour:02d}:{minute:02d}:00"


def astar_prepare(graph, start, goal, start_time, heuristic="t"):
    if heuristic.upper() == "S":
        start_time, end_time, path = astar_multi_come_from(graph, start.upper(), goal.upper(),
                                                           csvToObj.time_to_minutes_after_midnight(start_time))
        print_astar(minute_after_midnight_to_str(start_time), minute_after_midnight_to_str(end_time), path)

    elif heuristic.upper() == "T":
        start_time, end_time, path = astar(graph, start.upper(), goal.upper(),
                                           csvToObj.time_to_minutes_after_midnight(start_time),
                                           lowest_time_heuristic_manhattan)
        print_astar(minute_after_midnight_to_str(start_time), minute_after_midnight_to_str(end_time), path)

    elif heuristic.upper() == "T+":
        start_time, end_time, path = astar(graph, start.upper(), goal.upper(),
                                           csvToObj.time_to_minutes_after_midnight(start_time),
                                           lowest_time_heuristic_avg_manhattan_euclidean)
        print_astar(minute_after_midnight_to_str(start_time), minute_after_midnight_to_str(end_time), path)

    elif heuristic.upper() == "T-":
        start_time, end_time, path = astar(graph, start.upper(), goal.upper(),
                                           csvToObj.time_to_minutes_after_midnight(start_time),
                                           circle_heuristic)
        print_astar(minute_after_midnight_to_str(start_time), minute_after_midnight_to_str(end_time), path)


def print_path_on_map(path):
    m = folium.Map(location=[51.14, 17.02], zoom_start=12)
    current_line = path[0][3]
    color = 'blue'
    for i in range(len(path) - 1):
        start_node = path[i]

        if i == len(path) - 2:
            end_node = path[i]
            end_coords = (float(end_node[7]), float(end_node[8]))

        else:
            end_node = path[i + 1]
            end_coords = (float(end_node[5]), float(end_node[6]))

        start_coords = (float(start_node[5]), float(start_node[6]))

        if i == 0:
            folium.Marker(location=start_coords, icon=folium.Icon(color='green')).add_to(m)
        else:
            folium.Marker(location=start_coords, icon=folium.Icon(color)).add_to(m)

        if current_line != start_node[3]:
            color = negation_color(color)

        folium.PolyLine(locations=[start_coords, end_coords], color=color).add_to(m)

        current_line = start_node[3]

    folium.Marker(location=end_coords, icon=folium.Icon(color='red')).add_to(m)
    m.save('dijkstra_map.html')
    webbrowser.open('dijkstra_map.html')


def negation_color(color):
    if color == 'blue':
        return 'orange'
    else:
        return 'blue'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--start_stop", help="Start stop", required=True)
    parser.add_argument("-g", "--goal_stop", help="Goal stop", required=True)
    parser.add_argument("-t", "--time", help="Time", required=True)
    parser.add_argument("-m", "--mode",
                        help="Mode heuristic (T - Euclidean, T+ - AVG euclidean + manhattan , T- Circle , S - Lowest "
                             "switch line)",
                        required=True)

    args = parser.parse_args()

    list_csv = csvToObj.create_list_from_csv('data_avg.csv')
    graph = csvToObj.create_graph_from_list(list_csv)

    astar_prepare(graph, args.start_stop.upper(), args.goal_stop.upper(), args.time, args.mode)
