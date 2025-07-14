import tkinter as tk
import pandas as pd
import time
from tkinter import ttk, filedialog
from shared import SharedData

class InputComponent:
    def __init__(self, process_component):
        self.opsi_sekarang = tk.StringVar(value="Daftar Nama Kota")
        self.process_component = process_component

    def create_tabel_input(self, frame_input):
        tabel = ttk.Treeview(frame_input, columns=("Kota Asal", "Kota Tujuan", "Jarak"), show="headings", height=10)
        for col in tabel["columns"]:
            if col == "Jarak": tabel.column(col, width=75)
            else: tabel.column(col, width=120)
            tabel.heading(col, text=col)
        return tabel
    
    def update_tabel(self, data_jarak):
        self.tabel.delete(*self.tabel.get_children())
        for _, row in data_jarak.iterrows():
            self.tabel.insert("", "end", values=row.tolist())

    def unggah_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("File CSV", "*.csv")])
        if file_path:
            data_jarak = pd.read_csv(file_path, names=["Kota Asal", "Kota Tujuan", "Jarak"], skiprows=1)
            SharedData.data_jarak = data_jarak
            self.update_tabel(data_jarak)
            self.set_daftar_nama_kota(data_jarak)
            self.update_dropdown_option()

    def set_daftar_nama_kota(self, data_jarak):
        self.daftar_nama_kota = list(dict.fromkeys(data_jarak["Kota Asal"].tolist()+data_jarak["Kota Tujuan"].tolist()))

    def update_dropdown_option(self):
        dropdown_baru = self.dropdown["menu"]
        dropdown_baru.delete(0, "end")

        for opsi in self.daftar_nama_kota:
            dropdown_baru.add_command(label=opsi, command=lambda value=opsi: self.opsi_sekarang.set(value))
        if self.daftar_nama_kota:
            self.opsi_sekarang.set(self.daftar_nama_kota[0])
        else:
            self.opsi_sekarang.set("No Data")

    def reset_process_shared_data(self):
        SharedData.subtour_sekarang = []
        SharedData.unvisited_kota = []
        SharedData.tabel_perhitungan = []
        SharedData.kota_yang_disisipkan = []
        
        SharedData.bobot_antarsimpul = []
        SharedData.hasil_penyelesaian = []

    def create_frame_input(self, frame_utama):
        frame_input = tk.Frame(frame_utama, relief="ridge", bd=2, width=400)
        frame_input.pack(side="left", fill="y", padx=8, pady=3)
        tk.Label(frame_input, text="Input", font=("Arial", 14, "bold")).pack(anchor="w", padx=5, pady=5)

        tombol_unggah = tk.Button(frame_input, text="Upload Data Jarak Antarkota", font=("Arial", 12, "bold"), bd=6, command=self.unggah_csv)
        tombol_unggah.pack(anchor="w", padx=5, pady=5)

        self.tabel = self.create_tabel_input(frame_input)
        self.tabel.pack(padx=5, pady=5)

        tk.Label(frame_input, text="Masukkan Kota Pertama").pack(side="left", padx=(0, 5))
        
        self.dropdown = ttk.OptionMenu(frame_input, self.opsi_sekarang, "")
        self.dropdown.pack(side="left")

        tombol_solve = tk.Button(frame_input, text="SOLVE", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.solve)
        tombol_solve.pack(anchor="w", padx=5, pady=10)

    def solve(self):
        SharedData.start_time = time.perf_counter()
        self.reset_process_shared_data()
        SharedData.kota_pertama = self.opsi_sekarang.get()
        self.process_component.run_process()