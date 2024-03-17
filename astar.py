import heapq
import csvToObj
import math
import graph
from geopy.distance import geodesic


def astar(graph, start, goal, start_time):
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
                priority = new_cost - cost_so_far[current] + lowest_time_heuristic(neighbor, graph.graph_dict[goal][0])
                heapq.heappush(front, (priority, neighbor[3]))
                came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8]

    path = [(goal, None, None, None, None)]
    current = came_from[goal]
    while current[0] != start:
        path.append(current)
        current = came_from[current[0]]
    path.append(current)
    path.reverse()

    return start_time, cost_so_far[goal], path


def astar_lower_line_switch(graph, start, goal, start_time):
    front = [(start_time, start)]
    came_from = {start: (None, None, None, None, None)}
    cost_so_far = {start: (start_time, start_time)}

    while front:
        _, current = heapq.heappop(front)

        if current == goal:
            break

        if current not in graph.graph_dict:
            continue

        for neighbor in graph.graph_dict[current]:

            weight = neighbor[2]
            if neighbor[1] < cost_so_far[current][0]:
                weight = weight + 24 * 60
            while 0 > weight - cost_so_far[current][0]:
                weight = weight + 60 * 24
            weight = weight - cost_so_far[current][0]
            new_cost = cost_so_far[current][0] + weight + lowest_stop_heuristic(neighbor, graph.graph_dict[goal][0],
                                                                                came_from[current][3])

            # if (neighbor[3] == "poczta główna".upper()):
            #     print("elo")

            # priority = new_cost + lowest_stop_heuristic(neighbor, graph.graph_dict[goal][0],
            #                                             came_from[current][3])  # test

            # if neighbor[3] not in cost_so_far or priority < cost_so_far[neighbor[3]]:  # test
            if neighbor[3] not in cost_so_far or new_cost < cost_so_far[neighbor[3]][1]:  # test
                # if neighbor[3] not in cost_so_far or weight < cost_so_far[neighbor[3]][0]:
                cost_so_far[neighbor[3]] = (weight,new_cost)  # test
                came_from[neighbor[3]] = current, neighbor[2], neighbor[1], neighbor[0], neighbor[8]  # orgin
                # if neighbor[3] not in cost_so_far or new_cost < cost_so_far[neighbor[3]]:  # orgin
                #     cost_so_far[neighbor[3]] = new_cost
                # cost_so_far[neighbor[3]] = new_cost#orgin
                priority = new_cost + lowest_time_heuristic(neighbor, graph.graph_dict[goal][0], )  # orgin
                # cost_so_far[neighbor[3]] = (cost_so_far[neighbor[3]][0],new_cost)  # test
                heapq.heappush(front, (priority, neighbor[3]))  # orgin


    path = [(goal, None, None, None, None)]
    current = came_from[goal]
    while current[0] != start:
        path.append(current)
        current = came_from[current[0]]
    path.append(current)
    path.reverse()

    return start_time, cost_so_far[goal], path


def manhattan_distance(current_stop, goal_stop):
    distance = int(geodesic((current_stop[6], current_stop[7]), (goal_stop[4], goal_stop[5])).meters)
    return distance


def meters_to_min(meters):
    min = meters // 300
    return min


def lowest_time_heuristic(current_stop, goal_stop):
    return meters_to_min(manhattan_distance(current_stop, goal_stop))


def lowest_stop_heuristic(current_stop, goal_stop, line):
    fine = 120

    if line is None or current_stop[0] == line:
        return 0
    else:
        return fine


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


def minute_after_midnight_to_str(time):
    hour = (time // 60) % 24
    minute = time % 60
    return f"{hour:02d}:{minute:02d}:00"


def astar2(graph, start, goal, start_time, heuristic="t"):
    if heuristic.upper() != "T":
        start_time, end_time, path = astar_lower_line_switch(graph, start.upper(), goal.upper(),
                                                             csvToObj.time_to_minutes_after_midnight(start_time))
        end_time = end_time[0]
    else:
        start_time, end_time, path = astar(graph, start.upper(), goal.upper(),
                                           csvToObj.time_to_minutes_after_midnight(start_time))

    print_astar(minute_after_midnight_to_str(start_time), minute_after_midnight_to_str(end_time), path)
