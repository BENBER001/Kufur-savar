Merhaba, Sonnet 5 ve Gemini 3.1 ile yaptığım açık kaynak kodlu Spotify ve Youtube Music için küfür engelleme şeysini göstereceğim.

Her şeyden önce Spotify Premium (Spotify sürümü için) ve bilgisayarınızda Python olmalı!

GitHub - BENBER001/Kufur-savar: Spotify'daki küfürleri engeller üzerinden dosyaları indirin.
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
Youtube Music için
GitHub - BENBER001/Kufur-savar: Spotify'daki küfürleri engeller üzerinden istediğiniz sürümü indirin (Spotify veya Youtube Music) dosyaları indirin.
Dosyaları rar'dan çıkartın.
CMD veya PowerShell'i açın ve oraya pip install flask flask-cors syncedlyrics yazın. Her şey indikten sonra sıradaki adıma geçin.
Tarayıcınızdan "chrome://extensions/" linkine Gidin
Sağ üst köşede "geliştirici modunu açın.
Sol üst'den "Paketlenmemiş öğeleri yükle" ye basın
İçinde "manifest.json" ve "content.js" Olan dosyayı seçin. Main adlı dosyayı seçmeyin !
Artık eklentimiz yüklendi. Web'den Youtube music'e girip bir şarkı başlatın. sağ tık ve ardından incele yapın ve oradan console kısmına gelin. Eğer açtığınız şarkı orada gözüküyora her şey tamam demektir. Sırasıyla şu adımlar uygulayın.

content.js ve manifest.json adlı dosyaların olduğu klasördeki main dosyasına girin.
Boş bir yere sağ tık yapın ve "terminalde aç" basın CMD ekranına pthon main.py yazın ve artık uygulama çalışıyor.
Chorome eklentisi sebebiyle güvenlik derdiniz olmasın. Tamamen açık kaynak kodlu, kodun ne yaptığına istediğiniz gibi bakabilirsiniz.

Uygulama daha çok yeni ve hala daha geliştirme aşamasında. Kod açık kaynak olduğu için koddaki tüm her şeyi kendinize göre değiştirebilirsiniz. Değiştirilmiş sürümleri Google Drive'a yükleyip burada paylaşırsanız çok sevinirim.

Peki nasıl çalışıyor?

Şarkı Takibi: Script, API üzerinden arka planda Spotify'da o an çalan şarkıyı sürekli olarak takip ediyor.

Sözlerin Çekilmesi: Şarkı değiştiğinde, açık kaynaklı şarkı sözü veritabanlarından (Lrclib vb.) O şarkının zaman damgalı (hangi milisaniyede hangi satırın söylendiğini belirten) sözlerini otomatik olarak indiriyor.

Zaman Hesaplaması: İndirilen sözleri sizin oluşturduğunuz blacklist.txt dosyasındaki kelimelerle karşılaştırıyor. Eğer satırda yasaklı bir kelime bulursa, kelimenin uzunluğuna göre tam olarak hangi milisaniyede söylendiğini matematiksel olarak hesaplıyor.

Anlık Ses Kısma: Şarkı tam o hesaplanan milisaniyeye geldiğinde uygulamanın sesini anında %0'a çekiyor ve o kelime biter bitmez sesi eski seviyesine geri döndürüyor. Böylece satırın tamamı değil, sadece yasaklı kelime duyulmamış oluyor.

Cahce Özelliği: Daha önce çaldığı şarkıları kaydeder, daha sonra tekrar aynı şarkı çalınca tekrar tarama yapmasına gerek kalmaz. En fazla 1KB yer kaplar. D


Umarım seversiniz!
