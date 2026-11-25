// Captions: 1-3 words, crisp bold font (supports both Devanagari Hindi & English), white with thick ink outline, ONE yellow word.
import { ctx, C, clamp, lerp, seg, eob, HAS_DEVANAGARI, FONT_STACK } from './lib.js';
import { T, lineWords } from './timing.js';

export const CAP = { y: 1420, size: 132, maxW: 920 };
let caps = [];

function autoChunks(text) {
  const ws = String(text || '').trim().split(/\s+/).filter(Boolean), out = [];
  for (let i = 0; i < ws.length;) {
    const n = ws.length - i === 4 ? 2 : Math.min(3, ws.length - i);
    out.push(ws.slice(i, i + n));
    i += n;
  }
  return out.map((c) => {
    const k = c.reduce((b, w, j) => (w.replace(/[^\p{L}\p{N}]/gu, '').length > c[b].replace(/[^\p{L}\p{N}]/gu, '').length ? j : b), 0);
    return c.map((w, j) => (j === k ? '*' + w : w)).join(' ');
  });
}

export function buildCaptions(script) {
  caps = [];
  script.lines.forEach((ln, i) => {
    const chunks = (ln.caps ? ln.caps.split('|') : autoChunks(ln.text)).map((s) => s.trim()).filter(Boolean);
    const ws = lineWords(i);
    if (!ws.length) {
      // Fallback evenly spread across line duration
      const lineObj = T.lines[i];
      if (!lineObj) return;
      const d = (lineObj.end - lineObj.start) / Math.max(1, chunks.length);
      chunks.forEach((c, j) => {
        caps.push({
          line: i,
          s: lineObj.start + j * d - 0.04,
          words: c.split(/\s+/).map((w) => ({ txt: w.replace(/\*/g, ''), hi: w.includes('*') }))
        });
      });
      return;
    }
    const counts = chunks.map((c) => c.split(/\s+/).length), N = counts.reduce((a, b) => a + b, 0);
    const nm = (w) => String(w).toLowerCase().replace(/[^\p{L}\p{N}']+/gu, '');
    let acc = 0, from = 0;
    chunks.forEach((c, j) => {
      const first = nm(c.split(/\s+/)[0]);
      let idx = j === 0 ? 0 : ws.findIndex((w, k) => k > from && first && (nm(w.w) === first || (first.length > 2 && nm(w.w).startsWith(first))));
      if (idx < 0) idx = Math.max(from + (j ? 1 : 0), Math.min(ws.length - 1, Math.round(acc * ws.length / Math.max(1, N))));
      acc += counts[j]; from = idx;
      caps.push({ line: i, s: ws[idx].s - 0.05, words: c.split(/\s+/).map((w) => ({ txt: w.replace(/\*/g, ''), hi: w.includes('*') })) });
    });
  });
  caps.forEach((c, k) => {
    const next = caps[k + 1], lineEnd = T.lines[c.line].end;
    c.e = next ? (next.s - lineEnd > 0.7 && next.line !== c.line ? lineEnd + 0.35 : next.s) : T.dur;
  });
  return caps;
}
export const captionList = () => caps;

export function drawCaption(t) {
  const c = caps.find((c) => t >= c.s && t < c.e); if (!c) return;
  const lt = t - c.s;
  const fullStr = c.words.map((w) => w.txt).join(' ');
  const isHindi = HAS_DEVANAGARI(fullStr);
  const size = isHindi ? 104 : CAP.size;
  ctx.font = `900 ${size}px ${FONT_STACK}`;
  if (!isHindi) ctx.letterSpacing = '-2px';
  const sp = size * (isHindi ? 0.30 : 0.26);
  c.words.forEach((w) => (w.w = ctx.measureText(w.txt).width));
  const width = (ws) => ws.reduce((a, w) => a + w.w, 0) + sp * (ws.length - 1);
  let lines = [c.words];
  if (width(c.words) > CAP.maxW && c.words.length > 1) {
    let best = null;
    for (let i = 1; i < c.words.length; i++) {
      const a = c.words.slice(0, i), b = c.words.slice(i), m = Math.max(width(a), width(b));
      if (!best || m < best.m) best = { m, l: [a, b] };
    }
    lines = best.l;
  }
  const fit = Math.min(1, CAP.maxW / Math.max(1, ...lines.map(width)));
  const sc = (lt < 0.2 ? lerp(0.65, 1, eob(seg(lt, 0, 0.2))) : 1) * fit;
  ctx.save(); ctx.translate(540, CAP.y); ctx.scale(sc, sc);
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left'; ctx.lineJoin = 'round';
  const lh = size * (isHindi ? 1.25 : 1.0), y0 = -(lines.length - 1) * lh / 2;
  lines.forEach((ln, li) => {
    let x = -width(ln) / 2; const y = y0 + li * lh;
    for (const w of ln) {
      ctx.lineWidth = isHindi ? 24 : 30;
      ctx.strokeStyle = C.ink;
      ctx.strokeText(w.txt, x, y + 8);
      ctx.strokeText(w.txt, x, y);
      ctx.fillStyle = w.hi ? C.yellow : C.white;
      ctx.fillText(w.txt, x, y);
      x += w.w + sp;
    }
  });
  ctx.letterSpacing = '0px'; ctx.restore();
}
