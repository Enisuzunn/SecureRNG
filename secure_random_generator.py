"""
Güvenli Rastgele Sayı Üreteci
=============================
Kullanıcı seed'i + zaman + sistem rastgeleliği birleştirilerek
SHA-256 ile güvenli sayılar üretilir.
"""

import hashlib
import time
import os


class SecureRandomGenerator:
    """Güvenli rastgele sayı üreteci."""
    
    def __init__(self, user_seed: int):
        """
        Üreteci başlat.
        
        Args:
            user_seed: 4 basamaklı sayı (1000-9999)
        """
        if not (1000 <= user_seed <= 9999):
            raise ValueError("Seed 4 basamaklı olmalı (1000-9999)")
        
        self.user_seed = user_seed
        self.counter = 0
        self.state = self._initialize_state()
    
    def _initialize_state(self) -> bytes:
        """Başlangıç durumunu oluştur."""
        # 3 farklı kaynak birleştir
        combined = f"{self.user_seed}{time.time_ns()}{os.urandom(16).hex()}"
        return hashlib.sha256(combined.encode()).digest()
    
    def generate_32bit(self) -> int:
        """32-bit rastgele sayı üret."""
        # Mevcut durum + sayaç birleştir
        data = self.state + self.counter.to_bytes(8, 'big')
        
        # SHA-256 uygula
        self.state = hashlib.sha256(data).digest()
        self.counter += 1
        
        # İlk 4 byte'ı sayıya çevir
        return int.from_bytes(self.state[:4], 'big')
    
    def generate_hex_string(self, length: int = 32) -> str:
        """Hex formatında rastgele şifre üret."""
        result = ''
        while len(result) < length:
            random_int = self.generate_32bit()
            result += f'{random_int:08x}'
        return result[:length]


def test_avalanche_effect(seed1: int, seed2: int, iterations: int = 5):
    """Avalanche etkisini test et."""
    print("\n" + "="*60)
    print("AVALANCHE ETKİSİ TESTİ")
    print("="*60)
    print(f"Seed 1: {seed1}")
    print(f"Seed 2: {seed2}")
    print(f"Fark: {abs(seed1 - seed2)}")
    print("-"*60)
    
    gen1 = SecureRandomGenerator(seed1)
    gen2 = SecureRandomGenerator(seed2)
    
    total_diff_bits = 0
    
    for i in range(iterations):
        val1 = gen1.generate_32bit()
        val2 = gen2.generate_32bit()
        
        diff = val1 ^ val2
        diff_bits = bin(diff).count('1')
        total_diff_bits += diff_bits
        
        print(f"Iterasyon {i+1}:")
        print(f"  Değer 1: {val1:032b} ({val1})")
        print(f"  Değer 2: {val2:032b} ({val2})")
        print(f"  Farklı bit: {diff_bits}/32 ({diff_bits/32*100:.1f}%)")
    
    avg_diff = total_diff_bits / iterations
    print("-"*60)
    print(f"Ortalama farklı bit: {avg_diff:.1f}/32 ({avg_diff/32*100:.1f}%)")
    print("(İdeal değer: ~%50)")


def demo():
    """Üreteci demonstre et."""
    print("="*60)
    print("KRİPTOGRAFİK GÜVENLİ RASTGELE SAYI ÜRETECİ")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n4 basamaklı bir sayı girin (1000-9999): ")
            seed = int(user_input)
            if 1000 <= seed <= 9999:
                break
            print("Hata: 1000-9999 arasında bir sayı girin!")
        except ValueError:
            print("Hata: Geçerli bir sayı girin!")
    
    generator = SecureRandomGenerator(seed)
    
    print("\n" + "-"*60)
    print("ÜRETİLEN DEĞERLER:")
    print("-"*60)
    
    print("\n32-bit Rastgele Sayılar:")
    for i in range(5):
        value = generator.generate_32bit()
        print(f"  {i+1}. {value:>10} (0x{value:08X})")
    
    print("\n32 Karakterlik Hex Şifreler:")
    for i in range(3):
        hex_str = generator.generate_hex_string(32)
        print(f"  {i+1}. {hex_str}")
    
    test_avalanche_effect(seed, seed + 1)


if __name__ == "__main__":
    demo()
