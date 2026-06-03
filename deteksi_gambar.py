import sys
import os
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from tensorflow.keras.preprocessing import image

ORGANIK_KEYWORDS = [
    "banana", "apple", "orange", "lemon", "strawberry", "pineapple",
    "broccoli", "carrot", "cucumber", "cabbage", "cauliflower",
    "mushroom", "corn", "ear", "acorn", "fig", "pomegranate",
    "hay", "leaf", "tree", "plant", "flower", "wood", "food"
]

NON_ORGANIK_KEYWORDS = [
    "bottle", "water_bottle", "wine_bottle", "beer_bottle",
    "can", "soda_can", "plastic", "packet", "carton", "cardboard",
    "paper", "cup", "glass", "jar", "container", "spoon", "fork",
    "knife", "straw", "metal", "box"
]

def tentukan_kategori(label):
    label_lower = label.lower()

    for key in ORGANIK_KEYWORDS:
        if key in label_lower:
            return "Organik", "Buang ke tempat sampah hijau / dapat dibuat kompos."

    for key in NON_ORGANIK_KEYWORDS:
        if key in label_lower:
            return "Non-Organik", "Buang ke tempat sampah kuning/biru / dapat didaur ulang."

    return "Non-Organik", "Objek tidak ada di daftar organik, dikategorikan non-organik."

def deteksi_gambar(path):
    if not os.path.exists(path):
        print("File gambar tidak ditemukan:", path)
        return

    print("Memuat model AI MobileNetV2...")
    model = MobileNetV2(weights="imagenet")

    img = image.load_img(path, target_size=(224, 224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    preds = model.predict(arr, verbose=0)
    results = decode_predictions(preds, top=3)[0]

    print("\n=== HASIL DETEKSI ===")
    for i, (_, label, score) in enumerate(results, start=1):
        print(f"{i}. {label} - {score*100:.2f}%")

    top_label = results[0][1]
    top_score = results[0][2] * 100

    kategori, rekomendasi = tentukan_kategori(top_label)

    print("\n=== KLASIFIKASI SAMPAH ===")
    print("Objek terdeteksi :", top_label)
    print("Confidence       :", f"{top_score:.2f}%")
    print("Kategori         :", kategori)
    print("Rekomendasi      :", rekomendasi)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai:")
        print("python deteksi_gambar.py nama_file_gambar.jpg")
    else:
        deteksi_gambar(sys.argv[1])
