# GPU'yu kontrol et (T4 GPU'nuzun etkin olduğundan emin olun)
!nvidia-smi

# Ultralytics (YOLOv8) kurulumu
!pip install ultralytics

# Gerekli kütüphaneleri içe aktarma
import os
from google.colab import drive

# Google Drive'ı /content/drive klasörüne bağla
drive.mount('/content/drive')

# Bu yol, içinde images/ ve labels/ klasörlerini barındıran ana klasör olmalıdır.
ROOT_DIR = '/content/drive/MyDrive/Drone_vs_Flying_Bird'

# ----------------------------------------------------------------------
# 1. data.yaml dosyasını oluşturma ve kaydetme
# ----------------------------------------------------------------------
print(f"Veri seti ana yolu: {ROOT_DIR}")

yaml_content = f"""
# path, images ve labels klasörlerini {ROOT_DIR} altından bulacaktır.
path: {ROOT_DIR}
train: images/train
val: images/val
nc: 2
names: ['drone', 'bird'] # Sınıf indekslerinizle (0:drone, 1:bird) eşleştiğinden emin olun.
"""

# data.yaml dosyasını Colab'ın çalışma klasöründe oluşturma
with open('data.yaml', 'w') as f:
    f.write(yaml_content)

# data.yaml dosyasını Drive'a kaydetme (kalıcı olması için)
drive_yaml_path = os.path.join(ROOT_DIR, 'data.yaml')
!cp data.yaml {drive_yaml_path}

print("✅ Kurulum, bağlantı ve data.yaml hazırlığı tamamlandı.")


# 1. Eğitimi Başlatma
print("Eğitim başlatılıyor...")
!yolo task=detect mode=train model=yolov8s.pt data=data.yaml epochs=50 imgsz=640 batch=16

# 2. Sonuçları Kaydetme (Eğitim Bittikten Sonra Çalışır)
print("\nEğitim tamamlandı. Sonuçlar Drive'a kopyalanıyor...")

# Sonuçlar klasörünün yolu (YOLO buraya kaydeder)
results_path = '/content/runs'

# Drive'da kaydedileceği klasörün yolu (Kendi Drive'ınızdaki yeni bir klasör)
drive_save_path = '/content/drive/MyDrive/Drone_vs_Flying_Bird_YOLO_Sonuclari'

# Sonuçları Drive'a kopyalama
!cp -r {results_path} {drive_save_path}

print(f"✅ Eğitim bitti ve sonuçlar Drive'a kopyalandı: {drive_save_path}")
