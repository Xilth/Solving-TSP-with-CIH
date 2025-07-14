from shared import SharedData
import pandas as pd
import math
import time

class TSPsolver:
    def __init__(self):
        self.start_time = time.perf_counter()
        self.inf = math.inf
        self.data_jarak = SharedData.data_jarak
        self.daftar_nama_kota = self.get_daftar_nama_kota()
        self.jarak_antarkota = pd.DataFrame(0, index=self.daftar_nama_kota, columns=self.daftar_nama_kota)
        self.kota_pertama = SharedData.kota_pertama
        self.kandidat_kota = ""
        self.arc = []
        self.tour = []
        self.end_time = 0

    def create_kandidat_subtour(self, indeks):
        self.kandidat_subtour = self.subtour.copy()
        self.kandidat_subtour[indeks] = [self.arc[0], self.kandidat_kota]
        self.kandidat_subtour.insert(indeks+1, [self.kandidat_kota, self.arc[1]])

    def create_matriks_jarak_antarkota(self):
        for _, row in self.data_jarak.iterrows():
            self.jarak_antarkota.at[row["Kota Asal"], row["Kota Tujuan"]] = row["Jarak"]
            self.jarak_antarkota.at[row["Kota Tujuan"], row["Kota Asal"]] = row["Jarak"]

    def create_tour(self):
        self.tour = [self.subtour[0][0]]
        for arc in self.subtour:
            self.tour.append(arc[1])

    def reset_data(self, data):
        if isinstance(data, pd.DataFrame):
            data.drop(data.index, inplace=True)
        elif isinstance(data, int):
            return 0
        else: data.clear()

    def get_arc_baru(self, indeks):
        self.create_kandidat_subtour(indeks)
        return [pasangan_arc for pasangan_arc in self.kandidat_subtour if pasangan_arc not in self.subtour]

    def get_kota_terakhir(self):
        kota_terakhir = ""
        jarak_terdekat = self.inf
        for jarak_kota in self.jarak_antarkota[self.kota_pertama]:
            if jarak_kota != 0:
                if (jarak_terdekat > jarak_kota):
                    jarak_terdekat = jarak_kota
                    indeks_kota_terakhir = self.jarak_antarkota[self.kota_pertama].values.tolist().index(jarak_terdekat)
                    kota_terakhir = self.daftar_nama_kota[indeks_kota_terakhir]
        return kota_terakhir

    def get_minimum_cost_index(self, tabel_perhitungan):
        min_cost = self.inf
        min_index = -1
        daftar_cost = tabel_perhitungan["Cost"].tolist()
        for i in range(len(daftar_cost)):
            cost = daftar_cost[i]
            if (min_cost > cost):
                min_cost = cost
                min_index = i
        return min_index

    def get_daftar_nama_kota(self):
        return list(dict.fromkeys(self.data_jarak["Kota Asal"].tolist()+self.data_jarak["Kota Tujuan"].tolist()))

    def get_total_jarak_tempuh(self):
        jarak_tempuh = 0
        for i in range(len(self.tour)-1):
            jarak_kota_ke_kota = self.jarak_antarkota[self.tour[i]][self.tour[i+1]]
            SharedData.bobot_antarsimpul.append(jarak_kota_ke_kota)
            jarak_tempuh += jarak_kota_ke_kota
        return jarak_tempuh

    def calculate_cost(self):
        return ( self.jarak_antarkota[self.arc[0]][self.kandidat_kota] + 
                self.jarak_antarkota[self.arc[1]][self.kandidat_kota] - 
                self.jarak_antarkota[self.arc[0]][self.arc[1]] )

    def set_subtour(self):
        self.subtour = [[self.kota_pertama, self.kota_terakhir], [self.kota_terakhir, self.kota_pertama]]

    def update_subtour(self, tabel_perhitungan, minimum_cost_index):
        matriks_tabel_perhitungan = tabel_perhitungan.values.tolist()
        arc_lama = matriks_tabel_perhitungan[minimum_cost_index][0]
        indeks_arc_yang_diganti = self.subtour.index(arc_lama)
        self.subtour.pop(indeks_arc_yang_diganti)
        daftar_substitusi_arc = matriks_tabel_perhitungan[minimum_cost_index][1]
        SharedData.kota_yang_disisipkan.append(daftar_substitusi_arc[0][1])
        for substitusi_arc in reversed(daftar_substitusi_arc):
            self.subtour.insert(indeks_arc_yang_diganti, substitusi_arc)

    def cih(self):
        indeks = 0
        arcs = []
        arcs_baru = []
        costs = []
        while self.unvisited_kota:
            self.kandidat_kota = self.unvisited_kota[indeks]
            for i in range(len(self.subtour)):
                self.arc = self.subtour[i].copy()
                arc_baru = self.get_arc_baru(i)
                cost = self.calculate_cost()
                arcs.append(self.arc)
                arcs_baru.append(arc_baru)
                costs.append(cost)

            indeks += 1
            if indeks == len(self.unvisited_kota): 
                tabel_perhitungan = pd.DataFrame({"Arc yang diganti":arcs, 
                                                  "Arc yang akan ditambah ke subtour":arcs_baru, 
                                                  "Cost": costs})

                minimum_cost_index = self.get_minimum_cost_index(tabel_perhitungan)
                SharedData.tabel_perhitungan.append(tabel_perhitungan.copy())

                self.update_subtour(tabel_perhitungan, minimum_cost_index)
                pass_subtour_sekarang = self.subtour.copy()
                SharedData.subtour_sekarang.append(pass_subtour_sekarang)

                self.unvisited_kota.remove(arcs_baru[minimum_cost_index][0][1])
                SharedData.unvisited_kota.append(self.unvisited_kota)

                indeks = self.reset_data(indeks)
                self.reset_data(arcs)
                self.reset_data(arcs_baru)
                self.reset_data(costs)
                self.reset_data(tabel_perhitungan)

    def run(self):
        self.create_matriks_jarak_antarkota()
        self.kota_terakhir = self.get_kota_terakhir()
        self.set_subtour()
        pass_subtour_sekarang = self.subtour.copy()
        SharedData.subtour_sekarang.append(pass_subtour_sekarang)
        self.unvisited_kota = [nama_kota for nama_kota in self.daftar_nama_kota if nama_kota not in self.subtour[0]]
        SharedData.unvisited_kota.append(self.unvisited_kota)
        self.cih()
        self.create_tour()
        total_jarak_tempuh = self.get_total_jarak_tempuh()
        end_time = time.perf_counter()
        print("Waktu untuk CIH membuat solusi: ", end_time - self.start_time)
        return [self.tour, total_jarak_tempuh]