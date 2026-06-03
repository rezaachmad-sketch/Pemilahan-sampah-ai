import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from tensorflow.keras.preprocessing import image

# ============================================================
# DETEKSI SAMPAH PYTHON - MOBILENETV2
# Tanpa training dataset sendiri.
# Model langsung memakai MobileNetV2 pretrained ImageNet.
# ============================================================

ORGANIK_KEYWORDS = [
    "banana", "apple", "orange", "lemon", "strawberry", "pineapple",
    "broccoli", "carrot", "cucumber", "cabbage", "cauliflower",
    "mushroom", "corn", "ear", "acorn", "fig", "pomegranate",
    "custard_apple", "jackfruit", "artichoke", "zucchini",
    "spaghetti_squash", "butternut_squash",
    "hay", "leaf", "tree", "plant", "flower", "pot",
    "wood", "eggnog", "meat", "food"
]

NON_ORGANIK_KEYWORDS = [
    "bottle", "water_bottle", "wine_bottle", "beer_bottle",
    "can", "soda_can", "tin", "plastic", "plastic_bag",
    "packet", "carton", "cardboard", "paper", "envelope",
    "cup", "mug", "glass", "jar", "container",
    "spoon", "fork", "knife", "straw",
    "remote_control", "cellular_telephone", "laptop", "keyboard",
    "metal", "bucket", "box"
]


def tentukan_kategori(label):
    label_lower = label.lower()

    for key in ORGANIK_KEYWORDS:
        if key in label_lower:
            return "Organik", (0, 255, 0), "Buang ke tempat sampah hijau / bisa dibuat kompos."

    for key in NON_ORGANIK_KEYWORDS:
        if key in label_lower:
            return "Non-Organik", (0, 165, 255), "Buang ke tempat sampah kuning/biru / dapat didaur ulang."

    return "Non-Organik", (0, 165, 255), "Objek tidak ada di daftar organik, dikategorikan non-organik."


def prediksi_frame(model, frame):
    # Ambil area tengah agar background tidak terlalu memengaruhi
    h, w, _ = frame.shape
    size = min(h, w)
    x1 = (w - size) // 2
    y1 = (h - size) // 2
    crop = frame[y1:y1 + size, x1:x1 + size]

    # OpenCV BGR -> RGB
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    # Resize sesuai MobileNetV2
    img = cv2.resize(rgb, (224, 224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    preds = model.predict(arr, verbose=0)
    hasil = decode_predictions(preds, top=3)[0]

    top_label = hasil[0][1]
    top_score = hasil[0][2] * 100

    kategori, warna, rekomendasi = tentukan_kategori(top_label)

    return kategori, warna, rekomendasi, top_label, top_score, (x1, y1, size)


def main():
    print("Memuat model AI MobileNetV2...")
    print("Jika pertama kali dijalankan, proses ini bisa agak lama karena download model.")
    model = MobileNetV2(weights="imagenet")
    print("Model siap.")

    camera = cv2.VideoCapture(1)

    # Biar kamera lebih lebar
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        print("Webcam tidak bisa dibuka.")
        return

    print("Webcam aktif. Tekan Q untuk keluar.")

    WINDOW_NAME = "AI Klasifikasi Sampah - Python"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1366, 768)

    last_kategori = "Menunggu..."
    last_label = "-"
    last_score = 0
    last_warna = (255, 255, 255)
    last_rekomendasi = "Arahkan objek sampah ke kamera."

    counter = 0
    interval = 15  # prediksi tiap 15 frame agar tidak berat

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Frame kamera tidak terbaca.")
            break

        counter += 1

        if counter % interval == 0:
            try:
                kategori, warna, rekomendasi, label, score, crop_data = prediksi_frame(model, frame)
                last_kategori = kategori
                last_label = label
                last_score = score
                last_warna = warna
                last_rekomendasi = rekomendasi
                x1, y1, size = crop_data
            except Exception as e:
                print("Error prediksi:", e)
                h, w, _ = frame.shape
                size = min(h, w)
                x1 = (w - size) // 2
                y1 = (h - size) // 2
        else:
            h, w, _ = frame.shape
            size = min(h, w)
            x1 = (w - size) // 2
            y1 = (h - size) // 2

        # Kotak area yang dianalisis
        cv2.rectangle(frame, (x1, y1), (x1 + size, y1 + size), last_warna, 2)

        teks_utama = f"{last_kategori} ({last_score:.2f}%)"
        teks_objek = f"Objek: {last_label}"

        cv2.putText(
            frame, teks_utama, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, last_warna, 2
        )

        cv2.putText(
            frame, teks_objek, (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, last_warna, 2
        )

        cv2.putText(
            frame, "Tekan Q untuk keluar", (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )

        # Resize tampilan agar jendela besar
        frame_full = cv2.resize(frame, (1366, 768))
        cv2.imshow(WINDOW_NAME, frame_full)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
