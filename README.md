# 🗑️ Smart Waste Classification System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-AI-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MobileNetV2](https://img.shields.io/badge/Model-MobileNetV2-purple)
![License](https://img.shields.io/badge/License-Educational-yellow)

Sistem klasifikasi sampah berbasis **Artificial Intelligence** menggunakan **Python**, **OpenCV**, **TensorFlow**, dan **MobileNetV2** untuk mendeteksi sampah organik dan non-organik secara realtime melalui webcam.

---

## 🎯 Overview

**Smart Waste Classification System** adalah aplikasi AI sederhana yang dapat:

- 🔍 **Mendeteksi objek** dari webcam secara realtime
- 🧠 **Mengklasifikasikan sampah** menjadi organik dan non-organik
- ⚡ **Menggunakan MobileNetV2 pretrained** tanpa training dataset sendiri
- 🌐 **Memproses gambar realtime** menggunakan OpenCV
- 📊 **Menampilkan hasil prediksi** berupa kategori, objek, dan confidence

---

## 🧠 Metode AI

Project ini menggunakan model **MobileNetV2 pretrained** dari TensorFlow/Keras.

Model MobileNetV2 sudah dilatih sebelumnya menggunakan dataset besar sehingga mampu mengenali berbagai objek umum. Hasil deteksi objek dari MobileNetV2 kemudian dipetakan menjadi dua kategori, yaitu **organik** dan **non-organik** berdasarkan daftar kata kunci.

| Kategori | Contoh Objek |
|---|---|
| Organik | banana, apple, corn, leaf, food |
| Non-Organik | bottle, can, plastic, paper, cardboard |

---

## 🧩 Alur Sistem

```text
Load Model MobileNetV2
        ↓
Aktifkan Webcam
        ↓
Ambil Gambar dari Kamera
        ↓
Crop Area Tengah
        ↓
Preprocessing Gambar
        ↓
Prediksi Objek
        ↓
Mapping ke Organik / Non-Organik
        ↓
Tampilkan Hasil