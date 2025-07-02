from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import pandas as pd
import os
import sys

# Menemukan path python yang sedang menjalankan skrip ini secara otomatis
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# 1. Inisialisasi Aplikasi Flask dan Spark
app = Flask(__name__)

# --- MODIFIKASI PENTING: Konfigurasi CORS yang lebih spesifik ---
# Ini secara eksplisit mengizinkan permintaan dari server frontend Anda
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"]
    }
})

spark = SparkSession.builder.appName("CHF Prediction Server").getOrCreate()

# 2. Muat model yang sudah dilatih
MODEL_PATH = "chf_spark_model"
try:
    prediction_model = PipelineModel.load(MODEL_PATH)
    print(f"Model dari '{MODEL_PATH}' berhasil dimuat.")
except Exception as e:
    print(f"KRITIS: Error memuat model dari '{MODEL_PATH}'. Server tidak dapat melakukan prediksi. Detail: {e}")
    prediction_model = None

# 3. Definisikan API Endpoint
@app.route('/api/v1/predict', methods=['POST'])
def predict():
    """Endpoint untuk menerima data pasien dan mengembalikan prediksi."""
    print("\n--- PERMINTAAN PREDIKSI DITERIMA ---")  # LOG 1

    if not prediction_model:
        print("-> GAGAL: Model tidak dimuat.")  # LOG 2
        return jsonify({"error": "Model tidak tersedia atau gagal dimuat"}), 500

    try:
        data = request.get_json()
        print(f"-> Data diterima dari frontend: {data}")  # LOG 3
        if not all(key in data for key in ['age', 'sex', 'height', 'weight']):
            print("-> GAGAL: Data input tidak lengkap.")  # LOG 4
            return jsonify({"error": "Data input tidak lengkap. Butuh 'age', 'sex', 'height', 'weight'."}), 400
    except Exception as e:
        print(f"-> GAGAL: Error saat parsing JSON dari request: {e}")  # LOG 5
        return jsonify({"error": "Request body harus dalam format JSON."}), 400

    try:
        # Buat Spark DataFrame dari data input
        print("-> Membuat Spark DataFrame...")  # LOG 6
        input_df = spark.createDataFrame([
            (int(data['age']), data['sex'], float(data['height']), float(data['weight']))
        ], ["age", "sex", "height", "weight"])

        # Lakukan prediksi menggunakan pipeline
        print("-> Menjalankan model.transform()...")  # LOG 7
        result_df = prediction_model.transform(input_df)
        
        # Ekstrak hasil
        prediction_result = result_df.select("prediction", "probability").first()
        prediction = int(prediction_result['prediction'])
        probability_vector = prediction_result['probability']
        confidence_score = probability_vector[prediction]

        response = {
            "prediction": prediction,
            "prediction_label": "Risiko CHF Terdeteksi" if prediction == 1 else "Risiko CHF Rendah",
            "probability": confidence_score
        }
        print(f"-> SUKSES: Prediksi selesai. Mengirim hasil: {response}")  # LOG 8
        return jsonify(response)

    except Exception as e:
        print(f"-> KRITIS: Terjadi error saat proses prediksi Spark: {e}")  # LOG 9
        return jsonify({"error": f"Terjadi kesalahan saat melakukan prediksi: {e}"}), 500

# Endpoint statistik tetap sama
@app.route('/api/v1/statistics', methods=['GET'])
def get_stats():
    # ... (kode endpoint statistics tetap sama) ...
    return jsonify({"total_records": 21799, "average_age": 61.8, "chf_cases": 450, "non_chf_cases": 21349})

# 4. Jalankan server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)