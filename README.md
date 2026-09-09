# 💧 Su Cini

**Masaüstündeki küçük su molası arkadaşın.**

Su Cini, bilgisayar başında su içmeyi hatırlatan bir Windows masaüstü uygulamasıdır. Sistem tepsisinde çalışır; Türkçe mesajları, hareketli damla karakteri ve hedef kutlamalarıyla su molalarına eşlik eder.

## ✨ Özellikler

- **Kişisel hedef:** 6, 8, 10 veya 12 bardaklık hazır seçeneklerden birini kullanın ya da 1–30 bardak arasında kendi hedefinizi seçin.
- **Bardak miktarı:** Bir bardağı 50–1000 ml arasında ayarlayın; ilerlemenizi bardak ve mililitre olarak görün.
- **Esnek hatırlatmalar:** 5–120 dakika arasında, beşer dakika artan 24 aralık seçeneği.
- **Beş dakika erteleme:** Uygun olmadığınızda hatırlatmayı erteleyin.
- **Tam ekran algılama:** Windows'ta tam ekran uygulaması algılandığında otomatik hatırlatmayı bekletir.
- **Öpücüklü kutlama:** Hedef tamamlandığında Su Cini ekranın ortasına gelir, kalplerle öpücük gönderir ve yerine döner.
- **Yeni hedef turları:** Tamamlanan hedefin ardından aynı hedefi tekrarlayın veya yeni bir hedef seçin.
- **Saklambaç:** Su Cini sağdan, soldan, tepeden ya da görev çubuğunun üstünden göz atar.
- **İlerlemeyi sıfırlama:** Bugünkü sayaçları menüden onay vererek sıfırlayın.
- **Yerel kayıt:** Hesap açmadan kullanın; ayarlar ve kayıtlar bilgisayarınızda saklanır.

## 🚀 Başlatma

### Hazır Windows paketiyle

Elinizde taşınabilir Windows paketi varsa ZIP dosyasının tamamını bir klasöre çıkartıp `SuCini.exe` dosyasını çalıştırın. Python kurmanız gerekmez.

**EXE dosyasını tek başına taşımayın.** Yanındaki `_internal` klasörü ve diğer paket dosyaları aynı yerde kalmalıdır.

Kurulum paketi kullanıyorsanız kurulumdan sonra Su Cini'yi oluşturulan kısayoldan açabilirsiniz.

### Kaynak koddan

Windows'ta Python **3.11 veya üzeri, 64 bit** kurulu olmalıdır. Projeyi GitHub'dan indirin veya klonlayın, ardından proje klasöründeki PowerShell terminalinde çalıştırın:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

`py` komutu bulunamıyorsa ilk komutta `python` kullanabilirsiniz. Bağımlılıklar proje içindeki sanal ortama kurulur; ortamı ayrıca etkinleştirmek gerekmez.

Terminal penceresi olmadan başlatmak için:

```powershell
Start-Process -FilePath ".\.venv\Scripts\pythonw.exe" -ArgumentList "main.py"
```

Kaynak koddan çalıştırırken tüm `.py` dosyalarını ve `assets` klasörünü birlikte tutun. Özellikle `app_resources.py`, `celebration_effect.py` ve `goal_cycle_dialog.py` uygulamanın parçasıdır.

## 🎯 İlk kullanım

1. Açılış ekranından bardak hedefinizi belirleyin.
2. Bir bardağın kaç mililitre olduğunu seçin.
3. **Bugünkü görevi başlat** düğmesine basın.
4. Sistem tepsisindeki damla simgesinden hatırlatma aralığını ayarlayın.

Hedef seçme ekranının sağ üstündeki **×** düğmesi uygulamayı tamamen kapatır. Henüz onaylanmamış hedef değişiklikleri kaydedilmez.

Hatırlatma geldiğinde **💧 Su içtim** düğmesi bir bardak kaydeder; **5 dk ertele** hatırlatmayı erteler. Normal hatırlatma penceresini sürükleyerek taşıyabilirsiniz.

## 💕 Hedef tamamlandığında

Su Cini bulunduğu monitörün ortasına yumuşakça süzülür. Yolculuk sırasında konuşma balonu, ilerleme yazısı ve düğmeler kaybolur; ortada yalnızca karakter ve yükselen kalpler görünür. Gözlerini kapatıp öpücük gönderdikten sonra eski yerine döner, yazılar ve düğmeler yeniden görünür olur.

Gidiş ve dönüş yaklaşık **1,6 saniye**, öpücük bölümü **2,4 saniye** sürer.

Hedefe ulaşıldığında bardak ve mililitre sayaçları **yeni tur için otomatik sıfırlanır**. Kutlama tamamlandıktan sonra iki seçenek sunulur:

- **↻ Aynı hedefi tekrarla:** Mevcut hedef ve bardak miktarıyla yeni tura başlar.
- **✦ Yeni bir hedef seç:** Hedef ve bardak miktarı ayarlarını açar.

Her tamamlanan turda yeniden kutlama yapılabilir. Su içme kayıtları geçmişte tutulur; ekrandaki bardak ve mililitre değerleri, tamamlanan turların gün boyu toplamı yerine **mevcut turun ilerlemesini** gösterir. Otomatik hatırlatmalar devam eder.

## 👀 Su Cini nereye saklandı?

Su Cini bazen kendiliğinden ekran kenarından göz atar. Sistem tepsisindeki **Su Cini nereye saklandı?** seçeneğiyle de bu davranışı tetikleyebilirsiniz.

- Sağ veya sol kenardan kısmen görünür.
- Tepeden baş aşağı bakar.
- Görev çubuğunun üstünden hafifçe yükselir.

Fare imlecinin bulunduğu monitörü kullanır. Konum rastgele seçilir ve aynı kenar art arda gelmez. Fareyle yaklaşınca geldiği yöne geri kaçar; yaklaşmazsanız kısa süre sonra kendiliğinden saklanır.

Tam ekran uygulaması veya görünür hatırlatma penceresi varken saklanma gösterimi bekletilir.

## 🖱️ Sistem tepsisi menüsü

Damla simgesi görünmüyorsa görev çubuğundaki gizli simgeler bölümünü kontrol edin. Simgeye sağ tıklayarak menüyü açabilirsiniz.

| Seçenek | İşlev |
| --- | --- |
| Su Cinini göster | Hatırlatma penceresini açar. |
| Şimdi su içtim | Ayarlanan miktarda bir bardak kaydeder. |
| Günlük hedefi değiştir | Hedefi ve bardak miktarını düzenler. |
| Hatırlatma aralığı | 5–120 dakika arasında bir aralık seçtirir. |
| Bugünkü ilerlemeyi göster | Mevcut turun bardak, hedef ve mililitre bilgisini gösterir. |
| Bugünkü ilerlemeyi sıfırla | Onayınızla bugünkü sayaçları sıfırlar; hedef ve bardak miktarı korunur. |
| Su Cini nereye saklandı? | Uygun olduğunda ekran kenarı animasyonunu gösterir. |
| Çıkış | Uygulamayı tamamen kapatır. |

## 💾 Kayıtlar nasıl çalışır?

- Her **Su içtim** işlemi bir bardak sayılır. Kısa aralıklarla tekrar basmak kaydı engellemez; farklı bir mesaj gösterilebilir.
- Programı kapatıp açmak, tamamlanmamış turun kayıtlarını silmez.
- Hedefi değiştirmek mevcut kayıtları sıfırlamaz. Test kayıtlarını temizlemek için **Bugünkü ilerlemeyi sıfırla** seçeneğini kullanın.
- Bardak miktarını değiştirmek önceki kayıtların mililitre değerini değiştirmez; yeni miktar sonraki kayıtlara uygulanır.
- Gün değiştiğinde günlük sayaçlar yenilenir; hedef ve bardak miktarı ayarları korunur.
- Tek bir kaydı geri alma özelliği bulunmaz.

### Verilerin konumu

Kaynak koddan veya normal Windows EXE'sinden çalıştırıldığında ana kayıt dosyası:

```text
%USERPROFILE%\AppData\Roaming\SuCini\data.json
```

Dosyada ayarlar, sayaçlar ve son 2000 işlem tutulur. Son su içme zamanı ayrıca Qt'nin yerel ayar deposunda `MertApps / Su Cini` adıyla saklanır. MSIX kurulumu altında Windows'un uygulama verisi yönlendirmesi nedeniyle fiziksel konum farklı olabilir.

Uygulama hesap açmanızı istemez ve su kayıtlarınızı bir sunucuya göndermez. Yedeklemek için uygulamayı kapatıp veri dosyasını kopyalayabilirsiniz. Okunamayan veri dosyasıyla karşılaşılırsa mevcut değilse `data.json.corrupt` kopyası korunur.

## 🛠️ Sorun giderme

**Program açılmıyor veya `No module named PyQt6` hatası çıkıyor.**

Kaynak koddan çalıştırırken yukarıdaki `.venv` kurulum ve başlatma komutlarını kullanın. Hazır EXE paketinde ise arşivin tamamını çıkarttığınızdan emin olun.

**`No module named app_resources` veya başka bir proje modülü hatası çıkıyor.**

Kaynak dosyalar eksik olabilir. Yalnızca `main.py` dosyasını kopyalamayın; projenin tamamını indirin ve `assets` klasörünü koruyun.

**Programı yeniden başlatınca eski bardak sayısı görünüyor.**

Kayıtların korunması normaldir. Temiz bir tur başlatmak için tepsi menüsündeki **Bugünkü ilerlemeyi sıfırla** seçeneğini kullanın.

**Hedef tamamlandıktan sonra sayaç sıfır oldu.**

Bu sürümde hedef tamamlanınca yeni tur başlar. Kutlamanın ardından aynı hedefi tekrarlayabilir veya yeni hedef seçebilirsiniz.

**Pencere kayboldu ama program hâlâ çalışıyor.**

Su Cini sistem tepsisinde çalışmaya devam eder. Tamamen kapatmak için **Çıkış** seçeneğini kullanın.

**Hatırlatma hemen görünmüyor.**

Seçili aralığın dolması gerekir. Erteleme, açık hedef/hatırlatma penceresi veya tam ekran uygulaması otomatik gösterimi bekletebilir. Kontroller periyodik olduğu için birkaç saniyelik gecikme normaldir.

**Saklanma animasyonunu göremiyorum.**

Tam ekran uygulamasından çıkın ve açık hatırlatma penceresinin kapanmasını bekleyin. Birden fazla monitörünüz varsa fare imlecinin bulunduğu monitörün kenarlarına bakın.

## 🧪 Geliştirme ve testler

Uygulama Python ve PyQt6 ile geliştirilmiştir. Animasyonlar Qt ile çalışır; damla ve kalpler kodla çizilir.

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v test_regressions
```

Testler geçici veriler ve görünmez Qt pencereleri kullanır. Gerçek masaüstünde tam ekran geçişleri, çoklu monitör, farklı DPI ölçekleri ve paketli uygulamanın kurulumu ayrıca doğrulanmalıdır.

## 📦 Windows build ve Microsoft Store

Güncel kaynak paketindeki `build_store.bat`, ayrı bir `.build-venv` ortamı hazırlayıp PyInstaller ile Windows x64 build oluşturur:

```powershell
.\build_store.bat
```

**Bu komut önceki `build`, `dist` ve `release` klasörlerini temizler.** Saklamak istediğiniz eski dağıtımları çalıştırmadan önce başka bir konuma alın.

Çıktı `dist\SuCini\SuCini.exe` dosyasıdır. Dağıtırken `dist\SuCini` klasörünün tamamını kullanın. Inno Setup 6 standart konumda kuruluysa kurulum paketi de oluşturulur.

MSIX paketleme, Partner Center kimlikleri ve Store gönderimi için [Microsoft Store yayınlama rehberine](STORE_RELEASE_GUIDE.md) bakın. EXE build alınmış olması, uygulamanın Microsoft Store'da yayımlandığı anlamına gelmez.

## 💬 Hata bildirimi

GitHub üzerinden hata bildirirken Windows sürümünüzü, kullandığınız paketi veya çalıştırma komutunu, sorunu oluşturan adımları ve varsa hata metnini ekleyin.

Uygulama Windows kullanımına odaklanır. Diğer platformlarda tam ekran algılama devre dışıdır. Aynı anda tek bir uygulama örneği çalıştırın; Windows açılışında otomatik başlatma mevcut değildir.
