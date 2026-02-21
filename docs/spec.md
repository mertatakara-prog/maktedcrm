# CRM Web Uygulaması Teknik/Ürün Spesifikasyonu

## 1. Roller

- **sales**: Kendi müşteri portföyünü yönetir, aktiviteleri girer, görevlerini takip eder.
- **admin**: Tüm veriyi görür, kullanıcı ve süreç denetimi yapar, operasyonel raporlamayı yönetir.

## 2. Excel Eşlemesi

Mevcut Excel tabanlı yapıdan web uygulaması veri katmanına hedef eşleme:

- `MUSTERI_LISTESI` -> `customers`
- `GUNLUK_GIRIS` -> `activities` (**immutable log**)
- `MY_TASKS` -> **derived tasks** (fiziksel tablo değil, aktiviteler + kurallardan türetilir)
- `TASK_KAPATMA_LOG` -> `task_events` (**immutable**)

## 3. Veri Modeli

### 3.1 `users`

- `id` (UUID): Birincil anahtar.
- `email` (string, unique): Giriş ve bildirim adresi.
- `full_name` (string): Ad soyad.
- `role` (enum: `sales`, `admin`): Yetki seviyesi.
- `is_active` (boolean): Kullanıcı aktif/pasif durumu.
- `created_at` (timestamp): Oluşturulma zamanı.
- `updated_at` (timestamp): Son güncelleme zamanı.

### 3.2 `customers`

- `id` (UUID): Birincil anahtar.
- `owner_user_id` (UUID, FK -> users.id): Sorumlu satış kullanıcısı.
- `name` (string): Müşteri adı.
- `phone` (string, nullable): Telefon.
- `email` (string, nullable): E-posta.
- `city` (string, nullable): Şehir bilgisi.
- `status` (enum: `lead`, `active`, `lost`): Müşteri durumu.
- `source` (string, nullable): Potansiyel müşteri kaynağı.
- `notes` (text, nullable): Özet notlar.
- `created_at` (timestamp): Oluşturulma zamanı.
- `updated_at` (timestamp): Son güncelleme zamanı.

### 3.3 `activities` (immutable)

- `id` (UUID): Birincil anahtar.
- `customer_id` (UUID, FK -> customers.id): İlgili müşteri.
- `user_id` (UUID, FK -> users.id): Aktiviteyi giren kullanıcı.
- `activity_type` (enum: `call`, `meeting`, `note`, `follow`, `quote`): Aktivite tipi.
- `activity_at` (timestamp): Aktivitenin gerçekleştiği zaman.
- `summary` (string): Kısa özet.
- `detail` (text): Detay açıklama.
- `next_action_date` (date, nullable): Sonraki takip tarihi.
- `created_at` (timestamp): Sisteme yazılma zamanı.

> Not: `activities` kayıtları sonradan güncellenmez/silinmez; yalnızca yeni kayıt eklenir.

### 3.4 `task_events` (immutable)

- `id` (UUID): Birincil anahtar.
- `customer_id` (UUID, FK -> customers.id): İlgili müşteri.
- `user_id` (UUID, FK -> users.id): İşlemi yapan kullanıcı.
- `task_type` (enum: `FOLLOW`, `QUOTE`): Görev tipi.
- `event_type` (enum: `closed`, `reopened`, `deferred`): Görev olay tipi.
- `event_reason` (string, nullable): Olay gerekçesi.
- `event_at` (timestamp): Olay zamanı.
- `created_at` (timestamp): Sisteme yazılma zamanı.

> Not: `task_events` kayıtları değiştirilemez/silinemez; görev yaşam döngüsü olay geçmişinden okunur.

## 4. İş Kuralları

### 4.1 Immutable Kuralları

- `activities` ve `task_events` tablolarında `UPDATE` / `DELETE` yapılmaz.
- Hatalı veri düzeltmesi, yeni bir telafi kaydı (`activity` veya `task_event`) ile yapılır.

### 4.2 Zorunlu Alan Kuralları

- Kullanıcı: `email`, `full_name`, `role` zorunlu.
- Müşteri: `owner_user_id`, `name`, `status` zorunlu.
- Aktivite: `customer_id`, `user_id`, `activity_type`, `activity_at`, `summary`, `detail` zorunlu.
- Task olayı: `customer_id`, `user_id`, `task_type`, `event_type`, `event_at` zorunlu.

## 5. Task Mantığı

- `MY_TASKS` fiziksel tablo değildir; `activities` + `task_events` + zaman kurallarından hesaplanır.
- Görev tipleri:
  - `FOLLOW`: Takip araması/görüşmesi gerektiren görev.
  - `QUOTE`: Teklif hazırlama/gönderme takibi gerektiren görev.

### 5.1 Türetme Kuralları

- `activities.activity_type = follow` ise aday görev tipi `FOLLOW`.
- `activities.activity_type = quote` ise aday görev tipi `QUOTE`.
- `next_action_date` doluysa görevin hedef tarihi olarak kullanılır.
- İlgili görev için en son `task_events` kaydı `closed` ise görev kapalı kabul edilir; listede açık görev olarak gösterilmez.

### 5.2 Öncelik Kuralları

- **Yüksek öncelik**: Hedef tarihi geçmiş görevler (overdue).
- **Orta öncelik**: Hedef tarihi bugün olan görevler.
- **Düşük öncelik**: Hedef tarihi gelecekte olan görevler.
- Hedef tarihi olmayan görevler varsayılan olarak düşük öncelikte değerlendirilir.

## 6. Ekranlar

- **Login**: Kimlik doğrulama, rol bazlı yönlendirme.
- **Görevlerim**: Türetilmiş açık görevlerin kullanıcı bazlı listesi, öncelik ve durum filtreleri.
- **Müşteriler**: Müşteri listeleme, filtreleme, arama.
- **Müşteri Kartı**: Müşteri detayları + kronolojik aktivite ve görev olay geçmişi.
- **Aktivite Ekle**: Müşteri için yeni immutable aktivite oluşturma.
- **Yönetici Denetim**: Tüm kullanıcı/müşteri/aktivite görünümü, denetim ve raporlama ekranı.

## 7. API Endpoint Listesi

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/me`

- `GET /api/customers`
- `POST /api/customers`
- `GET /api/customers/:id`
- `PATCH /api/customers/:id`

- `GET /api/customers/:id/activities`
- `POST /api/customers/:id/activities`

- `GET /api/tasks/my` (derived tasks)
- `POST /api/tasks/:taskType/:customerId/close`
- `POST /api/tasks/:taskType/:customerId/reopen`
- `POST /api/tasks/:taskType/:customerId/defer`

- `GET /api/admin/audit/activities`
- `GET /api/admin/audit/task-events`
- `GET /api/admin/users`
