# 💧 Su Cini

Su Cini, bilgisayar başında su içmeyi hatırlatan küçük bir masaüstü uygulamasıdır. Sistem tepsisinde çalışır; hareketli bir damla karakteri ve Türkçe mesajlarla su molalarını hatırlatır, içtiğiniz bardakları kaydeder ve günlük hedefinizi takip eder.

## Özellikler

- **Günlük hedef:** Hazır seçeneklerden birini seçin veya 1–30 bardak arasında kendi hedefinizi belirleyin.
- **Bardak miktarı:** Bir bardağı 50–1000 ml arasında ayarlayın. İlerlemenizi hem bardak hem mililitre olarak görün.
- **Ayarlanabilir hatırlatmalar:** Sistem tepsisinden 30, 45, 60, 90 veya 120 dakikalık aralık seçin.
- **Beş dakika erteleme:** Uygun olmadığınızda hatırlatmayı erteleyin.
- **Tam ekran algılama:** Windows'ta tam ekran uygulaması algılandığında otomatik hatırlatma bekletilir. Tam ekrandan çıkıldıktan sonra kısa bir beklemeyle gösterilir.
- **Hareketli karakter:** Su Cini, ilerlemenize ve ertelemelerinize göre farklı ifadeler ve mesajlar gösterir. Zaman zaman ekranın sağ kenarından göz atar.
- **Yerel kayıt:** Günlük ilerlemeniz ve ayarlarınız bilgisayarınızda saklanır.

## Gereksinimler

- Python **3.10 veya üzeri**
- PyQt6 — kurulum sırasında `requirements.txt` üzerinden yüklenir.
- Sistem tepsisi destekleyen bir masaüstü ortamı

Windows kullanımı esas alınmıştır. Diğer platformlarda tam ekran algılama devre dışıdır; bu platformlar ayrıca doğrulanmamıştır.

## Kurulum

1. Bu GitHub sayfasındaki **Code → Download ZIP** seçeneğiyle projeyi indirin ve arşivi bir klasöre çıkartın. İsterseniz Git ile de klonlayabilirsiniz.
2. Python kurulu değilse [python.org](https://www.python.org/downloads/) üzerinden kurun. Windows kurulumunda **Add Python to PATH** seçeneğini işaretleyin.
3. Proje klasöründe bir terminal açın ve şu komutları çalıştırın:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Bu komutlar bağımlılıkları proje içindeki ayrı bir Python ortamına kurar. Ortamı etkinleştirmeniz gerekmez.

> Windows'ta `python` komutu bulunamıyorsa ilk komutta `python` yerine `py` kullanmayı deneyin.

## Başlatma

Proje klasöründe:

```powershell
.\.venv\Scripts\python.exe main.py
```

Açılışta günlük hedef ve bardak miktarı seçimi gösterilir. **Bugünkü görevi başlat** düğmesine bastığınızda uygulama sistem tepsisinde çalışmaya devam eder.

Kurulumdan sonra terminal penceresi olmadan başlatmak için:

```powershell
Start-Process -FilePath ".\.venv\Scripts\pythonw.exe" -ArgumentList "main.py"
```

Uygulama Windows açılışına otomatik olarak eklenmez; kullanmak istediğinizde başlatmanız gerekir. Aynı anda tek bir örneğini çalıştırın.

## Kullanım

Hatırlatma penceresindeki **💧 Su içtim** düğmesi, ayarladığınız miktarda bir bardak su kaydeder. **5 dk ertele** düğmesi hatırlatmayı beş dakika erteler. Pencereyi sürükleyerek yerini değiştirebilirsiniz.

Görev çubuğunun bildirim alanındaki damla simgesine sağ tıklayarak aşağıdaki işlemlere ulaşabilirsiniz. Simge görünmüyorsa gizli simgeler bölümünü kontrol edin.

| Menü seçeneği | İşlevi |
| --- | --- |
| Su Cinini göster | Hatırlatma penceresini açar. |
| Şimdi su içtim | Ayarlanan bardak miktarı kadar su kaydeder. |
| Günlük hedefi değiştir | Hedefi ve bardak miktarını düzenler. |
| Hatırlatma aralığı | Otomatik hatırlatma sıklığını değiştirir. |
| Bugünkü ilerlemeyi göster | Bardak sayısını, hedefi ve toplam miktarı gösterir. |
| Su Cini nereye saklandı? | Uygun olduğunda ekran kenarındaki karakteri gösterir. |
| Çıkış | Uygulamayı tamamen kapatır. |

### Kayıt ve hatırlatma davranışı

- Her **Su içtim** işlemi bir bardak olarak sayılır. Çok kısa aralıklarla tekrar basıldığında farklı bir mesaj gösterilir, ancak kayıt yine eklenir. Kayıt geri alma özelliği bulunmaz.
- Bardak miktarını değiştirmek önceki kayıtların mililitre miktarını değiştirmez; yeni miktar sonraki kayıtlara uygulanır.
- Gün değiştiğinde günlük sayaçlar yenilenir. Günlük hedef ve bardak miktarı ayarlarınız korunur.
- Günlük hedefe ulaşınca kutlama mesajı gösterilir; otomatik hatırlatmalar devam eder.
- Tam ekran algılama otomatik hatırlatmalar içindir. Menüden istediğiniz pencereler manuel olarak açılabilir.

## Veriler nerede saklanır?

Ana kayıt dosyası Windows'ta kullanıcı klasörünüzün altındadır:

```text
%USERPROFILE%\AppData\Roaming\SuCini\data.json
```

Diğer platformlarda `~/.su_cini/data.json` kullanılır. Ayarlar, günlük sayaçlar ve son 2000 içme/erteleme işlemi bu dosyada tutulur. Son su içme zamanı ayrıca Qt'nin yerel ayar deposuna kaydedilir; Windows'ta bu depo `MertApps / Su Cini` adıyla kayıt defterindedir.

Uygulama hesap açmanızı istemez ve kayıtlarınızı bir sunucuya göndermez. Yedek almak için uygulamayı kapatıp `data.json` dosyasını kopyalayabilirsiniz. Okunamayan veri dosyasıyla karşılaşıldığında mevcut değilse `data.json.corrupt` adlı bir kopya korunur.

## Sorun giderme

**`No module named PyQt6` hatası alıyorum.**

Bağımlılıkları kurduğunuz Python ortamıyla uygulamayı başlattığınızdan emin olun. Yukarıdaki `.venv` komutlarını kullanın.

**Pencere kayboldu ama uygulama kapanmadı.**

Su Cini sistem tepsisinde çalışır. Damla simgesinden pencereyi tekrar açabilir veya **Çıkış** ile uygulamayı kapatabilirsiniz.

**Hatırlatma hemen görünmüyor.**

Son su kaydınızdan itibaren seçili aralığın dolması gerekir. Erteleme, açık bir hatırlatma/hedef penceresi veya Windows'taki tam ekran uygulaması otomatik gösterimi bekletebilir. Kontroller belirli aralıklarla yapıldığı için birkaç saniyelik gecikme normaldir.

**Kayıt hatası görüyorum.**

Veri klasörüne yazma izniniz ve diskte boş alan olduğundan emin olun. Hata devam ederse terminal üzerinden başlatıp hata çıktısını inceleyin.

## Geliştirme ve testler

Arayüz Python ve PyQt6 ile hazırlanmıştır. Başlangıç noktası `main.py`; hatırlatma akışları `controller.py`, yerel kayıt işlemleri `data_manager.py` içindedir.

Testleri çalıştırmak için:

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_regressions
```

Testler geçici kayıt dosyaları ve görünmez Qt pencereleri kullanır; kişisel su kayıtlarını değiştirmez. Gün değişimi, veri doğrulama, kayıt hataları, erteleme, tam ekran dönüş akışı, menüler ve pencere zamanlayıcıları kapsanır.

Gerçek oyunlarla tam ekran geçişleri, çoklu monitör ve farklı DPI ölçekleri ayrıca masaüstünde doğrulanmalıdır.

## Hata bildirimi

Bir sorunla karşılaşırsanız GitHub üzerinden hata bildirirken işletim sisteminizi, Python sürümünüzü, sorunu oluşturan adımları ve varsa hata çıktısını ekleyin.
