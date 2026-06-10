import streamlit as st
from datetime import date, datetime, timedelta
import uuid
import plotly.graph_objects as go
import hashlib

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
    "grand":   {"name_en": "Grand Studio",  "name_fa": "گرند استودیو",
                "price": 70000, "seats": 120, "icon": "🎪",
                "desc_en": "120 seats · Professional lighting · Full backstage",
                "desc_fa": "۱۲۰ نفر · نور حرفه‌ای · پشت صحنه",
                "color": "#6d1f2a"},
    "studio2": {"name_en": "Studio 2",      "name_fa": "استودیو ۲",
                "price": 70000, "seats": 30,  "icon": "🎭",
                "desc_en": "30 seats · Mirrors · Sound system",
                "desc_fa": "۳۰ نفر · آینه · سیستم صوتی",
                "color": "#7c6fcd"},
}
SLOT_STARTS   = list(range(9, 21))   # 9 → 20  (last session ends at 21:00)
OWNER_PASS_DEFAULT = "admin123"
WINE  = "#6d1f2a"
GOLD  = "#b88a4a"
CREAM = "#f5eadf"

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
def _init():
    defs = {
        "lang":           "en",
        "page":           "gateway",      # gateway | login | register | home | owner-login | owner
        "owner_auth":     False,
        "owner_pass":     OWNER_PASS_DEFAULT,
        "reservations":   [],             # shared across ALL users
        "users":          {},             # {email: {name, pass_hash, reservations:[]}}
        "current_user":   None,           # email of logged-in user (None = guest)
        "smtp":           {"host": "", "port": 587, "user": "", "pass": ""},
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def hpw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def fmt(n: int) -> str:
    return f"{n:,} تومان"

def gen_id() -> str:
    return "RES-" + str(uuid.uuid4())[:8].upper()

def slot_label(start: int, dur: int) -> str:
    return f"{start:02d}:00–{start+dur:02d}:00"

def booked_hours(hall: str, date_str: str) -> set:
    taken = set()
    for r in st.session_state.reservations:
        if r["hall"] == hall and r["date"] == date_str and r["status"] == "active":
            for h in range(r["start_hour"], r["start_hour"] + r["duration"]):
                taken.add(h)
    return taken

def can_book(hall: str, date_str: str, start: int, dur: int) -> bool:
    taken = booked_hours(hall, date_str)
    for h in range(start, start + dur):
        if h in taken or h > 20:
            return False
    return True

def cancel_res(res_id: str):
    for r in st.session_state.reservations:
        if r["id"] == res_id:
            r["status"] = "cancelled"
            break

def is_fa() -> bool:
    return st.session_state.lang == "fa"

def go(page: str):
    st.session_state.page = page
    st.rerun()

FA = is_fa()
FONT = "'Vazirmatn','Tahoma',sans-serif" if FA else "'DM Sans',sans-serif"
DIR  = "rtl" if FA else "ltr"

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&family=Vazirmatn:wght@400;500;600;700&display=swap');
:root{{--wine:#6d1f2a;--gold:#b88a4a;--muted:#7f6b62;--line:#e7d8c6;--paper:#fffaf3;--ink:#241817}}
html,body,[data-testid="stAppViewContainer"]{{
  background:linear-gradient(135deg,#f6ecdf 0%,#fbf7f0 50%,#f1e2d2 100%)!important;
  font-family:{FONT}!important;color:var(--ink);direction:{DIR};
}}
[data-testid="stHeader"]{{background:rgba(255,249,240,.95)!important;border-bottom:1px solid var(--line)}}
[data-testid="stSidebar"]{{display:none}}
#MainMenu,footer,[data-testid="stToolbar"]{{display:none!important}}
section[data-testid="stMain"]{{padding-top:0!important}}
.display{{font-family:'Playfair Display',serif;font-weight:700}}

/* ── HERO ── */
.hero{{
  background:
    linear-gradient(90deg,rgba(36,24,23,.86),rgba(36,24,23,.28) 60%,rgba(36,24,23,.06)),
    url('https://images.unsplash.com/photo-1503095396549-807759245b35?w=1400&q=80&fit=crop') center/cover;
  border-radius:24px;padding:48px 44px;color:#fff;margin-bottom:22px;
  box-shadow:0 16px 48px rgba(72,16,25,.18);
}}
.hero h1{{font-family:'Playfair Display',serif;font-size:34px;font-weight:700;line-height:1.1;margin:0 0 10px}}
.hero p{{font-size:14px;color:rgba(255,255,255,.84);line-height:1.7;margin:0;max-width:500px}}
.hero-badge{{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:99px;
  background:var(--gold);font-size:11px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:#fff;margin-bottom:14px}}
.owner-hero{{
  background:
    linear-gradient(90deg,rgba(15,5,8,.92),rgba(15,5,8,.42) 60%,rgba(15,5,8,.08)),
    url('https://images.unsplash.com/photo-1503095396549-807759245b35?w=1400&q=80&fit=crop') center/cover;
  border-radius:24px;padding:36px 44px;color:#fff;margin-bottom:22px;
  box-shadow:0 16px 48px rgba(72,16,25,.22);
}}
.owner-hero h1{{font-family:'Playfair Display',serif;font-size:28px;font-weight:700;margin:0 0 6px}}
.owner-hero p{{font-size:13px;color:rgba(255,255,255,.78);margin:0}}
.owner-badge{{display:inline-flex;align-items:center;gap:4px;
  background:linear-gradient(135deg,var(--gold),#8a6030);color:#fff;
  font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  padding:3px 10px;border-radius:99px;margin-bottom:10px}}

/* ── PANELS ── */
.panel{{background:var(--paper);border:1px solid var(--line);border-radius:20px;
  padding:22px;box-shadow:0 6px 24px rgba(72,16,25,.05);margin-bottom:14px}}
.panel-dark{{background:#2f1d1a;border-radius:20px;padding:22px;color:#fff;margin-bottom:14px}}
.eyebrow{{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#9b7250;margin-bottom:4px}}
.eyebrow-light{{color:#d8b47b}}

/* ── GATEWAY CARDS ── */
.gcard{{border-radius:24px;padding:34px 22px;text-align:center;
  border:1.5px solid var(--line);background:var(--paper);margin-bottom:10px}}
.gcard-owner{{background:#1e0f0f;border:2px solid var(--gold);border-radius:24px;
  padding:34px 22px;text-align:center;margin-bottom:10px}}

/* ── HALL CARDS ── */
.hall-card{{border:1px solid var(--line);border-radius:16px;padding:16px;
  background:#fffdf9;transition:all .2s;margin-bottom:8px}}
.hall-card.sel{{border-color:var(--wine);background:#fff7f7;
  box-shadow:0 6px 20px rgba(109,31,42,.1)}}

/* ── STAT CARDS ── */
.stat-card{{background:var(--paper);border:1px solid var(--line);border-radius:18px;
  padding:18px;text-align:center;box-shadow:0 4px 14px rgba(72,16,25,.04)}}
.stat-num{{font-family:'Playfair Display',serif;font-size:30px;color:var(--wine);font-weight:700}}
.stat-lbl{{font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:#9b7250;margin-top:5px}}

/* ── RESERVATION CARDS ── */
.res-card{{background:var(--paper);border:1px solid var(--line);border-radius:18px;
  padding:16px;margin-bottom:10px;box-shadow:0 4px 12px rgba(72,16,25,.04)}}
.res-card.cancelled{{opacity:.6}}
.res-id{{font-size:10px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;
  color:#9b7250;margin-bottom:3px}}
.res-hall{{font-family:'Playfair Display',serif;font-size:18px;color:#2b1c19;margin-bottom:4px}}
.res-price{{font-family:'Playfair Display',serif;font-size:20px;color:var(--wine)}}
.badge-active{{display:inline-flex;padding:3px 10px;border-radius:99px;
  font-size:11px;font-weight:600;background:#e7f3ec;color:#2d7a58}}
.badge-cancelled{{display:inline-flex;padding:3px 10px;border-radius:99px;
  font-size:11px;font-weight:600;background:#f2e2e0;color:#8b2d36}}
.badge-owner{{display:inline-flex;padding:3px 10px;border-radius:99px;
  font-size:11px;font-weight:600;background:rgba(184,138,74,.18);color:#7a5a22}}

/* ── SUMMARY STRIP ── */
.summary-strip{{background:#f5eadf;border-radius:12px;padding:12px 16px;
  display:flex;justify-content:space-between;align-items:center;margin:12px 0}}

/* ── MESSAGES ── */
.msg-ok{{background:#e8f3ec;color:#2d6b4f;border-radius:11px;
  padding:10px 14px;font-size:14px;font-weight:500;margin:8px 0}}
.msg-err{{background:#f8e5e3;color:#8b2d36;border-radius:11px;
  padding:10px 14px;font-size:14px;font-weight:500;margin:8px 0}}
.msg-info{{background:#e8f0fb;color:#1a4a8a;border-radius:11px;
  padding:10px 14px;font-size:14px;font-weight:500;margin:8px 0}}

/* ── FIELDS ── */
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stDateInput>div>div>input{{
  border:1px solid var(--line)!important;background:#fffdf9!important;
  border-radius:12px!important;padding:12px 14px!important;
  font-family:{FONT}!important;font-size:14px!important;color:var(--ink)!important}}
.stTextInput>div>div>input:focus{{
  border-color:var(--wine)!important;box-shadow:0 0 0 3px rgba(109,31,42,.1)!important}}
label[data-testid="stWidgetLabel"]>div>p{{
  font-size:13px!important;font-weight:600!important;color:var(--ink)!important}}
.stSelectbox>div>div>div{{
  border:1px solid var(--line)!important;background:#fffdf9!important;
  border-radius:12px!important;font-family:{FONT}!important}}

/* ── BUTTONS ── */
.stButton>button{{
  background:var(--wine)!important;color:#fff!important;border:none!important;
  border-radius:13px!important;padding:11px 20px!important;
  font-family:{FONT}!important;font-size:14px!important;font-weight:600!important;
  box-shadow:0 4px 14px rgba(109,31,42,.2)!important;transition:.2s!important;width:100%!important}}
.stButton>button:hover{{background:#571821!important;transform:translateY(-1px)!important}}
.btn-gold>button{{background:linear-gradient(135deg,var(--gold),#8a6030)!important;
  color:#1e0f0f!important;box-shadow:0 4px 14px rgba(184,138,74,.25)!important}}
.btn-cancel>button{{background:#f2e2e0!important;color:#7b2932!important;
  box-shadow:none!important;font-size:12px!important;padding:7px 14px!important}}
.btn-ghost>button{{background:none!important;color:var(--muted)!important;
  border:1px solid var(--line)!important;box-shadow:none!important;font-size:13px!important}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{{gap:4px;background:transparent;border-bottom:2px solid var(--line)}}
.stTabs [data-baseweb="tab"]{{background:transparent!important;border:none!important;
  color:var(--muted)!important;font-family:{FONT}!important;font-weight:600!important;
  font-size:13px!important;padding:9px 16px!important;border-radius:0!important}}
.stTabs [aria-selected="true"]{{color:var(--wine)!important;border-bottom:2px solid var(--wine)!important}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:18px!important}}

hr{{border:none;border-top:1px solid var(--line);margin:14px 0}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LANGUAGE TOGGLE
# ─────────────────────────────────────────────
_, lc = st.columns([7, 1])
with lc:
    lx = st.selectbox("🌐", ["English", "فارسی"],
                      index=0 if st.session_state.lang == "en" else 1,
                      label_visibility="collapsed", key="lang_sel")
    nl = "en" if lx == "English" else "fa"
    if nl != st.session_state.lang:
        st.session_state.lang = nl
        st.rerun()


# ─────────────────────────────────────────────
#  SHARED: BOOKING FORM (used by both user & owner)
# ─────────────────────────────────────────────
def booking_form(prefix: str, booked_by_email: str, booked_by_name: str, is_owner_booking: bool = False):
    """Renders a full booking form. prefix avoids key collisions."""
    FA = is_fa()
    with st.form(f"book_form_{prefix}"):
        if is_owner_booking:
            st.markdown(f'<div class="msg-info">👑 {"Booking as owner — choose any hall and slot." if not FA else "رزرو به عنوان مدیر — هر سالن و بازه‌ای را انتخاب کنید."}</div>', unsafe_allow_html=True)
            gname = st.text_input("Guest Name" if not FA else "نام مهمان", value="", key=f"{prefix}_gname")
            gemail = st.text_input("Guest Email (optional)" if not FA else "ایمیل مهمان (اختیاری)", value="", key=f"{prefix}_gemail")
        else:
            gname  = booked_by_name
            gemail = booked_by_email

        bdate = st.date_input(
            "Date" if not FA else "تاریخ",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=60),
            value=date.today() + timedelta(days=1),
            key=f"{prefix}_date"
        )

        # Hall choice
        hall_options = {
            (HALLS["grand"]["name_fa"] if FA else HALLS["grand"]["name_en"]): "grand",
            (HALLS["studio2"]["name_fa"] if FA else HALLS["studio2"]["name_en"]): "studio2",
        }
        hall_label = st.selectbox(
            "Choose a Hall" if not FA else "انتخاب سالن",
            list(hall_options.keys()),
            key=f"{prefix}_hall"
        )
        hall_key = hall_options[hall_label]
        hall     = HALLS[hall_key]

        # Duration
        dur = st.slider(
            "Duration (hours)" if not FA else "مدت زمان (ساعت)",
            min_value=1, max_value=6, value=1,
            key=f"{prefix}_dur"
        )

        # Available slots — computed live
        date_str = str(bdate)
        avail = [
            s for s in SLOT_STARTS
            if s + dur <= 21 and can_book(hall_key, date_str, s, dur)
        ]
        taken_all = [
            s for s in SLOT_STARTS
            if not can_book(hall_key, date_str, s, 1)
        ]

        if avail:
            slot_map = {slot_label(s, dur): s for s in avail}
            chosen = st.selectbox(
                "Start Time Slot" if not FA else "بازه شروع",
                list(slot_map.keys()),
                key=f"{prefix}_slot"
            )
            start_hour = slot_map[chosen]
        else:
            st.warning("No slots available for this hall / date / duration." if not FA
                       else "هیچ بازه‌ای برای این سالن / تاریخ / مدت موجود نیست.")
            start_hour = None

        # Summary
        total = hall["price"] * dur
        slot_disp = slot_label(start_hour, dur) if start_hour is not None else "—"
        hall_name = hall["name_fa"] if FA else hall["name_en"]
        st.markdown(f"""
        <div class="summary-strip">
          <div>
            <div style="font-size:10px;font-weight:600;letter-spacing:.14em;
                        text-transform:uppercase;color:#9b7250">
              {"Selected Hall" if not FA else "سالن انتخابی"}
            </div>
            <div style="font-size:13px;color:#5e4d46;margin-top:2px">
              {hall["icon"]} {hall_name} · {slot_disp}
            </div>
          </div>
          <div style="text-align:{'left' if FA else 'right'}">
            <div style="font-size:10px;font-weight:600;letter-spacing:.14em;
                        text-transform:uppercase;color:#9b7250">
              {"Total Price" if not FA else "قیمت کل"}
            </div>
            <div style="font-family:'Playfair Display',serif;font-size:20px;
                        color:var(--wine);margin-top:2px">
              {fmt(total) if start_hour is not None else "—"}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "🎫 Confirm Reservation & Pay" if not FA else "🎫 تأیید رزرو و پرداخت",
            use_container_width=True
        )

    # ── handle submission outside form ──
    if submitted:
        if is_owner_booking:
            actual_name  = gname.strip() or "Owner Booking"
            actual_email = gemail.strip().lower() or "owner@padmart.internal"
        else:
            actual_name  = gname
            actual_email = gemail

        if start_hour is None:
            st.markdown('<div class="msg-err">⚠ ' +
                        ("No available slot selected." if not FA else "بازه‌ای انتخاب نشده.") +
                        "</div>", unsafe_allow_html=True)
        elif not can_book(hall_key, date_str, start_hour, dur):
            st.markdown('<div class="msg-err">⚠ ' +
                        ("This slot was just taken. Please pick another." if not FA
                         else "این بازه همین لحظه رزرو شد. لطفاً بازه دیگری انتخاب کنید.") +
                        "</div>", unsafe_allow_html=True)
        elif (not is_owner_booking and
              len([r for r in st.session_state.reservations
                   if r["email"] == actual_email and r["status"] == "active"]) >= 5):
            st.markdown('<div class="msg-err">⚠ ' +
                        ("Max 5 active bookings per account." if not FA
                         else "حداکثر ۵ رزرو فعال برای هر حساب.") +
                        "</div>", unsafe_allow_html=True)
        else:
            sl  = slot_label(start_hour, dur)
            new = {
                "id":           gen_id(),
                "name":         actual_name,
                "email":        actual_email,
                "hall":         hall_key,
                "hall_en":      hall["name_en"],
                "hall_fa":      hall["name_fa"],
                "hall_color":   hall["color"],
                "date":         date_str,
                "start_hour":   start_hour,
                "duration":     dur,
                "slot_label":   sl,
                "price":        total,
                "status":       "active",
                "booked_by":    "owner" if is_owner_booking else "user",
                "booked_at":    datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            st.session_state.reservations.append(new)
            # also attach to user record
            if actual_email in st.session_state.users:
                st.session_state.users[actual_email]["reservations"].append(new["id"])
            ok = ("✓ Reservation confirmed! " + hall_name + " · " + sl
                  if not FA else "✓ رزرو تأیید شد! " + hall_name + " · " + sl)
            st.markdown(f'<div class="msg-ok">{ok}</div>', unsafe_allow_html=True)
            st.balloons()
            st.rerun()


# ─────────────────────────────────────────────
#  SHARED: CALENDAR CHART
# ─────────────────────────────────────────────
def calendar_chart(reservations_list: list, title: str = ""):
    """Renders a Google-Calendar-style Gantt/timeline chart."""
    FA = is_fa()
    active = [r for r in reservations_list if r["status"] == "active"]
    if not active:
        st.markdown(f"""
        <div style="text-align:center;padding:48px;background:var(--paper);
                    border:2px dashed #d7c5b4;border-radius:20px;margin-top:10px">
          <div style="font-size:36px;margin-bottom:10px">📅</div>
          <div style="font-family:'Playfair Display',serif;font-size:18px;margin-bottom:6px">
            {"No active reservations" if not FA else "رزرو فعالی وجود ندارد"}
          </div>
          <div style="font-size:13px;color:var(--muted)">
            {"Confirmed bookings will appear on the calendar." if not FA
             else "رزروهای تأیید‌شده اینجا نمایش داده می‌شود."}
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Collect unique dates sorted
    dates = sorted(set(r["date"] for r in active))

    fig = go.Figure()
    y_labels   = []   # y-axis: each row = one hall+date combo
    row_map    = {}   # (hall, date) -> row index
    row_idx    = 0

    # Build one row per (date, hall) combination that has bookings
    for d in dates:
        for hk in ["grand", "studio2"]:
            hall_active = [r for r in active if r["date"] == d and r["hall"] == hk]
            if not hall_active:
                continue
            row_key = (hk, d)
            row_map[row_key] = row_idx
            hn = HALLS[hk]["name_fa"] if FA else HALLS[hk]["name_en"]
            y_labels.append(f"{d}  {HALLS[hk]['icon']}  {hn}")
            row_idx += 1

    for r in active:
        hk  = r["hall"]
        d   = r["date"]
        key = (hk, d)
        if key not in row_map:
            continue
        row  = row_map[key]
        x0   = r["start_hour"]
        x1   = r["start_hour"] + r["duration"]
        color = HALLS[hk]["color"]
        label = f"{r['name']}<br>{r['slot_label']}<br>{fmt(r['price'])}"

        # Main bar
        fig.add_trace(go.Bar(
            x=[r["duration"]],
            y=[row],
            base=[x0],
            orientation="h",
            marker=dict(
                color=color,
                opacity=0.82,
                line=dict(color="white", width=2),
            ),
            hovertemplate=(
                f"<b>{r['hall_en'] if not FA else r['hall_fa']}</b><br>"
                f"{'Guest' if not FA else 'مهمان'}: {r['name']}<br>"
                f"{'Date' if not FA else 'تاریخ'}: {r['date']}<br>"
                f"{'Slot' if not FA else 'بازه'}: {r['slot_label']}<br>"
                f"{'Duration' if not FA else 'مدت'}: {r['duration']}h<br>"
                f"{'Paid' if not FA else 'مبلغ'}: {fmt(r['price'])}<extra></extra>"
            ),
            name=r["name"],
            showlegend=False,
            text=r["name"],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=11),
        ))

    # Hour gridlines
    for h in range(9, 22):
        fig.add_vline(x=h, line=dict(color="rgba(200,180,160,.35)", width=1, dash="dot"))

    fig.update_layout(
        title=dict(
            text=title or ("📅 Reservation Calendar" if not FA else "📅 تقویم رزروها"),
            font=dict(family="Playfair Display, serif", size=18, color=WINE),
            x=0.5
        ),
        barmode="stack",
        plot_bgcolor="#fffaf3",
        paper_bgcolor="#fffaf3",
        xaxis=dict(
            range=[8.5, 21.5],
            tickvals=list(range(9, 22)),
            ticktext=[f"{h:02d}:00" for h in range(9, 22)],
            tickfont=dict(size=11, color="#7f6b62"),
            showgrid=False,
            title=dict(text="Hour" if not FA else "ساعت", font=dict(color="#9b7250", size=12)),
        ),
        yaxis=dict(
            tickvals=list(range(len(y_labels))),
            ticktext=y_labels,
            tickfont=dict(size=11, color="#5e4d46"),
            showgrid=True,
            gridcolor="rgba(231,216,198,.5)",
        ),
        height=max(300, 80 + len(y_labels) * 56),
        margin=dict(l=10, r=20, t=50, b=40),
        font=dict(family="DM Sans, sans-serif"),
        hoverlabel=dict(
            bgcolor="#fffaf3",
            bordercolor=WINE,
            font=dict(family="DM Sans", size=12, color="#241817"),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  SHARED: RES CARD + CANCEL
# ─────────────────────────────────────────────
def res_cards(reservations_list: list, cancel_prefix: str, show_email: bool = False):
    FA = is_fa()
    for r in sorted(reservations_list, key=lambda x: x["date"], reverse=True):
        cancelled = r["status"] == "cancelled"
        hn = r["hall_fa"] if FA else r["hall_en"]
        badge_cls = "badge-cancelled" if cancelled else "badge-active"
        badge_txt = ("✕ Cancelled" if not FA else "✕ لغو شده") if cancelled else ("✓ Confirmed" if not FA else "✓ تأیید شده")
        owner_tag = (f'<span class="badge-owner">👑 {"Owner" if not FA else "مدیر"}</span>'
                     if r.get("booked_by") == "owner" else "")
        email_row = f'<div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">Email</div><div style="margin-top:2px;font-size:11px;color:#4b3932;word-break:break-all">{r["email"]}</div></div>' if show_email else ""
        st.markdown(f"""
        <div class="res-card {'cancelled' if cancelled else ''}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap">
            <div>
              <div class="res-id">{r['id']}</div>
              <div class="res-hall">{r['hall_en' if not FA else 'hall_fa']}</div>
              <span class="{badge_cls}">{badge_txt}</span> {owner_tag}
            </div>
            <div class="res-price">{fmt(r['price'])}</div>
          </div>
          <div style="display:grid;grid-template-columns:repeat({'4' if not show_email else '5'},1fr);gap:8px;margin-top:10px;font-size:12px">
            <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{"Guest" if not FA else "مهمان"}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['name']}</div></div>
            {email_row}
            <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{"Date" if not FA else "تاریخ"}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['date']}</div></div>
            <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{"Slot" if not FA else "بازه"}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['slot_label']}</div></div>
            <div><div style="font-size:9px;font-weight:600;text-transform:uppercase;color:#9b7250">{"Dur." if not FA else "مدت"}</div><div style="margin-top:2px;font-weight:500;color:#4b3932">{r['duration']}h</div></div>
          </div>
          <div style="margin-top:10px;padding-top:8px;border-top:1px solid #eee0d3;font-size:11px;color:var(--muted)">
            {"Cancel anytime for a full refund." if not cancelled and not FA
             else "هر زمان لغو کنید — بازپرداخت کامل." if not cancelled
             else ("This reservation has been refunded." if not FA else "این رزرو بازپرداخت شده است.")}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if not cancelled:
            st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
            if st.button("Cancel & Refund" if not FA else "لغو و بازپرداخت",
                         key=f"{cancel_prefix}_cancel_{r['id']}"):
                cancel_res(r["id"])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██████  PAGE: GATEWAY
# ─────────────────────────────────────────────
if st.session_state.page == "gateway":
    FA = is_fa()
    st.markdown(f"""
    <div class="hero" style="text-align:center;padding:52px 32px">
      <div style="font-size:52px;margin-bottom:10px">🎭</div>
      <h1>Padmart</h1>
      <p style="font-size:13px;letter-spacing:.25em;text-transform:uppercase;
                color:rgba(200,169,110,.9);margin-top:4px">
        {"Acting School · Hall Reservations" if not FA else "مدرسه بازیگری · رزرو سالن"}
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="gcard">
          <div style="font-size:40px;margin-bottom:12px">🆕</div>
          <div style="font-family:'Playfair Display',serif;font-size:20px;color:var(--wine);margin-bottom:8px">
            {"Register" if not FA else "ثبت‌نام"}
          </div>
          <div style="font-size:13px;color:var(--muted);line-height:1.65;margin-bottom:0">
            {"Create an account to book halls and track all your reservations"
             if not FA else "ثبت‌نام کنید تا سالن رزرو کنید و همه رزروهایتان را پیگیری کنید"}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Account →" if not FA else "ایجاد حساب ←",
                     key="btn_register", use_container_width=True):
            go("register")

    with c2:
        st.markdown(f"""
        <div class="gcard">
          <div style="font-size:40px;margin-bottom:12px">🎟</div>
          <div style="font-family:'Playfair Display',serif;font-size:20px;color:var(--wine);margin-bottom:8px">
            {"Sign In" if not FA else "ورود"}
          </div>
          <div style="font-size:13px;color:var(--muted);line-height:1.65;margin-bottom:0">
            {"Sign in to your account to book, view your history and cancel reservations"
             if not FA else "وارد حساب خود شوید تا رزرو کنید، تاریخچه را ببینید و لغو کنید"}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign In →" if not FA else "ورود ←",
                     key="btn_login", use_container_width=True):
            go("login")

    with c3:
        st.markdown(f"""
        <div class="gcard-owner">
          <div style="font-size:40px;margin-bottom:12px">👑</div>
          <div style="font-family:'Playfair Display',serif;font-size:20px;color:#fff;margin-bottom:8px">
            {"Site Owner" if not FA else "مدیر سایت"}
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,.62);line-height:1.65;margin-bottom:0">
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
    <p style="text-align:center;font-size:13px;color:var(--muted);margin-top:20px">
      {"Grand Studio · Studio 2 · 70,000 تومان/hr · Full Refund on Cancellation"
       if not FA else "گرند استودیو · استودیو ۲ · ۷۰،۰۰۰ تومان/ساعت · بازپرداخت کامل در صورت لغو"}
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██████  PAGE: REGISTER
# ─────────────────────────────────────────────
elif st.session_state.page == "register":
    FA = is_fa()
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button("← Back" if not FA else "← بازگشت", key="reg_back"):
        go("gateway")
    st.markdown("</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown(f"""
        <div style="text-align:center;margin:20px 0 22px">
          <div style="font-size:40px;margin-bottom:8px">🆕</div>
          <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:var(--wine)">
            {"Create Your Account" if not FA else "ایجاد حساب کاربری"}
          </h2>
          <p style="font-size:13px;color:var(--muted);margin-top:4px">
            {"Book halls and track all your reservations in one place."
             if not FA else "سالن رزرو کنید و همه رزروهایتان را یکجا پیگیری کنید."}
          </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            rname = st.text_input("Full Name" if not FA else "نام و نام خانوادگی",
                                  placeholder="Sara Mohammadi")
            remail = st.text_input("Email" if not FA else "ایمیل",
                                   placeholder="sara@email.com")
            rpass1 = st.text_input("Password" if not FA else "رمز عبور",
                                   type="password", placeholder="min 6 characters")
            rpass2 = st.text_input("Confirm Password" if not FA else "تأیید رمز عبور",
                                   type="password", placeholder="repeat password")
            sub = st.form_submit_button(
                "Create Account" if not FA else "ایجاد حساب",
                use_container_width=True
            )

        if sub:
            if not rname.strip():
                st.markdown('<div class="msg-err">⚠ ' + ("Enter your name." if not FA else "نام خود را وارد کنید.") + "</div>", unsafe_allow_html=True)
            elif not remail.strip() or "@" not in remail:
                st.markdown('<div class="msg-err">⚠ ' + ("Enter a valid email." if not FA else "یک ایمیل معتبر وارد کنید.") + "</div>", unsafe_allow_html=True)
            elif remail.strip().lower() in st.session_state.users:
                st.markdown('<div class="msg-err">⚠ ' + ("Email already registered." if not FA else "این ایمیل قبلاً ثبت‌نام شده.") + "</div>", unsafe_allow_html=True)
            elif len(rpass1) < 6:
                st.markdown('<div class="msg-err">⚠ ' + ("Password must be at least 6 characters." if not FA else "رمز عبور باید حداقل ۶ کاراکتر باشد.") + "</div>", unsafe_allow_html=True)
            elif rpass1 != rpass2:
                st.markdown('<div class="msg-err">⚠ ' + ("Passwords do not match." if not FA else "رمزها یکسان نیستند.") + "</div>", unsafe_allow_html=True)
            else:
                email_key = remail.strip().lower()
                st.session_state.users[email_key] = {
                    "name":         rname.strip(),
                    "email":        email_key,
                    "pass_hash":    hpw(rpass1),
                    "reservations": [],
                }
                st.session_state.current_user = email_key
                st.markdown('<div class="msg-ok">✓ ' + ("Account created! Welcome, " + rname.strip() + "." if not FA else "حساب ایجاد شد! خوش آمدید، " + rname.strip() + ".") + "</div>", unsafe_allow_html=True)
                go("home")


# ─────────────────────────────────────────────
#  ██████  PAGE: LOGIN
# ─────────────────────────────────────────────
elif st.session_state.page == "login":
    FA = is_fa()
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button("← Back" if not FA else "← بازگشت", key="login_back"):
        go("gateway")
    st.markdown("</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown(f"""
        <div style="text-align:center;margin:20px 0 22px">
          <div style="font-size:40px;margin-bottom:8px">🎟</div>
          <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:var(--wine)">
            {"Sign In" if not FA else "ورود به حساب"}
          </h2>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            lemail = st.text_input("Email" if not FA else "ایمیل",
                                   placeholder="sara@email.com")
            lpass  = st.text_input("Password" if not FA else "رمز عبور",
                                   type="password")
            sub = st.form_submit_button(
                "Sign In" if not FA else "ورود",
                use_container_width=True
            )

        if sub:
            key = lemail.strip().lower()
            user = st.session_state.users.get(key)
            if not user or user["pass_hash"] != hpw(lpass):
                st.markdown('<div class="msg-err">⚠ ' + ("Incorrect email or password." if not FA else "ایمیل یا رمز عبور نادرست است.") + "</div>", unsafe_allow_html=True)
            else:
                st.session_state.current_user = key
                go("home")

        st.markdown("---")
        st.markdown(f'<p style="text-align:center;font-size:13px;color:var(--muted)">{"Don\'t have an account?" if not FA else "حساب ندارید؟"}</p>', unsafe_allow_html=True)
        if st.button("Create Account" if not FA else "ثبت‌نام کنید",
                     key="login_go_reg", use_container_width=True):
            go("register")


# ─────────────────────────────────────────────
#  ██████  PAGE: USER HOME
# ─────────────────────────────────────────────
elif st.session_state.page == "home":
    FA = is_fa()
    cu = st.session_state.current_user
    if not cu or cu not in st.session_state.users:
        go("login")

    user = st.session_state.users[cu]

    # Nav bar
    nav1, nav2 = st.columns([5, 1])
    with nav2:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("Sign Out" if not FA else "خروج", key="home_signout"):
            st.session_state.current_user = None
            go("gateway")
        st.markdown("</div>", unsafe_allow_html=True)

    # Hero
    st.markdown(f"""
    <div class="hero">
      <div class="hero-badge">🎟 {"Welcome back" if not FA else "خوش آمدید"}</div>
      <h1>{user['name']}</h1>
      <p>{"Book a hall, view your personal calendar and manage your reservations."
          if not FA else "سالن رزرو کنید، تقویم شخصی خود را ببینید و رزروهایتان را مدیریت کنید."}</p>
    </div>
    """, unsafe_allow_html=True)

    # User's reservations
    my_res = [r for r in st.session_state.reservations if r["email"] == cu]
    active_count = len([r for r in my_res if r["status"] == "active"])

    # Quick stats for user
    qs1, qs2, qs3 = st.columns(3)
    qs1.markdown(f'<div class="stat-card"><div class="stat-num">{len(my_res)}</div><div class="stat-lbl">{"Total Bookings" if not FA else "کل رزروها"}</div></div>', unsafe_allow_html=True)
    qs2.markdown(f'<div class="stat-card"><div class="stat-num">{active_count}</div><div class="stat-lbl">{"Active" if not FA else "فعال"}</div></div>', unsafe_allow_html=True)
    qs3.markdown(f'<div class="stat-card"><div class="stat-num">{fmt(sum(r["price"] for r in my_res if r["status"]=="active"))}</div><div class="stat-lbl">{"Total Spent" if not FA else "مجموع هزینه"}</div></div>', unsafe_allow_html=True)

    st.markdown("")

    tab_book, tab_cal, tab_myres = st.tabs([
        "📅 " + ("Book a Hall" if not FA else "رزرو سالن"),
        "📆 " + ("My Calendar" if not FA else "تقویم من"),
        "📋 " + ("My Account & Reservations" if not FA else "حساب و رزروهای من"),
    ])

    with tab_book:
        left, right = st.columns([1.3, 0.85], gap="medium")
        with left:
            st.markdown(f"""
            <div class="eyebrow">{"Book a Rehearsal Hall" if not FA else "رزرو سالن تمرین"}</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:16px">
              {"Choose your hall, duration and time slot" if not FA else "سالن، مدت و بازه زمانی را انتخاب کنید"}
            </h2>
            """, unsafe_allow_html=True)
            booking_form("user", cu, user["name"], is_owner_booking=False)

        with right:
            st.markdown(f"""
            <div class="panel-dark">
              <div class="eyebrow eyebrow-light">{"How It Works" if not FA else "نحوه عملکرد"}</div>
              <div style="font-family:'Playfair Display',serif;font-size:18px;margin:6px 0 14px">
                {"Simple Steps" if not FA else "مراحل ساده"}
              </div>
              <div style="font-size:12px;color:rgba(255,255,255,.72);line-height:1.7">
                <div style="display:flex;gap:8px;margin-bottom:8px">
                  <span style="color:var(--gold);font-weight:700;flex-shrink:0">01</span>
                  <span>{"Pick a hall and date." if not FA else "سالن و تاریخ را انتخاب کنید."}</span>
                </div>
                <div style="display:flex;gap:8px;margin-bottom:8px">
                  <span style="color:var(--gold);font-weight:700;flex-shrink:0">02</span>
                  <span>{"Set how many hours you need (1–6h)." if not FA else "تعداد ساعت مورد نیاز را تنظیم کنید (۱ تا ۶ ساعت)."}</span>
                </div>
                <div style="display:flex;gap:8px;margin-bottom:8px">
                  <span style="color:var(--gold);font-weight:700;flex-shrink:0">03</span>
                  <span>{"Only available slots (no overlaps) are shown." if not FA else "فقط بازه‌های موجود (بدون تداخل) نمایش داده می‌شود."}</span>
                </div>
                <div style="display:flex;gap:8px">
                  <span style="color:var(--gold);font-weight:700;flex-shrink:0">04</span>
                  <span>{"Cancel anytime for a full refund." if not FA else "هر زمان لغو کنید — بازپرداخت کامل."}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="panel">
              <div class="eyebrow" style="margin-bottom:10px">{"Hall Prices" if not FA else "قیمت سالن‌ها"}</div>
              <div style="display:flex;gap:10px;margin-bottom:12px">
                <div style="font-size:26px">🎪</div>
                <div>
                  <div style="font-weight:600">{"Grand Studio" if not FA else "گرند استودیو"}</div>
                  <div style="font-size:11px;color:var(--muted)">120 seats · Pro lighting</div>
                  <div style="font-size:14px;font-weight:700;color:var(--wine)">70,000 تومان/hr</div>
                </div>
              </div>
              <div style="display:flex;gap:10px">
                <div style="font-size:26px">🎭</div>
                <div>
                  <div style="font-weight:600">{"Studio 2" if not FA else "استودیو ۲"}</div>
                  <div style="font-size:11px;color:var(--muted)">30 seats · Mirrors</div>
                  <div style="font-size:14px;font-weight:700;color:var(--wine)">70,000 تومان/hr</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_cal:
        st.markdown(f"""
        <div class="eyebrow">{"My Reservation Calendar" if not FA else "تقویم رزروهای من"}</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:4px">
          {"Your Booked Sessions" if not FA else "جلسات رزروشده شما"}
        </h2>
        <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
          {"Each bar shows your reserved time block. Hover for details." if not FA
           else "هر نوار یک بلوک زمانی رزرو شده شما را نشان می‌دهد. برای جزئیات نگه دارید."}
        </p>
        """, unsafe_allow_html=True)
        calendar_chart(my_res, "📅 " + ("My Calendar" if not FA else "تقویم من"))

    with tab_myres:
        st.markdown(f"""
        <div class="eyebrow">{"Account & Reservations" if not FA else "حساب و رزروها"}</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:16px">
          {user['name']}
        </h2>
        """, unsafe_allow_html=True)

        # Account info card
        st.markdown(f"""
        <div class="panel" style="margin-bottom:18px">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:13px">
            <div>
              <div style="font-size:10px;font-weight:600;text-transform:uppercase;color:#9b7250">
                {"Name" if not FA else "نام"}
              </div>
              <div style="font-weight:600;color:var(--ink);margin-top:3px">{user['name']}</div>
            </div>
            <div>
              <div style="font-size:10px;font-weight:600;text-transform:uppercase;color:#9b7250">Email</div>
              <div style="font-weight:600;color:var(--ink);margin-top:3px">{cu}</div>
            </div>
            <div>
              <div style="font-size:10px;font-weight:600;text-transform:uppercase;color:#9b7250">
                {"Total Bookings" if not FA else "کل رزروها"}
              </div>
              <div style="font-weight:600;color:var(--wine);margin-top:3px">{len(my_res)}</div>
            </div>
            <div>
              <div style="font-size:10px;font-weight:600;text-transform:uppercase;color:#9b7250">
                {"Total Spent" if not FA else "مجموع هزینه"}
              </div>
              <div style="font-weight:600;color:var(--wine);margin-top:3px">
                {fmt(sum(r['price'] for r in my_res if r['status']=='active'))}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not my_res:
            st.markdown(f"""
            <div style="text-align:center;padding:40px;background:var(--paper);
                        border:2px dashed #d7c5b4;border-radius:20px">
              <div style="font-size:34px;margin-bottom:10px">🎟</div>
              <div style="font-family:'Playfair Display',serif;font-size:18px">
                {"No reservations yet" if not FA else "هنوز رزروی ندارید"}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            res_cards(my_res, "user_home", show_email=False)

        # Change password
        with st.expander("🔒 " + ("Change Password" if not FA else "تغییر رمز عبور")):
            with st.form("user_pass_form"):
                op  = st.text_input("Current Password" if not FA else "رمز فعلی", type="password")
                np1 = st.text_input("New Password" if not FA else "رمز جدید", type="password")
                np2 = st.text_input("Confirm New Password" if not FA else "تأیید رمز جدید", type="password")
                if st.form_submit_button("Save" if not FA else "ذخیره", use_container_width=True):
                    if user["pass_hash"] != hpw(op):
                        st.error("Current password incorrect." if not FA else "رمز فعلی نادرست است.")
                    elif len(np1) < 6:
                        st.error("Min 6 characters." if not FA else "حداقل ۶ کاراکتر.")
                    elif np1 != np2:
                        st.error("Passwords do not match." if not FA else "رمزها یکسان نیستند.")
                    else:
                        st.session_state.users[cu]["pass_hash"] = hpw(np1)
                        st.success("Password updated!" if not FA else "رمز عبور به‌روز شد!")


# ─────────────────────────────────────────────
#  ██████  PAGE: OWNER LOGIN
# ─────────────────────────────────────────────
elif st.session_state.page == "owner-login":
    FA = is_fa()
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button("← Back" if not FA else "← بازگشت", key="ol_back"):
        go("gateway")
    st.markdown("</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown(f"""
        <div style="text-align:center;margin:28px 0 22px">
          <div style="font-size:40px;margin-bottom:8px">👑</div>
          <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:var(--wine)">
            {"Owner Login" if not FA else "ورود مدیر"}
          </h2>
          <p style="font-size:13px;color:var(--muted);margin-top:4px">
            {"Enter your password to access the full dashboard."
             if not FA else "رمز عبور خود را برای دسترسی به داشبورد وارد کنید."}
          </p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("owner_login_form"):
            pw  = st.text_input("Password" if not FA else "رمز عبور",
                                type="password", placeholder="••••••••")
            sub = st.form_submit_button(
                "Enter Dashboard" if not FA else "ورود به داشبورد",
                use_container_width=True
            )
        if sub:
            if pw == st.session_state.owner_pass:
                st.session_state.owner_auth = True
                go("owner")
            else:
                st.markdown('<div class="msg-err">⚠ ' +
                            ("Incorrect password." if not FA else "رمز عبور نادرست است.") +
                            "</div>", unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;font-size:12px;color:var(--muted);margin-top:12px">{"Demo password:" if not FA else "رمز نمونه:"} <strong>admin123</strong></p>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██████  PAGE: OWNER DASHBOARD
# ─────────────────────────────────────────────
elif st.session_state.page == "owner":
    FA = is_fa()
    if not st.session_state.owner_auth:
        go("owner-login")

    nav1, nav2 = st.columns([5, 1])
    with nav2:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← Exit" if not FA else "← خروج", key="o_logout"):
            st.session_state.owner_auth = False
            go("gateway")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="owner-hero">
      <div class="owner-badge">👑 {"Owner Dashboard" if not FA else "داشبورد مدیر"}</div>
      <h1>{"Full Control. All Reservations." if not FA else "کنترل کامل. همه رزروها."}</h1>
      <p>{"Book on behalf of guests, manage all reservations, view analytics and settings."
          if not FA else "به جای مهمانان رزرو کنید، همه رزروها را مدیریت کنید، آمار ببینید و تنظیمات را پیکربندی کنید."}</p>
    </div>
    """, unsafe_allow_html=True)

    all_res    = st.session_state.reservations
    active_res = [r for r in all_res if r["status"] == "active"]
    revenue    = sum(r["price"] for r in active_res)
    ug         = len(set(r["email"] for r in all_res))

    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl in [
        (s1, len(all_res),    "Total Bookings"  if not FA else "کل رزروها"),
        (s2, len(active_res), "Active"           if not FA else "فعال"),
        (s3, f"{revenue:,}",  "Revenue (تومان)"  if not FA else "درآمد (تومان)"),
        (s4, ug,              "Unique Guests"    if not FA else "مهمانان یکتا"),
    ]:
        col.markdown(f'<div class="stat-card"><div class="stat-num">{val}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("")

    tab_book_o, tab_cal_o, tab_allres_o, tab_analytics_o, tab_settings_o = st.tabs([
        "📅 " + ("Book for Guest" if not FA else "رزرو برای مهمان"),
        "📆 " + ("All Calendar"   if not FA else "تقویم همه"),
        "📋 " + ("All Reservations" if not FA else "همه رزروها"),
        "📊 " + ("Analytics"       if not FA else "آمار"),
        "⚙️ " + ("Settings"        if not FA else "تنظیمات"),
    ])

    # ── Owner: Book for Guest ──
    with tab_book_o:
        left_o, right_o = st.columns([1.3, 0.85], gap="medium")
        with left_o:
            st.markdown(f"""
            <div class="eyebrow">{"Owner Booking" if not FA else "رزرو مدیر"}</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:16px">
              {"Reserve a Hall on Behalf of a Guest" if not FA else "رزرو سالن به نمایندگی از مهمان"}
            </h2>
            """, unsafe_allow_html=True)
            booking_form("owner", "owner@padmart.internal", "Owner", is_owner_booking=True)

        with right_o:
            st.markdown(f"""
            <div class="panel-dark">
              <div class="eyebrow eyebrow-light">{"Owner Booking Note" if not FA else "نکته رزرو مدیر"}</div>
              <div style="font-size:13px;color:rgba(255,255,255,.75);line-height:1.7;margin-top:8px">
                {"As owner you can reserve any hall for any guest. Enter the guest name and email (optional) — the booking will appear in the All Reservations list and on the calendar."
                 if not FA else "به عنوان مدیر می‌توانید هر سالنی را برای هر مهمانی رزرو کنید. نام و ایمیل مهمان را وارد کنید — رزرو در لیست همه رزروها و تقویم نمایش داده می‌شود."}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Owner: Calendar ──
    with tab_cal_o:
        st.markdown(f"""
        <div class="eyebrow">{"Full Reservation Calendar" if not FA else "تقویم کامل رزروها"}</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:4px">
          {"All Studios · All Days" if not FA else "همه استودیوها · همه روزها"}
        </h2>
        <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
          {"Each bar = one booking. Hover for guest name and details." if not FA
           else "هر نوار = یک رزرو. نگه دارید تا نام مهمان و جزئیات را ببینید."}
        </p>
        """, unsafe_allow_html=True)
        calendar_chart(all_res, "📅 " + ("All Reservations Calendar" if not FA else "تقویم همه رزروها"))

    # ── Owner: All Reservations list ──
    with tab_allres_o:
        search = st.text_input(
            "🔍", placeholder="Search by name or email…" if not FA else "جستجو با نام یا ایمیل…",
            label_visibility="collapsed", key="o_search"
        )
        filtered = [r for r in sorted(all_res, key=lambda x: x["date"], reverse=True)
                    if not search or
                    search.lower() in r["name"].lower() or
                    search.lower() in r["email"]]
        if not filtered:
            st.markdown(f"""
            <div style="text-align:center;padding:44px;background:var(--paper);
                        border:2px dashed #d7c5b4;border-radius:20px">
              <div style="font-size:34px;margin-bottom:10px">🎟</div>
              <div style="font-family:'Playfair Display',serif;font-size:18px">
                {"No reservations yet" if not FA else "هنوز رزروی ثبت نشده"}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            res_cards(filtered, "owner_all", show_email=True)

    # ── Owner: Analytics ──
    with tab_analytics_o:
        from collections import Counter
        WINE_C = "#6d1f2a"; GOLD_C = "#b88a4a"; CREAM_C = "#f5eadf"

        ac1, ac2, ac3 = st.columns(3)

        # Bar: by guest name
        with ac1:
            nc = Counter(r["name"] for r in active_res)
            fig = go.Figure(go.Bar(
                x=list(nc.keys()), y=list(nc.values()),
                marker=dict(color=list(nc.values()),
                            colorscale=[[0, CREAM_C],[0.5, GOLD_C],[1, WINE_C]],
                            line=dict(color=WINE_C, width=1)),
                text=list(nc.values()), textposition="outside",
                hovertemplate="<b>%{x}</b><br>Bookings: %{y}<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Bookings by Guest" if not FA else "رزرو به تفکیک مهمان",
                           font=dict(size=13, color=WINE_C), x=.5),
                plot_bgcolor=CREAM_C, paper_bgcolor=CREAM_C,
                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                yaxis=dict(gridcolor="#e7d8c6"),
                margin=dict(t=40,b=20,l=10,r=10), height=260,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Pie: hall usage
        with ac2:
            gc = sum(1 for r in active_res if r["hall"] == "grand")
            sc = sum(1 for r in active_res if r["hall"] == "studio2")
            fig = go.Figure(go.Pie(
                labels=["Grand Studio" if not FA else "گرند استودیو",
                        "Studio 2"     if not FA else "استودیو ۲"],
                values=[gc, sc],
                marker=dict(colors=[WINE_C, GOLD_C],
                            line=dict(color="#fffaf3", width=3)),
                hole=0.42, textfont=dict(size=12),
                hovertemplate="<b>%{label}</b><br>%{value}<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Hall Usage" if not FA else "سهم استفاده از سالن‌ها",
                           font=dict(size=13, color=WINE_C), x=.5),
                plot_bgcolor=CREAM_C, paper_bgcolor=CREAM_C,
                legend=dict(font=dict(size=11)),
                margin=dict(t=40,b=10,l=10,r=10), height=260,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Line: over time
        with ac3:
            dc = Counter(r["date"] for r in active_res)
            dates = sorted(dc.keys())
            fig = go.Figure(go.Scatter(
                x=dates, y=[dc[d] for d in dates],
                mode="lines+markers",
                line=dict(color=WINE_C, width=2.5),
                marker=dict(color=WINE_C, size=7,
                            line=dict(color="#fffaf3", width=2)),
                fill="tozeroy", fillcolor="rgba(109,31,42,.08)",
                hovertemplate="<b>%{x}</b><br>Bookings: %{y}<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Bookings Over Time" if not FA else "روند رزرو",
                           font=dict(size=13, color=WINE_C), x=.5),
                plot_bgcolor=CREAM_C, paper_bgcolor=CREAM_C,
                xaxis=dict(showgrid=False, tickfont=dict(size=9)),
                yaxis=dict(gridcolor="#e7d8c6"),
                margin=dict(t=40,b=20,l=10,r=10), height=260,
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Owner: Settings ──
    with tab_settings_o:
        set1, set2 = st.columns(2, gap="large")

        with set1:
            st.markdown(f'<div class="eyebrow">{"Security" if not FA else "امنیت"}</div>', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-family:\'Playfair Display\',serif;font-size:19px;margin-bottom:14px">{"Change Owner Password" if not FA else "تغییر رمز عبور مدیر"}</h3>', unsafe_allow_html=True)
            with st.form("owner_pass_form"):
                np1 = st.text_input("New Password"     if not FA else "رمز جدید",     type="password")
                np2 = st.text_input("Confirm Password" if not FA else "تأیید رمز جدید", type="password")
                if st.form_submit_button("Save Password" if not FA else "ذخیره رمز", use_container_width=True):
                    if len(np1) < 6:
                        st.error("Min 6 characters." if not FA else "حداقل ۶ کاراکتر.")
                    elif np1 != np2:
                        st.error("Passwords do not match." if not FA else "رمزها یکسان نیستند.")
                    else:
                        st.session_state.owner_pass = np1
                        st.success("Password updated!" if not FA else "رمز عبور به‌روز شد!")

        with set2:
            st.markdown(f'<div class="eyebrow">{"Email Settings" if not FA else "تنظیمات ایمیل"}</div>', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-family:\'Playfair Display\',serif;font-size:19px;margin-bottom:14px">{"SMTP Configuration" if not FA else "پیکربندی SMTP"}</h3>', unsafe_allow_html=True)
            smtp = st.session_state.smtp
            with st.form("smtp_form"):
                h  = st.text_input("SMTP Host"     if not FA else "هاست SMTP",   value=smtp["host"], placeholder="smtp.gmail.com")
                c1b, c2b = st.columns(2)
                with c1b: p = st.number_input("Port" if not FA else "پورت", value=smtp["port"], min_value=1, max_value=9999)
                with c2b: u = st.text_input("Sender Email" if not FA else "ایمیل فرستنده", value=smtp["user"])
                pw = st.text_input("App Password" if not FA else "رمز اپ", value=smtp["pass"], type="password")
                st.caption("Gmail: 2-Step Verification → App Passwords → Mail → Generate." if not FA else "Gmail: تأیید دو مرحله‌ای ← رمزهای اپ ← ایمیل ← ایجاد کنید.")
                if st.form_submit_button("Save" if not FA else "ذخیره", use_container_width=True):
                    st.session_state.smtp = {"host": h, "port": int(p), "user": u, "pass": pw}
                    st.success("Saved!" if not FA else "ذخیره شد!")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
FA = is_fa()
st.markdown(f"""
<div style="border-top:1px solid var(--line);padding:18px 0;text-align:center;margin-top:36px">
  <span style="font-family:'Playfair Display',serif;font-size:15px;color:var(--wine)">Padmart</span>
  <span style="color:#c8aa92;margin:0 8px">·</span>
  <span style="font-size:13px;color:var(--muted)">
    {"Acting School · Hall Reservations · Grand Studio & Studio 2 · 70,000 تومان/hr"
     if not FA else "مدرسه بازیگری · رزرو سالن · گرند استودیو و استودیو ۲ · ۷۰،۰۰۰ تومان/ساعت"}
  </span>
</div>
""", unsafe_allow_html=True)
