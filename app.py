import streamlit as st
from datetime import date, datetime, timedelta
import uuid

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
#  GLOBAL CSS  (matches Canva design)
# ══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#f6ecdf 0%,#fbf7f0 45%,#f1e2d2 100%) !important;
    font-family: 'DM Sans', sans-serif;
    color: #241817;
}
[data-testid="stAppViewContainer"]::before {
    content:"";
    position:fixed; inset:0;
    background-image: radial-gradient(rgba(36,24,23,.06) 1px, transparent 1px);
    background-size: 18px 18px;
    opacity:.18;
    pointer-events:none;
    z-index:0;
}
[data-testid="stHeader"] { background: rgba(255,249,240,0.92) !important; border-bottom: 1px solid #eadccf; }
[data-testid="stSidebar"] { display: none; }
section[data-testid="stMain"] { padding-top: 0 !important; }

/* ── hide streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { display:none !important; }

/* ── typography ── */
.display { font-family: 'Playfair Display', serif; font-weight: 700; }

/* ── top navbar ── */
.navbar {
    width: 100%;
    background: rgba(255,249,240,0.92);
    border-bottom: 1px solid #eadccf;
    padding: 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky; top: 0; z-index: 999;
}
.navbar-brand { display:flex; align-items:center; gap:12px; }
.brand-mark {
    width:40px; height:40px; border-radius:50%;
    background:#6d1f2a; color:#fff;
    display:flex; align-items:center; justify-content:center;
    font-size:18px;
}
.brand-name { font-family:'Playfair Display',serif; font-size:18px; font-weight:700; color:#241817; }
.brand-sub  { font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:#9b7250; margin-top:1px; }
.navbar-nav { display:flex; gap:28px; font-size:14px; font-weight:500; color:#5d4b45; }
.nav-link { cursor:pointer; padding:4px 0; border-bottom:2px solid transparent; transition:.2s; }
.nav-link:hover, .nav-link.active { color:#6d1f2a; border-bottom-color:#6d1f2a; }

/* ── hero banner ── */
.hero {
    background: linear-gradient(90deg, rgba(36,24,23,.85), rgba(36,24,23,.3) 55%, rgba(36,24,23,.05)),
                linear-gradient(135deg, #6d1f2a 0%, #3a0e15 100%);
    border-radius: 28px;
    padding: 56px 52px;
    margin: 24px 0 20px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 22px 60px rgba(72,16,25,.18);
}
.hero::after {
    content:"";
    position:absolute; inset:0;
    background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(255,255,255,.015) 40px, rgba(255,255,255,.015) 80px);
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px;
    padding:6px 14px; border-radius:999px;
    background:#b88a4a; color:#fff;
    font-size:11px; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
    margin-bottom:20px;
}
.hero h1 { font-family:'Playfair Display',serif; font-size:42px; line-height:1.05; margin:0 0 16px; }
.hero p  { font-size:16px; color:rgba(255,255,255,.85); line-height:1.7; max-width:520px; margin:0; }
.hero-note { display:flex; align-items:center; gap:8px; margin-top:22px; font-size:13px; color:rgba(255,255,255,.8); }

/* ── panel cards ── */
.panel {
    background: #fffaf3;
    border: 1px solid #eadccf;
    border-radius: 26px;
    padding: 32px 28px;
    box-shadow: 0 12px 40px rgba(72,16,25,.08);
    height: 100%;
}
.panel-dark {
    background: #2f1d1a;
    color: #fff;
    border-radius: 26px;
    padding: 28px 26px;
    box-shadow: 0 12px 40px rgba(72,16,25,.12);
}

/* ── eyebrow / section labels ── */
.eyebrow {
    font-size:11px; font-weight:600;
    letter-spacing:.2em; text-transform:uppercase;
    color:#9b7250; margin-bottom:6px;
}
.eyebrow-light { color:#d8b47b; }
.section-title { font-family:'Playfair Display',serif; font-size:26px; color:#241817; margin:4px 0 8px; }
.section-title-light { color:#fff; }

/* ── hall cards ── */
.hall-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:10px; }
.hall-card {
    border:1px solid #e7d8c6;
    border-radius:18px; padding:18px;
    background:#fffdf9;
    cursor:pointer;
    transition:.2s ease;
}
.hall-card:hover { transform:translateY(-2px); border-color:#c8aa92; }
.hall-card.selected { border-color:#6d1f2a; background:#fff7f7; box-shadow:0 8px 24px rgba(109,31,42,.1); }
.hall-icon-wrap {
    width:36px; height:36px; border-radius:50%;
    background:#f1dfd1; color:#6d1f2a;
    display:flex; align-items:center; justify-content:center;
    font-size:16px; margin-bottom:10px;
}
.hall-title { font-family:'Playfair Display',serif; font-size:18px; color:#241817; margin-bottom:4px; }
.hall-desc  { font-size:13px; color:#7f6b62; line-height:1.6; margin-bottom:14px; }
.hall-price { font-size:16px; font-weight:700; color:#6d1f2a; }

/* ── summary strip ── */
.summary-strip {
    background:#f5eadf;
    border-radius:14px; padding:16px 20px;
    display:flex; justify-content:space-between; align-items:center;
    margin:16px 0;
}
.summary-label  { font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:#9b7250; }
.summary-value  { font-family:'Playfair Display',serif; font-size:22px; color:#6d1f2a; margin-top:2px; }

/* ── form fields ── */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    border: 1px solid #e7d8c6 !important;
    background: #fffdf9 !important;
    border-radius: 14px !important;
    padding: 14px 15px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #241817 !important;
    transition: .2s ease !important;
}
.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: #6d1f2a !important;
    box-shadow: 0 0 0 3px rgba(109,31,42,.12) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #241817 !important;
    margin-bottom: 4px !important;
}
/* dark panel inputs */
.dark-input .stTextInput > div > div > input,
.dark-input .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.95) !important;
    color: #241817 !important;
}

/* ── buttons ── */
.stButton > button {
    width: 100%;
    background: #6d1f2a !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: .2s !important;
    box-shadow: 0 4px 16px rgba(109,31,42,.22) !important;
}
.stButton > button:hover {
    background: #571821 !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(109,31,42,.28) !important;
}
.btn-gold > button {
    background: #d1a15b !important;
    color: #2f1d1a !important;
    box-shadow: 0 4px 16px rgba(184,138,74,.25) !important;
}
.btn-gold > button:hover { background: #c4934d !important; }
.btn-cancel > button {
    background: #f2e2e0 !important;
    color: #7b2932 !important;
    box-shadow: none !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    border-radius: 12px !important;
}
.btn-cancel > button:hover { background: #ead3d0 !important; }

/* ── reservation cards ── */
.res-card {
    background: #fffaf3;
    border: 1px solid #eadccf;
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 8px 24px rgba(72,16,25,.05);
    margin-bottom: 14px;
    position: relative;
}
.res-card.cancelled { opacity:.68; }
.res-hall { font-family:'Playfair Display',serif; font-size:22px; color:#2b1c19; margin:6px 0; }
.res-status-active {
    display:inline-flex; align-items:center;
    padding:4px 12px; border-radius:999px;
    background:#ddf0e6; color:#2d7a58;
    font-size:12px; font-weight:600;
}
.res-status-cancelled {
    display:inline-flex; align-items:center;
    padding:4px 12px; border-radius:999px;
    background:#f2e2e0; color:#7b2932;
    font-size:12px; font-weight:600;
}
.res-meta-label { font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:#9b7250; margin-top:12px; }
.res-meta-value { font-size:15px; font-weight:500; color:#4b3932; margin-top:2px; }
.res-price { font-family:'Playfair Display',serif; font-size:26px; color:#6d1f2a; }
.res-note { font-size:12px; color:#7f6b62; margin-top:6px; }

/* ── success / error messages ── */
.msg-success {
    background:#ddf0e6; color:#2d7a58;
    border-radius:12px; padding:12px 16px;
    font-size:14px; font-weight:500;
    margin-top:8px;
}
.msg-error {
    background:#f2e2e0; color:#7b2932;
    border-radius:12px; padding:12px 16px;
    font-size:14px; font-weight:500;
    margin-top:8px;
}
.msg-info {
    background:#e8f0fb; color:#1a4a8a;
    border-radius:12px; padding:12px 16px;
    font-size:14px; font-weight:500;
    margin-top:8px;
}

/* ── divider ── */
hr { border:none; border-top:1px solid #e7d8c6; margin:20px 0; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap:4px;
    background:transparent;
    border-bottom:2px solid #e7d8c6;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important;
    border:none !important;
    color:#7f6b62 !important;
    font-family:'DM Sans',sans-serif !important;
    font-weight:600 !important;
    font-size:14px !important;
    padding:10px 20px !important;
    border-radius:0 !important;
}
.stTabs [aria-selected="true"] {
    color:#6d1f2a !important;
    border-bottom:2px solid #6d1f2a !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top:24px !important; }

/* ── misc ── */
.stAlert { border-radius:14px !important; }
[data-testid="stSpinner"] { color:#6d1f2a !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════
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
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "booking"
if "selected_hall" not in st.session_state:
    st.session_state.selected_hall = "Small Hall"

HALLS = {
    "Small Hall":  {"price": 80000,  "icon": "🎭", "desc": "Intimate rehearsal space for solo acts & small ensembles. Up to 30 students.", "capacity": 30},
    "Large Hall":  {"price": 150000, "icon": "🎪", "desc": "Full production stage with lighting rig — ideal for full cast rehearsals. Up to 120 students.", "capacity": 120},
}

def fmt(n):
    return f"{n:,} تومان"

def gen_id():
    return "RES-" + str(uuid.uuid4())[:8].upper()

# ══════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════
user_name = ""
if st.session_state.current_user and st.session_state.current_user in st.session_state.students:
    user_name = st.session_state.students[st.session_state.current_user]["name"]

st.markdown(f"""
<div class="navbar">
  <div class="navbar-brand">
    <div class="brand-mark">🎭</div>
    <div>
      <div class="brand-name">StagePass</div>
      <div class="brand-sub">Acting School · Hall Reservations</div>
    </div>
  </div>
  <div class="navbar-nav">
    <span class="nav-link {'active' if st.session_state.active_tab=='booking' else ''}">📅 Booking</span>
    <span class="nav-link {'active' if st.session_state.active_tab=='reservations' else ''}">📋 Reservations</span>
    <span class="nav-link {'active' if st.session_state.active_tab=='account' else ''}">👤 {'Signed in as ' + user_name if user_name else 'Account'}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">🎭 &nbsp; Now Accepting Reservations</div>
  <h1 class="display">Reserve Your Stage,<br>Perfect Your Craft</h1>
  <p>Book world-class rehearsal halls at our acting school. Whether you're preparing a solo piece or directing a full cast, we have the space for you.</p>
  <div class="hero-note">📅 &nbsp; Available 7 days a week · Instant confirmation · Full refund on cancellation</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════
tab_book, tab_res, tab_acc = st.tabs(["📅  Book a Hall", "📋  My Reservations", "👤  Account"])

# ════════════════════════════════════════════════════════
#  TAB 1 — BOOK A HALL
# ════════════════════════════════════════════════════════
with tab_book:
    col_left, col_right = st.columns([1.35, 0.85], gap="medium")

    # ── LEFT PANEL: BOOKING FORM ──
    with col_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Hall Reservations</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Book a Rehearsal Hall</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#7f6b62;font-size:14px;margin-bottom:20px">Select your preferred hall, date and fill in your details to reserve instantly.</p>', unsafe_allow_html=True)

        # — Student info —
        c1, c2 = st.columns(2)
        with c1:
            student_name = st.text_input("Student Name", placeholder="e.g. Ali Rezaei", key="book_name")
        with c2:
            student_email = st.text_input("Email Address", placeholder="e.g. ali@email.com", key="book_email")

        # — Date —
        reservation_date = st.date_input(
            "Reservation Date",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30),
            value=date.today() + timedelta(days=1),
            key="book_date"
        )

        # — Hall Selection —
        st.markdown('<label style="font-size:14px;font-weight:600;display:block;margin:8px 0 12px">Choose a Hall</label>', unsafe_allow_html=True)

        hall_col1, hall_col2 = st.columns(2)
        with hall_col1:
            small_selected = st.session_state.selected_hall == "Small Hall"
            st.markdown(f"""
            <div class="hall-card {'selected' if small_selected else ''}" onclick="">
              <div class="hall-icon-wrap">🎭</div>
              <div class="hall-title">Studio A</div>
              <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#9b7250;margin-bottom:6px">Small Hall</div>
              <div class="hall-desc">Intimate rehearsal space for solo acts & small ensembles. Up to 30 students.</div>
              <div class="hall-price">80,000 تومان / session</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select Studio A", key="sel_small"):
                st.session_state.selected_hall = "Small Hall"
                st.rerun()

        with hall_col2:
            large_selected = st.session_state.selected_hall == "Large Hall"
            st.markdown(f"""
            <div class="hall-card {'selected' if large_selected else ''}" onclick="">
              <div class="hall-icon-wrap">🎪</div>
              <div class="hall-title">Grand Stage</div>
              <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#9b7250;margin-bottom:6px">Large Hall</div>
              <div class="hall-desc">Full production stage with lighting rig — ideal for full cast rehearsals. Up to 120 students.</div>
              <div class="hall-price">150,000 تومان / session</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select Grand Stage", key="sel_large"):
                st.session_state.selected_hall = "Large Hall"
                st.rerun()

        # — Summary strip —
        selected_hall = st.session_state.selected_hall
        selected_price = HALLS[selected_hall]["price"]
        st.markdown(f"""
        <div class="summary-strip">
          <div>
            <div class="summary-label">Selected Hall</div>
            <div style="font-size:15px;margin-top:4px;color:#5e4d46">{selected_hall} &nbsp;·&nbsp; {HALLS[selected_hall]['icon']}</div>
          </div>
          <div style="text-align:right">
            <div class="summary-label">Session Price</div>
            <div class="summary-value">{fmt(selected_price)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # — Time slot —
        time_slots = [f"{h:02d}:00" for h in range(9, 21)]
        booked_slots = [
            r["time_slot"] for r in st.session_state.reservations
            if r["hall"] == selected_hall
            and str(r["date"]) == str(reservation_date)
            and r["status"] == "active"
        ]
        available_slots = [s for s in time_slots if s not in booked_slots]

        if available_slots:
            time_slot = st.selectbox(
                "Time Slot",
                options=available_slots,
                key="book_slot"
            )
        else:
            st.markdown('<div class="msg-error">⚠ No available slots for this hall on the selected date.</div>', unsafe_allow_html=True)
            time_slot = None

        # — Reserve button —
        st.markdown("")
        if st.button("✦ Confirm Reservation & Pay", key="btn_reserve", use_container_width=True):
            if not student_name.strip():
                st.markdown('<div class="msg-error">⚠ Please enter your name.</div>', unsafe_allow_html=True)
            elif not student_email.strip() or "@" not in student_email:
                st.markdown('<div class="msg-error">⚠ Please enter a valid email address.</div>', unsafe_allow_html=True)
            elif not time_slot:
                st.markdown('<div class="msg-error">⚠ No time slots available for this date.</div>', unsafe_allow_html=True)
            elif len([r for r in st.session_state.reservations if r["email"] == student_email.strip() and r["status"] == "active"]) >= 3:
                st.markdown('<div class="msg-error">⚠ Reservation limit reached (3 active). Please cancel an older booking first.</div>', unsafe_allow_html=True)
            else:
                new_res = {
                    "id": gen_id(),
                    "name": student_name.strip(),
                    "email": student_email.strip().lower(),
                    "hall": selected_hall,
                    "date": reservation_date,
                    "time_slot": time_slot,
                    "price": selected_price,
                    "status": "active",
                    "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.reservations.append(new_res)
                st.markdown(f'<div class="msg-success">✓ Reservation confirmed for {selected_hall} on {reservation_date.strftime("%d %b %Y")} at {time_slot}. Payment of {fmt(selected_price)} received.</div>', unsafe_allow_html=True)
                st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)  # end panel

    # ── RIGHT COLUMN ──
    with col_right:

        # Account Quick Panel
        st.markdown("""
        <div class="panel-dark">
          <div class="eyebrow eyebrow-light">Student Portal</div>
          <div class="section-title section-title-light" style="font-family:'Playfair Display',serif;font-size:24px;margin:6px 0 10px">Your Account</div>
          <p style="font-size:14px;color:rgba(255,255,255,.7);line-height:1.65">
            Create or access your student account to track all your reservations and manage payments from one place.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Hall Info Cards
        st.markdown("""
        <div class="panel" style="padding:22px">
          <div class="eyebrow">Hall Details</div>
          <hr style="margin:10px 0 16px"/>

          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px">
            <div class="hall-icon-wrap" style="flex-shrink:0">🎭</div>
            <div>
              <div style="font-family:'Playfair Display',serif;font-size:17px;color:#241817">Studio A</div>
              <div style="font-size:12px;color:#7f6b62;line-height:1.6;margin-top:3px">30 seats · Mirrors · Sound system · Piano available</div>
              <div style="font-size:14px;font-weight:700;color:#6d1f2a;margin-top:6px">80,000 تومان</div>
            </div>
          </div>

          <div style="display:flex;align-items:flex-start;gap:12px">
            <div class="hall-icon-wrap" style="flex-shrink:0">🎪</div>
            <div>
              <div style="font-family:'Playfair Display',serif;font-size:17px;color:#241817">Grand Stage</div>
              <div style="font-size:12px;color:#7f6b62;line-height:1.6;margin-top:3px">120 seats · Professional lighting · Full backstage · Costume room</div>
              <div style="font-size:14px;font-weight:700;color:#6d1f2a;margin-top:6px">150,000 تومان</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Stats
        active_count = len([r for r in st.session_state.reservations if r["status"] == "active"])
        total_count  = len(st.session_state.reservations)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div class="panel" style="padding:18px;text-align:center">
            <div style="font-size:32px;font-family:'Playfair Display',serif;color:#6d1f2a">{active_count}</div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:4px">Active Bookings</div>
          </div>
          <div class="panel" style="padding:18px;text-align:center">
            <div style="font-size:32px;font-family:'Playfair Display',serif;color:#6d1f2a">{total_count}</div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9b7250;margin-top:4px">Total Bookings</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  TAB 2 — MY RESERVATIONS
# ════════════════════════════════════════════════════════
with tab_res:
    st.markdown('<div class="eyebrow">Your Bookings</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">My Reservations</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#7f6b62;font-size:14px;margin-bottom:24px">View and manage all your hall reservations. Cancel anytime for a full refund.</p>', unsafe_allow_html=True)

    # Filter by email
    filter_email = st.text_input("🔍  Filter by your email address", placeholder="Enter your email to see your reservations", key="filter_email")

    if st.session_state.reservations:
        shown = st.session_state.reservations
        if filter_email.strip():
            shown = [r for r in shown if r["email"] == filter_email.strip().lower()]

        if not shown:
            st.markdown('<div class="msg-info">ℹ No reservations found for that email address.</div>', unsafe_allow_html=True)
        else:
            # Sort: active first, then by date
            shown_sorted = sorted(shown, key=lambda r: (r["status"] != "active", str(r["date"])))

            for i, res in enumerate(shown_sorted):
                cancelled = res["status"] == "cancelled"
                status_html = (
                    '<span class="res-status-cancelled">✕ Cancelled</span>'
                    if cancelled else
                    '<span class="res-status-active">✓ Confirmed</span>'
                )

                st.markdown(f"""
                <div class="res-card {'cancelled' if cancelled else ''}">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px">
                    <div>
                      <div class="eyebrow">Reservation ID: {res['id']}</div>
                      <div class="res-hall">{HALLS[res['hall']]['icon']} &nbsp;{res['hall']}</div>
                      {status_html}
                    </div>
                    <div class="res-price">{fmt(res['price'])}</div>
                  </div>
                  <hr/>
                  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
                    <div>
                      <div class="res-meta-label">Student</div>
                      <div class="res-meta-value">{res['name']}</div>
                    </div>
                    <div>
                      <div class="res-meta-label">Date</div>
                      <div class="res-meta-value">{res['date'].strftime('%d %b %Y') if hasattr(res['date'],'strftime') else res['date']}</div>
                    </div>
                    <div>
                      <div class="res-meta-label">Time Slot</div>
                      <div class="res-meta-value">{res['time_slot']}</div>
                    </div>
                  </div>
                  <div class="res-note" style="margin-top:10px">Booked on {res['booked_at']}</div>
                </div>
                """, unsafe_allow_html=True)

                if not cancelled:
                    st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
                    if st.button(f"Cancel & Refund this Reservation", key=f"cancel_{res['id']}_{i}"):
                        res["status"] = "cancelled"
                        st.success(f"✓ Reservation {res['id']} cancelled. {fmt(res['price'])} will be refunded.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px">
          <div style="font-size:52px;margin-bottom:16px">📋</div>
          <div style="font-family:'Playfair Display',serif;font-size:22px;color:#241817;margin-bottom:8px">No reservations yet</div>
          <div style="font-size:15px;color:#7f6b62;font-style:italic">Head to the Booking tab to reserve your first hall.</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  TAB 3 — ACCOUNT
# ════════════════════════════════════════════════════════
with tab_acc:
    acc_col1, acc_col2 = st.columns([1, 1], gap="large")

    with acc_col1:
        # Create Account
        st.markdown("""
        <div class="panel-dark" style="margin-bottom:20px">
          <div class="eyebrow eyebrow-light">New Student</div>
          <div class="section-title section-title-light" style="font-family:'Playfair Display',serif;font-size:24px;margin:6px 0 8px">Create Account</div>
          <p style="font-size:14px;color:rgba(255,255,255,.72);line-height:1.65">Join our acting school and start booking rehearsal halls instantly.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("create_account_form"):
            new_name    = st.text_input("Full Name",        placeholder="e.g. Sara Mohammadi")
            new_email   = st.text_input("Email Address",    placeholder="e.g. sara@email.com")
            new_id      = st.text_input("Student ID",       placeholder="e.g. S010 (you choose)")
            new_balance = st.number_input("Starting Balance (Tomans)", min_value=0, step=50000, value=300000)
            submitted = st.form_submit_button("✦ Create My Account", use_container_width=True)

            if submitted:
                nid = new_id.strip().upper()
                if not new_name.strip():
                    st.markdown('<div class="msg-error">⚠ Please enter your full name.</div>', unsafe_allow_html=True)
                elif not new_email.strip() or "@" not in new_email:
                    st.markdown('<div class="msg-error">⚠ Please enter a valid email address.</div>', unsafe_allow_html=True)
                elif not nid:
                    st.markdown('<div class="msg-error">⚠ Please choose a Student ID.</div>', unsafe_allow_html=True)
                elif nid in st.session_state.students:
                    st.markdown(f'<div class="msg-error">⚠ Student ID <b>{nid}</b> is already taken. Choose another.</div>', unsafe_allow_html=True)
                else:
                    st.session_state.students[nid] = {
                        "name": new_name.strip(),
                        "email": new_email.strip().lower(),
                        "balance": int(new_balance),
                    }
                    st.session_state.current_user = nid
                    st.markdown(f'<div class="msg-success">✓ Account created! Welcome, {new_name.strip()}. Your Student ID is <b>{nid}</b>.</div>', unsafe_allow_html=True)
                    st.balloons()

    with acc_col2:
        # Sign In
        st.markdown("""
        <div class="panel" style="margin-bottom:20px">
          <div class="eyebrow">Returning Student</div>
          <div class="section-title" style="margin-bottom:8px">Sign In</div>
          <p style="font-size:14px;color:#7f6b62;margin-bottom:16px">Enter your Student ID to access your account and reservations.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("signin_form"):
            signin_id = st.text_input("Student ID", placeholder="e.g. S001")
            signin_btn = st.form_submit_button("Enter the Stage →", use_container_width=True)

            if signin_btn:
                sid = signin_id.strip().upper()
                if sid in st.session_state.students:
                    st.session_state.current_user = sid
                    s = st.session_state.students[sid]
                    st.markdown(f'<div class="msg-success">✓ Welcome back, {s["name"]}!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="msg-error">⚠ Student ID not found. Please check and try again.</div>', unsafe_allow_html=True)

        # Demo accounts
        st.markdown("""
        <div style="background:#f5eadf;border-radius:16px;padding:18px 20px;margin-top:8px">
          <div class="eyebrow" style="margin-bottom:10px">Demo Student IDs</div>
          <div style="font-size:13px;color:#5e4d46;line-height:2;font-family:'DM Mono',monospace">
            S001 — Emma Larson &nbsp; · &nbsp; 500,000 تومان<br/>
            S002 — Luca Moretti &nbsp; · &nbsp; 400,000 تومان<br/>
            S003 — Sofia Andersen · 600,000 تومان
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Registered students list
        if st.session_state.students:
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown('<div class="eyebrow" style="margin-bottom:12px">Registered Students</div>', unsafe_allow_html=True)
            for sid, s in st.session_state.students.items():
                active_res = len([r for r in st.session_state.reservations if r.get("email","") == s.get("email","") and r["status"] == "active"])
                is_me = st.session_state.current_user == sid
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 14px;border-radius:12px;margin-bottom:6px;
                            background:{'#fff7f7' if is_me else '#fffdf9'};
                            border:1px solid {'#6d1f2a' if is_me else '#e7d8c6'}">
                  <div>
                    <span style="font-weight:600;color:#241817">{s['name']}</span>
                    <span style="font-size:11px;color:#9b7250;margin-left:8px;font-family:monospace">{sid}</span>
                    {'<span style="font-size:11px;background:#ddf0e6;color:#2d7a58;padding:2px 8px;border-radius:99px;margin-left:6px">You</span>' if is_me else ''}
                  </div>
                  <span style="font-size:12px;color:#7f6b62">{active_res} booking{'s' if active_res!=1 else ''}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #e7d8c6;padding:24px 0;text-align:center">
  <span style="font-family:'Playfair Display',serif;font-size:16px;color:#6d1f2a">StagePass</span>
  <span style="color:#c8aa92;margin:0 10px">·</span>
  <span style="font-size:13px;color:#9b7250">Acting School · Hall Reservations</span>
  <span style="color:#c8aa92;margin:0 10px">·</span>
  <span style="font-size:13px;color:#9b7250">Small Hall: 80,000 تومان &nbsp;|&nbsp; Large Hall: 150,000 تومان</span>
</div>
""", unsafe_allow_html=True)
