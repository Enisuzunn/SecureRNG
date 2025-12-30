# 🔐 SecureRNG - Güvenli Rastgele Sayı Üreteci

Kullanıcı seed'i + zaman + sistem rastgeleliği birleştirilerek SHA-256 ile güvenli sayılar üreten Python modülü.

## 📁 Dosya Bilgileri

| Özellik | Değer |
|---------|-------|
| **Dosya Adı** | secure_random_generator.py |
| **Toplam Satır** | 128 |
| **Dil** | Python |
| **Amaç** | Kriptografik güvenli rastgele sayı üreteci |

---

## 🚀 Kullanım

```bash
python secure_random_generator.py
```

Program çalıştırıldığında sizden 4 basamaklı bir seed girmenizi isteyecektir.

### Programatik Kullanım

```python
from secure_random_generator import SecureRandomGenerator

# Üreteci başlat (4 basamaklı seed)
generator = SecureRandomGenerator(1234)

# 32-bit rastgele sayı üret
random_number = generator.generate_32bit()
print(random_number)

# Hex formatında şifre üret
hex_password = generator.generate_hex_string(32)
print(hex_password)
```

---

## 🏗️ Mimari Yapı

### Sınıf: `SecureRandomGenerator`

Güvenli rastgele sayı üretimi için tasarlanmış ana sınıf.

| Metot | Açıklama |
|-------|----------|
| `__init__(user_seed)` | 4 basamaklı seed ile üreteci başlatır |
| `_initialize_state()` | Başlangıç durumunu oluşturur |
| `generate_32bit()` | 32-bit rastgele sayı üretir |
| `generate_hex_string(length)` | Hex formatında şifre üretir |

### Yardımcı Fonksiyonlar

| Fonksiyon | Açıklama |
|-----------|----------|
| `test_avalanche_effect()` | Avalanche etkisini test eder |
| `demo()` | İnteraktif demo çalıştırır |


### ✅ Güçlü Yönler

1. **Çoklu Entropi Kaynakları**
   - Kullanıcı seed'i
   - Nanosaniye hassasiyetinde zaman (`time.time_ns()`)
   - İşletim sistemi rastgeleliği (`os.urandom(16)`)

2. **SHA-256 Hash Kullanımı**
   - Kriptografik olarak güvenli hash fonksiyonu
   - Her iterasyonda durum güncelleniyor

3. **Sayaç Mekanizması**
   - Her üretimde artan sayaç
   - Aynı durumdan farklı çıktılar garantileniyor

4. **Input Validasyonu**
   - Seed değeri 1000-9999 aralığında kontrol ediliyor

## 🧪 Test Kapsamı

**Avalanche Testi:**
- Birbirine yakın seed'lerin çıktılarını karşılaştırır
- Bit farklılık oranını hesaplar
- İdeal değer: ~%50 (iyi bir hash fonksiyonunun göstergesi)

## 🔄 Çalışma Prensibi

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  User Seed  │ +  │  Timestamp  │ +  │  os.urandom │
│  (4 digit)  │    │  (ns)       │    │  (16 bytes) │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                          │
                    ┌─────▼─────┐
                    │  SHA-256  │
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │   State   │◄────┐
                    └─────┬─────┘     │
                          │           │
              ┌───────────▼───────────┐
              │  State + Counter      │
              └───────────┬───────────┘
                          │
                    ┌─────▼─────┐
                    │  SHA-256  │────► Yeni State
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │  Output   │
                    │ (32-bit)  │
                    └───────────┘
```

---

## 📋 Gereksinimler

- Python 3.6+
- Standart kütüphaneler: `hashlib`, `time`, `os`

---