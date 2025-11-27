# راهنمای استقرار (Deployment Guide)

## توصیه برای MVP

**برای MVP فعلی: از Streamlit استفاده کنید** ✅

### چرا Streamlit برای MVP؟
- ✅ اپلیکیشن شما از قبل آماده است
- ✅ استقرار سریع (فقط چند دقیقه)
- ✅ مناسب برای دمو و نمایش به استاد
- ✅ رابط کاربری فارسی کامل
- ✅ پیکربندی Docker و Liara از قبل انجام شده

### چرا Flask برای آینده؟
- 🔄 برای API endpoints (برای دوربین‌ها و سیستم‌های دیگر)
- 🔄 کنترل بیشتر روی backend
- 🔄 مناسب برای production در مقیاس بزرگ
- 🔄 امکان اتصال به دیتابیس و سیستم‌های دیگر

---

## استقرار Streamlit روی Liara

### مرحله 1: آماده‌سازی

1. مطمئن شوید که فایل‌های زیر موجود هستند:
   - `Dockerfile` ✅
   - `liara.json` ✅
   - `requirements.txt` ✅
   - `weights/best.pt` ✅
   - `weights/yolov8n_char_new.pt` ✅

### مرحله 2: نصب Liara CLI

```bash
npm install -g @liara/cli
```

### مرحله 3: لاگین به Liara

```bash
liara login
```

### مرحله 4: استقرار

```bash
# از دایرکتوری پروژه
liara deploy --platform docker --port 8501
```

یا اگر می‌خواهید نام خاصی برای اپلیکیشن انتخاب کنید:

```bash
liara deploy --app your-app-name --platform docker --port 8501
```

### مرحله 5: بررسی

بعد از استقرار، Liara یک URL به شما می‌دهد. اپلیکیشن شما در دسترس خواهد بود.

---

## نکات مهم برای استقرار

### 1. حجم فایل‌های Model
- فایل‌های `best.pt` و `yolov8n_char_new.pt` ممکن است بزرگ باشند
- Liara از Docker استفاده می‌کند، پس مشکلی نیست
- اگر حجم خیلی زیاد است، می‌توانید از Liara Disk استفاده کنید

### 2. منابع سخت‌افزاری
- برای YOLOv8، حداقل 2GB RAM توصیه می‌شود
- در Liara، پلن مناسب را انتخاب کنید

### 3. Environment Variables (اگر نیاز دارید)
می‌توانید در Liara Dashboard تنظیمات environment variables را اضافه کنید.

---

## استقرار Flask (برای آینده)

اگر در آینده خواستید Flask API بسازید:

### ساختار پیشنهادی:
```
Persian_Plate_Recognition/
├── app.py              # Streamlit (فعلی)
├── api/                # Flask API (جدید)
│   ├── __init__.py
│   ├── app.py          # Flask app
│   ├── routes.py       # API endpoints
│   └── models.py       # Model loading
├── shared/             # کد مشترک
│   └── detection.py    # توابع تشخیص
└── ...
```

### مزایای این رویکرد:
- ✅ کد Streamlit فعلی دست نخورده می‌ماند
- ✅ کد مشترک بین Streamlit و Flask
- ✅ می‌توانید هر دو را همزمان deploy کنید

---

## مقایسه سریع

| ویژگی | Streamlit (فعلی) | Flask (آینده) |
|-------|------------------|---------------|
| سرعت توسعه | ⚡ سریع | 🐢 کندتر |
| مناسب برای MVP | ✅ بله | ❌ نه |
| مناسب برای API | ❌ نه | ✅ بله |
| مناسب برای دوربین | ❌ نه | ✅ بله |
| رابط کاربری | ✅ خودکار | 🔧 باید بسازید |
| کنترل Backend | ⚠️ محدود | ✅ کامل |

---

## نتیجه‌گیری

**برای MVP: Streamlit را deploy کنید** 🚀

بعداً اگر نیاز به API یا اتصال به دوربین داشتید، می‌توانید Flask API اضافه کنید.




