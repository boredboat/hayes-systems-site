import pathlib, re, os

# GHL-native custom page generator v2 (10/25): interactive function mock.
# v2.1 (10/26 build card t_9e1bf65d): the page now boots from REAL data
# through the identity seam (POST /api/ghl/session -> page token; GET
# /api/ghl/page-data + /api/ghl/appointments populate every state) and
# every action button calls its real endpoint. Demo mode (no locationId
# param) keeps the original local behavior untouched for review.
# v2.2 (10/26 pause card t_e91966fa): Pause posts the picked resume date
# to /api/ghl/pause, Resume calls /api/ghl/resume, and the paused state
# reads page-data's campaign.paused/paused_until (the pill shows the real
# date; stats stay live through a pause). Demo mode (?state=paused) is
# unchanged and never touches the endpoints.
# v2.3 (10/27 fix card t_12d6bb14): reunifies the two lineages that split
# at e7c8c4e. That commit (plus 7a6d24c, a3282db) regenerated the page
# from a stale scratch copy of this generator, wiping the v2.2 pause
# wiring from the deployed artifact while the checked-in generator kept
# it. v2.3 = v2.2 pause wiring + body centering (e7c8c4e) + the one-shot
# frame beacon (7a6d24c) + the request-button state rules (a3282db).
# THIS file is the only canonical copy; the scratch twin is retired.
# States: running | paused | cancelled | none  (?state= for review; in-page
# transitions flip the same DOM). All copy per house rules: zero em-dashes,
# no timeline promises, claims match the engine.
# Emits BOTH artifacts: _ghl_native_page.html (review twin) and
# ghl-app.html (deployed, adds the noindex meta) so one run reproduces
# the live page byte-for-byte.

SITE = pathlib.Path('/home/mrh/real-estate-consulting/site')
src = (SITE/'index.html').read_text()
house = re.search(r'<symbol id="mark"[^>]*>\s*<path fill="#EDE8DD"[^>]*d="([^"]+)"', src).group(1)
panes = re.search(r'<path fill="#D9A441"[^>]*d="([^\"]+)"', src).group(1)

html = '''<!doctype html><html><head><meta charset="utf-8"><title>Your campaign</title><style>
/* GHL-native styling: Inter type, HighLevel brand palette (BrandKit tokens). */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:#FFFFFF;color:#37474F;line-height:1.55;padding:28px 32px;max-width:960px;margin:0 auto}
.lockup{display:flex;align-items:center;gap:12px;margin-bottom:24px}
.mark{width:32px;height:35px;flex-shrink:0}
.divider{width:1px;height:30px;background:#E0E0E0}
.bname{font-weight:700;font-size:11px;letter-spacing:.18em;color:#07223D;text-transform:uppercase}
h1{font-weight:700;font-size:24px;color:#07223D;margin-bottom:6px;letter-spacing:-.01em}
.status-row{display:flex;align-items:center;gap:12px;margin-bottom:26px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;gap:7px;border-radius:999px;padding:5px 14px;font-size:13px;font-weight:600}
.pill.run{background:rgba(23,217,75,.1);color:#0e9e33}
.pill.pausepill{background:rgba(255,184,0,.12);color:#b26a00}
.pill.stoppill{background:rgba(239,108,0,.1);color:#c05100}
.pill.nonepill{background:#ECEFF1;color:#607D8B}
.pill .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
.muted{font-size:13.5px;color:#90A4AE}
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:28px}
.stat{background:#F8FAFB;border:1px solid #ECEFF1;border-radius:12px;padding:16px 12px;text-align:center}
.stat .num{font-weight:700;font-size:28px;color:#07223D;line-height:1.1;margin-bottom:4px;letter-spacing:-.02em}
.stat .lbl{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#78909C}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:8px;padding:11px 22px;font-size:14.5px;font-weight:600;text-decoration:none;cursor:pointer;border:none;font-family:'Inter',sans-serif;transition:background .15s}
.btn-primary{background:#2896FB;color:#fff}
.btn-primary:hover{background:#095DC3}
.btn-primary:disabled{background:#CBD9E8;color:#7A8CA3;cursor:not-allowed}
.cooldown{margin-top:12px;font-size:12.5px;color:#90A4AE}
.retainer{color:#2896FB;font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.btn-ghost{background:#fff;border:1.5px solid #E0E0E0;color:#37474F}
.btn-ghost:hover:not(:disabled){border-color:#B0BEC5}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-danger{background:#fff;border:1.5px solid #FFCDD2;color:#C62828}
.contact{font-size:13.5px;font-weight:600;color:#2896FB;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.overlay{display:none;position:fixed;inset:0;background:rgba(7,34,61,.45);align-items:center;justify-content:center;z-index:10}
.overlay.show{display:flex}
.dialog{background:#fff;border-radius:12px;padding:28px;max-width:440px;width:calc(100vw - 40px);box-shadow:0 20px 60px rgba(7,34,61,.3)}
.dialog h3{font-weight:700;font-size:18px;color:#07223D;margin-bottom:10px}
.dialog p{font-size:14px;color:#546E7A;margin-bottom:22px}
.dialog-actions{display:flex;gap:12px;justify-content:flex-end}
.field{margin-bottom:16px}
.field label{display:block;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#78909C;margin-bottom:6px}
.field input[type=date]{width:100%;padding:10px 12px;border:1.5px solid #E0E0E0;border-radius:8px;font-family:'Inter',sans-serif;font-size:14.5px;color:#07223D;background:#fff}
.field input[type=date]:focus{outline:none;border-color:#2896FB}
.btn-danger-solid{background:#E53935;color:#fff}
.btn-danger-solid:hover{background:#C62828}
.sec{margin-top:26px}
.sec h2{font-weight:700;font-size:16px;color:#07223D;margin-bottom:12px}
table{width:100%;min-width:520px;border-collapse:collapse;font-size:14px;table-layout:fixed}
th{text-align:left;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#90A4AE;padding:8px 10px;border-bottom:1px solid #ECEFF1}
td{padding:11px 10px;border-bottom:1px solid #F5F5F5;color:#546E7A}
td .who{font-weight:600;color:#07223D}
td .when{color:#90A4AE;font-size:13px}
.badge{display:inline-block;border-radius:999px;padding:3px 12px;font-size:12px;font-weight:600;white-space:nowrap}
.badge.held{background:rgba(23,217,75,.1);color:#0e9e33}
.badge.booked{background:#E7F3FE;color:#095DC3}
.badge.reported{background:rgba(255,184,0,.12);color:#b26a00}
.appt-wrap{border:1px solid #ECEFF1;border-radius:10px}
.appt-scroll{max-height:260px;overflow:auto;-webkit-overflow-scrolling:touch}
.appt-scroll::-webkit-scrollbar{width:8px}
.appt-scroll::-webkit-scrollbar-track{background:#ECEFF1;border-radius:10px}
.appt-scroll::-webkit-scrollbar-thumb{background:#B0BEC5;border-radius:10px}
.appt-scroll::-webkit-scrollbar-thumb:hover{background:#90A4AE}
.appt-scroll table{margin:0}
.appt-scroll th{position:sticky;top:0;background:#fff;z-index:1}
.rns{white-space:nowrap;font-family:'Inter',sans-serif;font-size:12.5px;font-weight:600;color:#546E7A;background:#fff;border:1.5px solid #E0E0E0;border-radius:6px;padding:5px 12px;cursor:pointer}
.rns:hover{border-color:#B0BEC5;color:#37474F}
.empty{padding:28px 16px;text-align:center;color:#90A4AE;font-size:14px}
.past-total{margin-top:10px;font-size:12.5px;color:#90A4AE}
.ret-card{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:5px 14px;font-size:13px;font-weight:600;width:fit-content}
.ret-card.on{background:rgba(23,217,75,.1);color:#0e9e33}
.ret-card.off{background:rgba(198,40,40,.08);color:#C62828}
.ret-card .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
.ret-ad{max-width:520px;text-align:left}
.ret-ad h3{font-size:22px;margin-bottom:4px}
.ret-ad .ad-kicker{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#2896FB;margin-bottom:8px}
.ret-ad ul{list-style:none;margin:18px 0;display:grid;gap:11px}
.ret-ad li{display:flex;align-items:flex-start;gap:11px;font-size:14.5px;line-height:1.5;color:#37474F}
.ret-ad li svg{flex-shrink:0;margin-top:2px}
.ret-ad .ad-price{background:#E7F3FE;border-radius:10px;padding:13px 16px;font-size:15px;font-weight:600;color:#07223D;margin-bottom:16px;text-align:center}
.ret-ad .ad-check{display:flex;align-items:flex-start;gap:10px;font-size:13.5px;color:#37474F;margin-bottom:18px}
.ret-ad .ad-check input{width:17px;height:17px;margin-top:1px;accent-color:#2896FB}
.ret-ad .ad-check a{color:#2896FB;font-weight:600;text-decoration:underline;text-underline-offset:2px}
.ob-card{background:#fff;border:1px solid #ECEFF1;border-radius:14px;padding:34px 36px;max-width:640px;margin:0 auto;box-shadow:0 10px 30px rgba(7,34,61,.06)}
.ob-card h2{font-weight:700;font-size:21px;color:#07223D;margin-bottom:6px}
.ob-card .ob-sub{font-size:13.5px;color:#78909C;margin-bottom:24px}
.ob-step{margin-bottom:26px}
.ob-step h3{font-weight:600;font-size:14px;color:#07223D;margin-bottom:8px}
.ob-step p{font-size:14px;line-height:1.65;color:#546E7A}
.ob-step p b{color:#07223D;font-weight:600}
.ob-fields{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ob-field label{display:block;font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:#78909C;margin-bottom:6px}
.ob-field input{width:100%;padding:11px 13px;border:1.5px solid #E0E0E0;border-radius:8px;font-family:'Inter',sans-serif;font-size:14.5px;color:#07223D;background:#fff}
.ob-field input:focus{outline:none;border-color:#2896FB}
.ob-terms{background:#F8FAFB;border:1px solid #ECEFF1;border-radius:10px;padding:16px 18px;font-size:13px;line-height:1.6;color:#546E7A;max-height:170px;overflow-y:auto;margin-bottom:14px}
.ob-terms a{color:#2896FB;font-weight:600;text-decoration:underline;text-underline-offset:2px}
.ob-check{display:flex;align-items:flex-start;gap:10px;font-size:13.5px;color:#37474F;margin-bottom:16px}
.ob-check input{width:17px;height:17px;margin-top:1px;accent-color:#2896FB}
.ob-sign{display:grid;grid-template-columns:1fr 140px;gap:14px;margin-bottom:22px}
.ob-done{text-align:center;padding:30px 10px}
.ob-done .big{font-size:34px;margin-bottom:10px}
.ob-card-step{border:1.5px solid #E0E0E0;border-radius:10px;padding:16px;display:flex;align-items:center;gap:14px;margin-bottom:14px}
.ob-card-step .cs-icon{width:36px;height:36px;border-radius:8px;background:#E7F3FE;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ob-card-step .cs-txt{flex:1;font-size:13.5px;line-height:1.5;color:#546E7A}
.ob-card-step .cs-txt b{display:block;color:#07223D;font-size:14px;font-weight:600}
.ob-card-step .cs-state{font-size:12px;font-weight:600;white-space:nowrap}
.ob-card-step.done{border-color:#17D94B;background:rgba(23,217,75,.05)}
.ob-card-step.done .cs-state{color:#0e9e33}
.danger-row{margin-top:22px;text-align:right;display:flex;justify-content:flex-end;align-items:center;gap:20px}
.foot{margin-top:24px;font-size:12.5px;color:#B0BEC5;border-top:1px solid #F5F5F5;padding-top:14px}
#toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%) translateY(16px);background:#07223D;color:#fff;font-size:13.5px;font-weight:500;border-radius:10px;padding:12px 20px;box-shadow:0 12px 32px rgba(7,34,61,.35);opacity:0;pointer-events:none;transition:all .25s;max-width:86%;text-align:center}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.hide{display:none !important}
.spin{width:22px;height:22px;border:3px solid #E7F3FE;border-top-color:#2896FB;border-radius:50%;animation:sp 1s linear infinite;margin:0 auto 14px}
@keyframes sp{to{transform:rotate(360deg)}}
.ob-progress{display:flex;gap:6px;margin:0 0 18px 0}
.ob-progress span{flex:1;height:4px;border-radius:2px;background:#E3EBF3}
.ob-progress span.on{background:#2896FB}
.ob-walk{display:flex;gap:10px;justify-content:space-between;align-items:center;margin-top:18px}
.ob-walk .spacer{flex:1}
.ob-setup{margin:14px 0 0 0;padding:0;list-style:none;color:#5B7085}
.ob-setup li{margin:7px 0;padding-left:26px;position:relative}
.ob-setup li:before{content:'';position:absolute;left:0;top:3px;width:16px;height:16px;border-radius:50%;background:#E3EBF3}
.ob-setup li b{color:#07223D}

@media(max-width:999px){.stats{grid-template-columns:repeat(3,1fr)}}
@media(max-width:640px){
.stats{grid-template-columns:repeat(2,1fr)}
body{padding:20px 14px}
h1{font-size:20px}
.stat .num{font-size:26px}
.btn{padding:10px 16px;font-size:13.5px}
.danger-row{flex-wrap:wrap;justify-content:flex-start;gap:14px}
.danger-row .contact{font-size:12.5px}
}
</style></head><body>

<div class="lockup">
  <svg class="mark" viewBox="86 216 226 247"><path fill="#07223D" fill-rule="evenodd" d="@@HOUSE@@"/><path fill="#2896FB" fill-rule="evenodd" d="@@PANES@@"/></svg>
  <div class="divider"></div>
  <span class="bname">Hayes Systems &middot; Lead Reactivation</span>
</div>

<h1>Your campaign</h1>
<div id="obGate" class="hide">
  <div class="ob-card" id="obWelcome">
    <h2>Welcome to Hayes Systems</h2>
    <p>We reactivate the aged leads already sitting in your CRM with
    personalized email outreach and an AI booking agent that puts
    appointments straight on your calendar. You pay only for appointments
    that land.</p>
    <p style="margin-bottom:6px"><b>Setup takes about two minutes:</b></p>
    <ul class="ob-setup">
      <li><b>Connect</b> your location (one click, read-only)</li>
      <li><b>Review</b> how the service works</li>
      <li><b>Confirm</b> your business details</li>
      <li><b>Agree</b> to the terms and add a payment card</li>
    </ul>
    <p style="margin-top:12px;color:#90A4AE;font-size:12.5px">Nothing is
    charged until appointments land on your calendar.</p>
    <button class="btn btn-primary" id="obStart" style="margin-top:6px">Get started</button>
  </div>
  <div class="ob-card hide" id="obForm">
    <div class="ob-progress" id="obProgress"></div>

    <div class="ob-step" id="obConnectStep" style="display:none">
      <h3>Connect your location</h3>
      <p>One click connects us to this location in read-only mode, so we
      can count your workable leads and plan your campaign. We never
      write to your account.</p>
      <button class="btn btn-primary" id="obConnectBtn">Connect your location</button>
      <span class="cs-state" id="obConnectState" style="margin-left:10px"></span>
    </div>

    <div class="ob-step" data-ob="2">
      <h3>What we do</h3>
      <p>We run hands-free lead reactivation campaigns on all leads older
      than 90-days, utilizing personalized and professional email outreach
      combined with a Retell AI powered booking agent who assists leads in
      choosing a free slot on your calendar. Campaigns typically run 1-2
      months depending on list size and our outreach messages are timed to
      land during favorable days and hours to boost engagement. Leads
      receive 6 emails over the course of a month maximum.</p>
      <h3 style="margin-top:22px">What you pay</h3>
      <p>$60 per booked appointment. No other fees are charged.</p>

      <h3 style="margin-top:22px">Your data</h3>
      <p>Sensitive data is removed from our system at closeout. For full
      details please review our data agreement.</p>
    </div>

    <div class="ob-step" data-ob="3">
      <h3>Agency details</h3>
      <p>Please provide your business name and phone number you would like
      leads to see in our outreach.</p>
      <div class="ob-fields">
        <div class="ob-field"><label for="obBusiness">Business name</label>
          <input id="obBusiness" value="Summit Realty Group"></div>
        <div class="ob-field"><label for="obPhone">Phone number prospects should call</label>
          <input id="obPhone" value="+1 (413) 555-0142"></div>
      </div>
    </div>

    <div class="ob-step" data-ob="4">
      <h3>Data Agreement and Campaign Terms</h3>
      <div class="ob-terms">
        <b>Data Agreement and Campaign Terms.</b> You authorize Hayes
        Systems to contact the leads you provide on your behalf by email
        and by consented AI-assisted phone call. We read your contacts in
        read-only mode, we never write to your account, and every access
        token is deleted at the end of the engagement. Working copies of
        your list are deleted once your campaign is planned. You may stop
        all outreach at any time.
        <span id="obTermsFull" class="hide"> The full agreement text
        appears here at launch, loaded from the same source the website
        signs against, so what you sign is exactly what every client
        signs. <a href="https://www.hayessystems.com/privacy.html" target="_blank">Privacy
        policy</a> &middot; <a href="https://www.hayessystems.com/terms.html" target="_blank">Full
        terms</a></span>
      </div>
      <label class="ob-check"><input type="checkbox" id="obAgree">
        <span>I have read and agree to the Data Agreement and the Campaign
        Terms.</span></label>
      <div class="ob-sign">
        <div class="ob-field"><label for="obSign">Type your name to sign</label>
          <input id="obSign" placeholder="Your name"></div>
        <div class="ob-field"><label for="obDate">Date</label>
          <input id="obDate" value="Oct 26, 2026" readonly></div>
      </div>
      <div class="ob-card-step" id="obCardStep" style="display:none">
        <div class="cs-icon"><svg width="20" height="20" viewBox="0 0 20 20"><rect x="1" y="4" width="18" height="12" rx="2.5" fill="none" stroke="#07223D" stroke-width="1.6"/><path d="M1 8h18" stroke="#07223D" stroke-width="1.6"/><rect x="13" y="10.5" width="4" height="2.4" rx="1" fill="#07223D"/></svg></div>
        <div class="cs-txt"><b>Payment card</b>Charged only when appointments land on your calendar.</div>
        <span class="cs-state" id="obCardState"></span>
      </div>
      <button class="btn btn-primary" id="obSubmit" style="width:100%" disabled>Agree and finish setup</button>
    </div>
  </div>

  <div class="ob-card ob-done hide" id="obDone">
    <div class="big">&#10003;</div>
    <h2 style="margin-bottom:8px">You are all set</h2>
    <p style="font-size:14.5px;color:#546E7A;margin-bottom:6px">Here is
    what happens next:</p>
    <ul class="ob-setup" style="margin-top:0">
      <li>We read your CRM in read-only mode and count your workable
      leads</li>
      <li>Your qualification result appears right on this page</li>
      <li>When your list qualifies, request a campaign and it launches
      automatically</li>
      <li>Appointments land straight on your calendar</li>
    </ul>
    <button class="btn btn-primary" id="obGo" style="margin-top:18px">Go to your campaign</button>
  </div>
</div>

<div class="status-row" id="statusRow">
  <span class="pill run" id="pill"><span class="dot"></span><span id="pillTxt">Running</span></span>
  <div class="ret-card off" id="retCard"><span class="dot"></span><span id="retCardTxt">Retainer off</span></div>
  <span class="muted" id="pillSub">Week 3 of 4 &middot; Ends Oct 30 &middot; Updated Oct 18</span>
</div>
<div class="stats" id="stats">
  <div class="stat"><div class="num">1,847</div><div class="lbl">Workable leads</div></div>
  <div class="stat"><div class="num">65%</div><div class="lbl">List worked</div></div>
  <div class="stat"><div class="num">1,204</div><div class="lbl">Emails sent</div></div>
  <div class="stat"><div class="num">23</div><div class="lbl">Appointments</div></div>
  <div class="stat"><div class="num">1.9%</div><div class="lbl">Conversion</div></div>
  <div class="stat"><div class="num">$1,380</div><div class="lbl">Cost to date</div></div>
</div>

<div class="actions">
  <div class="card" id="connectBanner" style="display:none;border-left:4px solid var(--hl,#1a73e8);margin-bottom:14px">
    <h3 style="margin:0 0 6px 0">Finish setting up your account</h3>
    <p style="margin:0 0 12px 0">One more step: connect your location so we can read your CRM and count your workable leads. Takes one click.</p>
    <button class="btn btn-primary" id="connectLocBtn">Connect your location</button>
  </div>
  <button class="btn btn-primary" id="reqBtn" disabled>Request a new campaign</button>
  <button class="btn btn-ghost" id="resendBtn">Resend latest report</button>
  <button class="btn btn-ghost" id="pauseBtn">Pause campaign</button>
</div>
<div class="cooldown" id="cooldown">Campaigns need at least 3 months between runs. Your next campaign opens January 28, 2027.</div>
<div class="cooldown" id="retainerLine" style="margin-top:6px">Teams with large lists may want to <span class="retainer" id="retainerLink">check out our retainer service</span> for continual, automatic coverage.</div>

<div class="sec" id="apptSec">
  <h2>Appointments</h2>
  <div class="appt-wrap">
  <div class="appt-scroll">
  <table>
    <thead><tr><th>Lead</th><th>When</th><th style="width:140px">Status</th><th style="width:150px"></th></tr></thead>
    <tbody id="apptBody"></tbody>
  </table>
  </div>
  </div>
</div>

<div class="sec" id="pastSec">
  <h2>Past campaigns</h2>
  <div class="appt-wrap">
  <div class="appt-scroll">
  <table>
    <thead><tr><th>Campaign</th><th style="width:130px">Leads worked</th><th style="width:130px">Appointments</th><th style="width:110px">Cost</th></tr></thead>
    <tbody id="pastBody"></tbody>
  </table>
  </div>
  </div>
</div>

<div class="danger-row">
  <span class="contact" id="helpLink">Help / FAQ</span>
  <span class="contact" id="contactLink">Contact us</span>
  <button class="btn btn-danger" id="cancelBtn">Cancel campaign</button>
  <button class="btn btn-danger hide" id="cancelRetBtn">Cancel retainer</button>
</div>

<div class="foot">Hayes Systems &middot; hayessystems.com</div>

<div class="overlay" id="confirmOverlay">
  <div class="dialog">
    <h3>Cancel this campaign?</h3>
    <p>Remaining leads will not be contacted and the campaign will end on the current invoice week. Appointments already on your calendar are unaffected.</p>
    <div class="dialog-actions">
      <button class="btn btn-primary" data-close="confirmOverlay">Keep campaign running</button>
      <button class="btn btn-danger" id="confirmCancel">Yes, cancel campaign</button>
    </div>
  </div>
</div>

<div class="overlay" id="pauseOverlay">
  <div class="dialog">
    <h3>Pause this campaign</h3>
    <p><strong>Pausing stops new outreach only.</strong> Leads who reply during the pause are still answered and can still book appointments. Everything resumes automatically on the date you pick.</p>
    <div class="field">
      <label for="pauseStart">Pause starts</label>
      <input type="date" id="pauseStart" value="2026-10-24">
    </div>
    <div class="field">
      <label for="pauseEnd">Resume on</label>
      <input type="date" id="pauseEnd" value="2026-10-31">
    </div>
    <div class="dialog-actions">
      <button class="btn btn-ghost" data-close="pauseOverlay">Don&rsquo;t pause</button>
      <button class="btn btn-primary" id="confirmPause">Pause campaign</button>
    </div>
  </div>
</div>

<div class="overlay" id="resumeOverlay">
  <div class="dialog">
    <h3>Resume this campaign</h3>
    <p>Replies and bookings were never stopped. Outreach starts again.</p>
    <div class="dialog-actions">
      <button class="btn btn-ghost" data-close="resumeOverlay">Keep it paused</button>
      <button class="btn btn-primary" id="confirmResume">Resume now</button>
    </div>
  </div>
</div>

<div class="overlay" id="noshowOverlay">
  <div class="dialog">
    <h3>Report a no-show</h3>
    <p id="noshowBody">This refunds the appointment. Report it only if the lead did not show.</p>
    <div class="dialog-actions">
      <button class="btn btn-ghost" data-close="noshowOverlay">Not a no-show</button>
      <button class="btn btn-primary" id="confirmNoshow">Report no-show</button>
    </div>
  </div>
</div>

<div class="overlay" id="resendOverlay">
  <div class="dialog">
    <h3>Resend the latest report</h3>
    <p>The most recent report will be emailed to you again.</p>
    <div class="dialog-actions">
      <button class="btn btn-ghost" data-close="resendOverlay">Not now</button>
      <button class="btn btn-primary" id="confirmResend">Resend report</button>
    </div>
  </div>
</div>

<div class="overlay" id="cancelRetOverlay">
  <div class="dialog">
    <h3>Cancel your retainer?</h3>
    <p>Cancelling retainer service will end any active campaign outreach
    and revert your account to regular terms. You are responsible for any
    appointment fees that result from already completed outreach. Monthly
    fees are non-refundable and there are no cancellation fees.</p>
    <div class="dialog-actions">
      <button class="btn btn-primary" data-close="cancelRetOverlay">Keep retainer</button>
      <button class="btn btn-danger" id="confirmCancelRet">Yes, cancel retainer</button>
    </div>
  </div>
</div>

<div class="overlay" id="retainerOverlay">
  <div class="dialog ret-ad">
    <div class="ad-kicker">Retainer service</div>
    <h3>Work your cold leads, automatically</h3>
    <p style="font-size:14px;line-height:1.6;color:#546E7A;margin:12px 0 0">
      Retainer service is designed for operations that regularly produce a
      large volume of leads and would benefit from the continual working
      of leads that go inactive and age into our 90-day threshold. Please
      note that leads are only contacted once every 180 days and retainers
      do not bypass this limit.</p>
    <ul>
      <li><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#17D94B" opacity=".15"/><path d="M4.5 8.2l2.3 2.3 4.7-4.9" stroke="#17D94B" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Pay only $40 per appointment</li>
      <li><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#17D94B" opacity=".15"/><path d="M4.5 8.2l2.3 2.3 4.7-4.9" stroke="#17D94B" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        No waiting period between campaigns</li>
      <li><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#17D94B" opacity=".15"/><path d="M4.5 8.2l2.3 2.3 4.7-4.9" stroke="#17D94B" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Campaigns run continually</li>
      <li><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#17D94B" opacity=".15"/><path d="M4.5 8.2l2.3 2.3 4.7-4.9" stroke="#17D94B" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        No new setup</li>
    </ul>
    <div class="ad-price">$250 per month + $40 per appointment</div>
    <label class="ad-check"><input type="checkbox" id="retainerAgree">
      <span>By checking this box you agree to the <a href="https://www.hayessystems.com/retainer-terms.html" target="_blank">retainer terms</a> and understand that service and billing begins immediately after clicking "Start retainer service".</span></label>
    <div class="ob-field" style="margin:-6px 0 18px"><label for="retSign">Type your name to sign</label>
      <input id="retSign" placeholder="Your name" autocomplete="name"></div>
    <div class="dialog-actions">
      <button class="btn btn-ghost" data-close="retainerOverlay">Not now</button>
      <button class="btn btn-primary" id="retainerStart" disabled>Start retainer service</button>
    </div>
  </div>
</div>

<div class="overlay" id="installOverlay">
  <div class="dialog" style="text-align:center">
    <div id="installBody"></div>
  </div>
</div>

<div id="toast"></div>

<script>
// State machine. States: running | paused | cancelled | none.
// ?state= sets the initial state for review; every in-page action runs
// through the same apply() so what you click is what ships.
var S = 'running';
function $(id){return document.getElementById(id);}
function pill(cls, txt, sub){
  var p = $('pill'); p.className = 'pill ' + cls; $('pillTxt').textContent = txt; $('pillSub').textContent = sub;
}
function apply(s, until){
  S = s;
  var has = (s === 'running' || s === 'paused' || s === 'cancelled' || s === 'retainer');
  $('stats').classList.toggle('hide', !has);
  $('apptSec').classList.toggle('hide', s === 'none');
  $('pastSec').classList.toggle('hide', s === 'none');
  $('resendBtn').classList.toggle('hide', false);
  $('resendBtn').disabled = (s === 'none');
  $('pauseBtn').classList.toggle('hide', s === 'none' || s === 'cancelled');
  $('cancelBtn').classList.toggle('hide', s === 'none' || s === 'cancelled' || s === 'retainer');
  $('cancelRetBtn').classList.toggle('hide', s !== 'retainer');
  $('statusRow').classList.toggle('hide', s === 'none');
  $('cooldown').classList.toggle('hide', s === 'none' || s === 'retainer');
  $('retainerLine').classList.toggle('hide', s === 'none' || s === 'retainer');
  var req = $('reqBtn');
  req.textContent = 'Request a new campaign';
  req.disabled = (s !== 'none');
  $('reqBtn').classList.toggle('hide', s === 'retainer');
  var on = (s === 'retainer');
  $('retCard').className = 'ret-card ' + (on ? 'on' : 'off');
  $('retCardTxt').textContent = on ? 'Retainer on' : 'Retainer off';
  $('retCard').classList.toggle('hide', s === 'onboarding');
  if (s === 'running') { pill('run', 'Running', 'Week 3 of 4 \\u00b7 Ends Oct 30 \\u00b7 Updated Oct 18'); $('pauseBtn').textContent = 'Pause campaign'; }
  if (s === 'paused') { pill('pausepill', 'Paused', until ? 'Paused until ' + fmtDay(until) + ' \\u00b7 replies still answered \\u00b7 appointments still book' : 'Paused until Oct 31 \\u00b7 replies still answered \\u00b7 appointments still book'); $('pauseBtn').textContent = 'Resume campaign'; }
  if (s === 'cancelled') { pill('stoppill', 'Cancelled', 'Ended Oct 24 \\u00b7 appointments on your calendar are unaffected'); }
  if (s === 'none') { pill('nonepill', 'No campaign yet', 'Your account is connected \\u00b7 ready when you are'); }
  if (s === 'retainer') { pill('run', 'Active', ''); }
}
function open_(id){ $(id).classList.add('show'); }
function close_(id){ $(id).classList.remove('show'); }
document.querySelectorAll('[data-close]').forEach(function(b){
  b.addEventListener('click', function(){ close_(b.getAttribute('data-close')); });
});
var toastTimer;
function toast(msg){
  var t = $('toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(function(){ t.classList.remove('show'); }, 3400);
}

// ── REAL-DATA LAYER (10/26 build): API base + helpers ─────────────────
// Demo mode (no locationId) never touches the network: every handler
// below branches on PAGE.live.
var API = 'https://ops.hayessystems.com';
function auth(){ return {'Content-Type': 'application/json', 'X-Hayes-Token': PAGE.token}; }
function api(path, body){
  return fetch(API + path, {method: body ? 'POST' : 'GET', headers: auth(),
                            body: body ? JSON.stringify(body) : undefined})
    .then(function(r){
      return r.json().then(function(j){ j._status = r.status; return j; })
        .catch(function(){ return {ok: false, _status: r.status, error: 'no response'}; });
    });
}
function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function fmtNum(n){ return Number(n || 0).toLocaleString('en-US'); }
function fmtMoney(n){ return '$' + fmtNum(n); }
function fmtDay(iso){ var s = String(iso || '');
  // date-only stamps parse as UTC midnight and would display a day early
  // behind UTC; force local midnight for the YYYY-MM-DD shape
  var d = new Date(/^\\d{4}-\\d{2}-\\d{2}$/.test(s) ? s + 'T00:00:00' : s);
  return isNaN(d) ? '' : d.toLocaleDateString('en-US', {month: 'short', day: 'numeric'}); }
function fmtLongDate(iso){ var s = String(iso || '');
  var d = new Date(/^\\d{4}-\\d{2}-\\d{2}$/.test(s) ? s + 'T00:00:00' : s);
  return isNaN(d) ? '' : d.toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'}); }
function fmtWhen(iso){ var d = new Date(iso); if (isNaN(d)) return iso;
  return d.toLocaleDateString('en-US', {weekday: 'short', month: 'short', day: 'numeric'})
    + ' \\u00b7 ' + d.toLocaleTimeString('en-US', {hour: 'numeric', minute: '2-digit'}); }
function setStats(w, lp, e, a, cv, cost){
  var nums = document.querySelectorAll('#stats .num');
  if (nums.length < 6) return;
  nums[0].textContent = fmtNum(w); nums[1].textContent = (lp || 0) + '%';
  nums[2].textContent = fmtNum(e); nums[3].textContent = fmtNum(a);
  nums[4].textContent = (cv || 0) + '%'; nums[5].textContent = fmtMoney(cost);
}

// ── Appointments + past campaigns tables (demo rows first, real rows
// replace them once page-data lands) ───────────────────────────────────
var DEMO_APPTS = [
  {name: 'R. Delgado',   when: 'Fri Oct 24 \\u00b7 9:45 AM', status: 'booked',   reportable: false, ref: 'demo1'},
  {name: 'M. Okafor',    when: 'Mon Oct 27 \\u00b7 11:15 AM', status: 'booked',  reportable: false, ref: 'demo2'},
  {name: 'T. Whitfield', when: 'Wed Oct 29 \\u00b7 3:00 PM', status: 'booked',   reportable: false, ref: 'demo3'},
  {name: 'S. Chen',      when: 'Wed Oct 15 \\u00b7 2:30 PM', status: 'held',     reportable: true,  ref: 'demo4'},
  {name: 'D. Martinez',  when: 'Tue Oct 14 \\u00b7 10:00 AM', status: 'held',    reportable: true,  ref: 'demo5'},
  {name: 'J. Alvarez',   when: 'Fri Oct 10 \\u00b7 1:30 PM', status: 'reported', reportable: false, ref: 'demo6'},
  {name: 'K. Brennan',   when: 'Thu Oct 9 \\u00b7 4:15 PM', status: 'held',      reportable: false, ref: 'demo7'},
  {name: 'P. Novak',     when: 'Tue Oct 7 \\u00b7 9:00 AM', status: 'held',      reportable: false, ref: 'demo8'},
  {name: 'L. Fontaine',  when: 'Mon Oct 6 \\u00b7 11:45 AM', status: 'held',     reportable: false, ref: 'demo9'},
  {name: 'A. Osei',      when: 'Fri Oct 3 \\u00b7 2:00 PM', status: 'held',      reportable: false, ref: 'demo10'}
];
var DEMO_PAST = [
  {period: 'Feb 17 - Mar 12, 2026', leads_worked: 1612, appointments: 11, cost: 660},
  {period: 'Jun 17 - Jul 11, 2026', leads_worked: 1890, appointments: 16, cost: 960}
];
var noshowRow = null;
function bindNoshow(){
  document.querySelectorAll('tr[data-ref] .rns').forEach(function(b){
    var tr = b.closest('tr');
    b.addEventListener('click', function(){
      noshowRow = tr;
      var who = tr.querySelector('.who').textContent;
      var when = tr.querySelector('.when').textContent;
      $('noshowBody').textContent = who + ', ' + when + '. This refunds the appointment. Report it only if the lead did not show.';
      open_('noshowOverlay');
    });
  });
}
function renderAppts(rows){
  var tb = $('apptBody'); if (!tb) return;
  if (!rows.length) {
    tb.innerHTML = '<tr><td colspan="4" class="empty">No appointments yet. Booked calls land here.</td></tr>';
    return;
  }
  tb.innerHTML = rows.map(function(a){
    var badge = a.status === 'booked' ? '<span class="badge booked">Booked</span>'
      : a.status === 'reported' ? '<span class="badge reported">No-show reported</span>'
      : '<span class="badge held">Held</span>';
    var btn = a.reportable ? '<button class="rns">Report no-show</button>' : '';
    return '<tr data-ref="' + esc(a.ref) + '"><td><span class="who">' + esc(a.name)
      + '</span></td><td class="when">' + esc(a.when) + '</td><td>' + badge
      + '</td><td>' + btn + '</td></tr>';
  }).join('');
  bindNoshow();
}
function renderPast(rows){
  var tb = $('pastBody'); if (!tb) return;
  if (!rows.length) {
    tb.innerHTML = '<tr><td colspan="4" class="empty">Your campaign history appears here.</td></tr>';
    return;
  }
  tb.innerHTML = rows.map(function(p){
    return '<tr><td class="when">' + esc(p.period) + '</td><td>' + fmtNum(p.leads_worked)
      + '</td><td>' + fmtNum(p.appointments) + '</td><td>' + fmtMoney(p.cost) + '</td></tr>';
  }).join('');
}
renderAppts(DEMO_APPTS);
renderPast(DEMO_PAST);

// Pause / resume
function isoDay(d){ var x = new Date(d); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 10); }
$('pauseBtn').addEventListener('click', function(){
  if (S === 'paused') { open_('resumeOverlay'); }
  else {
    var today = isoDay(new Date());
    $('pauseStart').value = today;
    $('pauseEnd').value = isoDay(new Date(Date.now() + 7 * 86400000));
    $('pauseEnd').min = today;
    open_('pauseOverlay');
  }
});
$('confirmPause').addEventListener('click', function(){
  var end = $('pauseEnd').value;
  if (!end) { toast('Pick the date outreach resumes.'); return; }
  close_('pauseOverlay');
  if (PAGE.live) {
    api('/api/ghl/pause', {resume_on: end}).then(function(j){
      if (j.ok) {
        apply('paused', j.paused_until || end);
        toast('Paused until ' + fmtLongDate(j.paused_until || end) + '. Replies are still answered and appointments still book.');
      } else {
        toast(j.message || j.error || 'The pause did not go through. Try again in a moment.');
      }
    }).catch(function(){ toast('The pause did not go through. Try again in a moment.'); });
    return;
  }
  apply('paused', end);
  toast('Paused. Replies are still answered and appointments still book.');
});
$('confirmResume').addEventListener('click', function(){
  close_('resumeOverlay');
  if (PAGE.live) {
    api('/api/ghl/resume', {}).then(function(j){
      if (j.ok) {
        apply('running');
        toast('Campaign resumed. Outreach starts again.');
      } else {
        toast(j.error || 'The resume did not go through. Try again in a moment.');
      }
    }).catch(function(){ toast('The resume did not go through. Try again in a moment.'); });
    return;
  }
  apply('running');
  toast('Campaign resumed. Outreach starts again.');
});

// Cancel
$('cancelBtn').addEventListener('click', function(){ open_('confirmOverlay'); });
$('confirmCancel').addEventListener('click', function(){
  close_('confirmOverlay');
  if (PAGE.live) {
    api('/api/ghl/cancel-campaign', {}).then(function(j){
      if (j.ok) {
        apply('cancelled');
        toast('Campaign cancelled. Appointments already on your calendar are unaffected.');
      } else {
        toast(j.error || 'The cancel did not go through. Try again or write Matt@hayessystems.com.');
      }
    }).catch(function(){ toast('The cancel did not go through. Try again in a moment.'); });
    return;
  }
  apply('cancelled');
  toast('Campaign cancelled. Appointments already on your calendar are unaffected.');
});

// No-show report: confirm, then the row flips and the button never returns
// for that appointment (the 14-day window is decided server-side now;
// rows outside it simply render without a button).
$('confirmNoshow').addEventListener('click', function(){
  close_('noshowOverlay');
  function flip(){
    if (noshowRow) {
      noshowRow.querySelector('.badge').className = 'badge reported';
      noshowRow.querySelector('.badge').textContent = 'No-show reported';
      var cell = noshowRow.cells[3]; cell.textContent = '';
    }
    toast('That appointment is refunded. You never pay for an appointment that didn\\u2019t happen.');
  }
  if (PAGE.live && noshowRow) {
    api('/api/ghl/report-no-show',
        {appointment_ref: noshowRow.getAttribute('data-ref') || ''}).then(function(j){
      if (j.ok) { flip(); }
      else { toast(j.error || 'The report did not go through. Try again in a moment.'); }
    }).catch(function(){ toast('The report did not go through. Try again in a moment.'); });
    return;
  }
  flip();
});

// Resend report (confirm first - one misclick should not re-send mail)
$('resendBtn').addEventListener('click', function(){ open_('resendOverlay'); });
$('confirmResend').addEventListener('click', function(){
  close_('resendOverlay');
  if (PAGE.live) {
    api('/api/ghl/resend-report', {}).then(function(j){
      if (j.ok) { toast('The latest report is on its way to your email.'); }
      else { toast(j.message || j.error || 'No report is available to resend yet.'); }
    }).catch(function(){ toast('The resend did not go through. Try again in a moment.'); });
    return;
  }
  toast('The latest report is on its way to your email.');
});

// Request campaign (enabled only with no active campaign)
$('connectLocBtn').addEventListener('click', function(){
  this.disabled = true;
  var btn = this;
  api('/api/ghl/connect-location', {}).then(function(j){
    btn.disabled = false;
    if (j && j.ok && j.url) { window.open(j.url, '_blank'); }
    else { toast((j && j.error) || 'Could not start the connection. Try again.'); }
  }).catch(function(){ btn.disabled = false; toast('The connection could not start. Try again.'); });
});
$('reqBtn').addEventListener('click', function(){
  if (PAGE.live) {
    if (PAGE.worth && PAGE.worth.pass === false && PAGE.worth.ok !== false) {
      showInstall('fail', PAGE.worth.workable || 0, PAGE.worth.total || 0);
      return;
    }
    api('/api/ghl/request-campaign', {}).then(function(j){
      if (j && j.worth_fail) {
        PAGE.worth = {pass: false, workable: j.workable || 0, total: j.total || 0};
        showInstall('fail', j.workable || 0, j.total || 0);
        return;
      }
      toast(j.message || j.error || 'Request received. We will be in touch shortly.');
    }).catch(function(){ toast('The request did not go through. Try again in a moment.'); });
    return;
  }
  toast('Request received. We will follow up by email.');
});

// Retainer
$('retainerLink').addEventListener('click', function(){ open_('retainerOverlay'); });
$('cancelRetBtn').addEventListener('click', function(){ open_('cancelRetOverlay'); });
$('confirmCancelRet').addEventListener('click', function(){
  close_('cancelRetOverlay');
  if (PAGE.live) {
    api('/api/ghl/cancel-retainer', {}).then(function(j){
      if (j.ok) {
        apply(j.status === 'campaign-running' ? 'running' : 'none');
        toast('Retainer cancelled.' + (j.chapter ? ' Your current campaign runs to its finish.' : ''));
      } else {
        toast(j.error || 'The cancel did not go through. Try again in a moment.');
      }
    }).catch(function(){ toast('The cancel did not go through. Try again in a moment.'); });
    return;
  }
  S = 'cancelled'; apply('cancelled');
  toast('Retainer cancelled. Outreach stops today.');
});
function retGate(){
  $('retainerStart').disabled = !($('retainerAgree').checked
                                  && $('retSign').value.trim().length > 1);
}
$('retainerAgree').addEventListener('change', retGate);
$('retSign').addEventListener('input', retGate);
$('retainerStart').addEventListener('click', function(){
  close_('retainerOverlay');
  if (PAGE.live) {
    api('/api/ghl/start-retainer',
        {agreed: $('retainerAgree').checked, signature: $('retSign').value.trim()})
      .then(function(j){
        if (j.ok) {
          S = 'retainer'; apply('retainer');
          toast('Retainer active. Your coverage is now continuous.');
        } else {
          toast(j.error || 'Retainer signup did not go through. Try again in a moment.');
        }
      }).catch(function(){ toast('Retainer signup did not go through. Try again in a moment.'); });
    return;
  }
  S = 'retainer'; apply('retainer');
  toast('Retainer active. Your coverage is now continuous.');
});

// Help / contact open outside the iframe
$('helpLink').addEventListener('click', function(){ window.open('https://www.hayessystems.com/help.html', '_blank'); });
$('contactLink').addEventListener('click', function(){ window.open('mailto:Matt@hayessystems.com', '_blank'); });

// INSTALL-TIME QUALIFICATION POPUP (Matt 10/25): first-run pass/fail on
// workable leads. ?install=pass|fail|checking demos each; state=none
// shows it by default; the live page reads the install_check evidence
// from page-data (first_run only).
function installHTML(mode, workable, total){
  if (mode === 'checking') return '<div class="spin"></div><h3>Reading your CRM</h3>'
    + '<p style="margin-bottom:0">Counting your workable leads. This page'
    + ' updates when the count is ready.</p>';
  if (mode === 'pass') return '<h3>Your list qualifies</h3>'
    + '<p>' + fmtNum(workable) + ' workable leads after hygiene, out of ' + fmtNum(total) + ' total.</p>'
    + '<div class="dialog-actions" style="justify-content:center;margin-bottom:0">'
    + '<button class="btn btn-primary" onclick="closeInstall()">Request a new campaign</button></div>';
  return '<h3>Not enough workable leads yet</h3>'
    + '<p>A campaign needs at least 5,000 workable leads. Your list has '
    + fmtNum(workable) + ' workable of ' + fmtNum(total) + ' total. Duplicates,'
    + ' unreachable entries, and opted-out contacts are removed before counting.</p>'
    + '<div class="dialog-actions" style="justify-content:center;margin-bottom:0">'
    + '<button class="btn btn-ghost" onclick="closeInstall()">Got it</button></div>';
}
function showInstall(mode, workable, total){
  document.getElementById('installBody').innerHTML = installHTML(mode, workable, total);
  setTimeout(function(){ open_('installOverlay'); }, 400);
}
function closeInstall(){ close_('installOverlay'); }
(function(){
  var q = new URLSearchParams(location.search);
  var mode = q.get('install') || (q.get('state') === 'none' ? 'pass' : null);
  if (mode === 'pass') { showInstall('pass', 5214, 6102); }
  else if (mode === 'fail') { showInstall('fail', 1340, 3900); }
  else if (mode === 'checking') { showInstall('checking', 0, 0); }
})();

// IDENTITY SEAM BOOTSTRAP + REAL DATA BOOT: inside the GHL frame the URL
// carries the location's id; exchange it once for a signed session token,
// then pull page-data + appointments and populate every state from real
// data. Demo mode (no locationId param) skips all of this silently.
var PAGE = {token: null, name: null, data: null, live: false, worth: null, cooldownClosed: false, needsConnect: false};
function loadPageData(){
  if (!PAGE.token) return Promise.resolve();
  return api('/api/ghl/page-data').then(function(d){
    if (!d || !d.ok) return;
    PAGE.data = d;
    applyFromData(d);
    return api('/api/ghl/appointments').then(function(a){
      if (!a || !a.ok) return;
      renderAppts((a.appointments || []).map(function(x){
        return {name: x.lead_name, when: fmtWhen(x.when), status: x.status,
                reportable: !!x.reportable, ref: x.ref};
      }));
      if ((a.appointments || []).length) $('apptSec').classList.remove('hide');
    });
  }).catch(function(){});
}
function applyFromData(d){
  var st = (d.client && d.client.state) || 'none';
  var c = d.campaign;
  // a live campaign inside its pause window shows the paused state;
  // the server keeps state 'running' (the campaign stays fully alive)
  if (st === 'running' && c && c.paused) st = 'paused';
  apply(st, c && c.paused_until);
  PAGE.worth = d.install_check || null;
  PAGE.cooldownClosed = !!(d.cooldown && d.cooldown.open_now === false);
  PAGE.needsConnect = !!d.needs_location_connect;
  // the gate's Step 1 owns the first-run connect; the banner is the
  // fallback for already-onboarded clients (reinstall, revoked token)
  $('connectBanner').style.display =
    (PAGE.needsConnect && S !== 'onboarding') ? '' : 'none';
  if (typeof _updateConnectStep === 'function') { _updateConnectStep(); }
  if (PAGE.needsConnect) { $('reqBtn').disabled = true; }
  else if (st === 'none') {
    var rq = $('reqBtn');
    if (PAGE.cooldownClosed) { rq.disabled = true; }
    else if (PAGE.worth && PAGE.worth.pass === false) { rq.disabled = false; }
  }
  if (st === 'running' && c) {
    var sub = c.stopping
      ? 'Ending this week \\u00b7 appointments on your calendar are unaffected'
      : 'Week ' + c.week + ' of 4'
        + (c.projected_ends ? ' \\u00b7 Ends ' + fmtDay(c.projected_ends) : '')
        + (c.updated ? ' \\u00b7 Updated ' + fmtDay(c.updated) : '');
    pill(c.stopping ? 'stoppill' : 'run', c.stopping ? 'Ending' : 'Running', sub);
    setStats(c.workable, c.list_worked_pct, c.emails_sent, c.appointments,
             c.conversion_pct, c.cost_to_date);
  } else if (st === 'paused' && c) {
    // stats stay live through a pause (replies and bookings keep landing)
    setStats(c.workable, c.list_worked_pct, c.emails_sent, c.appointments,
             c.conversion_pct, c.cost_to_date);
  } else if (st === 'retainer') {
    if (c) {
      pill('run', 'Active', 'Chapter ' + c.week
           + (c.updated ? ' \\u00b7 Updated ' + fmtDay(c.updated) : ''));
      setStats(c.workable, c.list_worked_pct, c.emails_sent, c.appointments,
               c.conversion_pct, c.cost_to_date);
    } else {
      pill('run', 'Active', 'Continual coverage \\u00b7 the next chapter starts automatically');
    }
  }
  var cd = d.cooldown;
  if (st !== 'retainer' && cd && cd.next_opens) {
    $('cooldown').classList.remove('hide');
    $('cooldown').textContent = 'Campaigns need at least 3 months between runs. Your next campaign opens '
      + fmtLongDate(cd.next_opens) + '.';
  } else if (st === 'none') {
    $('cooldown').classList.add('hide');
  }
  renderPast(d.past_campaigns || []);
  // a client with history keeps their past-campaign table (and the
  // retainer offer) visible even with no live campaign - apply('none')
  // hides them for the fresh-install screen, real data brings them back
  if ((d.past_campaigns || []).length) {
    $('pastSec').classList.remove('hide');
    $('retainerLine').classList.remove('hide');
  }
  if (d.first_run && d.install_check && d.install_check.ok !== false
      && S !== 'onboarding') {
    showInstall(d.install_check.pass ? 'pass' : 'fail',
                d.install_check.workable || 0, d.install_check.total || 0);
  }
}
(function(){
  var loc = new URLSearchParams(location.search).get('locationId');
  // one-shot diagnostic (10/27): report what GHL passes to the frame
  try {
    fetch('https://ops.hayessystems.com/api/ghl/beacon', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        q: location.search, ref: document.referrer,
        href: location.href.slice(0, 300), ts: Date.now()})
    }).catch(function(){});
  } catch(e) {}
  if (!loc) return;
  try {
    fetch(API + '/api/ghl/session', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({locationId: loc})
    }).then(function(r){return r.ok ? r.json() : null;}).then(function(d){
      if (d && d.ok) {
        PAGE.token = d.token; PAGE.name = d.name; PAGE.live = true;
        loadPageData();
      }
    }).catch(function(){});
  } catch (e) {}
})();

// ONBOARDING GATE (Matt 10/25: nobody gets buttons or charges before they
// are told what it is and sign). state=onboarding shows ONLY the gate.
function applyOb(s){
  var on = (s === 'onboarding');
  $('obGate').classList.toggle('hide', !on);
  if (on) {
    $('obWelcome').classList.remove('hide');
    $('obForm').classList.add('hide');
    ['statusRow','stats','resendBtn','pauseBtn','cooldown','retainerLine',
     'apptSec','pastSec'].forEach(function(id){
      var el = $(id); if (el) el.classList.add('hide');
    });
    $('cancelBtn').classList.add('hide');
    $('cancelRetBtn').classList.add('hide');
    $('reqBtn').classList.add('hide');
  }
  if (typeof _updateConnectStep === 'function') { _updateConnectStep(); }
  // leaving onboarding: apply(S) owns visibility - applyOb never un-hides
  // (the old toggle('hide', on) shape un-hid EVERYTHING for non-onboarding
  // states, clobbering the none/retainer exclusions).
}
(function(){
  $('obAgree').addEventListener('change', function(){
    $('obTermsFull').classList.toggle('hide', !this.checked);
    updateObBtn();
  });
  function updateObBtn(){
    $('obSubmit').disabled = !($('obAgree').checked
      && $('obSign').value.trim().length > 1
      && _connectOk());
  }
  $('obSign').addEventListener('input', updateObBtn);
  var _cardOk = false, _pollTimer = null;
  function _updateCardStep() {
    var step = $('obCardStep'), state = $('obCardState');
    step.style.display = 'flex';
    if (_cardOk) {
      step.classList.add('done');
      state.textContent = 'On file';
      state.style.color = '#0e9e33';
      return true;
    }
    state.textContent = 'Needed';
    state.style.color = '#C62828';
    return false;
  }
  function _pollCard() {
    if (!PAGE.token) return;
    fetch(API + '/api/ghl/card-status', {
      headers: {'X-Hayes-Token': PAGE.token}
    }).then(function(r){return r.ok ? r.json() : null;}).then(function(d){
      if (d && d.ok && d.card_on_file) {
        _cardOk = true; _updateCardStep();
        if (_pollTimer) { clearInterval(_pollTimer); _pollTimer = null; }
        _maybeComplete();
      }
    }).catch(function(){});
  }
  // WIZARD: one step at a time, progress bar, back/continue injected.
  // The welcome screen opens first (obStart); gate entry resets there.
  var _obSteps = [], _obCur = -1;
  function _obInit() {
    _obSteps = Array.prototype.slice.call(
      document.querySelectorAll('#obForm .ob-step')).filter(function(el){
        return el.id !== 'obConnectStep'
          || (PAGE.needsConnect && !_connectDone);
      });
    var pr = $('obProgress'); pr.innerHTML = '';
    _obSteps.forEach(function(){ pr.appendChild(document.createElement('span')); });
    _obSteps.forEach(function(el, i){
      var row = document.createElement('div'); row.className = 'ob-walk';
      if (i > 0) {
        var b = document.createElement('button');
        b.className = 'btn btn-ghost'; b.textContent = 'Back';
        b.addEventListener('click', function(){ _obGo(i - 1); });
        row.appendChild(b);
      }
      var sp = document.createElement('div'); sp.className = 'spacer';
      row.appendChild(sp);
      if (el.id === 'obConnectStep') {
        var cb = $('obConnectBtn');
        if (cb) { row.insertBefore(cb, sp); }   // one footer row
      }
      if (i < _obSteps.length - 1) {
        var c = document.createElement('button');
        c.className = 'btn btn-primary'; c.textContent = 'Continue';
        if (el.id === 'obConnectStep') { c.id = 'obNextConnect'; }
        c.addEventListener('click', function(){ _obGo(i + 1); });
        row.appendChild(c);
      }
      el.appendChild(row);
    });
  }
  function _obGo(i) {
    if (i < 0 || i >= _obSteps.length) return;
    _obCur = i;
    _obSteps.forEach(function(el, j){ el.style.display = (j === i) ? '' : 'none'; });
    Array.prototype.slice.call($('obProgress').children).forEach(function(s, j){
      s.classList.toggle('on', j <= i);
    });
    var nc = $('obNextConnect');
    if (nc) { nc.disabled = !_connectOk(); }
  }
  $('obStart').addEventListener('click', function(){
    $('obWelcome').classList.add('hide');
    $('obForm').classList.remove('hide');
    _obInit(); _obGo(0);
  });

  // STEP 1: location connect (only shown when the credential is
  // company-scoped; hidden entirely for location-connected clients)
  var _connectDone = false, _connectPoll = null;
  function _connectOk() { return _connectDone || !PAGE.needsConnect; }
  function _updateConnectStep() {
    var st = $('obConnectStep');
    if (!st) return;
    $('obConnectState').textContent = _connectDone ? '\u2713 Connected' : '';
    $('obConnectBtn').classList.toggle('hide', _connectDone);
    var nc = $('obNextConnect');
    if (nc) { nc.disabled = !_connectOk(); }
    $('obSubmit').disabled = !($('obAgree').checked
      && $('obSign').value.trim().length > 1
      && _connectOk());
  }
  $('obConnectBtn').addEventListener('click', function(){
    var btn = this; btn.disabled = true;
    if (!PAGE.token) {   // demo mode: simulate the round trip
      setTimeout(function(){ _connectDone = true; PAGE.needsConnect = false;
        _updateConnectStep(); toast('Location connected.');
        if (_obCur === 0) { setTimeout(function(){ _obGo(1); }, 600); } }, 1200);
      return;
    }
    api('/api/ghl/connect-location', {}).then(function(j){
      btn.disabled = false;
      if (j && j.ok && j.url) { window.open(j.url, '_blank'); _startConnectPoll(); }
      else { toast((j && j.error) || 'Could not start the connection.'); }
    }).catch(function(){ btn.disabled = false;
      toast('The connection could not start.'); });
  });
  function _startConnectPoll() {
    if (_connectPoll) return;
    _connectPoll = setInterval(function(){
      if (_connectDone) { clearInterval(_connectPoll); _connectPoll = null; return; }
      loadPageData().then(function(){
        if (!_connectDone && !PAGE.needsConnect) {
          _connectDone = true; clearInterval(_connectPoll); _connectPoll = null;
          _updateConnectStep(); toast('Location connected.');
          if (_obCur === 0) { setTimeout(function(){ _obGo(1); }, 600); }
        }
      });
    }, 4000);
  }
  document.addEventListener('visibilitychange', function(){
    if (!document.hidden && PAGE.needsConnect && !_connectDone
        && S === 'onboarding') { loadPageData().then(function(){
          if (!PAGE.needsConnect) {
            _connectDone = true; _updateConnectStep();
            toast('Location connected.');
            if (_obCur === 0) { setTimeout(function(){ _obGo(1); }, 600); }
          }
        }); }
  });

  var _signed = false;
  function _maybeComplete() {
    if (!_signed || !_cardOk) return;
    if (_pollTimer) { clearInterval(_pollTimer); _pollTimer = null; }
    $('obForm').classList.add('hide');
    $('obDone').classList.remove('hide');
    toast('Setup complete.');
  }
  $('obSubmit').addEventListener('click', function(){
    _signed = true;
    if (_updateCardStep()) { _maybeComplete(); return; }
    // open Stripe checkout in a new tab (top-level: reliable for 3DS)
    if (PAGE.token) {
      fetch(API + '/api/ghl/stripe-setup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',
                  'X-Hayes-Token': PAGE.token},
        body: JSON.stringify({locationId:
          new URLSearchParams(location.search).get('locationId') || ''})
      }).then(function(r){return r.ok ? r.json() : null;}).then(function(d){
        if (d && d.checkout_url) window.open(d.checkout_url, '_blank');
        else toast('Card setup is unavailable right now. We will reach out.');
      }).catch(function(){ toast('Card setup is unavailable right now.'); });
    } else {
      // demo mode: simulate the card landing after a moment
      setTimeout(function(){ _cardOk = true; _updateCardStep(); _maybeComplete(); }, 1600);
    }
    _pollTimer = setInterval(_pollCard, 3000);
    _pollCard();
  });
  document.addEventListener('visibilitychange', function(){
    if (!document.hidden && _signed && !_cardOk) _pollCard();
  });
  $('obGo').addEventListener('click', function(){
    S = 'none'; apply('none'); applyOb('done');
    // live mode: skip the demo none-state and boot from real data instead
    if (PAGE.live) loadPageData();
  });
})();

// Initial state for review: ?state=running|paused|cancelled|none
var q = new URLSearchParams(location.search).get('state') || 'running';
var init = (['running','paused','cancelled','none','onboarding','retainer'].indexOf(q) > -1 ? q : 'running');
if (init === 'onboarding' && !location.search.includes('locationId=')) {
  PAGE.needsConnect = true;   // demo the gate's Step 1 for review
}
S = init;
apply(init);
applyOb(init);
</script>

</body></html>'''

html = html.replace('@@HOUSE@@', house).replace('@@PANES@@', panes)
(SITE/'_ghl_native_page.html').write_text(html)
# deployed artifact: same page + noindex (the GHL frame URL is not for
# search engines; the marketing site owns indexing)
(SITE/'ghl-app.html').write_text(
    html.replace('<meta charset="utf-8">',
                 '<meta charset="utf-8"><meta name="robots" content="noindex">', 1))
print('staged interactive v2.3 (review twin + deployed ghl-app.html)')
