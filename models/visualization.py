import networkx as nx
import matplotlib.pyplot as plt
import json

# Sample query result (replace this with your actual query result)
query_result = [
    {
        "Mac": "00:dd:ee:ff:00:11",
        "IP": "192.168.1.5",
        "ID": 5,
        "Vendor": "Dell",
        "SourceMac": "00:ee:ff:00:11:22",
        "DestMac": "00:ff:00:11:22:33",
        "Length": 500,
    },
    {
        "Mac": "00:ff:00:11:22:33",
        "IP": "192.168.1.6",
        "ID": 6,
        "Vendor": "Oracle",
        "SourceMac": "00:ff:00:11:22:33",
        "DestMac": "00:dd:ee:ff:00:11",
        "Length": 600,
    },
]

import networkx as nx
import matplotlib.pyplot as plt
import io
import base64


def draw(connection_data):
    # Create a graph
    G = nx.Graph()
    # Add nodes for each device
    # Add edges for each connection between devices
    for connection in connection_data:
        G.add_node(connection["Mac"], IP=connection["IP"], ID=connection["ID"], Vendor=connection["Vendor"])
        G.add_edge(connection["SourceMac"], connection["DestMac"], Protocol="Protocol",
                   Length=connection["Length"])
    # Plot the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    # Draw devices
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, font_size=8)
    # Draw connections
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1)
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, "Protocol")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    plt.title("Connections between Devices")
    plt.axis("off")
    plt.show()

draw(query_result)