# 🎭 Padmart — Acting School Hall Reservation System

A full Streamlit web app for booking rehearsal halls.

## 🚀 Deploy to Streamlit Cloud (Free — GitHub required)

### Step 1 — Push to GitHub
1. Create a new **public** repository on [github.com](https://github.com)
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`

### Step 2 — Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your repository, branch `main`, file `app.py`
5. Click **Deploy** — live in ~2 minutes at:
   `https://YOUR-USERNAME-padmart.streamlit.app`

## 🔑 Features
| Feature | Details |
|---|---|
| Gateway | Choose Guest or Owner on the first screen |
| Guest booking | Name + email, hall, 1–6h duration, time slot (10:00–11:00 format) |
| Slot conflict detection | Blocks overlapping hours automatically |
| Guest privacy | My Reservations filtered by email only |
| Owner dashboard | Stats, 3 charts, all reservations, cancel any booking |
| Settings | Change owner password + SMTP email config |
| Bilingual | Full English + Persian (RTL) toggle |

## 🔐 Default Owner Password
```
admin123
```
Change in **Owner Dashboard → Settings → Security**.

## 🏛️ Halls
| Hall | Seats | Price/hr |
|---|---|---|
| 🎪 Grand Studio | 120 | 150,000 تومان |
| 🎭 Studio 2 | 30 | 80,000 تومان |
