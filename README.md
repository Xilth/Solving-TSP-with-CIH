# Penyelesaian Traveling Salesman Problem dengan Cheapest Insertion Heuristics
Algoritma pendekatan heuristik untuk menyelesaikan Traveling Salesman Problem (TSP) dengan membangun *tour*. Dalam setiap langkah, algoritma ini menyisipkan kota yang memiliki biaya penyisipan minimum untuk membangun solusi yang tepat dan efisien.

# Spesifikasi Lingkungan
- matplotlib 3.4.3
- pandas 1.5.3
- networkx 3.1
- pyinstaller 6.14.2

## Prasyarat

- Python 3.9.0+
- pip (Versi Python 3.4+ sudah terinstall secara otomatis)
- *Code Editor: Visual Studio Code* (opsional)
- Input data berupa file *.csv*, yang sudah disiapkan dalam bentuk format:
    - Kolom pertama : kota\_asal
    - Kolom kedua   : kota\_tujuan
    - Kolom ketiga  : jarak

Contoh data dapat dilihat pada folder "contoh_kasus".
Versi ini digunakan untuk memastikan hasil dapat direproduksi dengan tepat.
*Code Editor* yang digunakan tidak harus digunakan. Pengembang dapat menggunakan *IDE* atau *text editor* sesuai keinginan.

## Langkah Instalasi Perangkat Lunak:

1. Mengunduh *source code* dari:
    - Berkas *archive* yang telah diberikan dan letakkan isi berkas ke suatu folder yang diinginkan, atau
    - *Clone* repositori menggunakan perintah: ```git clone https://github.com/Xilth/Solving-TSP-with-CIH.git``` pada *powershell*, *bash*, atau terminal lainnya sesuai dengan keinginan.
2. Instal pustaka yang dibutuhkan dengan menjalankan perintah: ```pip install -r pustaka.txt```.
3. Menjalankan perangkat lunak tanpa kompilasi ke file *.exec* menggunakan perintah: ```py main.py```.
4. Menjalankan PyInstaller untuk membuat file *.exec* menggunakan perintah: ```pyinstaller --onefile main.py```

## Catatan Penting:

- Perangkat lunak dapat menyelesaikan masalah TSP pada graf berbobot lengkap (*Completed Weighted Graph*).
- Memasukkan data selain graf tersebut dapat memunculkan jawaban yang tidak sesuai.

## License

Proyek ini dilisensikan di bawah Lisesni MIT. Silahkan liat file [LICENSE](LICENSE) untuk detail lebih lanjutnya.
