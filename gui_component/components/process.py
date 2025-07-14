import tkinter as tk
from tkinter import ttk
from core.cih import TSPsolver
from shared import SharedData

class ProcessComponent:
    def __init__(self, output_component):
        self.output_component = output_component
        self.daftar_tabel = []
        self.daftar_label = []

    def scroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
            
    def create_frame_process(self, frame_utama):
        frame_process = tk.Frame(frame_utama, relief="ridge", bd=2, width=800)
        frame_process.pack(side="right", fill="both", expand=True, padx=8, pady=3)
        tk.Label(frame_process, text="Proses Penyisipan", font=("Arial", 14, "bold")).pack(anchor="w", padx=5, pady=5)
        
        self.canvas = tk.Canvas(frame_process)
        scroll_y = tk.Scrollbar(frame_process, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, width=frame_process.winfo_width())

        frame_process.bind(
            "<Configure>", 
            lambda e: self.scrollable_frame.config(width=e.width, height=e.height)
        )
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.scrollable_frame.bind("<MouseWheel>", self.scroll)
        self.scrollable_frame.bind("<Button-4>", self.scroll)
        self.scrollable_frame.bind("<Button-5>", self.scroll)
        self.canvas.bind("<MouseWheel>", self.scroll)
        self.canvas.bind("<Button-4>", self.scroll)
        self.canvas.bind("<Button-5>", self.scroll)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll_y.set, highlightthickness=0, bd=0)

        self.canvas.pack(anchor="center", side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def add_langkah_process(self, tabel_perhitungan_sekarang, subtour_sekarang, kota_yang_disisipkan):
        format_subtour_sekarang = " | ".join([" - ".join(pasangan_simpul) for pasangan_simpul in subtour_sekarang])
        label_subtour = tk.Label(self.scrollable_frame, text="Subtour sekarang: "+format_subtour_sekarang, font=("Arial", 11, "bold"))
        label_subtour.pack(anchor="center", pady=1)

        label_kandidat = tk.Label(self.scrollable_frame, text="Daftar perhitungan kandidat kota:", font=("Arial", 9, "bold"))
        label_kandidat.pack(anchor="center", pady=(0, 2))
        
        tabel = ttk.Treeview(self.scrollable_frame, columns=("Arc yang diganti", "Arc yang akan ditambah ke subtour", "Costs"), show="headings", takefocus=0)
        col_width = [250, 350, 120]
        for width, col in zip(col_width, tabel["columns"]):
            tabel.heading(col, text=col, anchor="center")
            tabel.column(col, width=width, anchor="center")
        tabel.pack(expand=True, fill="y")

        for _, baris_data in tabel_perhitungan_sekarang.iterrows():
            list_baris_data = baris_data.tolist()
            list_baris_data[0] = " - ".join(list_baris_data[0])
            list_baris_data[1] = "".join(f"({' - '.join(pasangan_simpul)}) " for pasangan_simpul in list_baris_data[1])
            tabel.insert("", "end", values=list_baris_data)

        tabel["height"] = len(tabel.get_children())

        label_kota_terpilih = tk.Label(self.scrollable_frame, text="Kota yang akan disisipkan adalah kota: "+kota_yang_disisipkan, font=("Arial", 11, "bold"))
        label_kota_terpilih.pack(anchor="center", pady=(0, 20))

        label_subtour.bind("<MouseWheel>", self.scroll)
        label_subtour.bind("<Button-4>", self.scroll)
        label_subtour.bind("<Button-5>", self.scroll)
        label_kandidat.bind("<MouseWheel>", self.scroll)
        label_kandidat.bind("<Button-4>", self.scroll)
        label_kandidat.bind("<Button-5>", self.scroll)
        label_kota_terpilih.bind("<MouseWheel>", self.scroll)
        label_kota_terpilih.bind("<Button-4>", self.scroll)
        label_kota_terpilih.bind("<Button-5>", self.scroll)
        tabel.bind("<MouseWheel>", self.scroll)
        tabel.bind("<Button-4>", self.scroll)
        tabel.bind("<Button-5>", self.scroll)
        
        self.daftar_tabel.append(tabel)
        self.daftar_label.append([label_subtour, label_kandidat, label_kota_terpilih])

    def update_process_view(self):
        if self.daftar_label: 
            for label in self.daftar_label:
                label[0].destroy()
                label[1].destroy()
                label[2].destroy()
        if self.daftar_tabel: 
            for tabel in self.daftar_tabel:
                tabel.destroy()
        self.daftar_label.clear()
        self.daftar_tabel.clear()

        for i in range(len(SharedData.tabel_perhitungan)):
            self.add_langkah_process(SharedData.tabel_perhitungan[i], SharedData.subtour_sekarang[i], SharedData.kota_yang_disisipkan[i])

    def run_process(self):
        solver = TSPsolver()
        hasil_penyelesaian = solver.run()
        self.update_process_view()
        SharedData.hasil_penyelesaian = hasil_penyelesaian
        self.output_component.update_output()