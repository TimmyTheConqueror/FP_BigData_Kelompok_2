import os
import matplotlib.pyplot as plt
import wfdb
import sys

def convert_folder_to_png(base_directory):
    """
    Mencari semua file .hea di dalam direktori dan subdirektorinya,
    lalu membuat citra PNG dari data EKG yang sesuai.
    """
    # Validasi apakah direktori ada
    if not os.path.isdir(base_directory):
        print(f"Error: Direktori '{base_directory}' tidak ditemukan.")
        return

    print(f"Memulai pemindaian di direktori: {base_directory}")
    file_ditemukan = False
    
    # Berjalan melalui semua folder dan file di dalam base_directory
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.hea'):
                file_ditemukan = True
                record_path_without_ext = os.path.join(root, os.path.splitext(file)[0])
                png_output_path = record_path_without_ext + '.png'

                # Cek apakah file PNG sudah ada untuk menghindari pemrosesan ulang
                if os.path.exists(png_output_path):
                    print(f"Skipping: {png_output_path} sudah ada.")
                    continue

                print(f"Memproses: {record_path_without_ext} -> Membuat citra...")

                try:
                    # Baca data sinyal EKG
                    record = wfdb.rdrecord(record_path_without_ext)
                    signals = record.p_signal
                    leads = record.sig_name

                    # Buat plot
                    fig, axs = plt.subplots(4, 3, figsize=(15, 12))
                    fig.suptitle(f'ECG: {os.path.basename(record_path_without_ext)}', fontsize=16)
                    axs = axs.flatten()

                    for i, lead_name in enumerate(leads):
                        if i < len(axs):
                            ax = axs[i]
                            signal_data = signals[:, i]
                            ax.plot(signal_data)
                            ax.set_title(lead_name)
                            ax.set_xticks([])
                            ax.set_yticks([])
                            ax.grid(True, linestyle='--', alpha=0.6)

                    for i in range(len(leads), len(axs)):
                        axs[i].set_visible(False)
                    
                    plt.tight_layout(rect=[0, 0, 1, 0.96])
                    
                    # Simpan plot sebagai file PNG
                    plt.savefig(png_output_path)
                    plt.close(fig) # Penting untuk melepaskan memori

                except Exception as e:
                    print(f"  -> Gagal memproses {record_path_without_ext}. Error: {e}")

    if not file_ditemukan:
        print("Tidak ada file .hea yang ditemukan di dalam direktori yang diberikan.")
    else:
        print("\nKonversi selesai.")


if __name__ == '__main__':
    # Ambil nama folder dari argumen command line
    # Contoh penggunaan: python convert_to_png.py /path/to/records100/01000
    if len(sys.argv) < 2:
        print("Penggunaan: python convert_to_png.py <path_ke_folder_rekaman>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    convert_folder_to_png(folder_path)