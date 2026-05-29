# 🎭 Padmart — Acting School Hall Reservation System

A complete multi-page web app for booking rehearsal halls, built with plain HTML + JavaScript. No server, no framework, no build step — just open in a browser.

## 📁 File Structure

```
padmart-app/
├── index.html          ← Gateway (Guest or Owner)
├── guest.html          ← Guest booking + My Reservations
├── owner-login.html    ← Owner password screen
├── owner.html          ← Owner dashboard (all reservations, charts, settings)
├── store.js            ← Shared data store (localStorage)
└── README.md
```

## 🚀 How to Run Locally

1. Download all files into one folder
2. Double-click `index.html` — opens in any browser
3. No internet required after fonts load

## 🌐 Deploy to GitHub Pages (Free Hosting)

1. Create a free GitHub account at [github.com](https://github.com)
2. Click **New repository** → name it `padmart-app` → set to **Public**
3. Click **Add file → Upload files** → upload all 5 files
4. Go to **Settings → Pages → Source → main branch → / (root)**
5. Your app is live at: `https://YOUR-USERNAME.github.io/padmart-app/`

## 🔑 Features

| Feature | Details |
|---|---|
| **Two separate spaces** | Gateway routes Guest and Owner to separate pages |
| **Guest privacy** | Guests see only their own bookings (by email lookup) |
| **Duration selector** | Choose 1–6 hours per session |
| **Time slots** | Format: `10:00–11:00`, `11:00–12:00` … up to `20:00` |
| **Conflict detection** | Slots blocked if any hour overlaps an active booking |
| **Live sync** | All pages share `localStorage` — cancel on owner page, guest sees it instantly |
| **Bilingual** | Full English + Persian (RTL) toggle on every page |
| **Owner dashboard** | Stats cards + 3 charts (bar, pie, line) + search + cancel any booking |
| **Settings** | Change owner password + configure SMTP email |
| **Hall pricing** | Grand Studio: 150,000 تومان/hr · Studio 2: 80,000 تومان/hr |

## 🔐 Default Owner Password

```
admin123
```
Change it in **Owner Dashboard → Settings → Security**.

## 🏛️ Halls

| Hall | Capacity | Price/hr |
|---|---|---|
| 🎪 Grand Studio | 120 seats | 150,000 تومان |
| 🎭 Studio 2 | 30 seats | 80,000 تومان |

## 🛠️ Customisation

- **Prices**: edit `HALLS` in `store.js`
- **Max hours**: change `for (let d = 1; d <= 6; d++)` in `guest.html`
- **Opening hours**: edit `SLOT_STARTS` array in `store.js`
- **Colours**: change `--wine`, `--gold` CSS variables in each file
