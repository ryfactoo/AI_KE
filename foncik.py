import folium
import webbrowser

# Tworzenie listy punktów reprezentujących drogę
points = [(0, 0), (1, 1), (2, 0), (3, 1)]

# Tworzenie mapy
m = folium.Map(location=[0, 0], zoom_start=5)

# Dodawanie punktów na mapę
for point in points:
    folium.Marker(location=point).add_to(m)

# Rysowanie linii łączącej punkty
folium.PolyLine(points).add_to(m)

# Zapisywanie mapy do pliku HTML
m.save('map.html')

# Otwieranie pliku HTML w przeglądarce
webbrowser.open('map.html')