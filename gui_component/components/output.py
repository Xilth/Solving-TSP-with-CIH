import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import time
from shared import SharedData
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class OutputComponent:

    def create_frame_output(self, root_gui):
        frame_output = tk.Frame(root_gui, relief="ridge", bd=2, width=800)
        frame_output.pack(fill="both", expand=True, padx=7, pady=7)

        tk.Label(frame_output, text="Output", font=("Arial", 14, "bold")).pack(anchor="w", padx=5, pady=5)
        self.output_label = tk.Label(frame_output, text="HASIL: ", font=("Arial", 12), justify="left")
        self.output_label.pack(anchor="w", padx=5, pady=5)

        self.figure_graf = plt.figure(figsize=(100, 100))

        self.graph_canvas = FigureCanvasTkAgg(self.figure_graf, master=frame_output)
        self.widget_graph_canvas = self.graph_canvas.get_tk_widget()
        self.widget_graph_canvas.pack(fill="both", expand=True)

        frame_output.bind("<Configure>", self.wraptext_update)

    def wraptext_update(self, event):
        self.output_label.config(wraplength=event.width)

    def update_output(self):
        self.figure_graf.clear()
        tour = " - ".join(SharedData.hasil_penyelesaian[0])
        jarak = str(SharedData.hasil_penyelesaian[1])

        bobot_simpul = []
        self.graf = nx.Graph()

        self.graf.add_nodes_from(SharedData.hasil_penyelesaian[0])
        for i in range(len(SharedData.hasil_penyelesaian[0]) - 1):
            bobot_simpul.append((SharedData.hasil_penyelesaian[0][i], SharedData.hasil_penyelesaian[0][i+1], SharedData.bobot_antarsimpul[i]))
        self.graf.add_weighted_edges_from(bobot_simpul)
        label_sisi = nx.get_edge_attributes(self.graf, 'weight')
        layout_graf = nx.spring_layout(self.graf)

        node_colors = ["greenyellow" if node == SharedData.kota_pertama else "lightblue" for node in self.graf.nodes]

        nx.draw(self.graf, layout_graf, 
                with_labels=True,
                node_color=node_colors, 
                node_size=350,
                font_size=12)
        nx.draw_networkx_edge_labels(self.graf, layout_graf, edge_labels=label_sisi, font_size=12)

        self.graph_canvas.draw()
        SharedData.figure_graf = self.figure_graf

        self.output_label.config(text="Ditemukan bahwa tour: "+tour+" merupakan jarak terdekat dengan total jarak tempuh: "+jarak)
        end_time = time.perf_counter()
        print("Waktu dari User menekan tombol SOLVE: ", end_time - SharedData.start_time)