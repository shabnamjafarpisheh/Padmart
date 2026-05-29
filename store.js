// ═══════════════════════════════════════════════
//  PADMART — SHARED DATA STORE  (store.js)
//  Loaded by every page. All data lives in
//  localStorage so changes are instant across tabs.
// ═══════════════════════════════════════════════
const Store = (() => {

  /* ── persistence ── */
  function load(key, def) {
    try { return JSON.parse(localStorage.getItem('pm_' + key)) ?? def; }
    catch { return def; }
  }
  function save(key, val) {
    localStorage.setItem('pm_' + key, JSON.stringify(val));
    window.dispatchEvent(new CustomEvent('pm_update', { detail: { key } }));
  }

  /* ── language ── */
  function getLang()  { return localStorage.getItem('pm_lang') || 'en'; }
  function setLang(l) { localStorage.setItem('pm_lang', l); window.dispatchEvent(new Event('pm_lang')); }

  /* ── owner auth ── */
  function getOwnerPass()  { return localStorage.getItem('pm_owner_pass') || 'admin123'; }
  function setOwnerPass(p) { localStorage.setItem('pm_owner_pass', p); }
  function isOwnerIn()     { return sessionStorage.getItem('pm_owner_auth') === '1'; }
  function ownerLogin(p)   { if (p === getOwnerPass()) { sessionStorage.setItem('pm_owner_auth','1'); return true; } return false; }
  function ownerLogout()   { sessionStorage.removeItem('pm_owner_auth'); }

  /* ── smtp ── */
  function getSmtp() { return load('smtp', { host:'', port:587, user:'', pass:'' }); }
  function setSmtp(v){ save('smtp', v); }

  /* ── reservations ── */
  function getReservations()     { return load('reservations', []); }
  function addReservation(r)     { const a = getReservations(); a.push(r); save('reservations', a); }
  function cancelReservation(id) { save('reservations', getReservations().map(r => r.id===id ? {...r,status:'cancelled'} : r)); }
  function getByEmail(email)     { return getReservations().filter(r => r.email === email.toLowerCase()); }

  /* ── halls ── */
  const HALLS = {
    grand:   { key:'grand',   price:150000, en:'Grand Studio', fa:'گرند استودیو', seats:120, icon:'🎪' },
    studio2: { key:'studio2', price:80000,  en:'Studio 2',     fa:'استودیو ۲',   seats:30,  icon:'🎭' },
  };

  /* ── time slots ── */
  // Each slot is a 1-hour block label e.g. "09:00–10:00"
  const SLOT_STARTS = ['09','10','11','12','13','14','15','16','17','18','19','20'];
  function slotLabel(start, dur) {
    const s = parseInt(start);
    const e = s + dur;
    return `${String(s).padStart(2,'0')}:00–${String(e).padStart(2,'0')}:00`;
  }
  // Returns array of occupied start-hours for a hall+date
  function bookedHours(hall, date) {
    const hours = new Set();
    getReservations()
      .filter(r => r.hall===hall && r.date===date && r.status==='active')
      .forEach(r => {
        for (let h = r.startHour; h < r.startHour + r.duration; h++) hours.add(h);
      });
    return hours;
  }
  // Can a booking of `dur` hours fit starting at `startHour`?
  function canBook(hall, date, startHour, dur) {
    const taken = bookedHours(hall, date);
    for (let h = startHour; h < startHour + dur; h++) {
      if (taken.has(h) || h > 20) return false;
    }
    return true;
  }

  /* ── helpers ── */
  function genId() { return 'RES-' + Math.random().toString(36).substr(2,8).toUpperCase(); }
  function fmt(n)  { return n.toLocaleString() + ' تومان'; }

  return {
    getLang, setLang,
    getOwnerPass, setOwnerPass, isOwnerIn, ownerLogin, ownerLogout,
    getSmtp, setSmtp,
    getReservations, addReservation, cancelReservation, getByEmail,
    HALLS, SLOT_STARTS, slotLabel, bookedHours, canBook,
    genId, fmt,
  };
})();
