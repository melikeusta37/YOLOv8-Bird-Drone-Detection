# YOLOv8 Bird-Drone Detection Inference Code
# Environment: Google Colab

!pip install ultralytics

from google.colab import files
from google.colab import drive
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

# Google Drive bağlantısı
drive.mount('/content/drive')

# Eğitilmiş model ağırlık dosyası
TRAIN_FOLDER_NAME = 'train2'
MODEL_PATH = f'/content/drive/MyDrive/Drone_vs_Flying_Bird_YOLO_Sonuclari/runs/detect/{TRAIN_FOLDER_NAME}/weights/best.pt'

# Modeli yükleme
print("Model yükleniyor, lütfen bekleyin...")
model = YOLO(MODEL_PATH)

# Test görüntüsü yükleme
print("\nLütfen test etmek istediğiniz fotoğrafı seçin (.jpg, .png vb.):")
uploaded = files.upload()

for filename in uploaded.keys():
    TEST_IMAGE_PATH = os.path.join('/content/', filename)

    print(f"\nİşleniyor: {filename}...")

    # Tahmin işlemi
    results = model.predict(
        source=TEST_IMAGE_PATH,
        conf=0.5,
        save=False
    )

    for r in results:
        # Tespit sonuçlarını yazdırma
        if len(r.boxes) > 0:
            print(f"{len(r.boxes)} adet nesne tespit edildi:")

            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                print(f"- {model.names[cls]} | Güven: %{conf * 100:.2f}")
        else:
            print("Herhangi bir drone veya kuş tespit edilemedi.")

        # Görsel sonucu oluşturma
        im_array = r.plot()
        im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)
       
        plt.figure(figsize=(12, 9))
        plt.imshow(im_rgb)
        plt.title(f"Tahmin Sonucu: {filename}")
        plt.axis('off')
        plt.show()
