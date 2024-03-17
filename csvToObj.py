import csv
import graph
import dijkstra
import astar
import time


def create_list_from_csv(csv_file):
    edges = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:

            if len(row) == 11:
                row[3] = time_to_minutes_after_midnight(row[3])
                row[4] = time_to_minutes_after_midnight(row[4])
                row[5] = row[5].upper()
                row[6] = row[6].upper()

                edges.append(row)
    return edges


def create_graph_from_list(edges):
    return graph.Graph(edges)


def normalize_hour(hour_str):
    hour, minute, second = map(int, hour_str.split(':'))
    if hour >= 24:
        hour -= 24
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def time_to_minutes_after_midnight(time_str):
    hour, minute, second = map(int, time_str.split(':'))

    if hour >= 24:
        hour = hour % 24

    return hour * 60 + minute


if __name__ == '__main__':
    list = create_list_from_csv('data.csv')
    # list = create_list_from_csv('mini.csv')

    graph = create_graph_from_list(list)

    # dijkstra.print_path(dijkstra.shortest_path(graph,"PAPROTNA".upper(), "Poczta Główna".upper(), "20:52:00"))
    # astar.astar2(graph,"PAPROTNA".upper(), "Poczta Główna".upper(), "20:52:00","s")

    # dijkstra.print_path(dijkstra.shortest_path(graph,"PAPROTNA".upper(), "Poczta główna".upper(), "20:52:00"))
    # astar.astar2(graph,"PAPROTNA".upper(), "Poczta główna".upper(), "20:52:00", "s")

    # start_time = time.time()
    # dijkstra.print_path(dijkstra.shortest_path(graph,"krzyki".upper(), "Jarnołtów".upper(), "23:00:00"))
    # end_time = time.time()
    #
    # elapsed_time = end_time - start_time
    # print("Czas działania funkcji: ", elapsed_time, "sekundy")
    #
    #
    # start_time = time.time()
    # astar.astar2(graph,"krzyki".upper(), "Jarnołtów".upper(), "23:00:00","t")
    # end_time = time.time()
    #
    # elapsed_time = end_time - start_time
    # print("Czas działania funkcji: ", elapsed_time, "sekundy")

    dijkstra.print_path(dijkstra.shortest_path(graph,"krzyki".upper(), "Jarnołtów".upper(), "23:00:00"))
    print("-------------------------")
    astar.astar2(graph,"krzyki".upper(), "Jarnołtów".upper(), "23:00:00","s")

    # dijkstra.print_path(dijkstra.shortest_path(graph,"Wyszyńskiego".upper(), "pl. grunwaldzki".upper(), "07:15:00"))
    # print("-------------------------")
    # astar.astar2(graph,"Wyszyńskiego".upper(), "pl. grunwaldzki".upper(), "07:15:00","t")


    # dijkstra.print_path(dijkstra.shortest_path(graph, "Wyszyńskiego".upper(), "PL. grunwaldzki".upper(), "11:33:00"))
    # astar.astar2(graph,"Wyszyńskiego".upper(), "PL. grunwaldzki".upper(), "11:33:00")




