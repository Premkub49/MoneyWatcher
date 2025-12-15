# MoneyWatcher

![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=flat-square)

> ⚠️ **Note:** Project นี้กำลังอยู่ในช่วงพัฒนา (Under Development) โครงสร้าง Database และ API อาจมีการเปลี่ยนแปลงได้ตลอดเวลา

**MoneyWatcher** คือระบบบันทึกรายรับ-รายจ่ายอัตโนมัติ (Automated Expense Tracker) ที่ทำงานร่วมกับ Mobile Banking ผ่าน Webhook โดยมีหัวใจหลักคือการตัดปัญหา "ขี้เกียจจด" ด้วยการใช้ Automation

## Features (Current & Planned)

- [x] **Webhook Listener:** รับข้อมูลแจ้งเตือนธนาคาร (เช่น Krungthai) ผ่าน API
- [x] **Categorization:** จำแยก Category ก่อนส่ง API
- [ ] **Data Persistence:** บันทึกลง PostgreSQL (Async SQLAlchemy)
- [ ] **Dashboard:** แสดงผลกราฟการเงินผ่าน Grafana
- [ ] **Telegram Notify:** แจ้งเตือนสรุปยอดรายวัน

## Tech Stack

- **Backend:** Python (FastAPI), Pydantic
- **Database:** PostgreSQL, SQLAlchemy (Async), Alembic
- **Integration:** MacroDroid (Android Automation)
- **Monitoring:** Grafana (Visualization)
- **Control & Notification** Telegram
---

## Installation & Setup

1. **Clone Repository**
    ```bash
    git clone https://github.com/Premkub49/MoneyWatcher.git
    cd MoneyWatcher
    ```

2.  **Setup Environment**
    สร้างไฟล์ `.env` โดยดูตัวอย่างจาก `.env.example`

    ```env
    DATABASE_URL=postgresql+asyncpg://[user]:[pass]@localhost:5432/money_watcher_db
    ```

3. **รัน Docker Compose**
    เพื่อรัน grafana และ postgresql

    ```bash
    docker-compose up -d --build
    ```

4.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Database Migration**

    ```bash
    alembic upgrade head
    ```

6.  **Run Server**

    ```bash
    uvicorn main:app --reload
    ```

-----

## MacroDroid Configuration

ระบบนี้ใช้ **MacroDroid** บน Android ในการดักจับ SMS/Notification จากธนาคาร แล้วยิง Webhook มาที่ Server

### วิธีการตั้งค่า (Setup Guide)

1.  **Trigger:** SMS Received / Notification Received (ในแอปกรุงไทยจะต้องเลือกเป็นไลน์และ Krungthai Contacts)
2.  **Download Profile:**
    > คุณสามารถโหลดไฟล์ Config ตัวอย่างได้ที่โฟลเดอร์: [`/integrations/macrodroid/Bank_Webhook.mdr`](https://www.google.com/search?q=./integrations/macrodroid/)

-----

## Grafana Dashboard

โปรเจกต์นี้มาพร้อมกับ Docker Compose สำหรับรัน Grafana เพื่อดู Dashboard ทางการเงิน

### การใช้งาน (Usage)

1.  รัน Docker Compose (ถ้ายังไม่รันตอน Setup):
    ```bash
    docker-compose up -d --build
    ```
2.  เข้าไปที่ `http://localhost:3000` และ login
3.  เชื่อมต่อ Data Source ไปที่ PostgreSQL ของโปรเจกต์
4.  **Import Dashboard:**
    > นำไฟล์ JSON จาก [`/integrations/grafana/dashboard.json`](https://www.google.com/search?q=./integrations/grafana/) ไป Import ในหน้า Dashboard

-----

## Project Structure

```text
MoneyWatcher/
├── app/
│   ├── api/          # Route Handlers
│   ├── models/       # Database Models
│   ├── schemas/      # Pydantic Schemas
│   ├── services/     # Business Logic
│   └── database/     # DB Connection & Init data
├── integrations/
│   ├── grafana/      # Dashboard JSON files
│   └── macrodroid/   # .mdr files for Android
├── migrations/       # Alembic versions
└── main.py
```

## Contributing

เนื่องจากโปรเจกต์ยังไม่เสร็จสมบูรณ์ (WIP) หากพบ Bug หรือต้องการเสนอแนะ Feature สามารถเปิด Issue ทิ้งไว้ได้เลยครับ

-----

*Created by Premkub49*

````
