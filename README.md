# Excel Tabanlı CRM'den Web Uygulamasına Geçiş

## Proje Amacı

Bu projenin amacı, mevcut Excel tabanlı CRM operasyonunu çok kullanıcılı, izlenebilir, rol bazlı yetkilendirilmiş ve sürdürülebilir bir web uygulamasına dönüştürmektir.

## Aşamalar

1. **Keşif ve Kapsam Netleştirme**
   - Excel dosyalarındaki veri yapıları, iş kuralları ve süreçlerin analizi
   - Hedef veri modeli ve ekran kapsamının belirlenmesi

2. **Mimari ve Teknik Tasarım**
   - Backend/Frontend sınırlarının tanımlanması
   - API kontratları, rol/yetki modeli, immutable kayıt yaklaşımı

3. **MVP Geliştirme**
   - Kimlik doğrulama ve rol bazlı erişim
   - Müşteri yönetimi
   - Aktivite girişi ve görev türetme mantığı

4. **Doğrulama ve Geçiş**
   - Veri doğruluğu kontrolleri
   - Kullanıcı kabul testleri
   - Kademeli canlı geçiş

5. **İyileştirme ve Ölçekleme**
   - Raporlama, performans ve operasyonel iyileştirmeler
   - Süreç bazlı ek modüller

## İlerleme Planı

- [x] Proje iskeleti klasörlerinin oluşturulması (`backend/`, `frontend/`, `docs/`)
- [x] Temel ürün/teknik spesifikasyonun dokümante edilmesi (`docs/spec.md`)
- [ ] Teknoloji seçimi ve mimari karar kayıtlarının netleştirilmesi
- [ ] Backend API iskeleti ve veri tabanı şemasının oluşturulması
- [ ] Frontend uygulama iskeleti ve temel ekranların hazırlanması
- [ ] Test, denetim ve dağıtım süreçlerinin tanımlanması
