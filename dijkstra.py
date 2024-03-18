import heapq


def dijkstra(graph, start, start_time):
    distances = {node: float('inf') for node in graph.start_stop_end_stops}
    distances[start] = start_time
    pq = [(start_time, start)]
    prev_nodes = {node: None for node in graph.graph_dict}
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node] or curr_node not in graph.graph_dict:
            continue
        for node in graph.graph_dict[curr_node]:

            if node[8] == "72026":#debuger
                print("",end="")

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
                weight = weight + 60*24
            weight = weight - curr_dist
            new_dist = curr_dist + weight

            neighbor = node[3]

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = (curr_node,node[1],node[0],node[8])#ID HELLPER
                heapq.heappush(pq, (new_dist, neighbor))
    return distances, prev_nodes


def shortest_path(graph, start, goal, start_time_str):
    hour, minute, second = map(int, start_time_str.split(':'))
    distances, prev_nodes = dijkstra(graph, start, hour*60+minute)
    path = []
    curr_node = goal
    while curr_node is not None:
        if (prev_nodes[curr_node] is not None):  # ID HELLPER
            path.append((curr_node,distances[curr_node],prev_nodes[curr_node][1],
                         prev_nodes[curr_node][2],prev_nodes[curr_node][3]))
        else:
            path.append((curr_node,distances[curr_node]))  # ID HELLPER


        if(prev_nodes[curr_node] is not None):#ID HELLPER
            curr_node = prev_nodes[curr_node][0]
        else:
            curr_node = prev_nodes[curr_node]#ID HELLPER

    path.reverse()
    hour = (distances[goal] // 60)%24
    minute = distances[goal]%60
    return start_time_str,f"{hour:02d}:{minute:02d}:00", path

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
        if(last_line != stop[3]):
            last_line = stop[3]
            hour = stop[2] // 60
            minute = stop[2] % 60
            print()
            print(f"LINE : {last_line}")
            print(f"{hour:02d}:{minute:02d}:00", end="")
            print(" ---> " + last_stop[0], end="")

        last_stop = stop
        last_line = last_stop[3]

        print(" ---> " + stop[0],end="")

    hour = last_stop[1] // 60
    minute = last_stop[1] % 60
    print(" ---> " + f"{hour:02d}:{minute:02d}:00")
