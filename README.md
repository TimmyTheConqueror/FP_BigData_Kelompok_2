# 🩺 Dashboard Analisis & Prediksi Gagal Jantung (CHF) dengan PySpark

<p align="center">
  <a href="https://youtu.be/oDVLVuaJwcY">
    <img src="LINK_LANGSUNG_KE_GAMBAR_THUMBNAIL_ANDA.png" alt="Demonstrasi Proyek Dashboard CHF" width="800"/>
  </a>
</p>
<p align="center">
  <em>Klik pada gambar di atas untuk menonton demonstrasi lengkap proyek kami di YouTube!</em>
</p>

Selamat datang di proyek Dashboard Analisis dan Prediksi Gagal Jantung Kongestif (CHF)! Proyek ini adalah sebuah studi kasus *end-to-end* yang kami bangun untuk mendemonstrasikan bagaimana teknologi Big Data seperti **Apache Spark** dapat dimanfaatkan untuk memproses data medis berskala besar, melatih model *machine learning*, dan menyajikannya dalam sebuah aplikasi web yang interaktif dan mudah digunakan.

Dashboard ini tidak hanya menampilkan statistik dari dataset EKG **PTB-XL** yang terkenal, tetapi juga menyediakan fitur prediksi *real-time* untuk mengklasifikasikan risiko CHF pada pasien berdasarkan data demografis sederhana.

---

## ✨ Fitur Utama

* **Prediksi Real-time**: Masukkan data demografis pasien (usia, jenis kelamin, tinggi, berat) dan dapatkan prediksi risiko Gagal Jantung secara langsung dari model Machine Learning yang telah kami latih.
* **Dashboard Statistik Agregat**: Visualisasikan ringkasan data dari ribuan rekaman EKG, termasuk total kasus, distribusi kelas (CHF vs. Non-CHF), dan demografi pasien melalui grafik yang interaktif.
* **Visualisasi Sinyal EKG**: Unggah folder rekaman yang telah diubah menjadi citra `.png` untuk melihat visualisasi dari sinyal Elektrokardiogram 12-lead.
* **Arsitektur Terpisah (Decoupled)**: Demonstrasi arsitektur modern dengan backend (Flask & PySpark) yang menangani pemrosesan data berat dan frontend (HTML & JavaScript) yang ringan untuk interaksi pengguna.

---

## ⚙️ Teknologi yang Digunakan

Proyek ini kami bangun menggunakan kombinasi teknologi untuk pemrosesan data, machine learning, dan pengembangan web.

| Kategori | Teknologi |
| --- | --- |
| **Data Processing & ML** | Apache Spark, PySpark, Spark MLlib, Pandas |
| **Backend API** | Flask, Flask-CORS |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript (ES6), Chart.js, DataTables.js |
| **Lingkungan** | Python 3.10+, Java JDK 17, Hadoop WinUtils (untuk Windows) |

---

## 🧗 Tantangan dan Pembelajaran

Dalam pengembangan proyek ini, beberapa tantangan teknis menjadi peluang pembelajaran yang berharga bagi kami:

1.  **Menangani *Imbalanced Dataset***: Dataset medis sering kali tidak seimbang. Dataset PTB-XL memiliki kasus Non-CHF yang jauh lebih banyak daripada kasus CHF. Proyek ini mendemonstrasikan pentingnya mengenali masalah ini dan menerapkan teknik (seperti simulasi data dalam skrip pelatihan) untuk menciptakan model yang fungsional.

2.  **Konfigurasi Lingkungan Spark di Windows**: Menjalankan Spark di Windows memerlukan konfigurasi yang cermat, termasuk pengaturan variabel lingkungan seperti `JAVA_HOME`, `HADOOP_HOME`, dan penggunaan `winutils.exe`. Proyek ini adalah contoh nyata dari proses *debugging* untuk membuat ekosistem Java dan Python bekerja secara harmonis.

3.  **Komunikasi Frontend-Backend (CORS)**: Mengintegrasikan frontend yang berjalan di satu server dengan backend di server lain memunculkan masalah klasik Cross-Origin Resource Sharing (CORS). Proyek ini mengimplementasikan solusi standar industri dengan menyajikan frontend dari server lokal dan mengonfigurasi backend untuk menerima permintaan secara eksplisit.

---

## 📂 Struktur Proyek

Berikut adalah struktur folder utama dari proyek ini.

```
/proyek-chf/
├── backend/
│   ├── app.py                      # Server API Flask untuk prediksi & statistik
│   ├── train_and_save_model.py     # Skrip untuk melatih & menyimpan model (dijalankan sekali)
│   ├── convert_to_png.py           # Skrip utilitas untuk konversi sinyal ke citra
│   ├── dashboard.html              # File utama frontend
│   ├── requirements.txt            # Daftar library Python yang dibutuhkan
│   │
│   ├── ptbxl_database.csv          # Dataset fitur (diperlukan)
│   ├── scp_statements.csv          # Dataset deskripsi (diperlukan)
│   │
│   └── /chf_spark_model/           # Folder ini dibuat setelah train_and_save_model.py dijalankan
│
└── ... (file lainnya)
```

---

## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer lokal.

### **1. Prasyarat**

* **Python**: Versi 3.10 atau lebih baru.
* **Java**: **JDK versi 17**. Pastikan `JAVA_HOME` environment variable sudah diatur.
* **Git**: Untuk meng-kloning repositori.

### **2. Kloning Repositori**

```bash
git clone [https://link-ke-repositori-github-anda.git](https://link-ke-repositori-github-anda.git)
cd nama-folder-proyek
```

### **3. Pengaturan Lingkungan Python**

```bash
# Pindah ke direktori utama proyek
cd backend

# Buat virtual environment (direkomendasikan)
python -m venv venv

# Aktifkan virtual environment
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate

# Install semua library yang dibutuhkan
pip install -r requirements.txt
```

### **4. Konfigurasi Khusus untuk Pengguna Windows**

Ini adalah langkah paling penting untuk menjalankan Spark di Windows.
* **Atur `HADOOP_HOME`**:
    1.  Unduh `winutils.exe` untuk Hadoop 3.x dari [repositori ini](https://github.com/cdarlint/winutils).
    2.  Buat folder `C:\hadoop\bin`.
    3.  Letakkan `winutils.exe` di dalam `C:\hadoop\bin`.
    4.  Atur environment variable `HADOOP_HOME` ke `C:\hadoop`.
* Pastikan `JAVA_HOME` sudah menunjuk ke direktori instalasi **JDK 17**.

### **5. Langkah-langkah Menjalankan Aplikasi**

Anda perlu membuka **dua jendela terminal** yang terpisah.

**Di Terminal 1 (Untuk Backend):**
1.  Pastikan Anda berada di dalam folder `backend` dan virtual environment sudah aktif.
2.  **Latih Model (Hanya dilakukan sekali):** Jalankan skrip ini untuk membuat file model.
    ```bash
    python train_and_save_model.py
    ```
    Tunggu hingga selesai dan folder `chf_spark_model` dibuat.
3.  **Jalankan Server Backend:**
    ```bash
    python app.py
    ```
    Biarkan terminal ini terbuka. Server API kami sekarang berjalan di `http://127.0.0.1:5000`.

**Di Terminal 2 (Untuk Frontend):**
1.  Buka terminal baru, pindah ke folder `backend` yang sama, dan aktifkan virtual environment.
2.  **Jalankan Server Web Sederhana:**
    ```bash
    python -m http.server 8080
    ```
    Biarkan terminal ini juga terbuka.

### **6. Akses Dashboard**

Buka browser web Anda dan kunjungi alamat:

**`http://localhost:8080/dashboard.html`**

Sekarang Anda dapat berinteraksi dengan semua fitur dashboard secara penuh!

---

## 🤝 Kontribusi

Kontribusi, isu, dan permintaan fitur sangat kami terima! Jangan ragu untuk membuat *fork* dari repositori ini dan membuat *pull request* Anda.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.
