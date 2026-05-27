import streamlit as st
from datetime import date, datetime, timedelta
import uuid
import plotly.graph_objects as go
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ══════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="StagePass — Acting School",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════
T = {
    "en": {
        "brand":            "StagePass",
        "brand_sub":        "Acting School · Hall Reservations",
        "tab_book":         "📅  Book a Hall",
        "tab_res":          "📋  Reservations Chart",
        "tab_acc":          "👤  Account",
        "tab_settings":     "⚙️  Settings",
        "hero_badge":       "🎭  Now Accepting Reservations",
        "hero_title":       "Reserve Your Stage,\nPerfect Your Craft",
        "hero_desc":        "Book world-class rehearsal halls at our acting school. Whether you're preparing a solo piece or directing a full cast, we have the space for you.",
        "hero_note":        "Available 7 days a week · Instant confirmation · Full refund on cancellation",
        "book_eyebrow":     "Hall Reservations",
        "book_title":       "Book a Rehearsal Hall",
        "book_desc":        "Select your preferred hall, date and fill in your details to reserve instantly.",
        "student_name":     "Student Name",
        "student_email":    "Email Address",
        "res_date":         "Reservation Date",
        "choose_hall":      "Choose a Hall",
        "small_hall":       "Studio A",
        "small_sub":        "Small Hall",
        "small_desc":       "Intimate rehearsal space for solo acts & small ensembles. Up to 30 students.",
        "large_hall":       "Grand Stage",
        "large_sub":        "Large Hall",
        "large_desc":       "Full production stage with lighting rig — ideal for full cast rehearsals. Up to 120 students.",
        "select_small":     "Select Studio A",
        "select_large":     "Select Grand Stage",
        "selected_hall":    "Selected Hall",
        "session_price":    "Session Price",
        "time_slot":        "Time Slot",
        "confirm_pay":      "✦ Confirm Reservation & Pay",
        "chart_title":      "Reservations by Student",
        "chart_eyebrow":    "Analytics Dashboard",
        "chart_desc":       "Visual overview of all hall bookings across students.",
        "filter_email":     "🔍 Filter by your email address",
        "cancel_btn":       "Cancel & Refund",
        "no_res":           "No reservations yet",
        "no_res_sub":       "Head to the Booking tab to reserve your first hall.",
        "active":           "✓ Confirmed",
        "cancelled":        "✕ Cancelled",
        "acc_eyebrow":      "New Student",
        "acc_title":        "Create Account",
        "acc_desc":         "Join our acting school and start booking rehearsal halls instantly.",
        "full_name":        "Full Name",
        "student_id_label": "Student ID",  
        "starting_bal":     "Starting Balance (Tomans)",
        "create_acc":       "✦ Create My Account",
        "signin_title":     "Sign In",
        "signin_desc":      "Enter your Student ID to access your account.",
        "signin_btn":       "Enter the Stage →",
        "demo_ids":         "Demo Student IDs",
        "reg_students":     "Registered Students",
        "active_bookings":  "Active Bookings",
        "total_bookings":   "Total Bookings",
        "hall_details":     "Hall Details",
        "settings_title":   "Language Settings",
        "lang_label":       "Choose Language",
        "email_sent":       "✓ Confirmation email sent to",
        "email_fail":       "⚠ Could not send email (check SMTP settings)",
        "email_subject":    "Your Hall Reservation Confirmation — StagePass",
        "err_name":         "⚠ Please enter your name.",
        "err_email":        "⚠ Please enter a valid email address.",
        "err_noslot":       "⚠ No time slots available for this date.",
        "err_limit":        "⚠ Reservation limit reached (3 active). Please cancel an older booking first.",
        "err_id_taken":     "⚠ This Student ID is already taken.",
        "err_id_empty":     "⚠ Please choose a Student ID.",
        "ok_booked":        "✓ Reservation confirmed for",
        "ok_account":       "✓ Account created! Welcome",
        "ok_signin":        "✓ Welcome back",
        "err_signin":       "⚠ Student ID not found.",
        "footer_small":     "Small Hall: 80,000 Tomans",
        "footer_large":     "Large Hall: 150,000 Tomans",
        "bar_chart_title":  "Bookings per Student",
        "pie_chart_title":  "Hall Usage Share",
        "line_chart_title": "Bookings Over Time",
        "student_lbl":      "Student",
        "date_lbl":         "Date",
        "time_lbl":         "Time Slot",
        "price_lbl":        "Price Paid",
        "booked_lbl":       "Booked On",
        "res_id_lbl":       "Reservation ID",
        "smtp_host":        "SMTP Host (e.g. smtp.gmail.com)",
        "smtp_port":        "SMTP Port",
        "smtp_user":        "Sender Email",
        "smtp_pass":        "App Password",
        "smtp_save":        "Save Email Settings",
        "email_settings":   "Email Settings (for sending confirmations)",
        "no_slots":         "No available slots",
    },
    "fa": {
        "brand":            "استیج‌پس",
        "brand_sub":        "مدرسه بازیگری · رزرو سالن",
        "tab_book":         "📅  رزرو سالن",
        "tab_res":          "📋  نمودار رزروها",
        "tab_acc":          "👤  حساب کاربری",
        "tab_settings":     "⚙️  تنظیمات",
        "hero_badge":       "🎭  پذیرش رزرو آغاز شد",
        "hero_title":       "صحنه خود را رزرو کنید\nهنرتان را به کمال برسانید",
        "hero_desc":        "سالن‌های تمرین حرفه‌ای مدرسه بازیگری ما را رزرو کنید. چه برای تمرین انفرادی، چه برای تمرین گروهی، سالن مناسب شما را داریم.",
        "hero_note":        "هفت روز هفته · تأیید فوری · بازپرداخت کامل در صورت لغو",
        "book_eyebrow":     "رزرو سالن",
        "book_title":       "رزرو سالن تمرین",
        "book_desc":        "سالن، تاریخ و اطلاعات خود را وارد کنید تا رزرو فوری انجام شود.",
        "student_name":     "نام هنرجو",
        "student_email":    "آدرس ایمیل",
        "res_date":         "تاریخ رزرو",
        "choose_hall":      "انتخاب سالن",
        "small_hall":       "استودیو الف",
        "small_sub":        "سالن کوچک",
        "small_desc":       "فضای تمرین صمیمی برای تک‌نفره و گروه‌های کوچک. ظرفیت ۳۰ نفر.",
        "large_hall":       "صحنه بزرگ",
        "large_sub":        "سالن بزرگ",
        "large_desc":       "صحنه حرفه‌ای با تجهیزات نور و صدا — ایده‌آل برای تمرین گروه کامل. ظرفیت ۱۲۰ نفر.",
        "select_small":     "انتخاب استودیو الف",
        "select_large":     "انتخاب صحنه بزرگ",
        "selected_hall":    "سالن انتخابی",
        "session_price":    "هزینه جلسه",
        "time_slot":        "بازه زمانی",
        "confirm_pay":      "✦ تأیید رزرو و پرداخت",
        "chart_title":      "رزروها بر اساس هنرجو",
        "chart_eyebrow":    "داشبورد آماری",
        "chart_desc":       "نمای کلی از رزروهای سالن برای تمام هنرجویان.",
        "filter_email":     "🔍 جستجو با ایمیل",
        "cancel_btn":       "لغو و بازپرداخت",
        "no_res":           "هنوز رزروی ثبت نشده",
        "no_res_sub":       "به تب رزرو بروید و اولین سالن خود را رزرو کنید.",
        "active":           "✓ تأیید شده",
        "cancelled":        "✕ لغو شده",
        "acc_eyebrow":      "هنرجوی جدید",
        "acc_title":        "ایجاد حساب کاربری",
        "acc_desc":         "به مدرسه بازیگری ما بپیوندید و همین حالا شروع به رزرو سالن کنید.",
        "full_name":        "نام و نام خانوادگی",
        "student_id_label": "شناسه هنرجو",
        "starting_bal":     "موجودی اولیه (تومان)",
        "create_acc":       "✦ ایجاد حساب کاربری",
        "signin_title":     "ورود به حساب",
        "signin_desc":      "شناسه هنرجوی خود را وارد کنید.",
        "signin_btn":       "ورود به صحنه ←",
        "demo_ids":         "شناسه‌های نمونه",
        "reg_students":     "هنرجویان ثبت‌نام‌شده",
        "active_bookings":  "رزروهای فعال",
        "total_bookings":   "کل رزروها",
        "hall_details":     "مشخصات سالن‌ها",
        "settings_title":   "تنظیمات زبان",
        "lang_label":       "انتخاب زبان",
        "email_sent":       "✓ ایمیل تأییدیه ارسال شد به",
        "email_fail":       "⚠ ارسال ایمیل ناموفق بود (تنظیمات SMTP را بررسی کنید)",
        "email_subject":    "تأییدیه رزرو سالن شما — استیج‌پس",
        "err_name":         "⚠ لطفاً نام خود را وارد کنید.",
        "err_email":        "⚠ لطفاً یک آدرس ایمیل معتبر وارد کنید.",
        "err_noslot":       "⚠ بازه زمانی خالی برای این تاریخ وجود ندارد.",
        "err_limit":        "⚠ سقف رزرو (۳ رزرو فعال) پر شده. لطفاً یک رزرو قدیمی را لغو کنید.",
        "err_id_taken":     "⚠ این شناسه قبلاً استفاده شده است.",
        "err_id_empty":     "⚠ لطفاً یک شناسه انتخاب کنید.",
        "ok_booked":        "✓ رزرو تأیید شد برای",
        "ok_account":       "✓ حساب ایجاد شد! خوش آمدید",
        "ok_signin":        "✓ خوش برگشتید",
        "err_signin":       "⚠ شناسه هنرجو یافت نشد.",
        "footer_small":     "سالن کوچک: ۸۰،۰۰۰ تومان",
        "footer_large":     "سالن بزرگ: ۱۵۰،۰۰۰ تومان",
        "bar_chart_title":  "رزرو به تفکیک هنرجو",
        "pie_chart_title":  "سهم استفاده از سالن‌ها",
        "line_chart_title": "روند رزرو در طول زمان",
        "student_lbl":      "هنرجو",
        "date_lbl":         "تاریخ",
        "time_lbl":         "بازه زمانی",
        "price_lbl":        "مبلغ پرداختی",
        "booked_lbl":       "تاریخ ثبت",
        "res_id_lbl":       "شناسه رزرو",
        "smtp_host":        "هاست SMTP (مثلاً smtp.gmail.com)",
        "smtp_port":        "پورت SMTP",
        "smtp_user":        "ایمیل فرستنده",
        "smtp_pass":        "رمز اپ",
        "smtp_save":        "ذخیره تنظیمات ایمیل",
        "email_settings":   "تنظیمات ایمیل (برای ارسال تأییدیه)",
        "no_slots":         "بازه‌ای خالی نیست",
    }
}

# ══════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "students" not in st.session_state:
    st.session_state.students = {
        "S001": {"name": "Emma Larson",    "email": "emma@example.com",  "balance": 500000},
        "S002": {"name": "Luca Moretti",   "email": "luca@example.com",  "balance": 400000},
        "S003": {"name": "Sofia Andersen", "email": "sofia@example.com", "balance": 600000},
    }
if "reservations" not in st.session_state:
    st.session_state.reservations = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "selected_hall" not in st.session_state:
    st.session_state.selected_hall = "Small Hall"
if "smtp" not in st.session_state:
    st.session_state.smtp = {"host": "", "port": 587, "user": "", "pass": ""}

def t(key):
    return T[st.session_state.lang].get(key, key)

def fmt(n):
    return f"{n:,} تومان"

def gen_id():
    return "RES-" + str(uuid.uuid4())[:8].upper()

is_fa = st.session_state.lang == "fa"
dir_attr = 'dir="rtl"' if is_fa else ''
font_fa  = "'Vazirmatn', 'Tahoma', sans-serif" if is_fa else "'DM Sans', sans-serif"

HALLS_DATA = {
    "Small Hall":  {"price": 80000,  "icon": "🎭", "capacity": 30,  "name_key": "small_hall", "sub_key": "small_sub", "desc_key": "small_desc"},
    "Large Hall":  {"price": 150000, "icon": "🎪", "capacity": 120, "name_key": "large_hall", "sub_key": "large_sub", "desc_key": "large_desc"},
}

# ══════════════════════════════════════════
#  EMAIL SENDER
# ══════════════════════════════════════════
def send_confirmation_email(to_email, student_name, hall, res_date, time_slot, price, res_id, lang):
    cfg = st.session_state.smtp
    if not cfg["host"] or not cfg["user"] or not cfg["pass"]:
        return False
    try:
        if lang == "fa":
            subject = f"تأییدیه رزرو سالن — استیج‌پس | {res_id}"
            body = f"""
<div dir="rtl" style="font-family:Tahoma,sans-serif;color:#241817;max-width:560px;margin:auto">
  <div style="background:#6d1f2a;padding:28px 32px;border-radius:16px 16px 0 0;text-align:center">
    <h1 style="color:#fff;font-size:26px;margin:0">🎭 استیج‌پس</h1>
    <p style="color:rgba(255,255,255,.8);margin:6px 0 0;font-size:13px;letter-spacing:.1em">مدرسه بازیگری · رزرو سالن</p>
  </div>
  <div style="background:#fffaf3;padding:32px;border:1px solid #eadccf;border-top:none;border-radius:0 0 16px 16px">
    <p style="font-size:17px;color:#241817">هنرجوی گرامی <strong>{student_name}</strong>،</p>
    <p style="color:#5e4d46;line-height:1.8">رزرو شما با موفقیت ثبت شد. جزئیات رزرو در زیر آمده است:</p>
    <div style="background:#f5eadf;border-radius:12px;padding:20px 24px;margin:20px 0">
      <table style="width:100%;font-size:14px;color:#4b3932;border-collapse:collapse">
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">شناسه رزرو</td><td style="text-align:left;font-family:monospace">{res_id}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">سالن</td><td style="text-align:left">{t('small_hall') if hall=='Small Hall' else t('large_hall')}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">تاریخ</td><td style="text-align:left">{res_date}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">بازه زمانی</td><td style="text-align:left">{time_slot}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">مبلغ پرداختی</td><td style="text-align:left;color:#6d1f2a;font-weight:700">{fmt(price)}</td></tr>
      </table>
    </div>
    <p style="color:#7f6b62;font-size:13px">در صورت نیاز به لغو رزرو، از طریق پنل کاربری اقدام کنید. بازپرداخت کامل انجام خواهد شد.</p>
    <p style="color:#6d1f2a;font-weight:600;margin-top:20px">موفق باشید روی صحنه 🎭</p>
  </div>
</div>"""
        else:
            subject = f"Your Hall Reservation Confirmation — StagePass | {res_id}"
            body = f"""
<div style="font-family:'DM Sans',sans-serif;color:#241817;max-width:560px;margin:auto">
  <div style="background:#6d1f2a;padding:28px 32px;border-radius:16px 16px 0 0;text-align:center">
    <h1 style="color:#fff;font-size:26px;margin:0">🎭 StagePass</h1>
    <p style="color:rgba(255,255,255,.8);margin:6px 0 0;font-size:13px;letter-spacing:.1em">Acting School · Hall Reservations</p>
  </div>
  <div style="background:#fffaf3;padding:32px;border:1px solid #eadccf;border-top:none;border-radius:0 0 16px 16px">
    <p style="font-size:17px;color:#241817">Dear <strong>{student_name}</strong>,</p>
    <p style="color:#5e4d46;line-height:1.8">Your reservation has been confirmed. Here are your booking details:</p>
    <div style="background:#f5eadf;border-radius:12px;padding:20px 24px;margin:20px 0">
      <table style="width:100%;font-size:14px;color:#4b3932;border-collapse:collapse">
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">Reservation ID</td><td style="text-align:right;font-family:monospace">{res_id}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">Hall</td><td style="text-align:right">{hall}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">Date</td><td style="text-align:right">{res_date}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">Time Slot</td><td style="text-align:right">{time_slot}</td></tr>
        <tr><td style="padding:8px 0;color:#9b7250;font-weight:600">Amount Paid</td><td style="text-align:right;color:#6d1f2a;font-weight:700">{fmt(price)}</td></tr>
      </table>
    </div>
    <p style="color:#7f6b62;font-size:13px">To cancel your reservation and receive a full refund, please use the student portal.</p>
    <p style="color:#6d1f2a;font-weight:600;margin-top:20px">Break a leg on stage! 🎭</p>
  </div>
</div>"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = cfg["user"]
        msg["To"]      = to_email
        msg.attach(MIMEText(body, "html", "utf-8"))
        with smtplib.SMTP(cfg["host"], int(cfg["port"])) as server:
            server.starttls()
            server.login(cfg["user"], cfg["pass"])
            server.sendmail(cfg["user"], to_email, msg.as_string())
        return True
    except Exception:
        return False

# ══════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&family=Vazirmatn:wght@400;500;600;700&display=swap');
*,*::before,*::after{{box-sizing:border-box}}
html,body,[data-testid="stAppViewContainer"]{{
  background:linear-gradient(135deg,#f6ecdf 0%,#fbf7f0 45%,#f1e2d2 100%) !important;
  font-family:{font_fa};
  color:#241817;
  direction:{'rtl' if is_fa else 'ltr'};
}}
[data-testid="stAppViewContainer"]::before{{
  content:"";position:fixed;inset:0;
  background-image:radial-gradient(rgba(36,24,23,.06) 1px,transparent 1px);
  background-size:18px 18px;opacity:.18;pointer-events:none;z-index:0;
}}
[data-testid="stHeader"]{{background:rgba(255,249,240,0.92)!important;border-bottom:1px solid #eadccf}}
[data-testid="stSidebar"]{{display:none}}
section[data-testid="stMain"]{{padding-top:0!important}}
#MainMenu,footer,[data-testid="stToolbar"]{{display:none!important}}
.display{{font-family:'Playfair Display',serif;font-weight:700}}
.navbar{{
  width:100%;background:rgba(255,249,240,0.95);
  border-bottom:1px solid #eadccf;padding:14px 40px;
  display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:999;
}}
.brand-mark{{width:40px;height:40px;border-radius:50%;background:#6d1f2a;color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:18px}}
.brand-name{{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#241817}}
.brand-sub{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#9b7250;margin-top:1px}}
.hero{{
  background:linear-gradient(90deg,rgba(36,24,23,.85),rgba(36,24,23,.3) 55%,rgba(36,24,23,.05)),
             linear-gradient(135deg,#6d1f2a 0%,#3a0e15 100%);
  border-radius:28px;padding:56px 52px;margin:24px 0 20px;
  color:#fff;position:relative;overflow:hidden;
  box-shadow:0 22px 60px rgba(72,16,25,.18);
}}
.hero-badge{{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;
  border-radius:999px;background:#b88a4a;color:#fff;
  font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;margin-bottom:20px}}
.hero h1{{font-family:'Playfair Display',serif;font-size:40px;line-height:1.1;margin:0 0 16px;white-space:pre-line}}
.hero p{{font-size:15px;color:rgba(255,255,255,.85);line-height:1.7;max-width:520px;margin:0}}
.hero-note{{display:flex;align-items:center;gap:8px;margin-top:22px;font-size:13px;color:rgba(255,255,255,.8)}}
.panel{{background:#fffaf3;border:1px solid #eadccf;border-radius:26px;
  padding:32px 28px;box-shadow:0 12px 40px rgba(72,16,25,.08)}}
.panel-dark{{background:#2f1d1a;color:#fff;border-radius:26px;
  padding:28px 26px;box-shadow:0 12px 40px rgba(72,16,25,.12)}}
.eyebrow{{font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#9b7250;margin-bottom:6px}}
.eyebrow-light{{color:#d8b47b}}
.section-title{{font-family:'Playfair Display',serif;font-size:26px;color:#241817;margin:4px 0 8px}}
.section-title-light{{color:#fff}}
.hall-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}}
.hall-card{{border:1px solid #e7d8c6;border-radius:18px;padding:18px;background:#fffdf9;cursor:pointer;transition:.2s ease}}
.hall-card:hover{{transform:translateY(-2px);border-color:#c8aa92}}
.hall-card.selected{{border-color:#6d1f2a;background:#fff7f7;box-shadow:0 8px 24px rgba(109,31,42,.1)}}
.hall-icon-wrap{{width:36px;height:36px;border-radius:50%;background:#f1dfd1;color:#6d1f2a;
  display:flex;align-items:center;justify-content:center;font-size:16px;margin-bottom:10px}}
.hall-title{{font-family:'Playfair Display',serif;font-size:18px;color:#241817;margin-bottom:4px}}
.hall-desc{{font-size:13px;color:#7f6b62;line-height:1.6;margin-bottom:14px}}
.hall-price{{font-size:16px;font-weight:700;color:#6d1f2a}}
.summary-strip{{background:#f5eadf;border-radius:14px;padding:16px 20px;
  display:flex;justify-content:space-between;align-items:center;margin:16px 0}}
.summary-label{{font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#9b7250}}
.summary-value{{font-family:'Playfair Display',serif;font-size:22px;color:#6d1f2a;margin-top:2px}}
.stTextInput>div>div>input,.stDateInput>div>div>input,.stNumberInput>div>div>input{{
  border:1px solid #e7d8c6!important;background:#fffdf9!important;
  border-radius:14px!important;padding:14px 15px!important;
  font-family:{font_fa}!important;font-size:15px!important;color:#241817!important;
}}
.stTextInput>div>div>input:focus{{border-color:#6d1f2a!important;box-shadow:0 0 0 3px rgba(109,31,42,.12)!important}}
label[data-testid="stWidgetLabel"]>div>p{{font-size:14px!important;font-weight:600!important;color:#241817!important}}
.stButton>button{{
  width:100%;background:#6d1f2a!important;color:#fff!important;border:none!important;
  border-radius:16px!important;padding:14px 24px!important;
  font-family:{font_fa}!important;font-size:15px!important;font-weight:600!important;
  box-shadow:0 4px 16px rgba(109,31,42,.22)!important;transition:.2s!important;
}}
.stButton>button:hover{{background:#571821!important;transform:translateY(-1px);box-shadow:0 8px 24px rgba(109,31,42,.28)!important}}
.btn-gold>button{{background:#d1a15b!important;color:#2f1d1a!important;box-shadow:0 4px 16px rgba(184,138,74,.25)!important}}
.btn-gold>button:hover{{background:#c4934d!important}}
.btn-cancel>button{{background:#f2e2e0!important;color:#7b2932!important;box-shadow:none!important;font-size:13px!important;padding:8px 18px!important;border-radius:12px!important}}
.btn-cancel>button:hover{{background:#ead3d0!important}}
.res-card{{background:#fffaf3;border:1px solid #eadccf;border-radius:24px;
  padding:22px;box-shadow:0 8px 24px rgba(72,16,25,.05);margin-bottom:14px;position:relative}}
.res-card.cancelled{{opacity:.68}}
.res-hall{{font-family:'Playfair Display',serif;font-size:22px;color:#2b1c19;margin:6px 0}}
.res-status-active{{display:inline-flex;align-items:center;padding:4px 12px;border-radius:999px;
  background:#ddf0e6;color:#2d7a58;font-size:12px;font-weight:600}}
.res-status-cancelled{{display:inline-flex;align-items:center;padding:4px 12px;border-radius:999px;
  background:#f2e2e0;color:#7b2932;font-size:12px;font-weight:600}}
.res-meta-label{{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:12px}}
.res-meta-value{{font-size:15px;font-weight:500;color:#4b3932;margin-top:2px}}
.res-price{{font-family:'Playfair Display',serif;font-size:26px;color:#6d1f2a}}
.msg-success{{background:#ddf0e6;color:#2d7a58;border-radius:12px;padding:12px 16px;font-size:14px;font-weight:500;margin-top:8px}}
.msg-error{{background:#f2e2e0;color:#7b2932;border-radius:12px;padding:12px 16px;font-size:14px;font-weight:500;margin-top:8px}}
.msg-info{{background:#e8f0fb;color:#1a4a8a;border-radius:12px;padding:12px 16px;font-size:14px;font-weight:500;margin-top:8px}}
hr{{border:none;border-top:1px solid #e7d8c6;margin:20px 0}}
.stTabs [data-baseweb="tab-list"]{{gap:4px;background:transparent;border-bottom:2px solid #e7d8c6}}
.stTabs [data-baseweb="tab"]{{background:transparent!important;border:none!important;
  color:#7f6b62!important;font-family:{font_fa}!important;font-weight:600!important;
  font-size:14px!important;padding:10px 20px!important;border-radius:0!important}}
.stTabs [aria-selected="true"]{{color:#6d1f2a!important;border-bottom:2px solid #6d1f2a!important}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:24px!important}}
.stSelectbox>div>div>div{{border:1px solid #e7d8c6!important;background:#fffdf9!important;
  border-radius:14px!important;font-family:{font_fa}!important;color:#241817!important}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  LANGUAGE TOGGLE (top right)
# ══════════════════════════════════════════
lang_col1, lang_col2 = st.columns([6,1])
with lang_col2:
    lang_choice = st.selectbox("🌐", ["English", "فارسی"], 
                                index=0 if st.session_state.lang=="en" else 1,
                                label_visibility="collapsed", key="lang_sel")
    new_lang = "en" if lang_choice == "English" else "fa"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

# ══════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════
user_name = ""
if st.session_state.current_user and st.session_state.current_user in st.session_state.students:
    user_name = st.session_state.students[st.session_state.current_user]["name"]

st.markdown(f"""
<div class="navbar" {dir_attr}>
  <div style="display:flex;align-items:center;gap:12px">
    <div class="brand-mark">🎭</div>
    <div>
      <div class="brand-name">{t('brand')}</div>
      <div class="brand-sub">{t('brand_sub')}</div>
    </div>
  </div>
  <div style="font-size:13px;color:#9b7250">
    {'👤 ' + user_name if user_name else ''}
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero" {dir_attr}>
  <div class="hero-badge">{t('hero_badge')}</div>
  <h1>{t('hero_title')}</h1>
  <p>{t('hero_desc')}</p>
  <div class="hero-note">📅 &nbsp; {t('hero_note')}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════
tab_book, tab_chart, tab_acc, tab_settings = st.tabs([
    t("tab_book"), t("tab_res"), t("tab_acc"), t("tab_settings")
])

# ══════════════════════════════════════════════════════════
#  TAB 1 — BOOK A HALL
# ══════════════════════════════════════════════════════════
with tab_book:
    col_left, col_right = st.columns([1.35, 0.85], gap="medium")

    with col_left:
        st.markdown(f'<div class="panel" {dir_attr}>', unsafe_allow_html=True)
        st.markdown(f'<div class="eyebrow">{t("book_eyebrow")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{t("book_title")}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#7f6b62;font-size:14px;margin-bottom:20px">{t("book_desc")}</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            student_name = st.text_input(t("student_name"), placeholder="e.g. Sara Mohammadi", key="book_name")
        with c2:
            student_email = st.text_input(t("student_email"), placeholder="sara@email.com", key="book_email")

        reservation_date = st.date_input(
            t("res_date"),
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30),
            value=date.today() + timedelta(days=1),
            key="book_date"
        )

        st.markdown(f'<label style="font-size:14px;font-weight:600;display:block;margin:8px 0 12px">{t("choose_hall")}</label>', unsafe_allow_html=True)

        hc1, hc2 = st.columns(2)
        with hc1:
            small_sel = st.session_state.selected_hall == "Small Hall"
            st.markdown(f"""
            <div class="hall-card {'selected' if small_sel else ''}" {dir_attr}>
              <div class="hall-icon-wrap">🎭</div>
              <div class="hall-title">{t('small_hall')}</div>
              <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#9b7250;margin-bottom:6px">{t('small_sub')}</div>
              <div class="hall-desc">{t('small_desc')}</div>
              <div class="hall-price">80,000 تومان</div>
            </div>""", unsafe_allow_html=True)
            if st.button(t("select_small"), key="sel_small"):
                st.session_state.selected_hall = "Small Hall"
                st.rerun()

        with hc2:
            large_sel = st.session_state.selected_hall == "Large Hall"
            st.markdown(f"""
            <div class="hall-card {'selected' if large_sel else ''}" {dir_attr}>
              <div class="hall-icon-wrap">🎪</div>
              <div class="hall-title">{t('large_hall')}</div>
              <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#9b7250;margin-bottom:6px">{t('large_sub')}</div>
              <div class="hall-desc">{t('large_desc')}</div>
              <div class="hall-price">150,000 تومان</div>
            </div>""", unsafe_allow_html=True)
            if st.button(t("select_large"), key="sel_large"):
                st.session_state.selected_hall = "Large Hall"
                st.rerun()

        sel_hall  = st.session_state.selected_hall
        sel_price = HALLS_DATA[sel_hall]["price"]
        hall_display = t("small_hall") if sel_hall == "Small Hall" else t("large_hall")

        st.markdown(f"""
        <div class="summary-strip" {dir_attr}>
          <div>
            <div class="summary-label">{t('selected_hall')}</div>
            <div style="font-size:15px;margin-top:4px;color:#5e4d46">{hall_display} &nbsp;·&nbsp; {HALLS_DATA[sel_hall]['icon']}</div>
          </div>
          <div style="text-align:{'left' if is_fa else 'right'}">
            <div class="summary-label">{t('session_price')}</div>
            <div class="summary-value">{fmt(sel_price)}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Time slot
        time_slots   = [f"{h:02d}:00" for h in range(9, 21)]
        booked_slots = [r["time_slot"] for r in st.session_state.reservations
                        if r["hall"] == sel_hall and str(r["date"]) == str(reservation_date) and r["status"] == "active"]
        avail_slots  = [s for s in time_slots if s not in booked_slots]

        if avail_slots:
            time_slot = st.selectbox(t("time_slot"), options=avail_slots, key="book_slot")
        else:
            st.markdown(f'<div class="msg-error">{t("err_noslot")}</div>', unsafe_allow_html=True)
            time_slot = None

        st.markdown("")
        if st.button(t("confirm_pay"), key="btn_reserve", use_container_width=True):
            if not student_name.strip():
                st.markdown(f'<div class="msg-error">{t("err_name")}</div>', unsafe_allow_html=True)
            elif not student_email.strip() or "@" not in student_email:
                st.markdown(f'<div class="msg-error">{t("err_email")}</div>', unsafe_allow_html=True)
            elif not time_slot:
                st.markdown(f'<div class="msg-error">{t("err_noslot")}</div>', unsafe_allow_html=True)
            elif len([r for r in st.session_state.reservations
                      if r["email"] == student_email.strip().lower() and r["status"] == "active"]) >= 3:
                st.markdown(f'<div class="msg-error">{t("err_limit")}</div>', unsafe_allow_html=True)
            else:
                rid = gen_id()
                new_res = {
                    "id":        rid,
                    "name":      student_name.strip(),
                    "email":     student_email.strip().lower(),
                    "hall":      sel_hall,
                    "date":      reservation_date,
                    "time_slot": time_slot,
                    "price":     sel_price,
                    "status":    "active",
                    "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.reservations.append(new_res)

                # Send email
                sent = send_confirmation_email(
                    student_email.strip(), student_name.strip(),
                    sel_hall, reservation_date.strftime("%d %b %Y"),
                    time_slot, sel_price, rid, st.session_state.lang
                )

                date_str = reservation_date.strftime("%d %b %Y")
                st.markdown(f'<div class="msg-success">{t("ok_booked")} {hall_display} — {date_str} {time_slot}</div>', unsafe_allow_html=True)
                if sent:
                    st.markdown(f'<div class="msg-success">{t("email_sent")} {student_email.strip()}</div>', unsafe_allow_html=True)
                elif st.session_state.smtp["host"]:
                    st.markdown(f'<div class="msg-error">{t("email_fail")}</div>', unsafe_allow_html=True)
                st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Dark account panel
        st.markdown(f"""
        <div class="panel-dark" {dir_attr}>
          <div class="eyebrow eyebrow-light">{t('acc_eyebrow')}</div>
          <div class="section-title section-title-light" style="font-family:'Playfair Display',serif;font-size:22px;margin:6px 0 10px">{t('signin_title')}</div>
          <p style="font-size:14px;color:rgba(255,255,255,.7);line-height:1.65">{t('acc_desc')}</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Hall info
        st.markdown(f"""
        <div class="panel" style="padding:22px" {dir_attr}>
          <div class="eyebrow">{t('hall_details')}</div><hr style="margin:10px 0 16px"/>
          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px">
            <div class="hall-icon-wrap" style="flex-shrink:0">🎭</div>
            <div>
              <div style="font-family:'Playfair Display',serif;font-size:17px">{t('small_hall')}</div>
              <div style="font-size:12px;color:#7f6b62;line-height:1.6;margin-top:3px">30 {'نفر' if is_fa else 'seats'} · {'میکروفن · پیانو' if is_fa else 'Mirrors · Sound system · Piano'}</div>
              <div style="font-size:14px;font-weight:700;color:#6d1f2a;margin-top:6px">80,000 تومان</div>
            </div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:12px">
            <div class="hall-icon-wrap" style="flex-shrink:0">🎪</div>
            <div>
              <div style="font-family:'Playfair Display',serif;font-size:17px">{t('large_hall')}</div>
              <div style="font-size:12px;color:#7f6b62;line-height:1.6;margin-top:3px">120 {'نفر' if is_fa else 'seats'} · {'نور حرفه‌ای · پشت صحنه' if is_fa else 'Pro lighting · Full backstage'}</div>
              <div style="font-size:14px;font-weight:700;color:#6d1f2a;margin-top:6px">150,000 تومان</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        active_c = len([r for r in st.session_state.reservations if r["status"]=="active"])
        total_c  = len(st.session_state.reservations)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px" {dir_attr}>
          <div class="panel" style="padding:18px;text-align:center">
            <div style="font-size:32px;font-family:'Playfair Display',serif;color:#6d1f2a">{active_c}</div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:4px">{t('active_bookings')}</div>
          </div>
          <div class="panel" style="padding:18px;text-align:center">
            <div style="font-size:32px;font-family:'Playfair Display',serif;color:#6d1f2a">{total_c}</div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:4px">{t('total_bookings')}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TAB 2 — RESERVATIONS CHART
# ══════════════════════════════════════════════════════════
with tab_chart:
    st.markdown(f'<div class="eyebrow">{t("chart_eyebrow")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{t("chart_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#7f6b62;font-size:14px;margin-bottom:24px">{t("chart_desc")}</p>', unsafe_allow_html=True)

    all_res = st.session_state.reservations

    if not all_res:
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px">
          <div style="font-size:52px;margin-bottom:16px">📊</div>
          <div style="font-family:'Playfair Display',serif;font-size:22px;color:#241817;margin-bottom:8px">{t('no_res')}</div>
          <div style="font-size:15px;color:#7f6b62;font-style:italic">{t('no_res_sub')}</div>
        </div>""", unsafe_allow_html=True)
    else:
        WINE   = "#6d1f2a"
        GOLD   = "#b88a4a"
        CREAM  = "#f5eadf"
        WINE2  = "#9b3545"
        GOLD2  = "#d4a96a"

        # ── Chart 1: Bar — bookings per student (name only, no ID) ──
        from collections import Counter, defaultdict
        name_counts = Counter(r["name"] for r in all_res if r["status"] == "active")
        names  = list(name_counts.keys())
        counts = list(name_counts.values())

        fig_bar = go.Figure(go.Bar(
            x=names, y=counts,
            marker=dict(
                color=counts,
                colorscale=[[0, CREAM], [0.5, GOLD2], [1, WINE]],
                line=dict(color=WINE, width=1.2)
            ),
            text=counts,
            textposition="outside",
            textfont=dict(color=WINE, size=13, family="Playfair Display"),
            hovertemplate="<b>%{x}</b><br>" + ("رزرو: " if is_fa else "Bookings: ") + "%{y}<extra></extra>",
        ))
        fig_bar.update_layout(
            title=dict(text=t("bar_chart_title"), font=dict(family="Playfair Display", size=20, color=WINE), x=0.5),
            plot_bgcolor="#fffaf3", paper_bgcolor="#fffaf3",
            font=dict(family=font_fa, color="#241817"),
            xaxis=dict(showgrid=False, tickfont=dict(size=13)),
            yaxis=dict(gridcolor="#eadccf", gridwidth=1, title=""),
            margin=dict(t=60, b=40, l=20, r=20),
            height=340,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        cc1, cc2 = st.columns(2)

        # ── Chart 2: Pie — hall usage ──
        with cc1:
            hall_counts = Counter(r["hall"] for r in all_res if r["status"] == "active")
            hall_labels = [t("small_hall") if h == "Small Hall" else t("large_hall") for h in hall_counts.keys()]
            fig_pie = go.Figure(go.Pie(
                labels=hall_labels,
                values=list(hall_counts.values()),
                marker=dict(colors=[WINE, GOLD], line=dict(color="#fffaf3", width=3)),
                textfont=dict(family="Playfair Display", size=14),
                hovertemplate="<b>%{label}</b><br>%{value} " + ("رزرو" if is_fa else "bookings") + "<extra></extra>",
                hole=0.4,
            ))
            fig_pie.update_layout(
                title=dict(text=t("pie_chart_title"), font=dict(family="Playfair Display", size=18, color=WINE), x=0.5),
                plot_bgcolor="#fffaf3", paper_bgcolor="#fffaf3",
                font=dict(family=font_fa),
                legend=dict(font=dict(size=13)),
                margin=dict(t=60, b=20, l=20, r=20),
                height=320,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # ── Chart 3: Line — bookings over time ──
        with cc2:
            date_counts = Counter(str(r["date"]) for r in all_res if r["status"] == "active")
            sorted_dates = sorted(date_counts.keys())
            fig_line = go.Figure(go.Scatter(
                x=sorted_dates,
                y=[date_counts[d] for d in sorted_dates],
                mode="lines+markers",
                line=dict(color=WINE, width=2.5),
                marker=dict(color=WINE, size=8, line=dict(color="#fffaf3", width=2)),
                fill="tozeroy",
                fillcolor="rgba(109,31,42,0.08)",
                hovertemplate="<b>%{x}</b><br>" + ("رزرو: " if is_fa else "Bookings: ") + "%{y}<extra></extra>",
            ))
            fig_line.update_layout(
                title=dict(text=t("line_chart_title"), font=dict(family="Playfair Display", size=18, color=WINE), x=0.5),
                plot_bgcolor="#fffaf3", paper_bgcolor="#fffaf3",
                font=dict(family=font_fa, color="#241817"),
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#eadccf", gridwidth=1),
                margin=dict(t=60, b=20, l=20, r=20),
                height=320,
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # ── Reservation Table (name only, no ID) ──
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(f'<div class="eyebrow" style="margin-bottom:14px">{t("chart_title")}</div>', unsafe_allow_html=True)

        filter_e = st.text_input(t("filter_email"), placeholder="sara@email.com", key="chart_filter")
        displayed = [r for r in sorted(all_res, key=lambda x: str(x["date"]), reverse=True)
                     if not filter_e.strip() or r["email"] == filter_e.strip().lower()]

        for i, res in enumerate(displayed):
            cancelled = res["status"] == "cancelled"
            hall_disp = t("small_hall") if res["hall"] == "Small Hall" else t("large_hall")
            status_html = (f'<span class="res-status-cancelled">{t("cancelled")}</span>'
                           if cancelled else f'<span class="res-status-active">{t("active")}</span>')
            d_str = res["date"].strftime("%d %b %Y") if hasattr(res["date"], "strftime") else res["date"]

            st.markdown(f"""
            <div class="res-card {'cancelled' if cancelled else ''}" {dir_attr}>
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px">
                <div>
                  <div class="res-hall">{HALLS_DATA[res['hall']]['icon']} &nbsp;{hall_disp}</div>
                  {status_html}
                </div>
                <div class="res-price">{fmt(res['price'])}</div>
              </div>
              <hr/>
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
                <div>
                  <div class="res-meta-label">{t('student_lbl')}</div>
                  <div class="res-meta-value">{res['name']}</div>
                </div>
                <div>
                  <div class="res-meta-label">{t('date_lbl')}</div>
                  <div class="res-meta-value">{d_str}</div>
                </div>
                <div>
                  <div class="res-meta-label">{t('time_lbl')}</div>
                  <div class="res-meta-value">{res['time_slot']}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            if not cancelled:
                st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
                if st.button(t("cancel_btn"), key=f"chart_cancel_{res['id']}_{i}"):
                    res["status"] = "cancelled"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TAB 3 — ACCOUNT
# ══════════════════════════════════════════════════════════
with tab_acc:
    a1, a2 = st.columns([1, 1], gap="large")

    with a1:
        st.markdown(f"""
        <div class="panel-dark" style="margin-bottom:20px" {dir_attr}>
          <div class="eyebrow eyebrow-light">{t('acc_eyebrow')}</div>
          <div class="section-title section-title-light" style="font-family:'Playfair Display',serif;font-size:24px;margin:6px 0 8px">{t('acc_title')}</div>
          <p style="font-size:14px;color:rgba(255,255,255,.72);line-height:1.65">{t('acc_desc')}</p>
        </div>""", unsafe_allow_html=True)

        with st.form("create_account_form"):
            new_name    = st.text_input(t("full_name"),        placeholder="Sara Mohammadi")
            new_email   = st.text_input(t("student_email"),    placeholder="sara@email.com")
            new_id      = st.text_input(t("student_id_label"), placeholder="S010")
            new_balance = st.number_input(t("starting_bal"), min_value=0, step=50000, value=300000)
            submitted = st.form_submit_button(t("create_acc"), use_container_width=True)

            if submitted:
                nid = new_id.strip().upper()
                if not new_name.strip():
                    st.markdown(f'<div class="msg-error">{t("err_name")}</div>', unsafe_allow_html=True)
                elif not new_email.strip() or "@" not in new_email:
                    st.markdown(f'<div class="msg-error">{t("err_email")}</div>', unsafe_allow_html=True)
                elif not nid:
                    st.markdown(f'<div class="msg-error">{t("err_id_empty")}</div>', unsafe_allow_html=True)
                elif nid in st.session_state.students:
                    st.markdown(f'<div class="msg-error">{t("err_id_taken")}</div>', unsafe_allow_html=True)
                else:
                    st.session_state.students[nid] = {"name": new_name.strip(), "email": new_email.strip().lower(), "balance": int(new_balance)}
                    st.session_state.current_user = nid
                    st.markdown(f'<div class="msg-success">{t("ok_account")} {new_name.strip()}!</div>', unsafe_allow_html=True)
                    st.balloons()

    with a2:
        st.markdown(f"""
        <div class="panel" style="margin-bottom:20px" {dir_attr}>
          <div class="eyebrow">{t('signin_title')}</div>
          <div class="section-title" style="margin-bottom:8px">{t('signin_title')}</div>
          <p style="font-size:14px;color:#7f6b62;margin-bottom:16px">{t('signin_desc')}</p>
        </div>""", unsafe_allow_html=True)

        with st.form("signin_form"):
            signin_id = st.text_input(t("student_id_label"), placeholder="S001")
            if st.form_submit_button(t("signin_btn"), use_container_width=True):
                sid = signin_id.strip().upper()
                if sid in st.session_state.students:
                    st.session_state.current_user = sid
                    st.markdown(f'<div class="msg-success">{t("ok_signin")} {st.session_state.students[sid]["name"]}!</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="msg-error">{t("err_signin")}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#f5eadf;border-radius:16px;padding:18px 20px;margin-top:8px" {dir_attr}>
          <div class="eyebrow" style="margin-bottom:10px">{t('demo_ids')}</div>
          <div style="font-size:13px;color:#5e4d46;line-height:2.2;font-family:monospace">
            S001 — Emma Larson · 500,000 تومان<br/>
            S002 — Luca Moretti · 400,000 تومان<br/>
            S003 — Sofia Andersen · 600,000 تومان
          </div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.students:
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown(f'<div class="eyebrow" style="margin-bottom:12px">{t("reg_students")}</div>', unsafe_allow_html=True)
            for sid, s in st.session_state.students.items():
                is_me = st.session_state.current_user == sid
                res_c = len([r for r in st.session_state.reservations if r.get("email","") == s.get("email","") and r["status"]=="active"])
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 14px;border-radius:12px;margin-bottom:6px;
                            background:{'#fff7f7' if is_me else '#fffdf9'};
                            border:1px solid {'#6d1f2a' if is_me else '#e7d8c6'}" {dir_attr}>
                  <div>
                    <span style="font-weight:600;color:#241817">{s['name']}</span>
                    {'<span style="font-size:11px;background:#ddf0e6;color:#2d7a58;padding:2px 8px;border-radius:99px;margin-left:6px">You</span>' if is_me else ''}
                  </div>
                  <span style="font-size:12px;color:#7f6b62">{res_c} {'رزرو' if is_fa else 'booking'}{'s' if not is_fa and res_c!=1 else ''}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TAB 4 — SETTINGS (Email + Language)
# ══════════════════════════════════════════════════════════
with tab_settings:
    s1, s2 = st.columns([1, 1], gap="large")

    with s1:
        st.markdown(f"""
        <div class="panel" {dir_attr}>
          <div class="eyebrow">{t('email_settings')}</div>
          <div class="section-title" style="font-size:22px;margin-bottom:16px">📧 SMTP</div>
          <p style="font-size:13px;color:#7f6b62;margin-bottom:20px">
            {'برای فعال‌سازی ارسال ایمیل تأییدیه، اطلاعات SMTP را وارد کنید. برای Gmail از App Password استفاده کنید.' if is_fa else 'Enter your SMTP details to enable confirmation emails. For Gmail, use an App Password (not your main password).'}
          </p>
        </div>""", unsafe_allow_html=True)

        with st.form("smtp_form"):
            smtp_host = st.text_input(t("smtp_host"), value=st.session_state.smtp["host"], placeholder="smtp.gmail.com")
            smtp_port = st.number_input(t("smtp_port"), value=st.session_state.smtp["port"], min_value=1, max_value=9999)
            smtp_user = st.text_input(t("smtp_user"), value=st.session_state.smtp["user"], placeholder="yourname@gmail.com")
            smtp_pass = st.text_input(t("smtp_pass"), value=st.session_state.smtp["pass"], type="password", placeholder="xxxx xxxx xxxx xxxx")
            if st.form_submit_button(t("smtp_save"), use_container_width=True):
                st.session_state.smtp = {"host": smtp_host, "port": int(smtp_port), "user": smtp_user, "pass": smtp_pass}
                st.markdown('<div class="msg-success">✓ Email settings saved.</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#f5eadf;border-radius:14px;padding:16px 18px;margin-top:16px;font-size:13px;color:#7f6b62" {dir_attr}>
          <strong style="color:#6d1f2a">{'راهنمای Gmail:' if is_fa else 'Gmail guide:'}</strong><br/><br/>
          {'۱. به تنظیمات Google خود بروید<br/>۲. Security → 2-Step Verification را فعال کنید<br/>۳. App Passwords → Mail → بسازید<br/>۴. رمز ۱۶ کاراکتری را اینجا وارد کنید' if is_fa else '1. Go to your Google Account settings<br/>2. Enable 2-Step Verification<br/>3. Security → App Passwords → Mail → Generate<br/>4. Paste the 16-character password above'}
        </div>""", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="panel" {dir_attr}>
          <div class="eyebrow">{t('settings_title')}</div>
          <div class="section-title" style="font-size:22px;margin-bottom:16px">🌐 {t('lang_label')}</div>
        </div>""", unsafe_allow_html=True)

        lang_opt = st.radio(t("lang_label"), ["English 🇬🇧", "فارسی 🇮🇷"],
                            index=0 if st.session_state.lang=="en" else 1,
                            label_visibility="collapsed")
        new_lang2 = "en" if "English" in lang_opt else "fa"
        if new_lang2 != st.session_state.lang:
            st.session_state.lang = new_lang2
            st.rerun()

        st.markdown(f"""
        <div style="background:#f5eadf;border-radius:14px;padding:16px 18px;margin-top:16px;font-size:14px;color:#5e4d46" {dir_attr}>
          🌐 {'زبان فعلی: ' + ('فارسی' if is_fa else 'English') + '<br/><br/>تغییر زبان، تمام متون برنامه را به‌روز می‌کند.' if is_fa else 'Current language: ' + ('Persian (فارسی)' if is_fa else 'English') + '<br/><br/>Switching language updates all text across the entire app.'}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #e7d8c6;padding:24px 0;text-align:center" {dir_attr}>
  <span style="font-family:'Playfair Display',serif;font-size:16px;color:#6d1f2a">{t('brand')}</span>
  <span style="color:#c8aa92;margin:0 10px">·</span>
  <span style="font-size:13px;color:#9b7250">{t('brand_sub')}</span>
  <span style="color:#c8aa92;margin:0 10px">·</span>
  <span style="font-size:13px;color:#9b7250">{t('footer_small')} &nbsp;|&nbsp; {t('footer_large')}</span>
</div>""", unsafe_allow_html=True)
