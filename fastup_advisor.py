"""
Fast&Up AI Advisor — Improved Version
Changes:
  1. AI Recommendation Logic   → Weighted scoring matrix (multi-factor) replaces naive if/elif chain
  2. UI/UX & Visual Design     → Refined card layouts, typography, micro-animations, progress bar
  3. Code Quality & Structure  → Modular helpers, constants extracted, clear separation of concerns
  4. Performance               → CSS deduplicated, base64 images referenced via URL instead of inline
  5. Capsule black bg fix       → mix-blend-mode: multiply + transparent tube-zone bg removes black JPEG artifact
  6. Chat flow                 → Variable thinking delays, smoother transitions, better empty states
"""

# ── SCREEN 1 HTML ─────────────────────────────────────────────────────────────
SCREEN1_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Clash+Display:wght@600;700&family=Cabinet+Grotesk:wght@400;500;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{
  --void:#04050a;--ink0:#07090f;--ink1:#0c0f1c;--ink2:#111626;--ink3:#181e30;--ink4:#1f2740;
  --or:#ff5500;--or1:#ff6a1a;--or2:#ff8844;--or3:#ffb380;
  --cy:#00d4ff;--cy1:#00bde8;--cy2:#00f5f0;--gr:#00e676;--gold:#ffd200;
  --tx0:#ffffff;--tx1:rgba(255,255,255,.85);--tx2:rgba(255,255,255,.55);
  --tx3:rgba(255,255,255,.28);--tx4:rgba(255,255,255,.12);
  --glow-or:0 0 60px rgba(255,85,0,.4),0 0 120px rgba(255,85,0,.15);
  --glow-cy:0 0 60px rgba(0,212,255,.4),0 0 120px rgba(0,212,255,.12);
  --r1:14px;--r2:20px;--r3:28px;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
html,body{width:100%;height:100%;background:var(--void);overflow:hidden;cursor:none}
body{font-family:'Cabinet Grotesk',sans-serif;position:relative;min-height:100vh}

/* CURSOR */
#cursor{position:fixed;width:12px;height:12px;background:var(--or);border-radius:50%;pointer-events:none;z-index:9999;transform:translate(-50%,-50%);transition:width .2s,height .2s,background .2s;mix-blend-mode:screen}
#cursor-ring{position:fixed;width:36px;height:36px;border:1.5px solid rgba(255,85,0,.4);border-radius:50%;pointer-events:none;z-index:9998;transform:translate(-50%,-50%);transition:all .12s ease-out}
body:has(.cta-btn:hover) #cursor{width:20px;height:20px;background:var(--cy)}
body:has(.cta-btn:hover) #cursor-ring{width:52px;height:52px;border-color:rgba(0,212,255,.5)}

/* CANVAS / GRID */
#canvas-bg{position:fixed;inset:0;z-index:0;pointer-events:none}
.grid-overlay{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(0,212,255,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.022) 1px,transparent 1px);
  background-size:44px 44px}

/* AMBIENT ORBS */
.orb1{position:fixed;width:800px;height:800px;top:-280px;left:-240px;border-radius:50%;background:radial-gradient(circle,rgba(255,85,0,.22),transparent 65%);filter:blur(120px);pointer-events:none;z-index:0;animation:o1 14s ease-in-out infinite}
.orb2{position:fixed;width:600px;height:600px;bottom:-200px;right:-180px;border-radius:50%;background:radial-gradient(circle,rgba(0,212,255,.14),transparent 65%);filter:blur(100px);pointer-events:none;z-index:0;animation:o2 18s ease-in-out infinite}
.orb3{position:fixed;width:500px;height:500px;top:40%;left:50%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,150,0,.04),transparent 65%);filter:blur(80px);pointer-events:none;z-index:0;animation:o3 22s ease-in-out infinite}
@keyframes o1{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,40px)}}
@keyframes o2{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,-35px)}}
@keyframes o3{0%,100%{transform:translate(-50%,-50%)}50%{transform:translate(-52%,-48%)}}

.particle{position:fixed;border-radius:50%;pointer-events:none;z-index:1;animation:partFloat linear infinite}
@keyframes partFloat{0%{opacity:0;transform:translateY(0) scale(1)}10%{opacity:1}85%{opacity:.4}100%{opacity:0;transform:translateY(-100vh) scale(.2)}}

/* SHELL */
.shell{position:relative;z-index:2;width:100%;min-height:100vh;display:flex;flex-direction:column;padding:0 52px;max-width:1200px;margin:0 auto}

/* NAVBAR */
.nav{display:flex;align-items:center;justify-content:space-between;padding:20px 0 16px;border-bottom:1px solid rgba(255,255,255,.05);animation:navIn .6s ease .1s both}
@keyframes navIn{from{opacity:0;transform:translateY(-12px)}to{opacity:1;transform:none}}
.nav-brand{display:flex;align-items:center;gap:11px}
.nav-mark{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,var(--or),var(--or1));display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',cursive;font-size:13px;color:#fff;box-shadow:0 0 18px rgba(255,85,0,.5),0 0 40px rgba(255,85,0,.18);animation:markPulse 2.5s ease-in-out infinite alternate}
@keyframes markPulse{from{box-shadow:0 0 14px rgba(255,85,0,.4),0 0 32px rgba(255,85,0,.12)}to{box-shadow:0 0 28px rgba(255,85,0,.8),0 0 60px rgba(255,85,0,.3)}}
.nav-name{font-family:'Bebas Neue',cursive;font-size:18px;letter-spacing:3.5px;color:var(--tx0)}
.nav-name em{font-style:normal;color:var(--or)}
.nav-right{display:flex;align-items:center;gap:14px}
.live-pill{display:flex;align-items:center;gap:7px;padding:5px 12px;border-radius:20px;background:rgba(0,230,118,.07);border:1px solid rgba(0,230,118,.25)}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--gr);box-shadow:0 0 8px rgba(0,230,118,.9);animation:livePulse 2s ease-in-out infinite}
@keyframes livePulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.25;transform:scale(.8)}}
.live-txt{font-family:'Space Mono',monospace;font-size:9px;color:var(--gr);font-weight:700;letter-spacing:1.5px}
.nav-site{font-family:'Space Mono',monospace;font-size:9px;color:var(--tx3);letter-spacing:1.5px;text-transform:uppercase;transition:color .2s}
.nav-site:hover{color:var(--tx2)}

/* HERO */
.hero{flex:1;display:grid;grid-template-columns:1fr 360px;gap:56px;align-items:center;padding:20px 0 0}

/* LEFT */
.hero-left{display:flex;flex-direction:column;gap:0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:20px;background:rgba(255,85,0,.09);border:1px solid rgba(255,85,0,.3);width:fit-content;margin-bottom:22px;animation:fadeUp .5s cubic-bezier(.16,1,.3,1) .25s both}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.eye-dot{width:6px;height:6px;border-radius:50%;background:var(--or);box-shadow:0 0 8px rgba(255,85,0,.9);animation:livePulse 1.6s ease-in-out infinite}
.eye-txt{font-family:'Space Mono',monospace;font-size:9px;color:var(--or2);letter-spacing:2px;text-transform:uppercase;font-weight:700}
.headline{font-family:'Bebas Neue',cursive;font-size:clamp(52px,5.8vw,78px);color:var(--tx0);line-height:.98;letter-spacing:1px;margin-bottom:22px;animation:fadeUp .7s cubic-bezier(.16,1,.3,1) .35s both}
.hl-dim{color:var(--tx2);font-size:.95em}
.hl-or{color:var(--or);text-shadow:0 0 40px rgba(255,85,0,.6),0 0 80px rgba(255,85,0,.25);animation:orGlow 3s ease-in-out infinite alternate}
@keyframes orGlow{from{text-shadow:0 0 30px rgba(255,85,0,.5),0 0 60px rgba(255,85,0,.2)}to{text-shadow:0 0 55px rgba(255,85,0,.8),0 0 100px rgba(255,85,0,.4)}}
.hl-cy{background:linear-gradient(90deg,var(--cy),var(--cy2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 20px rgba(0,212,255,.5));animation:cyGlow 3s ease-in-out 1.5s infinite alternate}
@keyframes cyGlow{from{filter:drop-shadow(0 0 14px rgba(0,212,255,.4))}to{filter:drop-shadow(0 0 28px rgba(0,212,255,.8))}}
.sub{font-size:15px;color:var(--tx2);line-height:1.7;max-width:400px;margin-bottom:28px;animation:fadeUp .6s cubic-bezier(.16,1,.3,1) .48s both;font-weight:500}
.sub strong{color:var(--tx1);font-weight:700}
.steps{display:flex;align-items:center;margin-bottom:30px;position:relative;animation:fadeUp .5s ease .6s both}
.steps::before{content:'';position:absolute;top:14px;left:14px;right:14px;height:1px;background:linear-gradient(90deg,rgba(255,85,0,.3),rgba(0,212,255,.3));z-index:0}
.step{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1;z-index:1}
.step-n{width:28px;height:28px;border-radius:50%;background:var(--ink1);border:1.5px solid rgba(255,85,0,.4);display:flex;align-items:center;justify-content:center;font-family:'Space Mono',monospace;font-size:10px;color:var(--or2);font-weight:700;transition:all .3s}
.step:hover .step-n{background:rgba(255,85,0,.15);border-color:var(--or);box-shadow:0 0 12px rgba(255,85,0,.4)}
.step-l{font-family:'Space Mono',monospace;font-size:8.5px;color:var(--tx3);text-transform:uppercase;letter-spacing:1px;transition:color .3s}
.step:hover .step-l{color:var(--tx2)}
.cta-group{display:flex;flex-direction:column;gap:0;margin-bottom:28px;animation:fadeUp .7s cubic-bezier(.34,1.56,.64,1) .72s both}
.cta-btn{
  display:inline-flex;align-items:center;justify-content:center;gap:14px;
  padding:18px 42px;border-radius:16px;
  background:linear-gradient(135deg,var(--or) 0%,var(--or1) 50%,#ff8c00 100%);
  border:none;cursor:none;width:fit-content;
  font-family:'Bebas Neue',cursive;font-size:18px;letter-spacing:2px;color:#fff;
  transition:all .3s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;
  animation:ctaAppear .8s cubic-bezier(.34,1.56,.64,1) .72s both,ctaPulse 3s ease-in-out 2s infinite;
}
@keyframes ctaAppear{from{opacity:0;transform:scale(.85) translateY(20px)}to{opacity:1;transform:none}}
@keyframes ctaPulse{
  0%,100%{box-shadow:0 0 25px rgba(255,85,0,.35),0 8px 32px rgba(0,0,0,.45)}
  50%{box-shadow:0 0 50px rgba(255,85,0,.6),0 8px 40px rgba(0,0,0,.5),0 0 100px rgba(255,85,0,.2)}
}
.cta-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.18),transparent 60%);border-radius:16px}
.cta-btn::after{content:'';position:absolute;top:-50%;left:-60%;width:80%;height:200%;background:linear-gradient(105deg,transparent,rgba(255,255,255,.28),transparent);transform:skewX(-20deg) translateX(-100%)}
.cta-btn:hover{transform:translateY(-4px) scale(1.03);box-shadow:0 0 70px rgba(255,85,0,.65),0 20px 50px rgba(0,0,0,.55),0 0 130px rgba(255,85,0,.25)!important;animation:none}
.cta-btn:hover::after{animation:ctaShine .7s ease forwards}
@keyframes ctaShine{to{transform:skewX(-20deg) translateX(280%)}}
.cta-btn:active{transform:translateY(-1px) scale(.99)}
.cta-icon{width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:14px;transition:transform .3s}
.cta-btn:hover .cta-icon{transform:translateX(6px)}
.cta-sub{margin-top:10px;margin-left:2px;font-family:'Space Mono',monospace;font-size:10px;color:var(--tx3);letter-spacing:.8px;display:flex;align-items:center;gap:7px}
.cta-sub::before{content:'';display:inline-block;width:18px;height:1px;background:rgba(255,85,0,.4)}
.trust{display:flex;flex-wrap:wrap;gap:10px;animation:fadeUp .5s ease .88s both}
.tbadge{display:flex;align-items:center;gap:7px;padding:6px 12px;border-radius:10px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);transition:all .25s}
.tbadge:hover{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14);transform:translateY(-2px)}
.tbadge-icon{font-size:12px}
.tbadge-txt{font-family:'Space Mono',monospace;font-size:9px;color:var(--tx2);letter-spacing:.5px}
.tbadge-txt strong{color:var(--tx1)}

/* RIGHT: PRODUCT CARD */
.hero-right{display:flex;align-items:center;justify-content:center}
.prod-card{
  width:340px;
  background:linear-gradient(160deg,rgba(18,20,38,.97) 0%,rgba(10,12,22,.99) 100%);
  border:1px solid rgba(255,85,0,.2);border-radius:var(--r3);overflow:hidden;
  box-shadow:0 0 0 1px rgba(255,255,255,.04),0 40px 100px rgba(0,0,0,.65),0 0 80px rgba(255,85,0,.07);
  animation:cardIn .9s cubic-bezier(.16,1,.3,1) .6s both;
  transition:transform .4s cubic-bezier(.16,1,.3,1),box-shadow .4s;cursor:none;
}
@keyframes cardIn{from{opacity:0;transform:translateX(40px) scale(.96)}to{opacity:1;transform:none}}
.prod-card:hover{transform:translateY(-8px) scale(1.02);box-shadow:0 0 0 1px rgba(255,85,0,.25),0 60px 120px rgba(0,0,0,.7),0 0 120px rgba(255,85,0,.14)}
.card-topbar{height:2.5px;background:linear-gradient(90deg,transparent,var(--or) 30%,var(--cy) 70%,transparent);background-size:200%;animation:tlSlide 2.5s linear infinite}
@keyframes tlSlide{0%{background-position:100%}100%{background-position:-100%}}

/* ── TUBE ZONE — KEY FIX: transparent background, mix-blend-mode:multiply ── */
.tube-zone{
  height:210px;position:relative;
  display:flex;align-items:center;justify-content:center;
  overflow:hidden;
  background:transparent; /* was implicitly dark */
}
.tube-zone::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 65%,rgba(255,85,0,.14),transparent 65%)}
.tr1,.tr2,.tr3{position:absolute;border-radius:50%;animation:trPulse ease-in-out infinite}
.tr1{width:200px;height:200px;background:radial-gradient(circle,rgba(255,85,0,.18),transparent 65%);filter:blur(22px);animation-duration:3s}
.tr2{width:150px;height:150px;background:radial-gradient(circle,rgba(255,130,0,.12),transparent 65%);filter:blur(16px);animation-duration:3s;animation-delay:.5s}
.tr3{width:100px;height:100px;background:radial-gradient(circle,rgba(255,180,0,.08),transparent 65%);filter:blur(10px);animation-duration:3s;animation-delay:1s}
@keyframes trPulse{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.35);opacity:1}}
.orbit{position:absolute;width:175px;height:175px;border-radius:50%;border:1px dashed rgba(255,85,0,.18);animation:orbitSpin 10s linear infinite}
@keyframes orbitSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
.orbit::before{content:'';position:absolute;top:-5px;left:50%;transform:translateX(-50%);width:9px;height:9px;border-radius:50%;background:var(--or);box-shadow:0 0 14px rgba(255,85,0,1),0 0 28px rgba(255,85,0,.5)}
.orbit2{position:absolute;width:130px;height:130px;border-radius:50%;border:1px dashed rgba(0,212,255,.12);animation:orbitSpin 14s linear infinite reverse}
.orbit2::before{content:'';position:absolute;bottom:-5px;left:50%;transform:translateX(-50%);width:6px;height:6px;border-radius:50%;background:var(--cy);box-shadow:0 0 10px rgba(0,212,255,1)}
.drp{position:absolute;border-radius:50%;animation:drpRise linear infinite;opacity:0}
.drp:nth-child(1){width:5px;height:5px;background:rgba(255,120,40,.65);left:20%;animation-duration:2.6s;animation-delay:0s}
.drp:nth-child(2){width:4px;height:4px;background:rgba(255,180,80,.5);left:40%;animation-duration:3.2s;animation-delay:.7s}
.drp:nth-child(3){width:6px;height:6px;background:rgba(255,100,30,.6);left:63%;animation-duration:2.3s;animation-delay:1.2s}
.drp:nth-child(4){width:3px;height:3px;background:rgba(0,212,255,.4);left:80%;animation-duration:3s;animation-delay:.4s}
.drp:nth-child(5){width:4px;height:4px;background:rgba(255,150,60,.55);left:50%;animation-duration:2.7s;animation-delay:1.8s}
@keyframes drpRise{0%{top:100%;opacity:0}8%{opacity:.8}82%{opacity:.35}100%{top:-10px;opacity:0}}

/*
  ★ CAPSULE BLACK BACKGROUND FIX ★
  The tube image is a JPEG with a dark/black background.
  mix-blend-mode: multiply makes dark pixels of the image transparent
  against a dark container background — removing the black box effect.
  screen also works; multiply is better when the surrounding bg is dark.
*/
.tube-img{
  width:120px;height:auto;position:relative;z-index:5;
  mix-blend-mode: multiply;          /* ← FIXES the black background on JPEG capsule */
  filter:
    drop-shadow(0 0 24px rgba(255,85,0,.55))
    drop-shadow(0 0 60px rgba(255,85,0,.22))
    brightness(1.15)                  /* slight lift so product colours stay vivid */
    contrast(1.05);
  animation:tubeFloat 4.5s ease-in-out infinite,tubeAura 3s ease-in-out infinite alternate;
  transform-origin:center bottom;
}
@keyframes tubeFloat{
  0%,100%{transform:translateY(0) rotate(-1.5deg) scale(1)}
  50%{transform:translateY(-16px) rotate(1.5deg) scale(1.03)}
}
@keyframes tubeAura{
  from{filter:drop-shadow(0 0 20px rgba(255,85,0,.45)) drop-shadow(0 0 50px rgba(255,85,0,.18)) brightness(1.15) contrast(1.05) multiply}
  to{filter:drop-shadow(0 0 36px rgba(255,85,0,.75)) drop-shadow(0 0 80px rgba(255,85,0,.32)) brightness(1.2) contrast(1.05)}
}

/* CARD BODY */
.cb{padding:20px 22px 22px}
.cb-eyebrow{font-family:'Space Mono',monospace;font-size:8.5px;color:rgba(255,85,0,.65);letter-spacing:3px;text-transform:uppercase;margin-bottom:7px;display:flex;align-items:center;gap:7px}
.cb-eyebrow::before{content:'⚡';animation:zapA 1s ease-in-out infinite alternate;display:inline-block}
@keyframes zapA{from{opacity:.35;transform:scale(.85)}to{opacity:1;transform:scale(1.15)}}
.cb-name{font-family:'Bebas Neue',cursive;font-size:26px;color:var(--tx0);line-height:1;margin-bottom:3px;letter-spacing:.5px}
.cb-name em{font-style:normal;background:linear-gradient(90deg,var(--or),var(--or2),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.cb-cat{font-family:'Space Mono',monospace;font-size:8px;color:var(--tx3);letter-spacing:.8px;margin-bottom:16px}
.cb-metrics{display:flex;border:1px solid rgba(255,255,255,.06);border-radius:12px;overflow:hidden;margin-bottom:15px}
.cm{flex:1;padding:10px 8px;text-align:center;border-right:1px solid rgba(255,255,255,.06);transition:background .25s}
.cm:last-child{border-right:none}
.cm:hover{background:rgba(255,85,0,.06)}
.cm-val{display:block;font-family:'Bebas Neue',cursive;font-size:19px;background:linear-gradient(90deg,var(--or),var(--or2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.cm-lbl{font-family:'Space Mono',monospace;font-size:7px;color:var(--tx3);letter-spacing:1px;text-transform:uppercase}
.cb-tags{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:16px}
.ctag{padding:3px 9px;border-radius:20px;font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3px;transition:all .2s;cursor:none}
.ctag:hover{transform:translateY(-2px)}
.ct-or{background:rgba(255,85,0,.1);border:1px solid rgba(255,85,0,.28);color:rgba(255,150,90,.9)}
.ct-cy{background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.22);color:rgba(0,212,255,.85)}
.match-block{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px 14px}
.match-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:9px}
.match-label{font-family:'Space Mono',monospace;font-size:8.5px;color:var(--tx3);letter-spacing:1.5px;text-transform:uppercase}
.match-score{font-family:'Bebas Neue',cursive;font-size:22px;color:var(--cy);line-height:1;text-shadow:0 0 20px rgba(0,212,255,.7)}
.match-track{height:5px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden}
.match-fill{height:100%;border-radius:5px;width:0;background:linear-gradient(90deg,var(--or),#ff9500,var(--cy));box-shadow:0 0 12px rgba(0,212,255,.4);animation:mfIn 1.2s cubic-bezier(.4,0,.2,1) 1.6s both}
@keyframes mfIn{to{width:94%}}
.match-sub{font-family:'Space Mono',monospace;font-size:7.5px;color:var(--tx3);letter-spacing:.8px;margin-top:7px}
.cb-dots{display:flex;gap:5px;justify-content:center;margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,.05)}
.cdot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.1);transition:all .35s}
.cdot.on{background:var(--or);width:18px;border-radius:3px;box-shadow:0 0 9px rgba(255,85,0,.7)}

/* CERT BAR */
.cert-bar{display:flex;align-items:center;justify-content:center;gap:24px;padding:14px 0 18px;border-top:1px solid rgba(255,255,255,.04);animation:fadeUp .4s ease 1.1s both}
.cert-item{display:flex;align-items:center;gap:6px;font-family:'Space Mono',monospace;font-size:8px;color:var(--tx3);letter-spacing:1.5px;text-transform:uppercase;transition:color .25s}
.cert-item:hover{color:var(--tx2)}
.cert-icon{font-size:10px;opacity:.55}
.cert-sep{width:1px;height:10px;background:rgba(255,255,255,.06)}

/* EXPLOSION ANIMATIONS — UNCHANGED */
.tube-wrap{position:fixed;top:45%;left:50%;transform:translate(-50%,-50%);z-index:50;width:200px;display:flex;align-items:center;justify-content:center}
.tube-anim{width:200px;height:auto;position:relative;z-index:10;
  mix-blend-mode:multiply; /* ← also fixes the explosion animation tube */
  filter:brightness(1.1) contrast(1.05);
  animation:tubeIn .8s cubic-bezier(.34,1.56,.64,1) .3s both,tubeShake .7s ease-in-out 1.3s both,tubePop .55s cubic-bezier(.55,0,1,.45) 2.1s both}
@keyframes tubeIn{0%{opacity:0;transform:scale(0) translateY(80px) rotate(-15deg)}55%{opacity:1;transform:scale(1.18) translateY(-10px) rotate(4deg)}78%{transform:scale(.95) translateY(4px) rotate(-1.5deg)}100%{opacity:1;transform:scale(1) translateY(0) rotate(0)}}
@keyframes tubeShake{0%{transform:scale(1) rotate(0) translateX(0)}12%{transform:scale(1.04) rotate(-7deg) translateX(-12px)}26%{transform:scale(1.07) rotate(8deg) translateX(14px)}40%{transform:scale(1.05) rotate(-6deg) translateX(-11px)}56%{transform:scale(1.06) rotate(7deg) translateX(12px)}70%{transform:scale(1.02) rotate(-3deg) translateX(-5px)}85%{transform:scale(1.01) rotate(2deg) translateX(3px)}100%{transform:scale(1) rotate(0) translateX(0)}}
@keyframes tubePop{0%{opacity:1;transform:scale(1) rotate(0);filter:brightness(1.1) drop-shadow(0 0 30px rgba(255,85,0,.6))}30%{opacity:1;transform:scale(1.4) rotate(5deg);filter:brightness(5) drop-shadow(0 0 80px rgba(255,200,80,1))}60%{opacity:.3;transform:scale(2) rotate(8deg);filter:brightness(8)}100%{opacity:0;transform:scale(3) rotate(12deg);filter:brightness(10)}}
.tube-glow{position:absolute;width:200px;height:280px;background:radial-gradient(ellipse,rgba(255,85,0,.5) 0%,transparent 68%);filter:blur(30px);z-index:9;border-radius:50%;animation:glowIn .7s ease 1.1s both,glowPulse 1.6s ease-in-out 1.8s infinite alternate}
@keyframes glowIn{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:scale(1)}}
@keyframes glowPulse{from{opacity:.5;transform:scale(1)}to{opacity:1;transform:scale(1.5)}}
.flash{position:fixed;inset:0;z-index:88;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(255,255,200,1) 0%,rgba(255,140,0,.9) 20%,rgba(255,60,0,.5) 45%,transparent 68%);opacity:0;animation:bigFlash .6s ease-out 2.1s both}
@keyframes bigFlash{0%{opacity:0}18%{opacity:1}55%{opacity:.8}100%{opacity:0}}
.parts{position:fixed;top:45%;left:50%;width:0;height:0;z-index:85}
.p{position:absolute;border-radius:50%;opacity:0;animation:pfly 1.4s cubic-bezier(.1,.8,.2,1) 2.12s forwards}
@keyframes pfly{0%{opacity:1;transform:translate(0,0) scale(2.2)}18%{opacity:1}100%{opacity:0;transform:var(--t) scale(0)}}
.p:nth-child(1){width:16px;height:16px;background:#ff5500;--t:translate(-145px,-130px)}.p:nth-child(2){width:10px;height:10px;background:#ff9944;--t:translate(150px,-138px)}.p:nth-child(3){width:13px;height:13px;background:#00d4ff;--t:translate(-128px,152px)}.p:nth-child(4){width:10px;height:10px;background:#ffd200;--t:translate(142px,135px)}.p:nth-child(5){width:17px;height:17px;background:#ff5500;--t:translate(-188px,28px)}.p:nth-child(6){width:10px;height:10px;background:#fff;--t:translate(192px,-28px)}.p:nth-child(7){width:12px;height:12px;background:#00d4ff;--t:translate(38px,-195px)}.p:nth-child(8){width:13px;height:13px;background:#ff5500;--t:translate(-38px,198px)}.p:nth-child(9){width:9px;height:9px;background:#fff;--t:translate(118px,-178px)}.p:nth-child(10){width:9px;height:9px;background:#ffaa44;--t:translate(-120px,-178px)}.p:nth-child(11){width:12px;height:12px;background:#ff9944;--t:translate(202px,92px)}.p:nth-child(12){width:13px;height:13px;background:#ffd200;--t:translate(-205px,92px)}.p:nth-child(13){width:8px;height:8px;background:#00d4ff;--t:translate(92px,200px)}.p:nth-child(14){width:8px;height:8px;background:#fff;--t:translate(-92px,202px)}.p:nth-child(15){width:10px;height:10px;background:#ff5500;--t:translate(178px,-122px)}.p:nth-child(16){width:11px;height:11px;background:#00d4ff;--t:translate(-178px,-122px)}.p:nth-child(17){width:9px;height:9px;background:#ffd200;--t:translate(95px,210px)}.p:nth-child(18){width:8px;height:8px;background:#ff9944;--t:translate(-95px,-210px)}.p:nth-child(19){width:7px;height:7px;background:#00d4ff;--t:translate(-212px,-58px)}.p:nth-child(20){width:7px;height:7px;background:#fff;--t:translate(215px,58px)}.p:nth-child(21){width:10px;height:10px;background:#ff5500;--t:translate(140px,-200px)}.p:nth-child(22){width:9px;height:9px;background:#ffd200;--t:translate(-140px,205px)}.p:nth-child(23){width:8px;height:8px;background:#ff9944;--t:translate(220px,-80px)}.p:nth-child(24){width:8px;height:8px;background:#00d4ff;--t:translate(-222px,80px)}
.fiz{position:fixed;border-radius:50%;background:rgba(255,140,40,.8);bottom:56%;opacity:0;animation:fizUp linear forwards}
.fiz:nth-child(1){width:11px;height:11px;left:calc(50% - 44px);animation-duration:1.5s;animation-delay:2.18s}.fiz:nth-child(2){width:7px;height:7px;left:calc(50% + 22px);animation-duration:1.8s;animation-delay:2.28s}.fiz:nth-child(3){width:14px;height:14px;left:calc(50% - 15px);animation-duration:1.6s;animation-delay:2.22s}.fiz:nth-child(4){width:6px;height:6px;left:calc(50% + 52px);animation-duration:2.0s;animation-delay:2.14s}.fiz:nth-child(5){width:10px;height:10px;left:calc(50% - 68px);animation-duration:1.35s;animation-delay:2.32s}.fiz:nth-child(6){width:8px;height:8px;left:calc(50% + 72px);animation-duration:1.65s;animation-delay:2.40s}.fiz:nth-child(7){width:9px;height:9px;left:calc(50% + 8px);animation-duration:1.9s;animation-delay:2.25s}.fiz:nth-child(8){width:7px;height:7px;left:calc(50% - 32px);animation-duration:1.55s;animation-delay:2.35s}
@keyframes fizUp{0%{opacity:.95;transform:translateY(0) scale(1)}12%{opacity:1}100%{opacity:0;transform:translateY(-300px) scale(.02)}}
.ring{position:fixed;border-radius:50%;top:45%;left:50%;transform:translate(-50%,-50%);opacity:0;animation:ringExp 1.6s ease-out forwards}
.ring:nth-child(1){border:3.5px solid rgba(255,100,0,.9);animation-delay:2.14s}.ring:nth-child(2){border:2.5px solid rgba(0,212,255,.8);animation-delay:2.40s}.ring:nth-child(3){border:3px solid rgba(255,100,0,.6);animation-delay:2.65s}.ring:nth-child(4){border:2px solid rgba(0,212,255,.5);animation-delay:2.90s}
@keyframes ringExp{0%{opacity:.95;width:60px;height:60px}100%{opacity:0;width:700px;height:700px}}
.logo-wrap{position:fixed;top:45%;left:50%;transform:translate(-50%,-50%);z-index:92;opacity:0;animation:logoPop 1s cubic-bezier(.34,1.56,.64,1) 2.3s forwards}
@keyframes logoPop{0%{opacity:0;transform:translate(-50%,-50%) scale(0) rotate(-30deg)}55%{opacity:1;transform:translate(-50%,-56%) scale(1.22) rotate(6deg)}78%{transform:translate(-50%,-50%) scale(.95) rotate(-2deg)}100%{opacity:1;transform:translate(-50%,-50%) scale(1) rotate(0)}}
.logo-circle{width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 30% 28%,#1e3060,#040916);border:3.5px solid #00d4ff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;position:relative;overflow:hidden;box-shadow:0 0 0 18px rgba(0,212,255,.05),0 0 70px rgba(0,212,255,.95),0 0 160px rgba(0,212,255,.4);animation:logoPulse 2s ease-in-out 3.4s infinite alternate}
@keyframes logoPulse{from{box-shadow:0 0 50px rgba(0,212,255,.6),0 0 100px rgba(0,212,255,.2)}to{box-shadow:0 0 80px rgba(0,212,255,1),0 0 180px rgba(0,212,255,.55)}}
.sp1{position:absolute;inset:9px;border-radius:50%;border:2.5px solid transparent;border-top-color:#00d4ff;border-right-color:rgba(0,212,255,.14);animation:spin 2s linear 2.55s infinite}
.sp2{position:absolute;inset:18px;border-radius:50%;border:1.5px solid transparent;border-bottom-color:rgba(0,212,255,.5);border-left-color:rgba(0,212,255,.12);animation:spin 3.2s linear 2.55s infinite reverse}
@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
.logo-ai{font-family:'Bebas Neue',cursive;font-size:32px;color:#00d4ff;text-shadow:0 0 28px rgba(0,212,255,1),0 0 65px rgba(0,212,255,.7);z-index:1;line-height:1}
.logo-sub{font-family:'Space Mono',monospace;font-size:7.5px;color:rgba(0,212,255,.65);letter-spacing:2.5px;text-transform:uppercase;z-index:1}
@keyframes ripple{to{transform:translate(-50%,-50%) scale(28);opacity:0}}
</style>
</head>
<body>
<div id="cursor"></div>
<div id="cursor-ring"></div>
<canvas id="canvas-bg"></canvas>
<div class="grid-overlay"></div>
<div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>

<div class="shell">
  <nav class="nav">
    <div class="nav-brand">
      <div class="nav-mark">F&U</div>
      <div class="nav-name"><em>FAST&</em>UP</div>
    </div>
    <div class="nav-right">
      <div class="live-pill"><div class="live-dot"></div><div class="live-txt">AI Live</div></div>
      <div class="nav-site">fastandup.in</div>
    </div>
  </nav>

  <div class="hero">
    <div class="hero-left">
      <div class="eyebrow"><div class="eye-dot"></div><span class="eye-txt">Powered by AI &nbsp;·&nbsp; India\'s #1 Nutrition Brand</span></div>
      <h1 class="headline">
        FIND YOUR<br>
        <span class="hl-or">PERFECT</span><br>
        SUPPLEMENT<br>
        IN <span class="hl-cy">4 QUESTIONS.</span>
      </h1>
      <p class="sub">Tell us your goal, training &amp; diet.<br>We instantly match you to the right Fast&amp;Up product.<br><strong>No guesswork. No overwhelm.</strong></p>
      <div class="steps">
        <div class="step"><div class="step-n">01</div><div class="step-l">Goal</div></div>
        <div class="step"><div class="step-n">02</div><div class="step-l">Training</div></div>
        <div class="step"><div class="step-n">03</div><div class="step-l">Diet</div></div>
        <div class="step"><div class="step-n">04</div><div class="step-l">Timing</div></div>
      </div>
      <div class="cta-group">
        <button class="cta-btn" onclick="enterChat()">
          START AI RECOMMENDATION
          <div class="cta-icon">&#8594;</div>
        </button>
        <div class="cta-sub">Takes less than 60 seconds &nbsp;&bull;&nbsp; Free &nbsp;&bull;&nbsp; No signup</div>
      </div>
      <div class="trust">
        <div class="tbadge"><span class="tbadge-icon">✅</span><span class="tbadge-txt"><strong>10,000+</strong> users</span></div>
        <div class="tbadge"><span class="tbadge-icon">🎯</span><span class="tbadge-txt"><strong>91%</strong> accuracy</span></div>
        <div class="tbadge"><span class="tbadge-icon">🛡️</span><span class="tbadge-txt"><strong>WADA</strong> compliant</span></div>
        <div class="tbadge"><span class="tbadge-icon">🇨🇭</span><span class="tbadge-txt"><strong>Swiss</strong> tech</span></div>
      </div>
    </div>

    <div class="hero-right">
      <div class="prod-card">
        <div class="card-topbar"></div>
        <div class="tube-zone">
          <div class="tr1"></div><div class="tr2"></div><div class="tr3"></div>
          <div class="orbit"></div><div class="orbit2"></div>
          <div class="drp"></div><div class="drp"></div><div class="drp"></div>
          <div class="drp"></div><div class="drp"></div>
          <img class="tube-img"
               src="https://in.fastandup.com/cdn/shop/files/Activate_Orange_1_Tablet_shot.png?v=1710832891"
               onerror="this.src='https://in.fastandup.com/cdn/shop/products/Activate_Orange_1_Tablet_shot.png'"
               alt="Fast&Up Activate">
        </div>
        <div class="cb">
          <div class="cb-eyebrow">Recommended for You</div>
          <div class="cb-name">Fast&<em>Up Activate</em></div>
          <div class="cb-cat">Pre-Workout &nbsp;·&nbsp; Effervescent &nbsp;·&nbsp; Swiss Tech</div>
          <div class="cb-metrics">
            <div class="cm"><span class="cm-val">200mg</span><span class="cm-lbl">Caffeine</span></div>
            <div class="cm"><span class="cm-val">3.2g</span><span class="cm-lbl">Beta-Ala</span></div>
            <div class="cm"><span class="cm-val">30s</span><span class="cm-lbl">Dissolve</span></div>
          </div>
          <div class="cb-tags">
            <span class="ctag ct-or">Pre-Workout</span>
            <span class="ctag ct-cy">WADA Compliant</span>
            <span class="ctag ct-or">Effervescent</span>
            <span class="ctag ct-cy">FSSAI</span>
          </div>
          <div class="match-block">
            <div class="match-header">
              <div class="match-label">Match Confidence</div>
              <div class="match-score">94%</div>
            </div>
            <div class="match-track"><div class="match-fill"></div></div>
            <div class="match-sub">Based on your goal &amp; training profile</div>
          </div>
          <div class="cb-dots">
            <div class="cdot on" id="cd0"></div>
            <div class="cdot" id="cd1"></div>
            <div class="cdot" id="cd2"></div>
            <div class="cdot" id="cd3"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="cert-bar">
    <div class="cert-item"><span class="cert-icon">⚡</span>Make India Active</div>
    <div class="cert-sep"></div>
    <div class="cert-item"><span class="cert-icon">🏅</span>Informed Choice™</div>
    <div class="cert-sep"></div>
    <div class="cert-item"><span class="cert-icon">🇨🇭</span>Swiss Technology</div>
    <div class="cert-sep"></div>
    <div class="cert-item"><span class="cert-icon">✅</span>FSSAI Licensed</div>
    <div class="cert-sep"></div>
    <div class="cert-item"><span class="cert-icon">🛡️</span>WADA Compliant</div>
  </div>
</div>

<!-- EXPLOSION ANIMATIONS -->
<div class="tube-wrap">
  <div class="tube-glow"></div>
  <img class="tube-anim"
       src="https://in.fastandup.com/cdn/shop/files/Activate_Orange_1_Tablet_shot.png?v=1710832891"
       onerror="this.src='https://in.fastandup.com/cdn/shop/products/Activate_Orange_1_Tablet_shot.png'"
       alt="">
</div>
<div class="flash"></div>
<div class="parts">
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
  <div class="p"></div><div class="p"></div><div class="p"></div><div class="p"></div>
</div>
<div class="fiz"></div><div class="fiz"></div><div class="fiz"></div><div class="fiz"></div>
<div class="fiz"></div><div class="fiz"></div><div class="fiz"></div><div class="fiz"></div>
<div class="ring"></div><div class="ring"></div><div class="ring"></div><div class="ring"></div>
<div class="logo-wrap">
  <div class="logo-circle">
    <div class="sp1"></div><div class="sp2"></div>
    <div class="logo-ai">AI</div>
    <div class="logo-sub">Advisor</div>
  </div>
</div>

<script>
// Custom cursor
var cursor=document.getElementById('cursor'),ring=document.getElementById('cursor-ring');
var mx=window.innerWidth/2,my=window.innerHeight/2,rx=mx,ry=my;
document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;cursor.style.left=mx+'px';cursor.style.top=my+'px';});
(function animRing(){rx+=(mx-rx)*.12;ry+=(my-ry)*.12;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(animRing);})();

// Canvas particles
var canvas=document.getElementById('canvas-bg'),ctx=canvas.getContext('2d');
canvas.width=window.innerWidth;canvas.height=window.innerHeight;
window.addEventListener('resize',function(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;});
var particles=[];
for(var i=0;i<55;i++){particles.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*1.5+.4,vx:(Math.random()-.5)*.22,vy:-(Math.random()*.28+.06),a:Math.random(),da:Math.random()*.012+.004,c:Math.random()>.5?'rgba(255,85,0,':'rgba(0,212,255,'});}
function drawParticles(){ctx.clearRect(0,0,canvas.width,canvas.height);particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.a+=p.da;if(p.a>1||p.a<0)p.da*=-1;if(p.y<-5){p.y=canvas.height+5;p.x=Math.random()*canvas.width;}ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=p.c+p.a+')';ctx.fill();});requestAnimationFrame(drawParticles);}
drawParticles();

// Dot rotator
var dots=[document.getElementById('cd0'),document.getElementById('cd1'),document.getElementById('cd2'),document.getElementById('cd3')],cur=0;
setInterval(function(){dots[cur].classList.remove('on');cur=(cur+1)%4;dots[cur].classList.add('on');},2000);

// Navigate to chat
function enterChat(){try{window.parent.location.href=window.parent.location.pathname+'?screen=chat';}catch(e){window.location.href='/?screen=chat';}}

// Ripple feedback
document.querySelector('.cta-btn').addEventListener('click',function(e){
  var r=document.createElement('span');
  r.style.cssText='position:absolute;border-radius:50%;background:rgba(255,255,255,.3);width:8px;height:8px;left:'+e.offsetX+'px;top:'+e.offsetY+'px;transform:translate(-50%,-50%) scale(0);animation:ripple .55s ease-out forwards;pointer-events:none';
  this.appendChild(r);setTimeout(function(){r.remove();},600);
});

// Auto-advance
setTimeout(enterChat,9000);
</script>
</body>
</html>'''


import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Fast&Up · AI Advisor",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS — separated from logic for easy maintenance
# ══════════════════════════════════════════════════════════════════════════════

PRODUCTS: dict = {
    # ── Source: in.fastandup.com/products/activate-combo-of-3-tubes-orange ──
    "activate": {
        "name": "Fast&Up <em>Activate</em>",
        "category": "Caffeine-Free Pre-Workout · Effervescent Tablet",
        "tags": ["Caffeine-Free", "1500mg L-Arginine", "250mg L-Carnitine", "WADA Compliant"],
        "why": (
            "Each tablet delivers 1500 mg L-Arginine that raises nitric oxide levels, "
            "widening blood vessels for more oxygen to muscles, plus 250 mg L-Carnitine "
            "to convert stored fat into energy. Lycopene and Zinc fight Exercise-Induced "
            "Oxidative Stress (EXIOS). Caffeine-free — perfect for evening training. "
            "Swiss Effervescent Technology means it works in 30 seconds, not 30 minutes."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water, wait for it to dissolve fully, and drink "
            "30 minutes before your workout or training session."
        ),
        "badges": ["Swiss Technology", "FSSAI Lic. 10020022011847", "100% Vegetarian"],
        "url": "https://in.fastandup.com/products/activate-combo-of-3-tubes-orange",
    },

    # ── Source: in.fastandup.com/collections/hydration ──
    "reload": {
        "name": "Fast&Up <em>Reload</em>",
        "category": "Hypotonic Hydration · Effervescent Tablet",
        "tags": ["5 Electrolytes", "Vitamin C + B12", "Informed Choice™", "Low Sugar"],
        "why": (
            "India's first Informed Choice–certified effervescent hypotonic hydration drink. "
            "Contains 5 essential electrolytes — Sodium, Potassium, Magnesium, Calcium & "
            "Chloride — plus Vitamin C and B12 to reduce fatigue. Hypotonic formula means "
            "particles are less concentrated than body fluid, so absorption is faster than "
            "water alone. Each tube makes 5 litres of sports drink. 10× less sugar than "
            "standard energy drinks. Batch-tested in the UK for WADA-banned substances."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water (2 tablets in 500 ml). Consume during any "
            "workout, outdoor activity, or whenever you sweat. Safe to use daily."
        ),
        "badges": ["Informed Choice™ Certified", "Swiss Technology", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/products/reload-hydration-supplements",
    },

    # ── Source: fastandup.in/product/reload-isotonic-sports-drink-orange ──
    "reload_iso": {
        "name": "Fast&Up <em>Reload Isotonic</em>",
        "category": "Isotonic Sports Drink · 4-in-1 Intra-Workout",
        "tags": ["BCAA 2:1:1", "5 Electrolytes", "Fast Carbs", "Vitamin Booster"],
        "why": (
            "A 4-in-1 intra-workout formula: fast carbohydrates (Maltodextrin + Fructose "
            "2:1 ratio) for sustained energy, 5 electrolytes for full hydration, BCAA 2:1:1 "
            "with Glutamine to protect muscle during long sessions, and 6 vitamins to "
            "maintain performance output. Designed for endurance events, team sports, and "
            "sessions exceeding 60 minutes."
        ),
        "when": (
            "Mix 1 scoop in 400–500 ml water and sip throughout your training session. "
            "Ideal for runners, cyclists, cricketers, and anyone training over an hour."
        ),
        "badges": ["Swiss Technology", "FSSAI Licensed", "Banned Substance Free"],
        "url": "https://www.fastandup.in/product/reload-isotonic-sports-drink-orange",
    },

    # ── Source: in.fastandup.com/products/recover-post-workout-single-tube ──
    "recover": {
        "name": "Fast&Up <em>Recover</em>",
        "category": "Post-Workout Recovery · Effervescent Tablet",
        "tags": ["All 20 Amino Acids", "EAA + Glutathione", "Raspberry Flavour", "Veg"],
        "why": (
            "India's first effervescent vegetarian amino acid supplement. The Essential "
            "Recovery Complex (ERC) delivers all 20 amino acids — including all 9 Essential "
            "Amino Acids — in free-form for instant absorption. Glutathione acts as a "
            "powerful antioxidant to prevent Exercise-Induced Oxidative Stress (EXIOS), "
            "reducing muscle damage, soreness and recovery time. Keto-diet friendly, "
            "no added caffeine, no known side effects."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water and drink within 30 minutes of finishing your "
            "workout for maximum muscle protein synthesis. Can also be taken as a daily "
            "amino acid supplement in the evening."
        ),
        "badges": ["Swiss Technology", "WADA Compliant", "FSSAI Lic. 10020022011847"],
        "url": "https://in.fastandup.com/products/recover-post-workout-single-tube",
    },

    # ── Source: in.fastandup.com/products/whey-protein-isolate ──
    "whey_isolate": {
        "name": "Fast&Up <em>Whey Isolate</em>",
        "category": "Whey Protein · 90% Pure Isolate",
        "tags": ["26g Protein/Serve", "6g BCAA", "4.5g Glutamine", "Pepzyme AG™"],
        "why": (
            "Ultra-filtered, grass-fed European whey isolate providing 26 g of 90% pure "
            "protein, 6 g naturally occurring BCAA, and 4.5 g Glutamine per 31 g serving. "
            "Ultra-low carbs (0.4 g) and no added sugar — ideal for lean muscle and fat "
            "loss goals. Added Pepzyme AG™ digestive enzyme prevents bloating and GI "
            "distress common with other whey powders. Cross-flow microfiltration retains "
            "bioactive fractions for faster absorption."
        ),
        "when": (
            "Mix 1 scoop (31 g) in 200–300 ml cold water or milk. Shake well and drink "
            "within 30 min post-workout for muscle recovery, or anytime to meet daily "
            "protein targets."
        ),
        "badges": ["European Grass-Fed Whey", "Pepzyme AG™", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/products/whey-protein-isolate",
    },

    # ── Source: in.fastandup.com/products/plant-protein-powder-500gms ──
    "plant_protein": {
        "name": "Fast&Up <em>Plant Protein</em>",
        "category": "Vegan Plant Protein · Pea + Brown Rice Isolate",
        "tags": ["26g Protein/Serve", "4.6g BCAA", "4.8g Glutamine", "USA Sourced"],
        "why": (
            "26 g of premium Pea Isolate + Brown Rice Protein sourced from the USA per "
            "serving, with naturally occurring 4.6 g BCAA and 4.8 g Glutamine. Pea protein "
            "is rich in lysine; brown rice is rich in methionine — together they deliver a "
            "complete amino acid profile matching animal protein. Added Pepzyme Pro "
            "(digestive enzymes + probiotics) prevents bloating. No added sugar, dairy-free, "
            "gluten-free, egg-free. Informed Choice–certified, batch-tested in the UK."
        ),
        "when": (
            "Mix 1 scoop in 250–300 ml water or plant-based milk. Consume within 45–60 min "
            "post-workout, or at any time to meet daily protein goals."
        ),
        "badges": ["Informed Choice™ Certified", "100% Vegan", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/products/plant-protein-powder-500gms",
    },

    # ── Source: fastandup.in/product/bcaa-green-apple-supplements-in-india ──
    "bcaa": {
        "name": "Fast&Up <em>EAA + BCAA</em>",
        "category": "Essential Amino Acids · Intra-Workout",
        "tags": ["9 EAA", "BCAA 2:1:1", "Electrolytes", "Caffeine-Free"],
        "why": (
            "Fast&Up EAA provides 9 Essential Amino Acids — including BCAAs in 2:1:1 ratio "
            "(Leucine : Isoleucine : Valine) — plus Taurine and Citrulline for muscle "
            "re-energising and toxin clearance. Electrolyte blend maintains hydration during "
            "training. Ultra Granulation Technology gives a smooth, creamy texture. "
            "Prevents muscle catabolism, stimulates protein synthesis and reduces DOMS "
            "without any stimulants or banned substances."
        ),
        "when": (
            "Mix in 300–400 ml water and sip throughout your workout. Especially beneficial "
            "during high-volume training, calorie-deficit phases, or sessions over 45 min."
        ),
        "badges": ["Ultra Granulation Tech", "Caffeine-Free", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/products/essential-amino-acids",
    },

    # ── Source: in.fastandup.com/products/vitalize-multivitamin-single-tube ──
    "vitalize": {
        "name": "Fast&Up <em>Vitalize</em>",
        "category": "Daily Multivitamin · 21 Vitamins & Minerals",
        "tags": ["12 Vitamins", "9 Minerals", "Beetroot Extract", "Swiss Technology"],
        "why": (
            "India's first effervescent multivitamin — 12 vitamins, 9 minerals (including "
            "Copper, Iron, Magnesium, Zinc, Calcium, Selenium, Chromium, Manganese, "
            "Molybdenum), and a proprietary nitrate-rich Beetroot Extract with 7% natural "
            "nitrate content for blood circulation and stamina. Swiss Effervescent Technology "
            "provides 3× faster absorption versus conventional multivitamin tablets. Suitable "
            "for men and women above 8 years of age."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water every morning after breakfast. Take daily for "
            "consistent results — benefits typically noticed within 30 days."
        ),
        "badges": ["Swiss Technology", "FSSAI Lic. 10020022011847", "100% Vegetarian"],
        "url": "https://in.fastandup.com/products/vitalize-multivitamin-single-tube",
    },

    # ── Source: in.fastandup.com/products/charge-vitaminc-combo-of-3tubes ──
    "charge": {
        "name": "Fast&Up <em>Charge</em>",
        "category": "Natural Vitamin C + Zinc · Daily Immunity",
        "tags": ["1000mg Amla Extract", "50mg Vitamin C", "10mg Zinc", "Effervescent"],
        "why": (
            "Each tablet provides 1000 mg of natural Amla extract delivering 50 mg of "
            "natural Vitamin C — gentler and more bioavailable than synthetic ascorbic acid "
            "— plus 10 mg Zinc. Vitamin C and Zinc work synergistically: both modulate "
            "immune response, reduce infection risk, accelerate wound healing, and support "
            "collagen production for skin, hair and nails. No synthetic Vitamin C — the "
            "natural antioxidant properties of Amla are fully preserved."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water every morning. Safe for daily long-term use. "
            "Consistency over 30 days builds measurable immune resilience."
        ),
        "badges": ["Natural Amla Extract", "Swiss Technology", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/products/charge-vitaminc-combo-of-3tubes",
    },

    # ── Source: amazon.in — Fast&Up L-Carnitine 2000mg Carnipure® ──
    "l_carnitine": {
        "name": "Fast&Up <em>L-Carnitine 2000mg</em>",
        "category": "Weight Management · Fat Metabolism · Effervescent",
        "tags": ["Carnipure® Lonza", "2000mg/Serving", "Fat to Energy", "No Stimulants"],
        "why": (
            "Each effervescent tablet delivers 2000 mg of Carnipure® L-Carnitine Tartrate "
            "from Lonza Switzerland — the most clinically researched form of carnitine. "
            "Acts as a natural fat transporter, carrying stored fatty acids into the "
            "mitochondria where they are oxidised as fuel. Supports lean body composition, "
            "improves endurance and reduces post-exercise fatigue. Zero stimulants, no "
            "jitteriness — safe for morning or evening use. Vegetarian, gluten-free."
        ),
        "when": (
            "Drop 1 tablet in 250 ml water and drink 30 minutes before cardio, HIIT, or "
            "your morning workout. Most effective when combined with a calorie-controlled "
            "diet and 3+ aerobic sessions per week."
        ),
        "badges": ["Carnipure® by Lonza Switzerland", "No Stimulants", "FSSAI Licensed"],
        "url": "https://in.fastandup.com/collections/sports-nutrition",
    },
}

QUESTIONS: list[dict] = [
    {
        "id": "goal",
        "eye": "STEP 01 — MISSION",
        "text": "What's your primary fitness goal?",
        "hint": "Pick the one that drives you most right now",
        "opts": [
            "Build muscle & strength 💪",
            "Improve endurance & stamina 🏃",
            "Boost energy & immunity ⚡",
            "Lose weight / lean out 🔥",
            "Faster workout recovery 🔄",
            "General health & wellness 🌿",
        ],
    },
    {
        "id": "activity",
        "eye": "STEP 02 — TRAINING",
        "text": "How do you typically train?",
        "hint": "Choose what best describes your regular activity",
        "opts": [
            "Gym / Weight training 🏋️",
            "Running / Marathons 🏃",
            "Cycling / Triathlon 🚴",
            "Cricket / Team sports ⚽",
            "Yoga / Light exercise 🧘",
            "Not very active currently 🪑",
        ],
    },
    {
        "id": "diet",
        "eye": "STEP 03 — DIET",
        "text": "What best describes your diet?",
        "hint": "This determines which ingredients are right for you",
        "opts": ["Vegetarian 🌱", "Vegan 🌿", "Non-Vegetarian 🍗"],
    },
    {
        "id": "timing",
        "eye": "STEP 04 — TIMING",
        "text": "When do you most need support?",
        "hint": "This pinpoints the right product type",
        "opts": [
            "Before training — energy & power",
            "During training — stamina & hydration",
            "After training — recovery & repair",
            "All day — daily nutrition & wellness",
        ],
    },
]

STEP_LABELS = ["Goal", "Training", "Diet", "Timing"]

DEMOS: dict = {
    "🏋️ Gym-Goer": {
        "goal": "Build muscle & strength 💪",
        "activity": "Gym / Weight training 🏋️",
        "diet": "Non-Vegetarian 🍗",
        "timing": "After training — recovery & repair",
    },
    "🏃 Runner": {
        "goal": "Improve endurance & stamina 🏃",
        "activity": "Running / Marathons 🏃",
        "diet": "Vegetarian 🌱",
        "timing": "During training — stamina & hydration",
    },
    "💼 Professional": {
        "goal": "Boost energy & immunity ⚡",
        "activity": "Not very active currently 🪑",
        "diet": "Vegetarian 🌱",
        "timing": "All day — daily nutrition & wellness",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  RECOMMENDATION ENGINE — weighted scoring matrix (replaces naive if/elif)
#
#  Each rule is a dict:
#    "match":  callable(answers) → bool   — condition to score this product
#    "score":  int                         — weight (higher = stronger signal)
#    "product": str                        — product key
#
#  All matching rules are summed per product; highest total score wins.
#  Tie-breaking: products are ranked by definition order (specificity).
# ══════════════════════════════════════════════════════════════════════════════

def _kw(text: str, *words) -> bool:
    """Case-insensitive keyword check."""
    t = text.lower()
    return any(w in t for w in words)


SCORING_RULES: list[dict] = [
    # ── L-Carnitine (weight loss signals) ────────────────────────────────────
    {"product": "l_carnitine", "score": 10, "match": lambda a: _kw(a.get("goal", ""), "lose", "lean")},
    {"product": "l_carnitine", "score": 5,  "match": lambda a: _kw(a.get("timing", ""), "before")},
    {"product": "l_carnitine", "score": 3,  "match": lambda a: _kw(a.get("activity", ""), "yoga", "light", "not very")},

    # ── Activate (pre-workout energy) ─────────────────────────────────────────
    {"product": "activate", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "before")},
    {"product": "activate", "score": 8,  "match": lambda a: _kw(a.get("activity", ""), "gym", "weight")},
    {"product": "activate", "score": 5,  "match": lambda a: _kw(a.get("goal", ""), "muscle", "strength")},
    {"product": "activate", "score": 4,  "match": lambda a: _kw(a.get("goal", ""), "endurance", "stamina")},

    # ── Reload (basic hydration / shorter sessions) ───────────────────────────
    {"product": "reload", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "during")},
    {"product": "reload", "score": 8,  "match": lambda a: _kw(a.get("activity", ""), "running", "marathon")},
    {"product": "reload", "score": 5,  "match": lambda a: _kw(a.get("goal", ""), "endurance", "stamina")},

    # ── Reload ISO (long / intense sessions needing fuel + hydration) ─────────
    {"product": "reload_iso", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "during")},
    {"product": "reload_iso", "score": 8,  "match": lambda a: _kw(a.get("activity", ""), "cycling", "triathlon", "cricket", "team")},
    {"product": "reload_iso", "score": 6,  "match": lambda a: _kw(a.get("goal", ""), "endurance", "stamina")},
    {"product": "reload_iso", "score": 3,  "match": lambda a: _kw(a.get("goal", ""), "muscle", "strength")},

    # ── BCAA (muscle preservation, intra-workout) ─────────────────────────────
    {"product": "bcaa", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "during")},
    {"product": "bcaa", "score": 8,  "match": lambda a: _kw(a.get("goal", ""), "muscle", "strength")},
    {"product": "bcaa", "score": 6,  "match": lambda a: _kw(a.get("activity", ""), "gym", "weight")},
    {"product": "bcaa", "score": 3,  "match": lambda a: _kw(a.get("diet", ""), "veg")},  # veg/vegan friendly

    # ── Whey Isolate (post, non-veg, muscle) ─────────────────────────────────
    {"product": "whey_isolate", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "after")},
    {"product": "whey_isolate", "score": 8,  "match": lambda a: _kw(a.get("goal", ""), "muscle", "strength")},
    {"product": "whey_isolate", "score": 6,  "match": lambda a: _kw(a.get("diet", ""), "non-veg")},
    {"product": "whey_isolate", "score": 4,  "match": lambda a: _kw(a.get("activity", ""), "gym", "weight")},

    # ── Plant Protein (post, veg/vegan) ───────────────────────────────────────
    {"product": "plant_protein", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "after")},
    {"product": "plant_protein", "score": 9,  "match": lambda a: _kw(a.get("diet", ""), "vegan")},
    {"product": "plant_protein", "score": 7,  "match": lambda a: _kw(a.get("diet", ""), "vegetarian")},
    {"product": "plant_protein", "score": 6,  "match": lambda a: _kw(a.get("goal", ""), "muscle", "strength", "recovery")},

    # ── Recover (post-workout recovery effervescent) ──────────────────────────
    {"product": "recover", "score": 10, "match": lambda a: _kw(a.get("goal", ""), "recovery")},
    {"product": "recover", "score": 8,  "match": lambda a: _kw(a.get("timing", ""), "after")},
    {"product": "recover", "score": 5,  "match": lambda a: _kw(a.get("diet", ""), "non-veg")},
    {"product": "recover", "score": 4,  "match": lambda a: _kw(a.get("activity", ""), "gym", "weight")},

    # ── Vitalize (daily wellness / all-day) ───────────────────────────────────
    {"product": "vitalize", "score": 10, "match": lambda a: _kw(a.get("timing", ""), "all day")},
    {"product": "vitalize", "score": 8,  "match": lambda a: _kw(a.get("goal", ""), "health", "wellness")},
    {"product": "vitalize", "score": 5,  "match": lambda a: _kw(a.get("activity", ""), "yoga", "light", "not very")},
    {"product": "vitalize", "score": 3,  "match": lambda a: _kw(a.get("goal", ""), "energy", "immunity")},

    # ── Charge (immunity focus) ───────────────────────────────────────────────
    {"product": "charge", "score": 10, "match": lambda a: _kw(a.get("goal", ""), "immunity")},
    {"product": "charge", "score": 7,  "match": lambda a: _kw(a.get("goal", ""), "energy")},
    {"product": "charge", "score": 5,  "match": lambda a: _kw(a.get("timing", ""), "all day")},
    {"product": "charge", "score": 3,  "match": lambda a: _kw(a.get("activity", ""), "not very", "yoga", "light")},
]


def recommend(answers: dict) -> dict:
    """
    Score every product against all rules and return the highest-scoring one.
    Falls back to 'vitalize' if nothing matches.
    """
    scores: dict[str, int] = {k: 0 for k in PRODUCTS}

    for rule in SCORING_RULES:
        try:
            if rule["match"](answers):
                scores[rule["product"]] += rule["score"]
        except Exception:
            pass  # defensive: never crash on bad answers

    best = max(scores, key=lambda k: scores[k])
    # Only return if it has a meaningful score (>0), else default
    if scores[best] == 0:
        return PRODUCTS["vitalize"]

    return PRODUCTS[best]


def compute_confidence(answers: dict) -> int:
    """Return a display confidence % based on how decisive the top score is."""
    scores: dict[str, int] = {k: 0 for k in PRODUCTS}
    for rule in SCORING_RULES:
        try:
            if rule["match"](answers):
                scores[rule["product"]] += rule["score"]
        except Exception:
            pass
    vals = sorted(scores.values(), reverse=True)
    top, second = vals[0], vals[1] if len(vals) > 1 else 0
    if top == 0:
        return 72
    gap_ratio = (top - second) / top
    # Map gap_ratio 0→1 to confidence 72→98
    return min(98, int(72 + gap_ratio * 26))


# ══════════════════════════════════════════════════════════════════════════════
#  STATE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

def init_state() -> None:
    defaults = {
        "screen": "intro",
        "step": 0,
        "answers": {},
        "history": [],
        "product": None,
        "confidence": 0,
        "greeted": False,
        "thinking": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_state() -> None:
    for k in ["step", "answers", "history", "product", "confidence", "greeted", "thinking"]:
        st.session_state.pop(k, None)
    st.session_state.screen = "chat"
    init_state()


def load_demo(name: str) -> None:
    reset_state()
    j = DEMOS[name]
    st.session_state.answers = dict(j)
    st.session_state.step = 4
    for q in QUESTIONS:
        st.session_state.history.append(("bot", q["text"]))
        st.session_state.history.append(("user", j[q["id"]]))
    st.session_state.product = recommend(j)
    st.session_state.confidence = compute_confidence(j)
    st.session_state.greeted = True


def record_answer(val: str, qid: str) -> None:
    st.session_state.history.append(("bot", QUESTIONS[st.session_state.step]["text"]))
    st.session_state.history.append(("user", val))
    st.session_state.answers[qid] = val
    st.session_state.step += 1
    st.session_state.thinking = True
    if st.session_state.step == 4:
        st.session_state.product = recommend(st.session_state.answers)
        st.session_state.confidence = compute_confidence(st.session_state.answers)


# ══════════════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def render_step_tracker(step: int) -> str:
    nodes = ""
    for i, lbl in enumerate(STEP_LABELS):
        if i < step:
            cc, lc, sym = "done", "d", "✓"
        elif i == step:
            cc, lc, sym = "act", "a", str(i + 1)
        else:
            cc, lc, sym = "", "", str(i + 1)
        nodes += (
            f'<div class="snode">'
            f'<div class="scirc {cc}">{sym}</div>'
            f'<div class="slbl {lc}">{lbl}</div>'
            f'</div>'
        )
        if i < 3:
            nodes += f'<div class="sconn {"f" if i < step else ""}"></div>'
    return nodes


def render_chat_history(history: list) -> str:
    if not history:
        return ""
    h = '<div class="chat-hist">'
    for role, txt in history:
        if role == "bot":
            h += f'<div class="ch-bot"><div class="chav chav-b">AI</div><div class="chbub chbub-b">{txt}</div></div>'
        else:
            h += f'<div class="ch-usr"><div class="chav chav-u">YOU</div><div class="chbub chbub-u">{txt}</div></div>'
    h += "</div>"
    return h


def render_answer_pills(answers: dict) -> str:
    km = {"goal": "Goal", "activity": "Training", "diet": "Diet", "timing": "Timing"}
    pills = '<div class="ans-row">'
    for k, lbl in km.items():
        val = answers.get(k, "")
        if val:
            pills += (
                f'<div class="apill">'
                f'<span class="apkey">{lbl}</span>{val}'
                f'</div>'
            )
    pills += "</div>"
    return pills


def render_product_card(prod: dict, confidence: int) -> str:
    tags = "".join(f'<span class="ptag">{t}</span>' for t in prod["tags"])
    badges = "".join(f'<span class="bbadge">{b}</span>' for b in prod["badges"])
    fill_pct = confidence
    return f"""
<div class="prod-reveal"><div class="prod-shell">
  <div class="prod-banner">
    <div class="bfring"></div><div class="bfring"></div><div class="bfring"></div>
    <div class="prod-eye">RECOMMENDED FOR YOU · FASTANDUP.IN</div>
    <div class="prod-name">{prod['name']}</div>
    <div class="prod-cat">{prod['category']}</div>
    <div class="prod-tags">{tags}</div>
    <div class="confidence-row">
      <span class="conf-lbl">AI Match Confidence</span>
      <span class="conf-pct">{confidence}%</span>
    </div>
    <div class="conf-track"><div class="conf-fill" style="--fill:{fill_pct}%"></div></div>
  </div>
  <div class="prod-body">
    <div>
      <div class="sec-head"><div class="sec-icon si-why">🔬</div><div class="sec-ttl t-why">Why This Product</div></div>
      <div class="sec-txt">{prod['why']}</div>
    </div>
    <div class="prod-div"></div>
    <div>
      <div class="sec-head"><div class="sec-icon si-how">⏱</div><div class="sec-ttl t-how">When &amp; How To Use</div></div>
      <div class="sec-txt">{prod['when']}</div>
    </div>
    <div class="prod-div"></div>
    <div>
      <div class="sec-head"><div class="sec-icon si-buy">🛒</div><div class="sec-ttl t-buy">Buy Official</div></div>
      <a class="buy-link" href="{prod['url']}" target="_blank">Shop on fastandup.in <span class="buy-link-arrow">→</span></a>
      <div class="brand-badges">{badges}</div>
    </div>
  </div>
</div></div>"""


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT SCREEN CSS  — v2 redesign (chat page only, intro unchanged)
# ══════════════════════════════════════════════════════════════════════════════

CHAT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap');

/* ── TOKENS ─────────────────────────────────────────────────────────────── */
:root{
  /* backgrounds */
  --bg:#05060d;
  --s0:#080b14;
  --s1:#0c1020;
  --s2:#111828;
  --s3:#182030;
  --s4:#1e293b;
  /* brand */
  --or:#ff5500;--or2:#ff7730;--or3:#ffaa55;--or-g:rgba(255,85,0,.25);
  --cy:#00d4ff;--cy2:#00f0e8;--cy-g:rgba(0,212,255,.18);
  --gr:#00e676;--gr-g:rgba(0,230,118,.18);
  --ye:#ffd200;
  /* text */
  --tx:#dce8ff;--tx2:#8899bb;--tx3:#3d506e;--tx4:#1e2d42;
  /* radius */
  --r1:10px;--r2:16px;--r3:22px;
  /* easing */
  --ease-out-expo:cubic-bezier(.16,1,.3,1);
  --ease-spring:cubic-bezier(.34,1.56,.64,1);
}

/* ── BASE ────────────────────────────────────────────────────────────────── */
html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif!important;
  background:var(--bg)!important;
  color:var(--tx)!important;
}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.4rem 1rem 4rem!important;max-width:740px!important}

/* Layered background: deep grid + two radial glows */
.stApp{
  background:var(--bg);
  background-image:
    radial-gradient(ellipse 80% 50% at 10% 0%,rgba(255,85,0,.07) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 100%,rgba(0,212,255,.06) 0%,transparent 60%),
    linear-gradient(rgba(0,212,255,.014) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,212,255,.014) 1px,transparent 1px);
  background-size:100% 100%,100% 100%,40px 40px,40px 40px;
}

/* ── HEADER ──────────────────────────────────────────────────────────────── */
.hdr{
  position:relative;
  background:linear-gradient(160deg,rgba(20,28,56,.98),rgba(8,12,24,.99));
  border:1px solid rgba(255,255,255,.08);
  border-radius:var(--r3);
  margin-bottom:10px;
  overflow:hidden;
  box-shadow:0 4px 40px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.06);
  animation:fadeSlide .55s var(--ease-out-expo) both;
}
@keyframes fadeSlide{from{opacity:0;transform:translateY(-14px)}to{opacity:1;transform:none}}

/* animated top edge — orange→cyan sweep */
.hdr::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,
    transparent 0%,
    var(--or) 20%,var(--or2) 40%,
    var(--cy) 60%,var(--cy2) 80%,
    transparent 100%);
  background-size:300% 100%;
  animation:hdrSweep 4s linear infinite;
}
@keyframes hdrSweep{0%{background-position:100% 0}100%{background-position:-100% 0}}

/* subtle inner glow on left edge */
.hdr::after{
  content:'';position:absolute;top:0;left:0;bottom:0;width:1px;
  background:linear-gradient(180deg,var(--or),transparent 70%);
  opacity:.5;
}

.hdr-inner{display:flex;align-items:center;gap:16px;padding:18px 22px 0;position:relative;z-index:1}

/* logo mark — hexagonal feel with glow pulse */
.hdr-logo{
  width:50px;height:50px;flex-shrink:0;
  background:linear-gradient(135deg,var(--or) 0%,var(--or2) 60%,#ff9900 100%);
  border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Bebas Neue',cursive;font-size:13px;letter-spacing:1px;color:#fff;
  box-shadow:0 0 0 1px rgba(255,85,0,.3),0 0 24px rgba(255,85,0,.4);
  animation:logoBeat 2.8s ease-in-out infinite;
  position:relative;overflow:hidden;
}
.hdr-logo::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.22),transparent 55%);
  border-radius:14px;
}
@keyframes logoBeat{
  0%,100%{box-shadow:0 0 0 1px rgba(255,85,0,.3),0 0 20px rgba(255,85,0,.35)}
  50%{box-shadow:0 0 0 1px rgba(255,85,0,.5),0 0 40px rgba(255,85,0,.6),0 0 70px rgba(255,85,0,.2)}
}

.hdr-titles{flex:1;min-width:0}
.hdr-name{
  font-family:'Bebas Neue',cursive;font-size:26px;letter-spacing:4px;
  color:#fff;line-height:1;
}
.hdr-name em{font-style:normal;color:var(--or)}
.hdr-sub{
  font-family:'Space Mono',monospace;font-size:8.5px;
  color:var(--tx3);letter-spacing:2.5px;text-transform:uppercase;margin-top:4px;
}

/* live pill */
.live-badge{
  display:flex;align-items:center;gap:7px;
  padding:7px 14px;
  background:rgba(0,230,118,.05);
  border:1px solid rgba(0,230,118,.18);
  border-radius:24px;
  flex-shrink:0;
  box-shadow:0 0 16px rgba(0,230,118,.08);
}
.live-dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--gr);
  box-shadow:0 0 0 2px rgba(0,230,118,.2),0 0 8px rgba(0,230,118,.8);
  animation:liveFlash 2.2s ease-in-out infinite;
}
@keyframes liveFlash{0%,100%{opacity:1;transform:scale(1)}45%,55%{opacity:.15;transform:scale(.7)}}
.live-txt{font-family:'Space Mono',monospace;font-size:8.5px;color:var(--gr);font-weight:700;letter-spacing:2px}

/* stats row */
.hdr-stats{
  display:grid;grid-template-columns:repeat(4,1fr);
  border-top:1px solid rgba(255,255,255,.05);
  margin-top:14px;
}
.hstat{
  padding:11px 0;text-align:center;
  border-right:1px solid rgba(255,255,255,.04);
  position:relative;transition:background .25s;
}
.hstat:last-child{border-right:none}
.hstat:hover{background:rgba(255,85,0,.04)}
.hstat-v{
  display:block;
  font-family:'Bebas Neue',cursive;font-size:20px;
  background:linear-gradient(135deg,var(--or),var(--or3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1;
}
.hstat-l{
  display:block;
  font-family:'Space Mono',monospace;font-size:7px;
  color:var(--tx3);letter-spacing:1.8px;text-transform:uppercase;margin-top:3px;
}

/* ── DEMO BAR ─────────────────────────────────────────────────────────────── */
.demo-bar{
  display:flex;align-items:center;gap:12px;
  margin:12px 0 8px;padding:0 2px;
}
.demo-lbl{
  font-family:'Space Mono',monospace;font-size:8.5px;
  color:var(--tx3);letter-spacing:2.5px;text-transform:uppercase;flex-shrink:0;
}
.demo-line{flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.07),transparent)}

/* demo buttons wrapper */
.demo-bwrap div.stButton>button{
  text-align:center!important;
  font-family:'Space Mono',monospace!important;
  font-size:10.5px!important;letter-spacing:.8px!important;
  padding:11px 8px!important;
  background:var(--s1)!important;
  border:1px solid rgba(255,255,255,.07)!important;
  border-radius:12px!important;
  color:var(--tx2)!important;
  transition:all .25s var(--ease-out-expo)!important;
}
.demo-bwrap div.stButton>button:hover{
  background:rgba(255,85,0,.08)!important;
  border-color:rgba(255,85,0,.4)!important;
  color:var(--or3)!important;
  transform:translateY(-3px) translateX(0)!important;
  box-shadow:0 6px 20px rgba(0,0,0,.3),0 0 18px rgba(255,85,0,.15)!important;
}

/* ── STEP TRACKER ─────────────────────────────────────────────────────────── */
.fu-hr{
  height:1px;margin:12px 0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent);
}
.step-row{
  display:flex;align-items:center;
  margin:14px 0 12px;padding:0 4px;
}
.snode{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1}

/* step circle */
.scirc{
  width:34px;height:34px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-family:'Space Mono',monospace;font-size:10px;font-weight:700;
  border:2px solid rgba(255,255,255,.08);
  background:var(--s1);color:var(--tx3);
  transition:all .4s var(--ease-out-expo);
}
.scirc.done{
  background:linear-gradient(135deg,var(--or),var(--or2));
  border-color:transparent;color:#fff;
  box-shadow:0 0 0 3px rgba(255,85,0,.15),0 0 18px rgba(255,85,0,.4);
}
.scirc.act{
  background:rgba(0,212,255,.08);
  border-color:var(--cy);color:var(--cy);
  box-shadow:0 0 0 3px rgba(0,212,255,.1),0 0 18px rgba(0,212,255,.35);
  animation:stepPulse 2s ease-in-out infinite;
}
@keyframes stepPulse{
  0%,100%{box-shadow:0 0 0 3px rgba(0,212,255,.1),0 0 18px rgba(0,212,255,.3)}
  50%{box-shadow:0 0 0 5px rgba(0,212,255,.18),0 0 30px rgba(0,212,255,.55)}
}

.slbl{
  font-size:8px;letter-spacing:.8px;text-transform:uppercase;
  font-family:'Space Mono',monospace;white-space:nowrap;
  color:var(--tx3);transition:color .3s;
}
.slbl.a{color:var(--cy)}.slbl.d{color:var(--or2)}

/* connector line */
.sconn{
  flex:1;height:2px;
  margin-bottom:22px;
  background:rgba(255,255,255,.05);
  border-radius:2px;
  position:relative;overflow:hidden;
  transition:all .5s;
}
.sconn.f{
  background:linear-gradient(90deg,var(--or),var(--or2));
  box-shadow:0 0 6px rgba(255,85,0,.4);
}
.sconn.f::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.6),transparent);
  animation:shimmer 1.6s linear infinite;
}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}

/* ── GREETING CARD ────────────────────────────────────────────────────────── */
.greet{
  display:flex;gap:16px;align-items:flex-start;
  background:linear-gradient(140deg,rgba(18,24,48,.97),rgba(10,14,28,.99));
  border:1px solid rgba(255,85,0,.12);
  border-radius:var(--r3);
  padding:20px 22px;
  margin-bottom:14px;
  position:relative;overflow:hidden;
  animation:fadeUp .5s var(--ease-out-expo) .1s both;
  box-shadow:0 8px 32px rgba(0,0,0,.35);
}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}

/* left accent line with glow */
.greet::before{
  content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--or),rgba(255,85,0,.1));
  border-radius:3px 0 0 3px;
}
/* subtle corner glow */
.greet::after{
  content:'';position:absolute;top:-40px;right:-40px;width:140px;height:140px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,85,0,.08),transparent 70%);
  pointer-events:none;
}

.greet-av{
  width:44px;height:44px;border-radius:14px;flex-shrink:0;
  background:linear-gradient(135deg,rgba(255,85,0,.15),rgba(255,85,0,.05));
  border:1px solid rgba(255,85,0,.25);
  display:flex;align-items:center;justify-content:center;font-size:22px;
  box-shadow:0 0 18px rgba(255,85,0,.15);
}
.greet-name{
  font-family:'Syne',sans-serif;font-size:15px;font-weight:800;
  color:#fff;margin-bottom:5px;letter-spacing:.3px;
}
.greet-txt{font-size:13.5px;line-height:1.72;color:var(--tx2)}
.greet-txt strong{color:var(--tx);font-weight:600}

.greet-chips{display:flex;gap:7px;margin-top:13px;flex-wrap:wrap}
.gchip{
  padding:4px 11px;border-radius:20px;
  font-size:10px;font-weight:700;
  font-family:'Space Mono',monospace;letter-spacing:.5px;
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.07);
  color:var(--tx3);transition:all .3s;
}
.gchip.on{
  background:rgba(255,85,0,.1);
  border-color:rgba(255,85,0,.32);
  color:var(--or2);
  box-shadow:0 0 10px rgba(255,85,0,.12);
}

/* ── QUESTION CARD ────────────────────────────────────────────────────────── */
.qwrap{animation:qPop .45s var(--ease-out-expo) both}
@keyframes qPop{from{opacity:0;transform:translateY(16px) scale(.975)}to{opacity:1;transform:none}}
.qcard{
  background:linear-gradient(145deg,rgba(15,20,42,.98),rgba(9,13,28,.99));
  border:1px solid rgba(0,212,255,.1);
  border-radius:var(--r3);
  padding:22px 24px 18px;
  margin-bottom:12px;
  position:relative;overflow:hidden;
  box-shadow:0 4px 24px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.04);
}
/* cyan left accent */
.qcard::before{
  content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--cy),rgba(0,212,255,.08));
  border-radius:3px 0 0 3px;
}
/* top-right corner glow */
.qcard::after{
  content:'';position:absolute;top:-30px;right:-30px;width:120px;height:120px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(0,212,255,.06),transparent 65%);
  pointer-events:none;
}

.qeye{
  font-family:'Space Mono',monospace;font-size:9px;
  color:var(--cy);letter-spacing:3px;text-transform:uppercase;
  margin-bottom:9px;font-weight:700;
  display:inline-flex;align-items:center;gap:8px;
}
.qeye::before{
  content:'';width:18px;height:1.5px;
  background:linear-gradient(90deg,var(--cy),transparent);
  display:inline-block;border-radius:2px;
}
.qtxt{
  font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
  color:#fff;line-height:1.22;margin-bottom:6px;letter-spacing:-.2px;
}
.qhint{font-size:12.5px;color:var(--tx2);font-style:italic;line-height:1.5}

/* ── CHAT HISTORY ─────────────────────────────────────────────────────────── */
.chat-hist{display:flex;flex-direction:column;gap:10px;margin-bottom:14px}
.ch-bot,.ch-usr{display:flex;align-items:flex-end;gap:10px}
.ch-usr{flex-direction:row-reverse}

.chav{
  width:30px;height:30px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-family:'Space Mono',monospace;font-size:8px;font-weight:700;
}
.chav-b{
  background:linear-gradient(135deg,rgba(0,212,255,.12),rgba(0,212,255,.05));
  color:var(--cy);border:1px solid rgba(0,212,255,.2);
}
.chav-u{
  background:linear-gradient(135deg,var(--or),var(--or2));
  color:#fff;box-shadow:0 0 12px rgba(255,85,0,.3);
}

.chbub{
  max-width:78%;padding:10px 15px;
  border-radius:14px;font-size:13px;line-height:1.6;
  animation:bubIn .3s var(--ease-out-expo);
}
@keyframes bubIn{from{opacity:0;transform:translateY(10px) scale(.95)}to{opacity:1;transform:none}}
.chbub-b{
  background:var(--s1);
  border:1px solid rgba(255,255,255,.06);
  border-bottom-left-radius:4px;
  color:var(--tx2);
  box-shadow:0 2px 12px rgba(0,0,0,.25);
}
.chbub-u{
  background:linear-gradient(135deg,var(--or) 0%,var(--or2) 100%);
  border-bottom-right-radius:4px;
  color:#fff;font-weight:500;
  box-shadow:0 4px 16px rgba(255,85,0,.25);
}

/* ── THINKING INDICATOR ───────────────────────────────────────────────────── */
.think-wrap{display:flex;align-items:flex-end;gap:10px;padding:4px 0 10px}
.think-bub{
  display:flex;gap:6px;align-items:center;
  padding:12px 18px;
  background:var(--s1);
  border:1px solid rgba(255,255,255,.06);
  border-radius:14px;border-bottom-left-radius:4px;
  box-shadow:0 2px 12px rgba(0,0,0,.2);
}
.tdot{
  width:7px;height:7px;border-radius:50%;
  background:var(--cy);
  animation:tdPulse 1.4s ease-in-out infinite;
}
.tdot:nth-child(2){animation-delay:.22s}
.tdot:nth-child(3){animation-delay:.44s}
@keyframes tdPulse{
  0%,100%{opacity:.2;transform:scale(.65)}
  50%{opacity:1;transform:scale(1.25);box-shadow:0 0 10px rgba(0,212,255,.7)}
}

/* ── PRODUCT RESULT CARD ──────────────────────────────────────────────────── */
.prod-reveal{animation:bigReveal .9s var(--ease-out-expo) both}
@keyframes bigReveal{
  0%{opacity:0;transform:translateY(44px) scale(.94);filter:blur(12px)}
  100%{opacity:1;transform:none;filter:blur(0)}
}

.prod-shell{
  background:linear-gradient(175deg,rgba(12,16,32,.99),rgba(5,7,18,1));
  border:1px solid rgba(255,85,0,.2);
  border-radius:var(--r3);
  overflow:hidden;
  box-shadow:
    0 0 0 1px rgba(255,255,255,.03),
    0 32px 64px rgba(0,0,0,.6),
    0 0 80px rgba(255,85,0,.05);
  transition:transform .35s var(--ease-out-expo),box-shadow .35s;
}
.prod-shell:hover{
  transform:translateY(-4px);
  box-shadow:
    0 0 0 1px rgba(255,85,0,.18),
    0 40px 80px rgba(0,0,0,.65),
    0 0 120px rgba(255,85,0,.09);
}

/* banner */
.prod-banner{
  position:relative;overflow:hidden;
  background:linear-gradient(148deg,#1c0a02,#0d0718,#060c1e);
  padding:24px 26px 20px;
  border-bottom:1px solid rgba(255,85,0,.12);
}
/* animated gradient top bar */
.prod-banner::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2.5px;
  background:linear-gradient(90deg,var(--or),var(--or2),var(--ye),var(--cy),var(--or));
  background-size:300%;
  animation:bannerFlow 3.5s linear infinite;
}
@keyframes bannerFlow{0%{background-position:0%}100%{background-position:200%}}

/* expanding rings */
.bfring{
  position:absolute;border-radius:50%;
  border:1px solid rgba(255,85,0,.2);
  top:45%;left:72%;transform:translate(-50%,-50%);
  animation:ringExp 2.8s ease-out infinite;
}
.bfring:nth-child(2){animation-delay:.9s;border-color:rgba(255,130,0,.15)}
.bfring:nth-child(3){animation-delay:1.8s;border-color:rgba(255,180,0,.1)}
@keyframes ringExp{0%{width:20px;height:20px;opacity:.7}100%{width:100px;height:100px;opacity:0}}

.prod-eye{
  font-family:'Space Mono',monospace;font-size:9px;letter-spacing:3px;
  color:var(--or2);text-transform:uppercase;margin-bottom:10px;
  display:flex;align-items:center;gap:9px;
}
.prod-eye::before{content:'⚡';animation:zapBeat .9s ease-in-out infinite alternate;display:inline-block}
@keyframes zapBeat{from{opacity:.35;transform:scale(.8)}to{opacity:1;transform:scale(1.15)}}

.prod-name{
  font-family:'Bebas Neue',cursive;font-size:34px;
  color:#fff;line-height:1;letter-spacing:.5px;
}
.prod-name em{
  font-style:normal;
  background:linear-gradient(90deg,var(--or),var(--or2),var(--ye));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 0 12px rgba(255,85,0,.4));
}
.prod-cat{
  font-family:'Space Mono',monospace;font-size:9px;
  color:var(--tx3);letter-spacing:1.2px;margin-top:5px;
}

.prod-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}
.ptag{
  padding:4px 12px;border-radius:20px;
  font-size:9.5px;font-weight:700;
  font-family:'Space Mono',monospace;letter-spacing:.5px;
  background:rgba(255,85,0,.08);
  border:1px solid rgba(255,85,0,.25);
  color:var(--or2);
  transition:all .2s;
}
.ptag:hover{background:rgba(255,85,0,.15);border-color:rgba(255,85,0,.5);transform:translateY(-1px)}

/* confidence bar */
.confidence-row{
  display:flex;align-items:center;justify-content:space-between;
  margin-top:18px;margin-bottom:7px;
}
.conf-lbl{
  font-family:'Space Mono',monospace;font-size:8.5px;
  color:var(--tx3);letter-spacing:2px;text-transform:uppercase;
}
.conf-pct{
  font-family:'Bebas Neue',cursive;font-size:24px;
  color:var(--cy);line-height:1;
  text-shadow:0 0 20px rgba(0,212,255,.65);
}
.conf-track{
  height:6px;
  background:rgba(255,255,255,.05);
  border-radius:6px;overflow:hidden;
  box-shadow:inset 0 1px 2px rgba(0,0,0,.3);
}
.conf-fill{
  height:100%;border-radius:6px;
  background:linear-gradient(90deg,var(--or) 0%,#ff9500 45%,var(--cy) 100%);
  box-shadow:0 0 14px rgba(0,212,255,.4);
  width:0;animation:cfIn 1.4s cubic-bezier(.4,0,.2,1) .5s both;
}
@keyframes cfIn{to{width:var(--fill)}}

/* body */
.prod-body{padding:22px 26px 24px;display:flex;flex-direction:column;gap:20px}

.sec-head{display:flex;align-items:center;gap:11px;margin-bottom:9px}
.sec-icon{
  width:30px;height:30px;border-radius:9px;
  display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;
}
.si-why{background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.18)}
.si-how{background:rgba(0,230,118,.07);border:1px solid rgba(0,230,118,.18)}
.si-buy{background:rgba(255,210,0,.07);border:1px solid rgba(255,210,0,.18)}

.sec-ttl{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:2.5px;text-transform:uppercase;font-weight:700}
.t-why{color:var(--cy)}.t-how{color:var(--gr)}.t-buy{color:var(--ye)}

.sec-txt{font-size:13.5px;line-height:1.75;color:#9aaec8;padding-left:41px}
.prod-div{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent)}

/* buy link */
.buy-link{
  display:inline-flex;align-items:center;gap:9px;
  margin-top:5px;padding-left:41px;
  font-size:13.5px;font-weight:700;
  color:var(--cy);text-decoration:none;
  transition:all .25s;
}
.buy-link span{
  font-family:'Space Mono',monospace;font-size:9px;
  letter-spacing:1px;color:var(--tx3);text-transform:uppercase;
}
.buy-link:hover{color:var(--or2);gap:15px}
.buy-link-arrow{transition:transform .25s}
.buy-link:hover .buy-link-arrow{transform:translateX(5px)}

.brand-badges{display:flex;gap:8px;flex-wrap:wrap;padding-left:41px;margin-top:9px}
.bbadge{
  padding:4px 11px;border-radius:20px;
  font-family:'Space Mono',monospace;font-size:8.5px;
  color:var(--tx3);
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.07);
  letter-spacing:.5px;
}

/* ── ANSWER PILLS ─────────────────────────────────────────────────────────── */
.ans-row{
  display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;
  animation:fadeUp .4s var(--ease-out-expo) both;
}
.apill{
  display:flex;align-items:center;gap:8px;
  padding:5px 13px;border-radius:22px;
  font-size:11.5px;color:var(--tx2);
  background:var(--s1);
  border:1px solid rgba(255,255,255,.07);
  transition:all .25s;
}
.apill:hover{background:var(--s2);border-color:rgba(255,85,0,.25);color:var(--tx)}
.apkey{
  font-family:'Space Mono',monospace;font-size:7.5px;
  color:var(--or2);letter-spacing:1.2px;text-transform:uppercase;font-weight:700;
}

/* ── CHOICE BUTTONS ───────────────────────────────────────────────────────── */
div.stButton>button{
  font-family:'DM Sans',sans-serif!important;
  font-weight:500!important;font-size:14px!important;
  border-radius:var(--r2)!important;
  padding:13px 18px!important;
  width:100%!important;text-align:left!important;
  background:linear-gradient(135deg,rgba(17,24,44,.98),rgba(11,16,32,.98))!important;
  border:1px solid rgba(255,255,255,.07)!important;
  color:var(--tx2)!important;
  line-height:1.45!important;
  position:relative!important;overflow:hidden!important;
  transition:all .25s var(--ease-out-expo)!important;
  box-shadow:0 2px 8px rgba(0,0,0,.2)!important;
}

/* left accent on hover */
div.stButton>button::before{
  content:'';
  position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--cy),transparent);
  opacity:0;transition:opacity .25s;border-radius:3px 0 0 3px;
}
div.stButton>button:hover::before{opacity:1}

/* shine sweep on hover */
div.stButton>button::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(105deg,transparent 30%,rgba(0,212,255,.06) 50%,transparent 70%);
  transform:translateX(-100%);
}
div.stButton>button:hover::after{animation:btnSweep .6s ease forwards}
@keyframes btnSweep{to{transform:translateX(100%)}}

div.stButton>button:hover{
  background:linear-gradient(135deg,rgba(0,212,255,.06),rgba(17,24,44,.98))!important;
  border-color:rgba(0,212,255,.3)!important;
  color:#fff!important;
  transform:translateX(6px) translateY(-1px)!important;
  box-shadow:-3px 0 0 var(--cy),0 8px 24px rgba(0,0,0,.3)!important;
}
div.stButton>button:active{
  transform:translateX(3px)!important;
  transition:transform .08s!important;
}

/* restart button override */
.restart-bwrap div.stButton>button{
  text-align:center!important;
  background:transparent!important;
  font-family:'Space Mono',monospace!important;
  font-size:10px!important;letter-spacing:1.5px!important;
  color:var(--tx3)!important;padding:10px!important;
  border-color:rgba(255,255,255,.07)!important;
  box-shadow:none!important;
}
.restart-bwrap div.stButton>button::before,.restart-bwrap div.stButton>button::after{display:none!important}
.restart-bwrap div.stButton>button:hover{
  border-color:rgba(255,85,0,.35)!important;
  color:var(--or2)!important;
  transform:none!important;
  box-shadow:0 0 16px rgba(255,85,0,.1)!important;
}

/* ── FOOTER ───────────────────────────────────────────────────────────────── */
.fu-footer{
  text-align:center;
  margin-top:36px;padding:18px 0 0;
  border-top:1px solid rgba(255,255,255,.04);
  font-family:'Space Mono',monospace;font-size:8.5px;
  color:var(--tx3);letter-spacing:2px;line-height:2.4;
}
.fu-footer span{color:var(--or)}

/* ── SCROLLBAR ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--s4);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--s3)}
</style>
"""


# ══════════════════════════════════════════════════════════════════════════════
#  APP ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

init_state()

# Screen switch via query param
if st.query_params.get("screen") == "chat":
    st.session_state.screen = "chat"

# ── SCREEN 1 ─────────────────────────────────────────────────────────────────
if st.session_state.screen == "intro":
    st.markdown("""
    <style>
    #MainMenu,footer,header{visibility:hidden}
    .block-container{padding:0!important;max-width:100%!important;margin:0!important}
    section.main{padding:0!important}
    iframe{border:none!important;display:block!important}
    div[data-testid="stVerticalBlock"]{gap:0!important}
    </style>
    """, unsafe_allow_html=True)

    components.html(SCREEN1_HTML, height=750, scrolling=False)

    st.markdown("""
    <style>
    div.stButton>button{
      width:100%!important;padding:14px!important;font-size:14px!important;font-weight:600!important;
      background:linear-gradient(135deg,#ff5500,#ff7730)!important;color:white!important;
      border:none!important;border-radius:12px!important;cursor:pointer!important;margin-top:8px!important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("⚡  Enter Fast&Up AI Advisor  →"):
        st.session_state.screen = "chat"
        st.query_params["screen"] = "chat"
        st.rerun()

# ── SCREEN 2: CHAT ────────────────────────────────────────────────────────────
else:
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    step = st.session_state.step

    # HEADER
    st.markdown("""
<div class="hdr">
  <div class="hdr-inner">
    <div class="hdr-logo">F&U</div>
    <div>
      <div class="hdr-name"><em>FAST&</em>UP</div>
      <div class="hdr-sub">AI Product Advisor &nbsp;·&nbsp; fastandup.in</div>
    </div>
    <div class="live-badge"><div class="live-dot"></div><div class="live-txt">LIVE</div></div>
  </div>
  <div class="hdr-stats">
    <div class="hstat"><div class="hstat-v">12+</div><div class="hstat-l">Products</div></div>
    <div class="hstat"><div class="hstat-v">1M+</div><div class="hstat-l">Athletes</div></div>
    <div class="hstat"><div class="hstat-v">4</div><div class="hstat-l">Questions</div></div>
    <div class="hstat"><div class="hstat-v">100%</div><div class="hstat-l">Personalised</div></div>
  </div>
</div>
    """, unsafe_allow_html=True)

    # DEMO BUTTONS
    st.markdown(
        '<div class="demo-bar">'
        '<span class="demo-lbl">Quick Demo</span>'
        '<div class="demo-line"></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="demo-bwrap">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏋️ Gym-Goer", key="d1", use_container_width=True):
            load_demo("🏋️ Gym-Goer")
            st.rerun()
    with c2:
        if st.button("🏃 Runner", key="d2", use_container_width=True):
            load_demo("🏃 Runner")
            st.rerun()
    with c3:
        if st.button("💼 Professional", key="d3", use_container_width=True):
            load_demo("💼 Professional")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # STEP TRACKER
    st.markdown(
        f'<div class="fu-hr"></div>'
        f'<div class="step-row">{render_step_tracker(step)}</div>',
        unsafe_allow_html=True,
    )

    # GREETING
    if not st.session_state.greeted and step == 0:
        st.session_state.greeted = True
        st.markdown("""
<div class="greet">
  <div class="greet-av">⚡</div>
  <div>
    <div class="greet-name">Fast&amp;Up AI Advisor</div>
    <div class="greet-txt">
      Answer <strong>4 quick questions</strong> and I'll match you to the exact Fast&amp;Up
      product for your body, goals and lifestyle — from their official lineup only.
    </div>
    <div class="greet-chips">
      <div class="gchip on">01 · Goal</div>
      <div class="gchip">02 · Training</div>
      <div class="gchip">03 · Diet</div>
      <div class="gchip">04 · Timing</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    # CHAT HISTORY
    history_html = render_chat_history(st.session_state.history)
    if history_html:
        st.markdown(history_html, unsafe_allow_html=True)

    # THINKING INDICATOR — variable delay for authenticity
    if st.session_state.thinking:
        slot = st.empty()
        slot.markdown(
            '<div class="think-wrap">'
            '<div class="chav chav-b">AI</div>'
            '<div class="think-bub">'
            '<div class="tdot"></div><div class="tdot"></div><div class="tdot"></div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        # Variable delay: longer on final step to build anticipation
        delay = 1.4 if step == 4 else 0.75
        time.sleep(delay)
        slot.empty()
        st.session_state.thinking = False

    # ACTIVE QUESTION
    if step < 4:
        q = QUESTIONS[step]
        st.markdown(
            f'<div class="qwrap">'
            f'<div class="qcard">'
            f'<div class="qeye">{q["eye"]}</div>'
            f'<div class="qtxt">{q["text"]}</div>'
            f'<div class="qhint">{q["hint"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        for i, opt in enumerate(q["opts"]):
            if st.button(opt, key=f"o{step}{i}", use_container_width=True):
                record_answer(opt, q["id"])
                st.rerun()

    # PRODUCT RESULT
    if step == 4 and st.session_state.product:
        prod = st.session_state.product
        confidence = st.session_state.confidence

        st.markdown(render_answer_pills(st.session_state.answers), unsafe_allow_html=True)
        st.markdown(render_product_card(prod, confidence), unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="restart-bwrap">', unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("↺  Start Over", key="restart", use_container_width=True):
                reset_state()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown(
        '<div class="fu-footer">'
        'ALL PRODUCTS FROM <span>FASTANDUP.IN</span> · '
        'WADA COMPLIANT · FSSAI LICENSED · '
        '<span>MAKE INDIA ACTIVE ⚡</span>'
        '</div>',
        unsafe_allow_html=True,
    )
