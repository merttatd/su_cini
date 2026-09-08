# Su Cini inceleme ve düzeltme raporu

Projenin tüm 10 Python uygulama modülü ve bağımlılık dosyası incelendi.

## Düzeltilen sorunlar

- Günlük sayaçlar artık uygulamayı yeniden başlatmadan, istatistik okunurken veya yeni işlem kaydedilirken gün değişimine uyum sağlar. Geçmiş korunur.
- Ayar ve sayaç türleri yükleme sırasında doğrulanır. Bozuk JSON veya UTF-8 içeriği `.json.corrupt` dosyasında korunur. Geçersiz tarih değerleri su kaydını çökertmez.
- Kayıtlar geçici dosya, diske yazma ve atomik dosya değiştirme ile yapılır. Yazma başarısız olursa bellekteki değişiklik geri alınır ve hata kullanıcıya bildirilir.
- Su içme ve erteleme, bekleyen tam ekran hatırlatmasını iptal eder. Normal kontrol döngüsü 25 saniyelik dönüş beklemesini atlamaz. Manuel erteleme de beş dakika sonunda çalışır.
- Yeni mesaj eski otomatik kapanma zamanlayıcısını iptal eder ve düğmeleri yeniden etkinleştirir. Görünen pencere her mesajda yeniden konumlandırılmaz.
- Gizlenen damlanın sürekli animasyonu durur. Menü yenilenirken eski menü serbest bırakılır; hatırlatma aralıkları birbirini dışlayan seçeneklerdir.
- Windows API çağrılarına açık 64 bit uyumlu parametre ve dönüş türleri eklendi. Monitör yapısı her kontrolde tekrar oluşturulmaz.
- Hedef seçicide ilk değer sınırlandırılır; tek sayılı hedeflerde yarı-hedef mesajı doğru eşikte gösterilir. Uzun hatırlatmalar için pencere yüksekliği içeriğe uyarlanır.
- Modal hedef penceresi açıkken otomatik hatırlatma ve saklanma gösterimi bekler. Küçük ekranlarda saklanan karakterin dikey konumu düzeltildi.
- Başlangıç ve Qt olay hataları konsol çıktısına ek olarak bir hata penceresiyle bildirilir.

## Doğrulama

`test_regressions.py` veri, zamanlama, Qt pencere yaşam döngüsü, menü ve başlangıç senaryolarını kapsar. Testler geçici dosyalar kullanır; kullanıcının gerçek su kayıtlarını değiştirmez. Qt arayüz testleri `offscreen` platformunda çalışır.

Normal Python kurulumu ile:

```powershell
python -m pip install -r requirements.txt
python -m unittest -v test_regressions
python main.py
```

Bu çalışma ortamında PyQt6 yalnızca `.test-deps` klasörüne kuruldu; sistem Python kurulumu değiştirilmedi. Python komutu PATH üzerinde mevcut değildi, kontroller ortamın Python 3.12 yorumlayıcısıyla yapıldı.

## Doğrulamanın sınırları

Gerçek oyun/tam ekran geçişleri, çoklu monitör ve farklı DPI ölçekleri masaüstünde elle denenmedi. Windows API imzaları ve hatırlatma durum geçişleri otomatik test edildi. Birden fazla uygulama örneğinin aynı veri dosyasını eşzamanlı değiştirmesi için süreçler arası kilit mevcut değil. Windows dışındaki platformlarda tam ekran algılama mevcut tasarım gereği devre dışıdır.
