class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.start_stop_end_stops = set()
        self.graph_dict = {}
        for (id, company, line, departure_time, arrival_time, start_stop, end_stop, start_stop_lat,
             start_stop_lon, end_stop_lat, end_stop_lon) in self.edges:

            self.start_stop_end_stops.add(start_stop)
            self.start_stop_end_stops.add(end_stop)

            if start_stop in self.graph_dict:
                self.graph_dict[start_stop].append((line, departure_time, arrival_time, end_stop, start_stop_lat,
                                                    start_stop_lon, end_stop_lat, end_stop_lon, id))#ID HELLPER
            else:
                self.graph_dict[start_stop] = [(line, departure_time, arrival_time, end_stop, start_stop_lat,
                                                start_stop_lon, end_stop_lat, end_stop_lon, id)]#ID HELLPER

    def __str__(self):
        result = ""
        for stop, connections in self.graph_dict.items():
            result += f"Stop: {stop}\n"
            for connection in connections:
                (line, departure_time, arrival_time, end_stop, start_stop_lat, start_stop_lon, end_stop_lat,
                end_stop_lon) = connection
                result += (f"  Line: {line}, Departure: {departure_time}, Arrival: {arrival_time}, End Stop: {end_stop}"
                           f", Start Lat: {start_stop_lat}, Start Lon: {start_stop_lon}, End Lat: {end_stop_lat}"
                           f", End Lon: {end_stop_lon}\n")
            result += "\n"
        return result

    def count_elements_in_list(self):
        total_elements = 0
        for sublist in self.graph_dict.values():
            total_elements += len(sublist)
        return total_elements
