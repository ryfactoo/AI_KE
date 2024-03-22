import heapq
import webbrowser
import folium


def dijkstra(graph, start, start_time):
    distances = {node: float('inf') for node in graph.start_stop_end_stops}
    distances[start] = start_time
    pq = [(start_time, start)]
    prev_nodes = {node: None for node in graph.graph_dict}
    prev_nodes[start] = (
    None, start_time, None, None, graph.graph_dict[start][0][4], graph.graph_dict[start][0][5], None, None)
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node] or curr_node not in graph.graph_dict:
            continue
        for node in graph.graph_dict[curr_node]:

            if node[8] == "72026":  # debuger
                print("", end="")

            # weight = 0??
            # if node[1] < curr_dist:
            #     weight = 24 * 60
            # if node[2] < curr_dist:
            #     weight = weight + 24*60
            #
            # weight = weight + node[2] - curr_dist

            weight = node[2]
            if node[1] < curr_dist:
                weight = weight + 24 * 60
            while 0 > weight - curr_dist:
                weight = weight + 60 * 24
            weight = weight - curr_dist
            new_dist = curr_dist + weight

            neighbor = node[3]

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = (
                curr_node, node[1], node[0], node[8], node[4], node[5], node[6], node[7])  # ID HELLPER
                heapq.heappush(pq, (new_dist, neighbor))
    return distances, prev_nodes


def shortest_path(graph, start, goal, start_time_str):
    hour, minute, second = map(int, start_time_str.split(':'))
    distances, prev_nodes = dijkstra(graph, start, hour * 60 + minute)
    path = []
    curr_node = goal
    while prev_nodes[curr_node][2] is not None:
        if (prev_nodes[curr_node] is not None):  # ID HELLPER
            path.append((curr_node, distances[curr_node], prev_nodes[curr_node][1],
                         prev_nodes[curr_node][2], prev_nodes[curr_node][3], prev_nodes[curr_node][4],
                         prev_nodes[curr_node][5],
                         prev_nodes[curr_node][6], prev_nodes[curr_node][7]))
        else:
            path.append((curr_node, distances[curr_node]))  # ID HELLPER

        if (prev_nodes[curr_node] is not None):  # ID HELLPER
            curr_node = prev_nodes[curr_node][0]
        else:
            curr_node = prev_nodes[curr_node]  # ID HELLPER

    path.append((curr_node, distances[curr_node], None, None,
                 None, prev_nodes[curr_node][4], prev_nodes[curr_node][5], None,
                 None))
    path.reverse()
    hour = (distances[goal] // 60) % 24
    minute = distances[goal] % 60

    return start_time_str, f"{hour:02d}:{minute:02d}:00", path


def print_path(time_start_end_path):
    start_str, end_str, path = time_start_end_path
    print(start_str + " -----> " + end_str, end="\n")

    last_stop = path[0]
    last_line = ""
    for stop in path[1:]:
        if (last_line != stop[3] and last_line != ""):
            hour = last_stop[1] // 60
            minute = last_stop[1] % 60
            print(" ---> " + f"{hour:02d}:{minute:02d}:00", end="")
        if (last_line != stop[3]):
            last_line = stop[3]
            hour = stop[2] // 60
            minute = stop[2] % 60
            print()
            print(f"LINE : {last_line}")
            print(f"{hour:02d}:{minute:02d}:00", end="")
            print(" ---> " + last_stop[0], end="")

        last_stop = stop
        last_line = last_stop[3]

        print(" ---> " + stop[0], end="")

    hour = last_stop[1] // 60
    minute = last_stop[1] % 60
    print(" ---> " + f"{hour:02d}:{minute:02d}:00")

    print_path_on_map(path)


def print_path_on_map(path):
    m = folium.Map(location=[51.14, 17.02], zoom_start=12)  # Ustawienie początkowego położenia mapy
    current_line = path[0][3]
    color = 'blue'
    for i in range(1, len(path)):
        start_node = path[i]

        if i == len(path) -1:
            end_node = path[i]
            end_coords = (float(end_node[7]), float(end_node[8]))

        else:
            end_node = path[i + 1]
            end_coords = (float(end_node[5]), float(end_node[6]))

        start_coords = (float(start_node[5]), float(start_node[6]))

        if i == 1:
            folium.Marker(location=start_coords, icon=folium.Icon(color='green')).add_to(m)
        else:
            folium.Marker(location=start_coords, icon=folium.Icon(color='blue')).add_to(m)

            # Dodanie pinezki na końcu każdego odcinka
        folium.Marker(location=end_coords, icon=folium.Icon(color='red')).add_to(m)

        # Dodanie linii łączącej punkty z odpowiednim kolorem
        if current_line != start_node[3]:
            color = negation_color(color)

        folium.PolyLine(locations=[start_coords, end_coords], color=color).add_to(m)

        current_line = start_node[3]

    m.save('dijkstra_map.html')
    webbrowser.open('dijkstra_map.html')

def negation_color(color):
    if color == 'blue':
        return 'red'
    else: return 'blue'

# def print_path_on_map(path):
#     m = folium.Map(location=[52.0, 20.0], zoom_start=10)  # Ustawienie początkowego położenia mapy
#     last_line = None
#     folium.Marker(location=(path[0][5], path[0][6])).add_to(m)
#
#     for i in range(1, len(path) - 1):
#         start_node = path[i]
#         end_node = path[i + 1]
#         start_coords = (float(start_node[5]), float(start_node[6]))
#         end_coords = (float(end_node[5]), float(start_node[6]))
#
#         folium.Marker(location=start_coords).add_to(m)
#
#         folium.PolyLine([start_coords,end_coords]).add_to(m)
#
#         # Zapisanie mapy do pliku HTML
#     m.save('dijkstra_map.html')
#     webbrowser.open('dijkstra_map.html')
