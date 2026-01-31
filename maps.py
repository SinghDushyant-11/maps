#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[2]:


import requests
import networkx as nx
import folium
#from IPython.display import HTML



#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class TextStyle:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
#--------------------------------------------------------------------------------------------------------------------------------
famous_places = [
    "Vidhana Soudha",
    "Bangalore Palace",
    "Lalbagh Botanical Garden",
    "Cubbon Park",
    "ISKCON Temple Bangalore",
    "Bannerghatta National Park",
    "Wonderla Amusement Park",
    "UB City Mall",
]

# Local Places and Bus Stands
local_places_bus_stands = [
    "Kempegowda Bus Station (Majestic)",
    "MG Road (Mahatma Gandhi Road)",
    "Commercial Street",
    "Malleswaram",
    "Banashankari Temple",
    "Yeshwantpur Railway Station",
    "Jayanagar 4th Block",
    "Shivajinagar Bus Stand",
]

# Metro Stations
metro_stations = [
    "Kempegowda Metro Station (Majestic)",
    "Vidhana Soudha Metro Station",
    "Cubbon Park Metro Station",
    "MG Road Metro Station",
    "Indiranagar Metro Station",
    "Jayanagar Metro Station",
]

# Print Famous Places with serial numbers
print("Famous Places:")
for i, place in enumerate(famous_places, start=1):
    print(f"A{i}: {place}")

# Print Local Places and Bus Stands with serial numbers
print("\nLocal Places and Bus Stands:")
for i, place in enumerate(local_places_bus_stands, start=1):
    print(f"B{i}: {place}")

# Print Metro Stations with serial numbers
print("\nMetro Stations:")
for i, station in enumerate(metro_stations, start=1):
    print(f"C{i}: {station}")
#-------------------------------------------------------------------------------------------------------------------------------
places_data = {
    "A1": {"name": "Vidhana Soudha", "category": "Famous Places", "latitude": 12.9719, "longitude": 77.5937},
    "A2": {"name": "Bangalore Palace", "category": "Famous Places", "latitude": 12.9985, "longitude": 77.5925},
    "A3": {"name": "Lalbagh Botanical Garden", "category": "Famous Places", "latitude": 12.9497, "longitude": 77.5848},
    "A4": {"name": "Cubbon Park", "category": "Famous Places", "latitude": 12.9750, "longitude": 77.5900},
    "A5": {"name": "ISKCON Temple Bangalore", "category": "Famous Places", "latitude": 13.0094, "longitude": 77.5510},
    "A6": {"name": "Bannerghatta National Park", "category": "Famous Places", "latitude": 12.8000, "longitude": 77.5770},
    "A7": {"name": "Wonderla Amusement Park", "category": "Famous Places", "latitude": 12.8346, "longitude": 77.4003},
    "A8": {"name": "UB City Mall", "category": "Famous Places", "latitude": 12.9716, "longitude": 77.5956},
    
    "B1": {"name": "Kempegowda Bus Station (Majestic)", "category": "Local Places/Bus Stands", "latitude": 12.9772, "longitude": 77.5726},
    "B2": {"name": "MG Road (Mahatma Gandhi Road)", "category": "Local Places/Bus Stands", "latitude": 12.9741, "longitude": 77.6073},
    "B3": {"name": "Commercial Street", "category": "Local Places/Bus Stands", "latitude": 12.9822, "longitude": 77.6088},
    "B4": {"name": "Malleswaram", "category": "Local Places/Bus Stands", "latitude": 13.0068, "longitude": 77.5701},
    "B5": {"name": "Banashankari Temple", "category": "Local Places/Bus Stands", "latitude": 12.9255, "longitude": 77.5468},
    "B6": {"name": "Yeshwantpur Railway Station", "category": "Local Places/Bus Stands", "latitude": 13.0232, "longitude": 77.5525},
    "B7": {"name": "Jayanagar 4th Block", "category": "Local Places/Bus Stands", "latitude": 12.9274, "longitude": 77.5900},
    "B8": {"name": "Shivajinagar Bus Stand", "category": "Local Places/Bus Stands", "latitude": 12.9835, "longitude": 77.6064},
    
    "C1": {"name": "Kempegowda Metro Station (Majestic)", "category": "Metro Stations", "latitude": 12.9772, "longitude": 77.5726},
    "C2": {"name": "Vidhana Soudha Metro Station", "category": "Metro Stations", "latitude": 12.9793, "longitude": 77.5922},
    "C3": {"name": "Cubbon Park Metro Station", "category": "Metro Stations", "latitude": 12.9746, "longitude": 77.5952},
    "C4": {"name": "MG Road Metro Station", "category": "Metro Stations", "latitude": 12.9752, "longitude": 77.6054},
    "C5": {"name": "Indiranagar Metro Station", "category": "Metro Stations", "latitude": 12.9784, "longitude": 77.6389},
    "C6": {"name": "Jayanagar Metro Station", "category": "Metro Stations", "latitude": 12.9253, "longitude": 77.5936},
}
n=int(input("entre no of stops (0 if none)(max 3)="))

#***********************************************************************************************************************


def decode(polyline_str):
    """
    Decodes a polyline encoded string into a list of latitude-longitude pairs.
    """
    index, length = 0, len(polyline_str)
    coordinates = []
    lat, lng = 0, 0

    while index < length:
        shift, result = 0, 0

        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        d_lat = ~(result >> 1) if result & 1 else result >> 1
        lat += d_lat

        shift, result = 0, 0

        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        d_lng = ~(result >> 1) if result & 1 else result >> 1
        lng += d_lng

        coordinates.append((lat * 1e-5, lng * 1e-5))

    return coordinates


def road(a,b):
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {'origin': f"{places_data[a]['latitude']},{places_data[a]['longitude']}",'destination': f"{places_data[b]['latitude']},{places_data[b]['longitude']}",'key': 'AIzaSyD757qcPbrXBXNH6bUYyuQRP4oLS_EeeQE',}
    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()
    # Extract the polyline from the response
    polyline = data['routes'][0]['overview_polyline']['points']
    polyline_points = decode(polyline)
    # Create a Folium map object
    map_dijkstra = folium.Map(location=[places_data[a]["latitude"], places_data[a]["longitude"]], zoom_start=12)
    # Create a list to store the coordinates of the decoded polyline points
    coordinates = []
    location=[places_data[a]["latitude"], places_data[a]["longitude"]]
    location=[places_data[b]["latitude"], places_data[b]["longitude"]]
    # Add the decoded points to the coordinates list
    for point in polyline_points:
        if(a in places_data):
            lat, lon = point
            coordinates.append([lat, lon])
    # Add the polyline to the map
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5,  # Adjust line weight as needed
        opacity=0.8,  # Adjust line opacity as needed
    ).add_to(map_dijkstra)
    return map_dijkstra



def dijkstra(graph, start, end):
    shortest_path = nx.shortest_path(graph, source=start, target=end, weight='time')
    return shortest_path

def visualize_route(graph, route, shortest_path):
    map_object = folium.Map(location=[13.104800, 77.576300], zoom_start=10)

    for node in route:
        pos = graph.nodes[node]['pos']
        #folium.Marker(location=pos, popup=node).add_to(map_object)

    # Draw edges
    for i in range(len(route) - 1):
        edge = (route[i], route[i + 1])
        color = 'purple' if edge in shortest_path or (edge[1], edge[0]) in shortest_path else 'gray'
        #folium.PolyLine([graph.nodes[edge[0]]['pos'], graph.nodes[edge[1]]['pos']], color=color).add_to(map_object)

    return map_object

# Create a graph
G = nx.Graph()

    # Add nodes (locations)
G.add_node("A", pos=(13.104800, 77.576300))
G.add_node("B", pos=(12.924900, 77.566200))
G.add_node("C", pos=(12.925453, 77.546761))

    # Add edges with properties
G.add_edge("A", "B", weight=5, time=3, traffic=1.2)
G.add_edge("B", "C", weight=4, time=2, traffic=1.5)
G.add_edge("A", "C", weight=8, time=4, traffic=1.8)

    # Find shortest path
start_node = "A"
end_node = "C"
start_node1 = "A"
end_node1 = "B"
shortest_path_dijkstra1 = dijkstra(G, start_node1, end_node1)
shortest_path_dijkstra = dijkstra(G, start_node, end_node)
from geopy.distance import geodesic



    # Visualize route on the map

map_dijkstra = visualize_route(G, shortest_path_dijkstra, G.edges())
map_dijkstra1 = visualize_route(G, shortest_path_dijkstra, G.edges())
    # Display the map
    #map_dijkstra 
    #map_dijkstra1
    

    
    #dijkstra.clear_layers()
map_dijkstra

#------------------------------------------------------------------------------------------------------------------------------


    
print("petrol pump and restaurents:")    
# Replace 'YOUR_GOOGLE_API_KEY' with your actual API key
api_key = 'AIzaSyDKdbMVwLb7ddZUTdM7B_IwsWCNLKVbIVw'

# Function to get nearby places
def get_nearby_places(latitude, longitude, place_type):
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    radius = 5000  # Search within a 5 km radius
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': place_type,
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    results = response.json().get('results', [])

    return results

def maped(a):
    print("A:-->")
    # Example usage for Vidhana Soudha
    latitude = places_data[a]["latitude"]
    longitude = places_data[a]["longitude"]

    petrol_pumps = get_nearby_places(latitude,longitude, 'gas_station')
    restaurants = get_nearby_places(latitude,longitude, 'restaurant')

    # Print results for Vidhana Soudha
    print(f"Petrol Pumps near ---> {len(petrol_pumps)} results")
    for result in petrol_pumps:
        location = result['geometry']['location']
        print(result['name'])
        folium.Marker([location['lat'], location['lng']], popup=result['name'], icon=folium.Icon(color='red')).add_to(map_dijkstra)

    print("\n")

    print(f"Restaurants near ---> {len(restaurants)} results")
    for result in restaurants:
        location = result['geometry']['location']
        print(result['name'])
        folium.Marker([location['lat'], location['lng']], popup=result['name'], icon=folium.Icon(color='green')).add_to(map_dijkstra)



    print("___________________________________________________________________________________________________________________________")


if(n==0):
    a=input("enter start : ")
    b=input("enter end : ")
    print(TextStyle.BOLD + TextStyle.RED +TextStyle.UNDERLINE +"FROM ",places_data[a]["name"]," TO ",places_data[b]["name"],":")
    
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {'origin': f"{places_data[a]['latitude']},{places_data[a]['longitude']}",'destination': f"{places_data[b]['latitude']},{places_data[b]['longitude']}",'key': 'AIzaSyD757qcPbrXBXNH6bUYyuQRP4oLS_EeeQE',}
    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()
    # Extract the polyline from the response
    polyline = data['routes'][0]['overview_polyline']['points']
    polyline_points = decode(polyline)
    # Create a Folium map object
    map_dijkstra = folium.Map(location=[places_data[a]["latitude"], places_data[a]["longitude"]], zoom_start=12)
    # Create a list to store the coordinates of the decoded polyline points
    coordinates = []
    location=[places_data[a]["latitude"], places_data[a]["longitude"]]
    location=[places_data[b]["latitude"], places_data[b]["longitude"]]
    # Add the decoded points to the coordinates list
    for point in polyline_points:
        if(a in places_data):
            lat, lon = point
            coordinates.append([lat, lon])
    # Add the polyline to the map
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5,  # Adjust line weight as needed
        opacity=0.8,  # Adjust line opacity as needed
    ).add_to(map_dijkstra)

    folium.Marker([places_data[a]["latitude"],places_data[a]["longitude"]],popup = (places_data[a]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b]["latitude"],places_data[b]["longitude"]],popup = (places_data[b]["name"])).add_to(map_dijkstra )
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[b]["latitude"],places_data[b]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    maped(a)
    maped(b)
    
   
    
#------------------------------------------------------------------------------------------------------------------------------


if(n==1):
    a=input("enter start : ")
    b=input("enter stop 1 : ")
    c=input("enter end : ")
    print(TextStyle.BOLD + TextStyle.RED +TextStyle.UNDERLINE +"FROM ",places_data[a]["name"]," TO ",places_data[c]["name"],":")


    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
    waypoints = '|'.join([f"{places_data[b]['latitude']},{places_data[b]['longitude']}"])

    params = {'origin': f"{places_data[a]['latitude']},{places_data[a]['longitude']}",'destination': f"{places_data[c]['latitude']},{places_data[c]['longitude']}",'waypoints': waypoints,'key': 'AIzaSyD757qcPbrXBXNH6bUYyuQRP4oLS_EeeQE',}
    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()
    # Extract the polyline from the response
    polyline = data['routes'][0]['overview_polyline']['points']
    polyline_points = decode(polyline)
    # Create a Folium map object
    map_dijkstra = folium.Map(location=[places_data[a]["latitude"], places_data[a]["longitude"]], zoom_start=12)
    # Create a list to store the coordinates of the decoded polyline points
    coordinates = []
    # Add the decoded points to the coordinates list
    for point in polyline_points:
        if(b in places_data):
            lat, lon = point
            coordinates.append([lat, lon])
    #print(coordinates)
    # Add the polyline to the map
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5,  # Adjust line weight as needed
        opacity=0.8,  # Adjust line opacity as needed
    ).add_to(map_dijkstra)
    
    folium.Marker([places_data[a]["latitude"],places_data[a]["longitude"]],popup = (places_data[a]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b]["latitude"],places_data[b]["longitude"]],popup = (places_data[b]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[c]["latitude"],places_data[c]["longitude"]],popup = (places_data[c]["name"])).add_to(map_dijkstra )
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[b]["latitude"],places_data[b]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b]["latitude"],places_data[b]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    maped(a)
    maped(b)
    maped(c)

    # Calculate geodesic distance
    origin = [places_data[a]["latitude"], places_data[a]["longitude"]]
    dest = [places_data[c]["latitude"], places_data[c]["longitude"]]
    distance_meters, distance_kilometers, distance_miles = RouteCalculator.calculate_distance(origin, dest)
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5,dash_array='5, 5').add_to( map_dijkstra)
    print("{:.3f} meters".format(distance_meters))
    print("{:.3f} kilometers".format(distance_kilometers))
    print("{:.3f} miles".format(distance_miles))
    
    
#------------------------------------------------------------------------------------------------------------------------------


if(n==2):
    a=input("enter start : ")
    b=input("enter stop 1 : ")
    b1=input("enter stop 2 : ")
    c=input("enter end : ")
    print(TextStyle.BOLD + TextStyle.RED +TextStyle.UNDERLINE +"FROM ",places_data[a]["name"]," TO ",places_data[c]["name"],":")
 
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
    waypoints = f"{places_data[b]['latitude']},{places_data[b]['longitude']}|{places_data[b1]['latitude']},{places_data[b2]['longitude']}"

    params = {'origin': f"{places_data[a]['latitude']},{places_data[a]['longitude']}",'destination': f"{places_data[c]['latitude']},{places_data[c]['longitude']}",'waypoints': waypoints,'key': 'AIzaSyD757qcPbrXBXNH6bUYyuQRP4oLS_EeeQE',}
    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()
    # Extract the polyline from the response
    polyline = data['routes'][0]['overview_polyline']['points']
    polyline_points = decode(polyline)
    # Create a Folium map object
    map_dijkstra = folium.Map(location=[places_data[a]["latitude"], places_data[a]["longitude"]], zoom_start=12)
    # Create a list to store the coordinates of the decoded polyline points
    coordinates = []
    # Add the decoded points to the coordinates list
    for point in polyline_points:
        if(b in places_data):
            lat, lon = point
            coordinates.append([lat, lon])
    #print(coordinates)
    # Add the polyline to the map
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5,  # Adjust line weight as needed
        opacity=0.8,  # Adjust line opacity as needed
    ).add_to(map_dijkstra)
    
    folium.Marker([places_data[a]["latitude"],places_data[a]["longitude"]],popup = (places_data[a]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b]["latitude"],places_data[b]["longitude"]],popup = (places_data[b]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b1]["latitude"],places_data[b1]["longitude"]],popup = (places_data[b1]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[c]["latitude"],places_data[c]["longitude"]],popup = (places_data[c]["name"])).add_to(map_dijkstra )
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[b]["latitude"],places_data[b]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b]["latitude"],places_data[b]["longitude"]]), ([places_data[b1]["latitude"],places_data[b1]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b1]["latitude"],places_data[b1]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    maped(a)
    maped(b)
    maped(b1)
    maped(c)
    
    # Calculate geodesic distance
    origin = [places_data[a]["latitude"], places_data[a]["longitude"]]
    dest = [places_data[c]["latitude"], places_data[c]["longitude"]]
    distance_meters, distance_kilometers, distance_miles = RouteCalculator.calculate_distance(origin, dest)
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5,dash_array='5, 5').add_to( map_dijkstra)
    print("{:.3f} meters".format(distance_meters))
    print("{:.3f} kilometers".format(distance_kilometers))
    print("{:.3f} miles".format(distance_miles))
    
#------------------------------------------------------------------------------------------------------------------------------


if(n==3):
    a=input("enter start : ")
    b=input("enter stop 1 : ")
    b1=input("enter stop 2 : ")
    b2=input("enter stop 3 : ")
    c=input("enter end : ")
    print(TextStyle.BOLD + TextStyle.RED +TextStyle.UNDERLINE +"FROM ",places_data[a]["name"]," TO ",places_data[c]["name"],":")


    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
    waypoints = f"{places_data[b]['latitude']},{places_data[b]['longitude']}|{places_data[b1]['latitude']},{places_data[b2]['longitude']}|{places_data[b3]['latitude']},{places_data[b3]['longitude']}"
    params = {'origin': f"{places_data[a]['latitude']},{places_data[a]['longitude']}",'destination': f"{places_data[c]['latitude']},{places_data[c]['longitude']}",'waypoints': waypoints,'key': 'AIzaSyD757qcPbrXBXNH6bUYyuQRP4oLS_EeeQE',}
    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()
    # Extract the polyline from the response
    polyline = data['routes'][0]['overview_polyline']['points']
    polyline_points = decode(polyline)
    # Create a Folium map object
    map_dijkstra = folium.Map(location=[places_data[a]["latitude"], places_data[a]["longitude"]], zoom_start=12)
    # Create a list to store the coordinates of the decoded polyline points
    coordinates = []
    # Add the decoded points to the coordinates list
    for point in polyline_points:
        if(b in places_data):
            lat, lon = point
            coordinates.append([lat, lon])
    #print(coordinates)
    # Add the polyline to the map
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5,  # Adjust line weight as needed
        opacity=0.8,  # Adjust line opacity as needed
    ).add_to(map_dijkstra)

    folium.Marker([places_data[a]["latitude"],places_data[a]["longitude"]],popup = (places_data[a]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b]["latitude"],places_data[b]["longitude"]],popup = (places_data[b]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b2]["latitude"],places_data[b2]["longitude"]],popup = (places_data[b2]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[b1]["latitude"],places_data[b1]["longitude"]],popup = (places_data[b1]["name"])).add_to(map_dijkstra )
    folium.Marker([places_data[c]["latitude"],places_data[c]["longitude"]],popup = (places_data[c]["name"])).add_to(map_dijkstra )
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[b]["latitude"],places_data[b]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b]["latitude"],places_data[b]["longitude"]]), ([places_data[b1]["latitude"],places_data[b1]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b1]["latitude"],places_data[b1]["longitude"]]), ([places_data[b2]["latitude"],places_data[b2]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    folium.PolyLine(locations = [([places_data[b1]["latitude"],places_data[b1]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5).add_to( map_dijkstra)
    maped(a)
    maped(b)
    maped(b1)
    maped(b2)
    maped(c)
    
    
    # Calculate geodesic distance
    origin = [places_data[a]["latitude"], places_data[a]["longitude"]]
    dest = [places_data[c]["latitude"], places_data[c]["longitude"]]
    distance_meters, distance_kilometers, distance_miles = RouteCalculator.calculate_distance(origin, dest)
    folium.PolyLine(locations = [([places_data[a]["latitude"],places_data[a]["longitude"]]), ([places_data[c]["latitude"],places_data[c]["longitude"]])],
                        line_opacity = 0.5,dash_array='5, 5').add_to( map_dijkstra)
    print("{:.3f} meters".format(distance_meters))
    print("{:.3f} kilometers".format(distance_kilometers))
    print("{:.3f} miles".format(distance_miles))
    
    
map_dijkstra


# # for key, place_info in places_data.items():
#         if(a in places_data):
#             latitude = place_info["latitude"]
#             print(latitude)
#             longitude = place_info["longitude"]
#             print(longitude)
#             coordinates.append([latitude, longitude])
#     # Add the decoded points to the coordinates list
#     for point in polyline_points:
#         if(a in places_data):
#             lat, lon = point
#             coordinates.append([lat, lon])

# In[ ]:




