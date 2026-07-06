# Kufur-savar
Spotify'daki küfürleri engeller

Merhaba, Sonnet 5 ve Gemini 3.1 ile yaptığım açık kaynak kodlu Spotify için küfür engelleme şeysini göstereceğim.

Her şeyden önce Spotify Premium ve bilgisayarınızda Python olmalı!

Files doyasını RAR'dan çıkartın.
spotify-for-developers Linkine gidin ve yeni proje oluşturun ve ayarları aşağıdaki gibi girin ve tekrar create App'a basın.

1783362159080.webp

Sonrasında "Client ID" adı altındaki sayı ve yazıları kopyalayın ve files dosyasının içindeki "kufur_savar.py" dosyasını bir bir editör ile açın.
24. satırdaki "buraya_yazcan" adlı bölüme kopyaladığımız ID'yi yapıştırın.
Tekrar aynı linke gidin ve bu sefer "Client ID"nin altındaki "Show Client secret" e basın ve gelen yeni ID'yi koddaki 25. satırdaki "buraya_yazcan" kısmı ile değiştirin.
pip install spotipy syncedlyricsBunu CMD'yi ya da PowerShell'i yönetici olarak başlatıp yazın.
"blacklist.txt" dosyasının içindekileri kendinize göre düzenleyin.
Her şey yüklendikten sonra tekrar files dosyasına girin ve boş bir yere sağ tıklayın ve "terminalde aç" a tıklayın.
Gelen CMD ekranına python kufur_savar.py yazın. Tarayıcınız açılacak ve oradan "devam et" e basın.
Ve artık uygulamayı kullanabilirsiniz!

Uygulama daha çok yeni ve hala daha geliştirme aşamasında. Kod açık kaynak olduğu için koddaki tüm her şeyi kendinize göre değiştirebilirsiniz. Değiştirilmiş sürümleri Google Drive'a yükleyip burada paylaşırsanız çok sevinirim.

Peki nasıl çalışıyor? Proje henüz çok yeni olduğu için hataları var, yakında düzelticeğim.

Şarkı Takibi: Script, API üzerinden arka planda Spotify'da o an çalan şarkıyı sürekli olarak takip ediyor.

Sözlerin Çekilmesi: Şarkı değiştiğinde, açık kaynaklı şarkı sözü veritabanlarından (Lrclib vb.) O şarkının zaman damgalı (hangi milisaniyede hangi satırın söylendiğini belirten) sözlerini otomatik olarak indiriyor.

Zaman Hesaplaması: İndirilen sözleri sizin oluşturduğunuz blacklist.txt dosyasındaki kelimelerle karşılaştırıyor. Eğer satırda yasaklı bir kelime bulursa, kelimenin uzunluğuna göre tam olarak hangi milisaniyede söylendiğini matematiksel olarak hesaplıyor.

Anlık Ses Kısma: Şarkı tam o hesaplanan milisaniyeye geldiğinde uygulamanın sesini anında %0'a çekiyor ve o kelime biter bitmez sesi eski seviyesine geri döndürüyor. Böylece satırın tamamı değil, sadece yasaklı kelime duyulmamış oluyor.

Umarım seversiniz!
