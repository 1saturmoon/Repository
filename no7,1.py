import streamlit as st
import random
import networkx as nx
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import json

# Load city data from the JSON file
def load_city_data():
    with open('city_data.json', 'r') as f:
        return json.load(f)

# Function to create and visualize the graph with automatic nodes and edges
def create_graph_and_visualize(num_nodes, num_edges):
    # Create an empty graph
    G = nx.Graph()
    
    # Add nodes
    G.add_nodes_from(range(num_nodes))
    
    # Add edges automatically
    st.write(f"Automatically generating {num_edges} edges...")
    added_edges = 0
    while added_edges < num_edges:
        # Randomly select two distinct nodes
        node1, node2 = random.sample(range(num_nodes), 2)
        
        # Add an edge if it doesn't already exist
        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2)
            added_edges += 1
    
    # Draw the graph using NetworkX and Matplotlib
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_weight='bold')
    plt.title(f"Graph with {num_nodes} Nodes and {num_edges} Edges")
    st.pyplot(plt)

# Function to create a map with connections between cities in West Java
def create_deck_map(province_name):
    if province_name == "West Java":
        # Load city data from JSON
        city_data = load_city_data()

        # Create an edge list from the city connections
        edges = []
        for city, data in city_data.items():
            lat1, lon1 = data["coords"]
            for connected_city in data["connections"]:
                if connected_city in city_data:
                    lat2, lon2 = city_data[connected_city]["coords"]
                    edges.append([lat1, lon1, lat2, lon2])

        # Prepare data for nodes (cities)
        node_data = pd.DataFrame([(city, lat, lon) for city, (lat, lon) in city_data.items()], columns=["City", "Lat", "Lon"])

        # Generate the map
        deck = pdk.Deck(
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    node_data,
                    get_position=["Lon", "Lat"],
                    get_radius=5000,
                    get_fill_color=[0, 255, 255, 140],
                    pickable=True,
                    auto_highlight=True,
                ),
                pdk.Layer(
                    "LineLayer",
                    pd.DataFrame(edges, columns=["Lat1", "Lon1", "Lat2", "Lon2"]),
                    get_source_position=["Lon1", "Lat1"],
                    get_target_position=["Lon2", "Lat2"],
                    get_color=[255, 0, 0, 255],
                    get_width=3,
                ),
            ],
            initial_view_state=pdk.ViewState(latitude=-6.9175, longitude=107.6191, zoom=10, pitch=0),
            map_style="mapbox://styles/mapbox/streets-v11",
        )
        return deck
    else:
        return None

# Streamlit UI
st.title("Aplikasi Multimenu")

# Sidebar menu
menu = st.sidebar.radio("Pilih Menu", ["Profile", "Graph Visualization", "City Map"])

if menu == "Profile":
    st.subheader("Team Members Profile")
    
    # Foto Profil
    st.write("1. **John Doe** - Developer and Data Scientist. Passionate about AI and Machine Learning.")
    st.image("https://github.com/1saturmoon/Repository/blob/main/dila.jpg?raw=true", width=300)  # Gantilah URL ini dengan link foto profil yang valid
    st.write("2. **Jane Smith** - UX/UI Designer. Focused on making user experiences smooth and enjoyable.")
    st.image("https://www.example.com/jane_smith.jpg", width=150)  # Gantilah URL ini dengan link foto profil yang valid
    st.write("3. **Mike Johnson** - Product Manager. Loves solving problems and delivering innovative solutions.")
    st.image("https://www.example.com/mike_johnson.jpg", width=150)  # Gantilah URL ini dengan link foto profil yang valid
    
elif menu == "Graph Visualization":
    st.subheader("Graph Visualizatin: Directed and Undirected")

    # Input for number of nodes and edges
    num_nodes = st.number_input("Enter the number of nodes", min_value=1, value=5)
    num_edges = st.number_input("Enter the number of edges", min_value=1, value=5)

    # Button to create and visualize the graph
    if st.button("Generate Graph"):
        create_graph_and_visualize(num_nodes, num_edges)

elif menu == "City Map":
    province_name = st.selectbox("Pilih Provinsi", ["West Java"])

    if province_name:
        deck = create_deck_map(province_name)
        if deck:
            st.pydeck_chart(deck)
