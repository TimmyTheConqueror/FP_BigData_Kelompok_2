import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, lit
from pyspark.sql.types import IntegerType
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, Imputer
from pyspark.ml.classification import RandomForestClassifier
import random

def train_and_save():
    """
    Fungsi ini mengambil logika inti dari notebook untuk melatih model
    dan menyimpannya ke disk.
    """
    print("Memulai proses pelatihan model...")

    # 1. Inisialisasi SparkSession
    spark = SparkSession.builder \
        .appName("CHF Model Training") \
        .getOrCreate()

    # 2. Muat Dataset
    try:
        df_ptbxl = spark.read.csv("ptbxl_database.csv", header=True, inferSchema=True)
    except Exception as e:
        print(f"Error: Tidak dapat membaca 'ptbxl_database.csv'. Pastikan file ada di folder backend. Detail: {e}")
        spark.stop()
        return

    print("Dataset berhasil dimuat.")

    # 3. Rekayasa Fitur dan Pelabelan
    # NOTE: Berdasarkan notebook, tidak ada kode SCP untuk 'failure' yang ditemukan di data.
    # Ini menyebabkan dataset yang sangat tidak seimbang (semua label 0).
    # Untuk tujuan demonstrasi agar model fungsional, kita akan SIMULASI beberapa kasus positif.
    
    # Fungsi untuk membuat label simulasi
    def generate_simulated_label(age, weight):
        # Membuat beberapa kasus positif secara acak, terutama pada usia lanjut atau berat badan tinggi
        # Ini adalah penyederhanaan untuk membuat model yang bisa dilatih
        if age is not None and age > 70 and random.random() < 0.25: # 25% kemungkinan CHF jika usia > 70
            return 1
        if weight is not None and weight > 90 and random.random() < 0.20: # 20% kemungkinan CHF jika berat > 90
            return 1
        if random.random() < 0.01: # 1% kemungkinan dasar untuk CHF
             return 1
        return 0

    # Daftarkan UDF
    generate_label_udf = udf(generate_simulated_label, IntegerType())
    
    # Tambahkan kolom label simulasi
    df_with_label = df_ptbxl.withColumn("label", generate_label_udf(col("age"), col("weight")))

    print("Distribusi kelas (dengan data simulasi):")
    df_with_label.groupBy("label").count().show()

    # 4. Prapemrosesan Data untuk Model MLlib
    numerical_cols = ['age', 'height', 'weight']
    categorical_cols = ['sex']
    
    categorical_indexed_cols = [c + "_indexed" for c in categorical_cols]
    categorical_encoded_cols = [c + "_encoded" for c in categorical_cols]

    # Tahap-tahap Pipeline
    imputer = Imputer(inputCols=numerical_cols, outputCols=numerical_cols).setStrategy("mean")
    string_indexer = StringIndexer(inputCols=categorical_cols, outputCols=categorical_indexed_cols, handleInvalid="keep")
    one_hot_encoder = OneHotEncoder(inputCols=categorical_indexed_cols, outputCols=categorical_encoded_cols)
    assembler_inputs = numerical_cols + categorical_encoded_cols
    vector_assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="features")
    rf = RandomForestClassifier(featuresCol="features", labelCol="label", seed=42)

    # Gabungkan semua tahap menjadi satu Pipeline
    pipeline = Pipeline(stages=[imputer, string_indexer, one_hot_encoder, vector_assembler, rf])

    # 5. Latih model
    print("Memulai pelatihan model RandomForest...")
    # Kita latih dengan seluruh data yang berlabel untuk mendapatkan model yang lebih robust
    model = pipeline.fit(df_with_label.filter(col("label").isNotNull()))
    print("Pelatihan model selesai.")

    # 6. Simpan Model
    # Ini akan membuat folder bernama 'chf_spark_model'
    model_path = "chf_spark_model"
    try:
        model.write().overwrite().save(model_path)
        print(f"Model berhasil disimpan di: {model_path}")
    except Exception as e:
        print(f"Error saat menyimpan model: {e}")
    
    # 7. Hentikan SparkSession
    spark.stop()

if __name__ == '__main__':
    train_and_save()