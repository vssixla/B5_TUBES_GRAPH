# GUDANG TERBAKAR (MST) — KELOMPOK 5B

**MATEMATIKA DISKRIT LANJUT (2026)**  
D4 Teknik Informatika · Kelas 2B · Kelompok 5 
Anggota Kelompok:
1. Alfina Azizah Anggrhaeni (251524034)
2. Alia Ardani (251524035)
3. Nazwa Rizqika Azzahra (251524060)
4. Shahnaz Saskia Putri (251524062)

Website simulasi rekonstruksi MST pada jaringan komunikasi sistem deteksi
kebakaran gudang. Kruskal dan Prim diimplementasikan sendiri dalam **Python**.
HTML, CSS, dan JavaScript digunakan untuk dashboard dan animasi.

## Menjalankan website

Ekstrak ZIP ke folder baru. Buka terminal di folder `matdis-sota-starterkit`, lalu:

```bash
python app.py
```

Buka **http://127.0.0.1:8000**. Gunakan `python3 app.py` jika nama perintah Python
di komputer kalian adalah `python3`. Dibutuhkan **Python 3.10+**, tanpa paket
eksternal. Tidak perlu `pip install` atau Node.js untuk menjalankan website.
Jika port sedang dipakai, gunakan `python app.py --port 8080`.
Hentikan server dengan `Ctrl+C`. Jangan membuka HTML langsung melalui explorer.

## Struktur proyek

```text
matdis-sota-starterkit/
├── README.md
├── TUTORIAL.md
├── GLOSSARY.md
├── CASESS.md
├── KODE_LENGKAP.md
├── requirements.txt
├── app.py
├── package.json                    # Preview opsional
├── config/
│   ├── __init__.py
│   └── settings.py                 # Path, port, parameter benchmark
├── core/
│   ├── __init__.py
│   ├── base_algorithm.py           # Abstract class dan semantic logger
│   ├── graph_model.py              # Node, Edge, SpatialGraphModel
│   ├── simulation_runner.py        # Orkestrasi, snapshot, timer
│   ├── simulation_observers.py     # Konsol dan ekspor trace JSON
│   └── analysis.py                 # Konektivitas dan validasi MST/MSF
├── cases/
│   ├── __init__.py
│   ├── scenario_loader.py
│   └── scenarios/
│       └── case_26_gudang_terbakar/
│           ├── scenario.json
│           ├── nodes.csv
│           └── edges.csv
├── algorithms/
│   ├── __init__.py
│   ├── registry.py
│   └── mst/
│       ├── __init__.py
│       ├── kruskal.py
│       ├── prim.py
│       └── union_find.py
├── static/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── graph.js
│   ├── denah.png
│   └── assets/audio/apiapi_saleh.mp3
├── tests/
│   ├── test_mst.py
│   ├── test_scenario_loader.py
│   └── test_simulation_runner.py
└── scripts/
    ├── __init__.py
    ├── run_simulation.py
    └── run_benchmark.py
```

Struktur mengikuti bagian relevan starterkit dosen. Visualizer adalah SVG pada
website, sehingga Matplotlib tidak diperlukan. Model graf tidak bergantung pada
NetworkX: implementasi algoritma dapat dipelajari langsung. Skenario memakai
manifest JSON dan CSV agar tidak membutuhkan PyYAML. Tidak ada Dijkstra atau
27 kasus lain karena proyek ini khusus kasus gudang terbakar dengan MST.
Ini adalah adaptasi struktur, bukan salinan kontrak framework dosen yang belum
dilampirkan kode sumbernya.

## Fitur dashboard revisi

- Tema kuning/oranye pastel, identitas KELOMPOK 5B, judul dan footer sesuai revisi.
- 29 node dan 70 edge awal, posisi tetap mengikuti CSV.
- Dua animasi berdampingan; dapat menampilkan Kruskal atau Prim saja.
- Play, Pause, langkah berikutnya, kecepatan, dan Selesaikan.
- Pilih edge dari graf/daftar; pemutusan manual atau acak bersifat kumulatif.
- Hasil tiap algoritma dilengkapi **Edge yang Terhubung**.
- Bagian bawah hanya CATATAN SIMULASI, Riwayat Iterasi, tabel, dan tombol ekspor/
  hapus riwayat. Panel detail, penjelasan hasil, dan tab delay/komponen dihapus.
- Alarm memakai audio dari lampiran **APIAPI_SALEH.mp4**, dikonversi menjadi MP3
  dan disertakan lokal. Alarm diputar sekali setiap pemutusan, tidak berulang
  otomatis. Reset atau menonaktifkan Suara alarm menghentikan pemutaran.

Daftar `E01 → E02 → ...` pada **Edge yang Terhubung** mengikuti urutan edge
diterima oleh algoritma. **Daftar tersebut bukan satu jalur antar-node.** MST
merupakan pohon bercabang. Urutan Kruskal dan Prim dapat berbeda.

Metrik rinci dan analisis jalur masih dihitung backend untuk ekspor dan validasi,
tetapi tidak ditampilkan sebagai tab tambahan. Penjelasan akademik ditempatkan
di dokumentasi agar dashboard berfokus pada proses MST.

## Cara menggunakan

1. Klik **Bangun MST awal**.
2. Amati proses, atau klik **Selesaikan** untuk melihat hasil akhir.
3. Pilih ID edge, lalu **Putus edge**. **Acak** memilih satu edge aktif.
4. Kedua algoritma menerima daftar kerusakan yang sama dan menghitung ulang.
5. Ulangi. Ketika tidak terhubung, status menjadi MSF dan node terputus berwarna
   oranye. Kolom total MST serta perubahannya menampilkan tanda `—`.
6. **Ekspor CSV** untuk menyimpan riwayat; **Reset graf** mengaktifkan seluruh
   edge kembali dan memulai sesi baru. Riwayat terdahulu tetap tersimpan.

Riwayat menggunakan penyimpanan browser. Refresh memulai graf awal/sesi baru
dan mempertahankan riwayat selesai. Hasil diurutkan per sesi dan iterasi.
Pemutusan dinonaktifkan selama animasi. Reset membatalkan animasi yang belum
selesai; iterasi yang dibatalkan tidak dicatat.

## Model dan batas interpretasi

Graf tidak berarah berbobot dengan edge paralel (**multigraph**). Dataset
memiliki 70 edge dan 65 pasangan endpoint unik. E15/E63, E19/E62, E21/E59,
E46/E61, E54/E69 adalah sambungan independen; ID tidak digabung.

N01 adalah pusat jaringan. Tiap vertex merepresentasikan perangkat dengan modul
komunikasi yang diasumsikan mendukung penerusan data. Kerusakan hanya pada edge;
29 node tetap ada. Kolom `edge_type` adalah metadata, bukan prioritas MST.
Program memilih dari edge yang tersedia; tidak membuat kabel baru setelah putus.
Koordinat merupakan posisi visual, bukan dasar perhitungan delay.

MST meminimalkan jumlah bobot edge, bukan waktu perjalanan tercepat setiap
sensor ke pusat. Penurunan bobot MSF ketika jaringan terputus bukan peningkatan
efisiensi MST. Konektivitas pusat menghitung N01 sendiri.

Untuk graf terhubung, MST memiliki 28 edge. Jika terdapat k komponen, MSF
memiliki 29-k edge. Selisih bobot dihitung terhadap MST awal 54,5 ms; persentase
adalah `(Wt-W0)/W0*100%`. Saat terputus, selisih dan persentase menjadi null.

Kruskal memakai Union-Find dan pengurutan edge: O(E log E). Prim memakai lazy
min-heap: O(V + E log E). Tie-break memakai ID edge. Keduanya dihitung ulang
dari awal pada setiap snapshot. Ini bukan algoritma dynamic MST inkremental.

Benchmark memakai pemanasan, 15 batch × 30 eksekusi, dan median waktu per
eksekusi; urutan algoritma bergantian. Waktu tidak mencakup animasi, HTTP,
analisis jalur, dan pencatatan trace. Parameter berada di `config/settings.py`.
Animasi dimulai bersama, sedangkan pengukuran Python dilakukan berurutan pada
input yang sama. Graf kecil dapat menghasilkan waktu yang bervariasi.

Posisi node tetap, dengan garis melengkung untuk membedakan edge paralel dan
menghindari node lain. Perpotongan antargaris mungkin terjadi dan bukan node
baru. Tombol zoom/fit dan tampilan satu algoritma membantu keterbacaan.

## Pengujian

```bash
python -m unittest discover -s tests -v
```

Pengujian mencakup oracle brute-force, urutan kerusakan lengkap, optimalitas,
edge paralel, sensor terisolasi, reset, loader skenario, registry, dan ekspor
observer. Panduan CLI/benchmark tersedia di `TUTORIAL.md`.

Keluaran referensi: kondisi awal 28 edge, total 54,5 ms untuk kedua algoritma.
Putus E28, E29, E38 secara berurutan untuk mengisolasi N02: akhir 2 komponen,
27 edge forest, total MSF 53 ms. Semua hasil tetap menggunakan 29 node.

Program untuk demonstrasi lokal dan pemodelan akademik, bukan rancangan
instalasi keselamatan atau layanan internet produksi.
