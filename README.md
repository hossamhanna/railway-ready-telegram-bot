# Mahami - Telegram Tasks Platform (Minimal Scaffold)

بوت تليجرام بسيط مع تسجيل مستخدمين، رابط إحالة، عرض رصيد، وقاعدة بيانات PostgreSQL عبر Docker Compose.

## المتطلبات
- Docker & Docker Compose
- ملف .env يحتوي على إعدادات BOT_TOKEN و DATABASE_URL و ADMIN_IDS

## خطوات التشغيل
1. انسخ `.env.example` إلى `.env` واملأ القيم (BOT_TOKEN إلخ).
2. شغل: `docker compose up --build -d`
3. راقب السجلات: `docker compose logs -f bot`