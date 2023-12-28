# import io
#
# import PIL
# import networkx as nx
# import matplotlib.pyplot as plt
# from typing import List

import io
# import PIL
import networkx as nx
import matplotlib.pyplot as plt
from typing import List


def visualize_network(lst_connections: List, lst_devices: List) -> object:
    G = nx.MultiDiGraph()
    edge_labels = {}
    for connection in lst_connections:
        # src_type = connection["srcType"]
        # dst_type = connection["dstType"]
        source_mac = connection["src_mac"]
        destination_mac = connection["dst_mac"]
        G.add_edge(source_mac, destination_mac)
        # G.nodes[source_mac]['label'] = source_mac, src_type
        # G.nodes[destination_mac]['label'] = destination_mac, dst_type
        # G.nodes[destination_mac]['color'] = "red" if dst_type=="Router" else "blue"
        # G.nodes[source_mac]['color'] = "red" if src_type=="Router" else "blue"# Set color attribute
        # edge_labels[(source_mac, destination_mac)] = "protocol"

        key = (source_mac, destination_mac)

        if key in edge_labels:
            edge_labels[key].add(connection["protocol"])
        else:
            edge_labels[key] = {connection["protocol"]}

    # Draw nodes with labels
    node_labels = nx.get_node_attributes(G, 'label')
    node_colors = [G.nodes[node]['color'] if 'color' in G.nodes[node] else 'skyblue' for node in G.nodes()]
    pos = nx.circular_layout(G)

    nx.draw_networkx(G, pos, labels=node_labels, with_labels=True, node_size=3000, font_size=9, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=8)
    plt.axis('off')
    plt.show()
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()  # Clear the plot
    return buffer