// Zack Explainer Engine: canvas, palette, math and drawing primitives.
export const W = 1080, H = 1920, FPS = 30;
export let ctx = null;
export function setCtx(c) { ctx = c; }

export const C = {
  skin: '#E8B89A', pink: '#E57A8A', red: '#D62839', cyan: '#4FD1E8', yellow: '#FFD43B', bg: '#F4F1EA',
  pinkLight: '#F29AA7', pinkDark: '#C9566E', skinShade: '#D49C7E', navy: '#0E1A2B', xnavy: '#0B2238',
  hair: '#3B2A20', hairHi: '#5A4030', shirt: '#3A7BD5', shirtShade: '#2F67BE', pants: '#1F2A44', pantsShade: '#18213A',
  ink: '#1A1A1E', mouth: '#6B2A2A', gum: '#F7F4EE', gumEdge: '#C9C2B5', white: '#FFFFFF',
  stomachBg: '#B83A55', stomachBgDark: '#A3304A', stomachFold: '#D4637C', floor: '#E4DCCB', sky: '#BFE3F2',
  leaf: '#5BAE6A', pot: '#C8734A', watch: '#1E2A44', green: '#2ECC71',
};

export function setHeroTheme(theme = {}) {
  if (theme.skin) C.skin = theme.skin;
  if (theme.skinShade) C.skinShade = theme.skinShade;
  if (theme.hair) C.hair = theme.hair;
  if (theme.hairHi) C.hairHi = theme.hairHi;
  if (theme.shirt) C.shirt = theme.shirt;
  if (theme.shirtShade) C.shirtShade = theme.shirtShade;
  if (theme.pants) C.pants = theme.pants;
  if (theme.bg) C.bg = theme.bg;
}

export const HAS_DEVANAGARI = (txt) => /[\u0900-\u097F]/.test(String(txt || ''));
export const FONT_STACK = "'Noto Sans Devanagari', 'Nirmala UI', 'Kohinoor Devanagari', Inter, sans-serif";

// ---------- math ----------
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / ((b - a) || 1e-6));
export const eo = (t) => 1 - Math.pow(1 - t, 3);
export const eio = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const eob = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
export const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
export const TAU = Math.PI * 2;

// ---------- primitives ----------
export function rr(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
export function circle(x, y, r, fill) { ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fillStyle = fill; ctx.fill(); }
export function ell(x, y, rx, ry, fill, rot = 0) { ctx.beginPath(); ctx.ellipse(x, y, rx, ry, rot, 0, TAU); ctx.fillStyle = fill; ctx.fill(); }
export function line(pts, color, w) {
  ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
  ctx.strokeStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke();
}
export function fillAll(color) { ctx.fillStyle = color; ctx.fillRect(-300, -300, W + 600, H + 600); }
export function bigText(text, x, y, size, fill = C.white, rot = 0, sc = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc);
  const fSize = HAS_DEVANAGARI(text) ? Math.round(size * 0.85) : size;
  ctx.font = `900 ${fSize}px ${FONT_STACK}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.lineWidth = fSize * 0.2; ctx.strokeStyle = C.ink; ctx.strokeText(text, 0, 0); ctx.fillStyle = fill; ctx.fillText(text, 0, 0);
  ctx.restore();
}
