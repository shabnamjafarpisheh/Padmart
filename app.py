import streamlit as st
from datetime import date, datetime, timedelta
import uuid, json, re

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Padmart — Acting School",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
HALLS = {
    "grand":   {"name_en": "Grand Studio", "name_fa": "گرند استودیو",
                "price": 150000, "seats": 120, "icon": "🎪",
                "desc_en": "120 seats · Professional lighting · Full backstage",
                "desc_fa": "۱۲۰ نفر · نور حرفه‌ای · پشت صحنه"},
    "studio2": {"name_en": "Studio 2",     "name_fa": "استودیو ۲",
                "price": 80000,  "seats": 30,  "icon": "🎭",
                "desc_en": "30 seats · Mirrors · Sound system",
                "desc_fa": "۳۰ نفر · آینه · سیستم صوتی"},
}
SLOT_STARTS = list(range(9, 21))          # 9 → 20
DEFAULT_OWNER_PASS = "admin123"

TR = {
    "en": {
        "page_book":       "📅 Book a Hall",
        "page_myres":      "📋 My Reservations",
        "page_owner":      "👑 Owner Dashboard",
        "page_allres":     "📋 All Reservations",
        "page_charts":     "📊 Analytics",
        "page_settings":   "⚙️ Settings",
        "hall_grand":      "Grand Studio",
        "hall_s2":         "Studio 2",
        "your_name":       "Your Name",
        "email":           "Email Address",
        "date_lbl":        "Date",
        "duration":        "Duration (hours)",
        "start_slot":      "Start Time Slot",
        "confirm_btn":     "🎫 Confirm Reservation & Pay",
        "my_res_title":    "My Reservations",
        "my_res_note":     "🔒 Enter your booking email — only your own reservations are shown.",
        "view_btn":        "View My Bookings",
        "cancel_btn":      "Cancel & Refund",
        "refunded":        "Refunded",
        "status_active":   "✓ Confirmed",
        "status_cancel":   "✕ Cancelled",
        "guest_lbl":       "Guest",
        "date_col":        "Date",
        "slot_col":        "Time Slot",
        "dur_col":         "Duration",
        "paid_col":        "Amount Paid",
        "active_note":     "Cancel anytime for a full refund.",
        "cancel_note":     "This reservation has been refunded.",
        "total_bk":        "Total Bookings",
        "active_bk":       "Active",
        "revenue":         "Revenue (Tomans)",
        "unique_g":        "Unique Guests",
        "all_res":         "All Reservations",
        "search_ph":       "Search by name or email…",
        "change_pass":     "Change Owner Password",
        "new_pass":        "New Password",
        "confirm_pass":    "Confirm New Password",
        "save_pass":       "Save Password",
        "smtp_title":      "SMTP Email Settings",
        "smtp_host":       "SMTP Host",
        "smtp_port":       "Port",
        "smtp_user":       "Sender Email",
        "smtp_pass":       "App Password",
        "smtp_note":       "Gmail: enable 2-Step Verification → App Passwords → Mail → Generate.",
        "save_smtp":       "Save Email Settings",
        "owner_pass_lbl":  "Owner Password",
        "owner_login_btn": "Enter Dashboard",
        "owner_hint":      "Demo password: **admin123**",
        "logout":          "← Exit Dashboard",
        "back_home":       "← Back to Home",
        "choose_hall":     "Choose a Hall",
        "select":          "Select",
        "selected":        "✓ Selected",
        "summary_hall":    "Selected Hall",
        "summary_price":   "Total Price",
        "avail":           "✓ Available",
        "taken":           "✗ Booked",
        "partial":         "~ Partial",
        "bar_title":       "Bookings by Guest",
        "pie_title":       "Hall Usage Share",
        "line_title":      "Bookings Over Time",
    },
    "fa": {
        "page_book":       "📅 رزرو سالن",
        "page_myres":      "📋 رزروهای من",
        "page_owner":      "👑 داشبورد مدیر",
        "page_allres":     "📋 همه رزروها",
        "page_charts":     "📊 آمار",
        "page_settings":   "⚙️ تنظیمات",
        "hall_grand":      "گرند استودیو",
        "hall_s2":         "استودیو ۲",
        "your_name":       "نام شما",
        "email":           "آدرس ایمیل",
        "date_lbl":        "تاریخ",
        "duration":        "مدت زمان (ساعت)",
        "start_slot":      "بازه شروع",
        "confirm_btn":     "🎫 تأیید رزرو و پرداخت",
        "my_res_title":    "رزروهای من",
        "my_res_note":     "🔒 ایمیل رزرو خود را وارد کنید — فقط رزروهای خودتان نمایش داده می‌شود.",
        "view_btn":        "مشاهده رزروهای من",
        "cancel_btn":      "لغو و بازپرداخت",
        "refunded":        "بازپرداخت شد",
        "status_active":   "✓ تأیید شده",
        "status_cancel":   "✕ لغو شده",
        "guest_lbl":       "مهمان",
        "date_col":        "تاریخ",
        "slot_col":        "بازه زمانی",
        "dur_col":         "مدت",
        "paid_col":        "مبلغ پرداختی",
        "active_note":     "هر زمان لغو کنید — بازپرداخت کامل.",
        "cancel_note":     "این رزرو لغو و بازپرداخت شده است.",
        "total_bk":        "کل رزروها",
        "active_bk":       "فعال",
        "revenue":         "درآمد (تومان)",
        "unique_g":        "مهمانان یکتا",
        "all_res":         "همه رزروها",
        "search_ph":       "جستجو با نام یا ایمیل…",
        "change_pass":     "تغییر رمز عبور مدیر",
        "new_pass":        "رمز جدید",
        "confirm_pass":    "تأیید رمز جدید",
        "save_pass":       "ذخیره رمز عبور",
        "smtp_title":      "تنظیمات ایمیل SMTP",
        "smtp_host":       "هاست SMTP",
        "smtp_port":       "پورت",
        "smtp_user":       "ایمیل فرستنده",
        "smtp_pass":       "رمز اپ",
        "smtp_note":       "Gmail: تأیید دو مرحله‌ای را فعال کنید ← رمزهای اپ ← ایمیل ← ایجاد کنید.",
        "save_smtp":       "ذخیره تنظیمات ایمیل",
        "owner_pass_lbl":  "رمز عبور مدیر",
        "owner_login_btn": "ورود به داشبورد",
        "owner_hint":      "رمز نمونه: **admin123**",
        "logout":          "← خروج از داشبورد",
        "back_home":       "← بازگشت به صفحه اصلی",
        "choose_hall":     "انتخاب سالن",
        "select":          "انتخاب",
        "selected":        "✓ انتخاب شده",
        "summary_hall":    "سالن انتخابی",
        "summary_price":   "قیمت کل",
        "avail":           "✓ آزاد",
        "taken":           "✗ رزرو شده",
        "partial":         "~ نیمه پر",
        "bar_title":       "رزرو به تفکیک مهمان",
        "pie_title":       "سهم استفاده از سالن‌ها",
        "line_title":      "روند رزرو در طول زمان",
    },
}

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "lang":          "en",
        "page":          "gateway",       # gateway | guest | owner-login | owner
        "owner_auth":    False,
        "owner_pass":    DEFAULT_OWNER_PASS,
        "reservations":  [],
        "smtp":          {"host": "", "port": 587, "user": "", "pass": ""},
        "g_hall":        "grand",
        "g_dur":         1,
        "g_start":       None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def t(key):
    return TR[st.session_state.lang].get(key, key)

def fmt(n):
    return f"{n:,} تومان"

def gen_id():
    return "RES-" + str(uuid.uuid4())[:8].upper()

def slot_label(start, dur):
    return f"{start:02d}:00–{start+dur:02d}:00"

def booked_hours(hall, date_str):
    taken = set()
    for r in st.session_state.reservations:
        if r["hall"] == hall and r["date"] == date_str and r["status"] == "active":
            for h in range(r["start_hour"], r["start_hour"] + r["duration"]):
                taken.add(h)
    return taken

def can_book(hall, date_str, start_hour, dur):
    taken = booked_hours(hall, date_str)
    for h in range(start_hour, start_hour + dur):
        if h in taken or h > 20:
            return False
    return True

def cancel_res(res_id):
    for r in st.session_state.reservations:
        if r["id"] == res_id:
            r["status"] = "cancelled"
            break

def is_fa():
    return st.session_state.lang == "fa"

def go(page):
    st.session_state.page = page
    st.rerun()

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
FA = is_fa()
DIR = "rtl" if FA else "ltr"
FONT = "'Vazirmatn','Tahoma',sans-serif" if FA else "'DM Sans',sans-serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&family=Vazirmatn:wght@400;500;600;700&display=swap');
:root{{--wine:#6d1f2a;--gold:#b88a4a;--muted:#7f6b62;--line:#e7d8c6;--paper:#fffaf3;--ink:#241817}}
html,body,[data-testid="stAppViewContainer"]{{
  background:linear-gradient(135deg,#f6ecdf 0%,#fbf7f0 50%,#f1e2d2 100%) !important;
  font-family:{FONT} !important;
  color:var(--ink);direction:{DIR};
}}
[data-testid="stHeader"]{{background:rgba(255,249,240,.95)!important;border-bottom:1px solid var(--line)}}
[data-testid="stSidebar"]{{display:none}}
#MainMenu,footer,[data-testid="stToolbar"]{{display:none!important}}
section[data-testid="stMain"]{{padding-top:0!important}}
.display{{font-family:'Playfair Display',serif;font-weight:700}}

/* hero */
.hero{{
  background:
    linear-gradient(90deg,rgba(36,24,23,.86),rgba(36,24,23,.28) 60%,rgba(36,24,23,.06)),
    url('https://images.unsplash.com/photo-1503095396549-807759245b35?w=1400&q=80&fit=crop') center/cover;
  border-radius:26px;padding:52px 48px;color:#fff;margin-bottom:24px;
  box-shadow:0 18px 50px rgba(72,16,25,.18);min-height:220px;
}}
.hero h1{{font-family:'Playfair Display',serif;font-size:36px;font-weight:700;line-height:1.1;margin:0 0 10px}}
.hero p{{font-size:15px;color:rgba(255,255,255,.84);line-height:1.7;margin:0;max-width:520px}}
.hero-badge{{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:99px;
  background:var(--gold);font-size:11px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:#fff;margin-bottom:16px}}
.owner-hero{{background:
  linear-gradient(90deg,rgba(20,8,10,.9),rgba(20,8,10,.4) 60%,rgba(20,8,10,.08)),
  url('https://images.unsplash.com/photo-1503095396549-807759245b35?w=1400&q=80&fit=crop') center/cover;
  border-radius:26px;padding:40px 48px;color:#fff;margin-bottom:24px;
  box-shadow:0 18px 50px rgba(72,16,25,.22);min-height:180px;}}
.owner-hero h1{{font-family:'Playfair Display',serif;font-size:30px;font-weight:700;margin:0 0 8px}}
.owner-hero p{{font-size:14px;color:rgba(255,255,255,.8);margin:0}}
.owner-badge{{display:inline-flex;align-items:center;gap:4px;background:linear-gradient(135deg,var(--gold),#8a6030);
  color:#fff;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  padding:3px 10px;border-radius:99px;margin-bottom:12px}}

/* panels */
.panel{{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:24px;
  box-shadow:0 8px 28px rgba(72,16,25,.06);margin-bottom:16px}}
.panel-dark{{background:#2f1d1a;border-radius:22px;padding:24px;color:#fff;margin-bottom:16px}}
.eyebrow{{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#9b7250;margin-bottom:4px}}
.eyebrow-light{{color:#d8b47b}}

/* gateway cards */
.gcard{{border-radius:26px;padding:36px 24px;text-align:center;cursor:pointer;transition:all .22s;border:1.5px solid var(--line);background:var(--paper)}}
.gcard:hover{{transform:translateY(-5px);border-color:#c8aa92;box-shadow:0 18px 44px rgba(72,16,25,.1)}}
.gcard-owner{{background:#1e0f0f;border:2px solid var(--gold);border-radius:26px;padding:36px 24px;text-align:center;cursor:pointer;transition:all .22s}}
.gcard-owner:hover{{transform:translateY(-5px);box-shadow:0 18px 44px rgba(72,16,25,.3)}}

/* hall cards */
.hall-card{{border:1px solid var(--line);border-radius:18px;padding:18px;background:#fffdf9;transition:all .2s;margin-bottom:10px}}
.hall-card.sel{{border-color:var(--wine);background:#fff7f7;box-shadow:0 8px 22px rgba(109,31,42,.1)}}
.hall-price{{font-size:15px;font-weight:700;color:var(--wine);margin-top:6px}}

/* slot grid */
.slot-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:6px}}
.slot-btn{{padding:9px 4px;border:1px solid var(--line);border-radius:10px;background:#fffdf9;
  font-size:11px;text-align:center;cursor:pointer;transition:.2s;line-height:1.3}}
.slot-btn.sel{{border-color:var(--wine);background:var(--wine);color:#fff;font-weight:600}}
.slot-btn.taken{{background:#fdf0f0;color:#c0a0a0;text-decoration:line-through;border-color:#f0d8d8}}
.slot-btn.partial{{background:#fdf6e0;color:#a08030;border-color:#e8d8a0}}
.slot-btn.avail:hover{{border-color:var(--wine);background:#fff7f7}}

/* summary strip */
.summary-strip{{background:#f5eadf;border-radius:13px;padding:13px 17px;
  display:flex;justify-content:space-between;align-items:center;margin:14px 0}}

/* stat cards */
.stat-card{{background:var(--paper);border:1px solid var(--line);border-radius:18px;
  padding:18px;text-align:center;box-shadow:0 4px 14px rgba(72,16,25,.04)}}
.stat-num{{font-family:'Playfair Display',serif;font-size:30px;color:var(--wine);font-weight:700}}
.stat-lbl{{font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:5px}}

/* res card */
.res-card{{background:var(--paper);border:1px solid var(--line);border-radius:20px;
  padding:18px;margin-bottom:12px;box-shadow:0 4px 14px rgba(72,16,25,.04)}}
.res-card.cancelled{{opacity:.64}}
.res-id{{font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#9b7250;margin-bottom:3px}}
.res-hall{{font-family:'Playfair Display',serif;font-size:20px;color:#2b1c19;margin-bottom:5px}}
.res-price{{font-family:'Playfair Display',serif;font-size:22px;color:var(--wine)}}
.badge-active{{display:inline-flex;padding:3px 10px;border-radius:99px;font-size:11px;font-weight:600;background:#e7f3ec;color:#2d7a58}}
.badge-cancelled{{display:inline-flex;padding:3px 10px;border-radius:99px;font-size:11px;font-weight:600;background:#f2e2e0;color:#8b2d36}}

/* form fields */
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stDateInput>div>div>input,.stTextArea>div>div>textarea{{
  border:1px solid var(--line)!important;background:#fffdf9!important;border-radius:13px!important;
  padding:13px 14px!important;font-family:{FONT}!important;font-size:14px!important;color:var(--ink)!important}}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{{
  border-color:var(--wine)!important;box-shadow:0 0 0 3px rgba(109,31,42,.1)!important}}
label[data-testid="stWidgetLabel"]>div>p{{font-size:13px!important;font-weight:600!important;color:var(--ink)!important}}
.stSelectbox>div>div>div{{border:1px solid var(--line)!important;background:#fffdf9!important;
  border-radius:13px!important;font-family:{FONT}!important}}

/* buttons */
.stButton>button{{
  background:var(--wine)!important;color:#fff!important;border:none!important;
  border-radius:14px!important;padding:12px 22px!important;
  font-family:{FONT}!important;font-size:14px!important;font-weight:600!important;
  box-shadow:0 4px 16px rgba(109,31,42,.2)!important;transition:.2s!important;width:100%!important;
}}
.stButton>button:hover{{background:#571821!important;transform:translateY(-1px)!important}}
.btn-gold>button{{background:linear-gradient(135deg,var(--gold),#8a6030)!important;color:#1e0f0f!important;box-shadow:0 4px 16px rgba(184,138,74,.25)!important}}
.btn-cancel>button{{background:#f2e2e0!important;color:#7b2932!important;box-shadow:none!important;font-size:13px!important;padding:8px 16px!important}}
.btn-cancel>button:hover{{background:#ead3d0!important}}
.btn-ghost>button{{background:none!important;color:var(--muted)!important;border:1px solid var(--line)!important;box-shadow:none!important;font-size:13px!important}}
.btn-ghost>button:hover{{background:#f5eadf!important}}

/* tabs */
.stTabs [data-baseweb="tab-list"]{{gap:4px;background:transparent;border-bottom:2px solid var(--line)}}
.stTabs [data-baseweb="tab"]{{background:transparent!important;border:none!important;
  color:var(--muted)!important;font-family:{FONT}!important;font-weight:600!important;
  font-size:13px!important;padding:10px 18px!important;border-radius:0!important}}
.stTabs [aria-selected="true"]{{color:var(--wine)!important;border-bottom:2px solid var(--wine)!important}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:20px!important}}

/* messages */
.msg-ok{{background:#e8f3ec;color:#2d6b4f;border-radius:12px;padding:11px 15px;font-size:14px;font-weight:500;margin:8px 0}}
.msg-err{{background:#f8e5e3;color:#8b2d36;border-radius:12px;padding:11px 15px;font-size:14px;font-weight:500;margin:8px 0}}
hr{{border:none;border-top:1px solid var(--line);margin:16px 0}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LANGUAGE TOGGLE (always visible top-right)
# ─────────────────────────────────────────────
_, lang_col = st.columns([6, 1])
with lang_col:
    lang_choice = st.selectbox("🌐", ["English", "فارسی"],
                               index=0 if st.session_state.lang == "en" else 1,
                               label_visibility="collapsed", key="lang_sel")
    new_lang = "en" if lang_choice == "English" else "fa"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

# ─────────────────────────────────────────────
#  ██  PAGE: GATEWAY
# ─────────────────────────────────────────────
if st.session_state.page == "gateway":
    st.markdown("""
    <div class="hero" style="text-align:center">
      <div style="font-size:56px;margin-bottom:10px">🎭</div>
      <h1 style="font-family:'Playfair Display',serif;font-size:48px;color:#fff;margin:0 0 8px">Padmart</h1>
      <p style="font-size:13px;letter-spacing:.25em;text-transform:uppercase;color:rgba(200,169,110,.9);margin:0">
        Acting School · Hall Reservations
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown(f"""
        <div class="gcard">
          <div style="font-size:44px;margin-bottom:14px">🎟</div>
          <div style="font-family:'Playfair Display',serif;font-size:22px;color:var(--wine);margin-bottom:10px">
            {"I'm a Guest" if not FA else "مهمان هستم"}
          </div>
          <div style="font-size:13px;color:var(--muted);line-height:1.7;margin-bottom:0">
            {"Book a hall, view and manage your own reservations"
             if not FA else "رزرو سالن، مشاهده و مدیریت رزروهای خودم"}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter as Guest →" if not FA else "ورود به عنوان مهمان ←",
                     key="btn_guest", use_container_width=True):
            go("guest")

    with c2:
        st.markdown(f"""
        <div class="gcard-owner">
          <div style="font-size:44px;margin-bottom:14px">👑</div>
          <div style="font-family:'Playfair Display',serif;font-size:22px;color:#fff;margin-bottom:10px">
            {"Site Owner" if not FA else "مدیر سایت"}
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,.62);line-height:1.7;margin-bottom:0">
            {"Full dashboard — all reservations, analytics & settings"
             if not FA else "داشبورد کامل — همه رزروها، آمار و تنظیمات"}
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("Owner Login →" if not FA else "ورود مدیر ←",
                     key="btn_owner", use_container_width=True):
            go("owner-login")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <p style="text-align:center;font-size:13px;color:var(--muted);margin-top:24px">
      {"Grand Studio · Studio 2 · Choose Duration · Full Refund on Cancellation"
       if not FA else "گرند استودیو · استودیو ۲ · انتخاب مدت · بازپرداخت کامل در صورت لغو"}
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██  PAGE: OWNER LOGIN
# ─────────────────────────────────────────────
elif st.session_state.page == "owner-login":
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button(t("back_home"), key="ol_back"):
        go("gateway")
    st.markdown("</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown(f"""
        <div style="text-align:center;margin:30px 0 24px">
          <div style="font-size:44px;margin-bottom:10px">👑</div>
          <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:var(--wine)">
            {"Owner Login" if not FA else "ورود مدیر"}
          </h2>
          <p style="font-size:14px;color:var(--muted);margin-top:4px">
            {"Enter your password to access the full dashboard"
             if not FA else "رمز عبور خود را برای دسترسی به داشبورد وارد کنید"}
          </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("owner_login_form"):
            pw = st.text_input(t("owner_pass_lbl"), type="password", placeholder="••••••••")
            submitted = st.form_submit_button(t("owner_login_btn"), use_container_width=True)
            if submitted:
                if pw == st.session_state.owner_pass:
                    st.session_state.owner_auth = True
                    go("owner")
                else:
                    st.markdown('<div class="msg-err">⚠ ' +
                                ("Incorrect password." if not FA else "رمز عبور نادرست است.") +
                                "</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <p style="text-align:center;font-size:12px;color:var(--muted);margin-top:14px">
          {t("owner_hint")}
        </p>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██  PAGE: GUEST
# ─────────────────────────────────────────────
elif st.session_state.page == "guest":

    # top bar
    nav1, nav2 = st.columns([5, 1])
    with nav2:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button(t("logout").replace("Dashboard", "Guest") if not FA else "← خروج",
                     key="g_exit"):
            go("gateway")
        st.markdown("</div>", unsafe_allow_html=True)

    # hero
    st.markdown(f"""
    <div class="hero">
      <div class="hero-badge">🎭 {"Now Accepting Reservations" if not FA else "پذیرش رزرو آغاز شد"}</div>
      <h1>{"Reserve Your Stage,<br>Perfect Your Craft" if not FA else "صحنه خود را رزرو کنید،<br>هنرتان را به کمال برسانید"}</h1>
      <p>{"Choose your duration, pick a time slot and confirm. Full refund on cancellation."
          if not FA else "مدت زمان را انتخاب کنید، بازه زمانی را مشخص کنید و تأیید کنید. بازپرداخت کامل در صورت لغو."}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_book, tab_myres = st.tabs([t("page_book"), t("page_myres")])

    # ── TAB: BOOK ──
    with tab_book:
        left, right = st.columns([1.3, 0.85], gap="medium")

        with left:
            st.markdown(f"""
            <div class="eyebrow">{"Hall Reservations" if not FA else "رزرو سالن"}</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:24px;margin-bottom:18px">
              {"Book a Rehearsal Hall" if not FA else "رزرو سالن تمرین"}
            </h2>
            """, unsafe_allow_html=True)

            with st.form("guest_book_form", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input(t("your_name"), placeholder="Sara Mohammadi", key="g_name")
                with c2:
                    email = st.text_input(t("email"), placeholder="sara@email.com", key="g_email")

                bdate = st.date_input(t("date_lbl"),
                                      min_value=date.today(),
                                      max_value=date.today() + timedelta(days=60),
                                      value=date.today() + timedelta(days=1),
                                      key="g_date")

                # Hall selection
                st.markdown(f"**{t('choose_hall')}**")
                hc1, hc2 = st.columns(2)
                with hc1:
                    h = HALLS["grand"]
                    sel = st.session_state.g_hall == "grand"
                    st.markdown(f"""
                    <div class="hall-card {'sel' if sel else ''}">
                      <div style="font-size:24px;margin-bottom:6px">{h['icon']}</div>
                      <div style="font-family:'Playfair Display',serif;font-size:17px;color:var(--wine)">
                        {h['name_fa'] if FA else h['name_en']}
                      </div>
                      <div style="font-size:11px;color:var(--muted);margin-top:3px">
                        {h['desc_fa'] if FA else h['desc_en']}
                      </div>
                      <div class="hall-price">150,000 تومان/hr</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.form_submit_button(t("selected") if sel else t("select") + " Grand",
                                            use_container_width=True):
                        st.session_state.g_hall = "grand"
                        st.session_state.g_start = None
                        st.rerun()
                with hc2:
                    h = HALLS["studio2"]
                    sel = st.session_state.g_hall == "studio2"
                    st.markdown(f"""
                    <div class="hall-card {'sel' if sel else ''}">
                      <div style="font-size:24px;margin-bottom:6px">{h['icon']}</div>
                      <div style="font-family:'Playfair Display',serif;font-size:17px;color:var(--wine)">
                        {h['name_fa'] if FA else h['name_en']}
                      </div>
                      <div style="font-size:11px;color:var(--muted);margin-top:3px">
                        {h['desc_fa'] if FA else h['desc_en']}
                      </div>
                      <div class="hall-price">80,000 تومان/hr</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.form_submit_button(t("selected") if sel else t("select") + " Studio 2",
                                            use_container_width=True):
                        st.session_state.g_hall = "studio2"
                        st.session_state.g_start = None
                        st.rerun()

                # Duration
                st.markdown(f"**{t('duration')}**")
                dur_cols = st.columns(6)
                for i, d in enumerate([1,2,3,4,5,6]):
                    with dur_cols[i]:
                        lbl = f"{d}{'h' if not FA else 'س'}"
                        if st.form_submit_button(
                            ("✓ " if st.session_state.g_dur == d else "") + lbl,
                            use_container_width=True):
                            st.session_state.g_dur = d
                            st.session_state.g_start = None
                            st.rerun()

                # Time slots
                st.markdown(f"**{t('start_slot')}**")
                date_str = str(bdate)
                hall_key = st.session_state.g_hall
                dur = st.session_state.g_dur
                taken_hours = booked_hours(hall_key, date_str)

                slot_html = '<div class="slot-grid">'
                for sh in SLOT_STARTS:
                    end = sh + dur
                    label = f"{sh:02d}:00–{end:02d}:00"
                    fits = end <= 21 and can_book(hall_key, date_str, sh, dur)
                    fully_taken = not can_book(hall_key, date_str, sh, 1)
                    is_sel = st.session_state.g_start == sh
                    if is_sel:
                        cls = "slot-btn sel"
                    elif fits:
                        cls = "slot-btn avail"
                    elif fully_taken:
                        cls = "slot-btn taken"
                    else:
                        cls = "slot-btn partial"
                    slot_html += f'<div class="{cls}">{label}</div>'
                slot_html += "</div>"
                st.markdown(slot_html, unsafe_allow_html=True)

                # slot selector (hidden but functional)
                avail_slots = [sh for sh in SLOT_STARTS
                               if sh + dur <= 21 and can_book(hall_key, date_str, sh, dur)]
                if avail_slots:
                    sel_options = {f"{sh:02d}:00–{sh+dur:02d}:00": sh for sh in avail_slots}
                    chosen_label = st.selectbox(
                        t("start_slot"),
                        options=list(sel_options.keys()),
                        label_visibility="collapsed",
                        key="g_slot_sel"
                    )
                    st.session_state.g_start = sel_options[chosen_label]
                else:
                    st.warning("No available slots for this hall/date/duration." if not FA
                               else "بازه‌ای موجود نیست.")
                    st.session_state.g_start = None

                # Summary strip
                hall = HALLS[st.session_state.g_hall]
                hall_name = hall["name_fa"] if FA else hall["name_en"]
                total = hall["price"] * dur
                slot_disp = (f"{st.session_state.g_start:02d}:00–"
                             f"{st.session_state.g_start+dur:02d}:00"
                             if st.session_state.g_start is not None else "—")
                st.markdown(f"""
                <div class="summary-strip">
                  <div>
                    <div style="font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#9b7250">{t('summary_hall')}</div>
                    <div style="font-size:13px;color:#5e4d46;margin-top:3px">{hall_name} · {slot_disp}</div>
                  </div>
                  <div style="text-align:right">
                    <div style="font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#9b7250">{t('summary_price')}</div>
                    <div style="font-family:'Playfair Display',serif;font-size:22px;color:var(--wine);margin-top:2px">{fmt(total) if st.session_state.g_start else '—'}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                submitted = st.form_submit_button(t("confirm_btn"), use_container_width=True)

            # handle booking outside form to show messages
            if submitted:
                err = None
                if not name.strip():
                    err = "⚠ " + ("Please enter your name." if not FA else "لطفاً نام خود را وارد کنید.")
                elif not email.strip() or "@" not in email:
                    err = "⚠ " + ("Please enter a valid email." if not FA else "لطفاً یک ایمیل معتبر وارد کنید.")
                elif st.session_state.g_start is None:
                    err = "⚠ " + ("Please select a time slot." if not FA else "لطفاً یک بازه زمانی انتخاب کنید.")
                elif not can_book(hall_key, date_str, st.session_state.g_start, dur):
                    err = "⚠ " + ("This slot is no longer available." if not FA else "این بازه دیگر موجود نیست.")
                elif len([r for r in st.session_state.reservations
                          if r["email"] == email.strip().lower() and r["status"] == "active"]) >= 3:
                    err = "⚠ " + ("Max 3 active bookings per email." if not FA else "حداکثر ۳ رزرو فعال برای هر ایمیل.")

                if err:
                    st.markdown(f'<div class="msg-err">{err}</div>', unsafe_allow_html=True)
                else:
                    hall = HALLS[st.session_state.g_hall]
                    sl = slot_label(st.session_state.g_start, dur)
                    st.session_state.reservations.append({
                        "id":         gen_id(),
                        "name":       name.strip(),
                        "email":      email.strip().lower(),
                        "hall":       st.session_state.g_hall,
                        "hall_en":    hall["name_en"],
                        "hall_fa":    hall["name_fa"],
                        "date":       date_str,
                        "start_hour": st.session_state.g_start,
                        "duration":   dur,
                        "slot_label": sl,
                        "price":      hall["price"] * dur,
                        "status":     "active",
                        "booked_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                    })
                    st.session_state.g_start = None
                    ok_msg = ("✓ Reservation confirmed! Check My Reservations tab."
                              if not FA else "✓ رزرو تأیید شد! تب رزروهای من را ببینید.")
                    st.markdown(f'<div class="msg-ok">{ok_msg}</div>', unsafe_allow_html=True)
                    st.balloons()

        with right:
            # how it works
            st.markdown(f"""
            <div class="panel-dark">
              <div class="eyebrow eyebrow-light">{"How It Works" if not FA else "نحوه عملکرد"}</div>
              <div style="font-family:'Playfair Display',serif;font-size:19px;margin:6px 0 14px">
                {"Simple Steps" if not FA else "مراحل ساده"}
              </div>
              <div style="display:flex;flex-direction:column;gap:10px;font-size:12px;color:rgba(255,255,255,.72);line-height:1.65">
                <div style="display:flex;gap:8px"><span style="color:var(--gold);font-weight:700;flex-shrink:0">01</span><span>{"Pick a hall and date." if not FA else "سالن و تاریخ را انتخاب کنید."}</span></div>
                <div style="display:flex;gap:8px"><span style="color:var(--gold);font-weight:700;flex-shrink:0">02</span><span>{"Choose how many hours (1–6h)." if not FA else "تعداد ساعت مورد نیاز را انتخاب کنید (۱ تا ۶ ساعت)."}</span></div>
                <div style="display:flex;gap:8px"><span style="color:var(--gold);font-weight:700;flex-shrink:0">03</span><span>{"Select an available time slot." if not FA else "یک بازه شروع موجود را انتخاب کنید."}</span></div>
                <div style="display:flex;gap:8px"><span style="color:var(--gold);font-weight:700;flex-shrink:0">04</span><span>{"Confirm & pay. Cancel anytime for a full refund." if not FA else "تأیید و پرداخت کنید. هر زمان لغو کنید — بازپرداخت کامل."}</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # hall details
            st.markdown(f"""
            <div class="panel">
              <div class="eyebrow" style="margin-bottom:12px">{"Hall Details" if not FA else "مشخصات سالن‌ها"}</div>
              <div style="display:flex;gap:10px;margin-bottom:12px">
                <div style="width:36px;height:36px;border-radius:10px;background:#f1dfd1;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">🎪</div>
                <div>
                  <div style="font-weight:600;font-size:13px">{"Grand Studio" if not FA else "گرند استودیو"}</div>
                  <div style="font-size:11px;color:var(--muted)">{"120 seats · Pro lighting · Backstage" if not FA else "۱۲۰ نفر · نور حرفه‌ای · پشت صحنه"}</div>
                  <div style="font-size:13px;font-weight:700;color:var(--wine);margin-top:2px">150,000 تومان/hr</div>
                </div>
              </div>
              <div style="display:flex;gap:10px">
                <div style="width:36px;height:36px;border-radius:10px;background:#f1dfd1;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">🎭</div>
                <div>
                  <div style="font-weight:600;font-size:13px">{"Studio 2" if not FA else "استودیو ۲"}</div>
                  <div style="font-size:11px;color:var(--muted)">{"30 seats · Mirrors · Sound system" if not FA else "۳۰ نفر · آینه · سیستم صوتی"}</div>
                  <div style="font-size:13px;font-weight:700;color:var(--wine);margin-top:2px">80,000 تومان/hr</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB: MY RESERVATIONS ──
    with tab_myres:
        st.markdown(f"""
        <div class="panel">
          <div class="eyebrow">{"Your Bookings Only" if not FA else "فقط رزروهای شما"}</div>
          <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:10px">{t("my_res_title")}</h2>
          <p style="font-size:13px;color:var(--muted);margin-bottom:14px">{t("my_res_note")}</p>
        </div>
        """, unsafe_allow_html=True)

        filter_email = st.text_input(
            "Email", placeholder="sara@email.com",
            label_visibility="collapsed", key="g_filter_email"
        )
        if st.button(t("view_btn"), key="g_view_btn"):
            st.rerun()

        if filter_email.strip():
            mine = [r for r in st.session_state.reservations
                    if r["email"] == filter_email.strip().lower()]
            mine.sort(key=lambda r: r["date"], reverse=True)

            if not mine:
                st.markdown(f"""
                <div style="text-align:center;padding:48px 20px;background:var(--paper);border:2px dashed #d7c5b4;border-radius:20px;margin-top:16px">
                  <div style="font-size:36px;margin-bottom:10px">🎟</div>
                  <div style="font-family:'Playfair Display',serif;font-size:18px;margin-bottom:6px">
                    {"No reservations found" if not FA else "رزروی یافت نشد"}
                  </div>
                  <div style="font-size:13px;color:var(--muted)">
                    {"No bookings found for this email." if not FA else "هیچ رزروی برای این ایمیل یافت نشد."}
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for r in mine:
                    cancelled = r["status"] == "cancelled"
                    hn = r["hall_fa"] if FA else r["hall_en"]
                    st_badge = f'<span class="badge-{"cancelled" if cancelled else "active"}">{t("status_cancel") if cancelled else t("status_active")}</span>'
                    st.markdown(f"""
                    <div class="res-card {'cancelled' if cancelled else ''}">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap">
                        <div>
                          <div class="res-id">{r['id']}</div>
                          <div class="res-hall">{hn}</div>
                          {st_badge}
                        </div>
                        <div class="res-price">{fmt(r['price'])}</div>
                      </div>
                      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px;font-size:12px">
                        <div><div style="font-size:9px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#9b7250">{t('guest_lbl')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['name']}</div></div>
                        <div><div style="font-size:9px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#9b7250">{t('date_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['date']}</div></div>
                        <div><div style="font-size:9px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#9b7250">{t('slot_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['slot_label']}</div></div>
                        <div><div style="font-size:9px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#9b7250">{t('dur_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['duration']}h</div></div>
                      </div>
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding-top:10px;border-top:1px solid #eee0d3">
                        <span style="font-size:11px;color:var(--muted)">{t('cancel_note') if cancelled else t('active_note')}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if not cancelled:
                        st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
                        if st.button(t("cancel_btn"), key=f"g_cancel_{r['id']}"):
                            cancel_res(r["id"])
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:48px 20px;background:var(--paper);border:2px dashed #d7c5b4;border-radius:20px;margin-top:16px">
              <div style="font-size:36px;margin-bottom:10px">🎟</div>
              <div style="font-family:'Playfair Display',serif;font-size:18px;margin-bottom:6px">
                {"Enter your email above" if not FA else "ایمیل خود را وارد کنید"}
              </div>
              <div style="font-size:13px;color:var(--muted)">
                {"Your reservations will appear here." if not FA else "رزروهای شما اینجا نمایش داده می‌شود."}
              </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██  PAGE: OWNER DASHBOARD
# ─────────────────────────────────────────────
elif st.session_state.page == "owner":
    if not st.session_state.owner_auth:
        go("owner-login")

    # top bar
    nav1, nav2 = st.columns([5, 1])
    with nav2:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button(t("logout"), key="o_logout"):
            st.session_state.owner_auth = False
            go("gateway")
        st.markdown("</div>", unsafe_allow_html=True)

    # hero
    st.markdown(f"""
    <div class="owner-hero">
      <div class="owner-badge">👑 {"Owner Dashboard" if not FA else "داشبورد مدیر"}</div>
      <h1>{"Full Control. All Reservations." if not FA else "کنترل کامل. همه رزروها."}</h1>
      <p>{"Manage all bookings, view live analytics and configure settings."
          if not FA else "تمام رزروها را مدیریت کنید، آمار زنده ببینید و تنظیمات را پیکربندی کنید."}</p>
    </div>
    """, unsafe_allow_html=True)

    # stats
    all_res = st.session_state.reservations
    active_res = [r for r in all_res if r["status"] == "active"]
    revenue = sum(r["price"] for r in active_res)
    unique_guests = len(set(r["email"] for r in all_res))

    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl in [
        (s1, len(all_res),      t("total_bk")),
        (s2, len(active_res),   t("active_bk")),
        (s3, f"{revenue:,}",    t("revenue")),
        (s4, unique_guests,     t("unique_g")),
    ]:
        col.markdown(f"""
        <div class="stat-card">
          <div class="stat-num">{val}</div>
          <div class="stat-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    tab_charts, tab_allres, tab_settings = st.tabs([
        t("page_charts"), t("page_allres"), t("page_settings")
    ])

    # ── TAB: CHARTS ──
    with tab_charts:
        import plotly.graph_objects as pgo
        
        from collections import Counter

        WINE = "#6d1f2a"; GOLD = "#b88a4a"; CREAM = "#f5eadf"

        cc1, cc2, cc3 = st.columns(3)

        # Bar: bookings by guest name
        with cc1:
            name_counts = Counter(r["name"] for r in active_res)
            fig = pgo.Figure(pgo.Bar(
                x=list(name_counts.keys()), y=list(name_counts.values()),
                marker=dict(color=list(name_counts.values()),
                            colorscale=[[0,CREAM],[0.5,GOLD],[1,WINE]],
                            line=dict(color=WINE, width=1)),
                text=list(name_counts.values()), textposition="outside",
                textfont=dict(color=WINE, size=12),
                hovertemplate="<b>%{x}</b><br>Bookings: %{y}<extra></extra>",
            ))
            fig.update_layout(title=dict(text=t("bar_title"), font=dict(size=14, color=WINE), x=.5),
                              plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                              xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#e7d8c6"),
                              margin=dict(t=40,b=20,l=10,r=10), height=280,
                              font=dict(family="DM Sans"))
            st.plotly_chart(fig, use_container_width=True)

        # Pie: hall usage
        with cc2:
            grand_c = sum(1 for r in active_res if r["hall"] == "grand")
            s2_c    = sum(1 for r in active_res if r["hall"] == "studio2")
            labels  = [HALLS["grand"]["name_fa"] if FA else HALLS["grand"]["name_en"],
                       HALLS["studio2"]["name_fa"] if FA else HALLS["studio2"]["name_en"]]
            fig = pgo.Figure(pgo.Pie(
                labels=labels, values=[grand_c, s2_c],
                marker=dict(colors=[WINE, GOLD], line=dict(color="#fffaf3", width=3)),
                hole=0.42, textfont=dict(size=12),
                hovertemplate="<b>%{label}</b><br>%{value} bookings<extra></extra>",
            ))
            fig.update_layout(title=dict(text=t("pie_title"), font=dict(size=14, color=WINE), x=.5),
                              plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                              legend=dict(font=dict(size=11)),
                              margin=dict(t=40,b=10,l=10,r=10), height=280,
                              font=dict(family="DM Sans"))
            st.plotly_chart(fig, use_container_width=True)

        # Line: bookings over time
        with cc3:
            date_counts = Counter(r["date"] for r in active_res)
            dates = sorted(date_counts.keys())
            counts = [date_counts[d] for d in dates]
            fig = pgo.Figure(pgo.Scatter(
                x=dates, y=counts,
                mode="lines+markers",
                line=dict(color=WINE, width=2.5),
                marker=dict(color=WINE, size=8, line=dict(color="#fffaf3", width=2)),
                fill="tozeroy", fillcolor="rgba(109,31,42,.08)",
                hovertemplate="<b>%{x}</b><br>Bookings: %{y}<extra></extra>",
            ))
            fig.update_layout(title=dict(text=t("line_title"), font=dict(size=14, color=WINE), x=.5),
                              plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                              xaxis=dict(showgrid=False),
                              yaxis=dict(gridcolor="#e7d8c6"),
                              margin=dict(t=40,b=20,l=10,r=10), height=280,
                              font=dict(family="DM Sans"))
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB: ALL RESERVATIONS ──
    with tab_allres:
        search = st.text_input("🔍", placeholder=t("search_ph"),
                               label_visibility="collapsed", key="o_search")
        filtered = [r for r in sorted(all_res, key=lambda x: x["date"], reverse=True)
                    if not search or
                    search.lower() in r["name"].lower() or
                    search.lower() in r["email"]]

        if not filtered:
            st.markdown(f"""
            <div style="text-align:center;padding:44px;background:var(--paper);border:2px dashed #d7c5b4;border-radius:20px">
              <div style="font-size:34px;margin-bottom:10px">🎟</div>
              <div style="font-family:'Playfair Display',serif;font-size:18px">
                {"No Reservations Yet" if not FA else "هنوز رزروی ثبت نشده"}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for r in filtered:
                cancelled = r["status"] == "cancelled"
                hn = r["hall_fa"] if FA else r["hall_en"]
                st_badge = f'<span class="badge-{"cancelled" if cancelled else "active"}">{t("status_cancel") if cancelled else t("status_active")}</span>'
                st.markdown(f"""
                <div class="res-card {'cancelled' if cancelled else ''}">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap">
                    <div>
                      <div class="res-id">{r['id']}</div>
                      <div class="res-hall">{hn}</div>
                      {st_badge}
                    </div>
                    <div class="res-price">{fmt(r['price'])}</div>
                  </div>
                  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:12px;font-size:12px">
                    <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{t('guest_lbl')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['name']}</div></div>
                    <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">Email</div><div style="margin-top:2px;font-size:11px;color:#4b3932;word-break:break-all">{r['email']}</div></div>
                    <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{t('date_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['date']}</div></div>
                    <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{t('slot_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['slot_label']}</div></div>
                    <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{t('dur_col')}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['duration']}h</div></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding-top:10px;border-top:1px solid #eee0d3">
                    <span style="font-size:11px;color:var(--muted)">{t('cancel_note') if cancelled else t('active_note')}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if not cancelled:
                    st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
                    if st.button(t("cancel_btn"), key=f"o_cancel_{r['id']}"):
                        cancel_res(r["id"])
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB: SETTINGS ──
    with tab_settings:
        set1, set2 = st.columns(2, gap="large")

        with set1:
            st.markdown(f"""
            <div class="eyebrow">{"Security" if not FA else "امنیت"}</div>
            <h3 style="font-family:'Playfair Display',serif;font-size:20px;margin-bottom:16px">{t("change_pass")}</h3>
            """, unsafe_allow_html=True)
            with st.form("owner_pass_form"):
                np1 = st.text_input(t("new_pass"), type="password")
                np2 = st.text_input(t("confirm_pass"), type="password")
                if st.form_submit_button(t("save_pass"), use_container_width=True):
                    if len(np1) < 6:
                        st.markdown('<div class="msg-err">⚠ ' + ("Min 6 characters." if not FA else "حداقل ۶ کاراکتر.") + "</div>", unsafe_allow_html=True)
                    elif np1 != np2:
                        st.markdown('<div class="msg-err">⚠ ' + ("Passwords do not match." if not FA else "رمزها یکسان نیستند.") + "</div>", unsafe_allow_html=True)
                    else:
                        st.session_state.owner_pass = np1
                        st.markdown('<div class="msg-ok">✓ ' + ("Password updated." if not FA else "رمز عبور به‌روز شد.") + "</div>", unsafe_allow_html=True)

        with set2:
            st.markdown(f"""
            <div class="eyebrow">{"Email Settings" if not FA else "تنظیمات ایمیل"}</div>
            <h3 style="font-family:'Playfair Display',serif;font-size:20px;margin-bottom:16px">{t("smtp_title")}</h3>
            """, unsafe_allow_html=True)
            with st.form("smtp_form"):
                smtp = st.session_state.smtp
                h = st.text_input(t("smtp_host"), value=smtp["host"], placeholder="smtp.gmail.com")
                c1, c2 = st.columns(2)
                with c1: p = st.number_input(t("smtp_port"), value=smtp["port"], min_value=1, max_value=9999)
                with c2: u = st.text_input(t("smtp_user"), value=smtp["user"], placeholder="you@gmail.com")
                pw = st.text_input(t("smtp_pass"), value=smtp["pass"], type="password")
                st.caption(t("smtp_note"))
                if st.form_submit_button(t("save_smtp"), use_container_width=True):
                    st.session_state.smtp = {"host": h, "port": int(p), "user": u, "pass": pw}
                    st.markdown('<div class="msg-ok">✓ ' + ("Email settings saved." if not FA else "تنظیمات ایمیل ذخیره شد.") + "</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="border-top:1px solid var(--line);padding:20px 0;text-align:center;margin-top:40px">
  <span style="font-family:'Playfair Display',serif;font-size:15px;color:var(--wine)">Padmart</span>
  <span style="color:#c8aa92;margin:0 8px">·</span>
  <span style="font-size:13px;color:var(--muted)">{"Acting School · Hall Reservations" if not FA else "مدرسه بازیگری · رزرو سالن"}</span>
  <span style="color:#c8aa92;margin:0 8px">·</span>
  <span style="font-size:13px;color:var(--muted)">{"Grand Studio: 150,000 تومان  |  Studio 2: 80,000 تومان" if not FA else "گرند استودیو: ۱۵۰،۰۰۰ تومان  |  استودیو ۲: ۸۰،۰۰۰ تومان"}</span>
</div>
""", unsafe_allow_html=True)
