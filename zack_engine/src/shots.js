// Data-driven Zack Explainer shot compiler. Reads storyboard.json + script.json + timing.
import { ctx, W, H, C, clamp, lerp, seg, eo, eio, eob, circle, ell, rr, line, fillAll, bigText } from './core/lib.js';
import { L, T } from './core/timing.js';
import * as K from './core/kit.js';

export function buildShots(storyboard = {}) {
  const S = [], CUES = [];
  const add = (o) => (S.push(o), o);
  const cue = (t, type, o = {}) => CUES.push({ t: +Math.max(0, t).toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : Math.max(0, L(i) - 0.08));

  const lines = storyboard.lines || [];
  const totalLines = Math.max(1, T.lines ? T.lines.length : lines.length);

  for (let i = 0; i < totalLines; i++) {
    const st = cut(i);
    const meta = lines[i] || {};
    const scene = String(meta.scene || (i === 0 ? 'hook_shock' : i % 3 === 1 ? 'xray_lungs' : i % 3 === 2 ? 'blood_vessel' : 'xray_brain'));
    const pillTxt = meta.pill ? String(meta.pill) : '';
    const sfx = String(meta.sfx || (i === 0 ? 'pop' : 'whoosh'));

    if (i > 0) cue(st, 'whoosh', { gain: 0.7 });
    if (sfx && sfx !== 'whoosh') cue(st + 0.12, sfx, { gain: 0.75 });

    add({
      id: `S${String(i + 1).padStart(2, '0')}`,
      at: st,
      cam: scene === 'blood_vessel' || scene === 'cosmos' ? [540, 920] : [540, 760],
      zoom: scene === 'hook_shock' || scene === 'outro_twist' ? 0.09 : 0.07,
      note: `${scene}${pillTxt ? ' · ' + pillTxt : ''}`,
      draw(lt, d, t) {
        const p = clamp(lt / Math.max(0.2, d));
        if (scene === 'hook_shock') {
          K.room();
          const wave = Math.sin(lt * 5);
          K.man({
            x: 540, y: 1220, s: 1.55,
            eyes: lt > 0.25 ? 'wide' : 'n',
            mouth: lt > 0.3 ? 'o' : 'flat',
            brow: eo(seg(lt, 0.1, 0.45)),
            arm: K.armPose(K.ARM.down, K.ARM.mouth, eo(seg(lt, 0.2, 0.7))),
            armL: K.ARM.down,
            look: wave * 0.25
          });
          K.shockLines(540, 680, 220, seg(lt, 0.2, 0.5) * (1 - seg(lt, 0.9, 1.3)));
        } else if (scene === 'xray_lungs') {
          K.xray(t);
          K.man({ x: 540, y: 1120, s: 1.25, xray: true, eyes: 'wide', mouth: 'flat', pulse: 0.5 + 0.5 * Math.sin(lt * 5) });
          K.lungs(540, 1010, 0.82, 0.5 + 0.5 * Math.sin(lt * 4), p > 0.6 ? 0.6 : 0.1);
        } else if (scene === 'xray_heart') {
          K.xray(t);
          K.man({ x: 540, y: 1120, s: 1.3, xray: true, eyes: 'n', mouth: 'flat' });
          const beat = Math.pow(Math.abs(Math.sin(lt * 7.5)), 4);
          K.heart(570, 1015, 0.95, beat);
        } else if (scene === 'xray_brain') {
          K.xray(t);
          K.man({ x: 540, y: 1220, s: 1.5, xray: true, eyes: p > 0.5 ? 'wide' : 'n', mouth: 'flat' });
          K.brain(540, 620, 0.54, 0.5 + 0.5 * Math.sin(lt * 6), p);
        } else if (scene === 'xray_stomach') {
          K.insideStomach(t, 0.85);
          K.stomach(540, 820, 2.2, 0.5 + 0.5 * Math.sin(lt * 5));
        } else if (scene === 'blood_vessel') {
          K.bloodVessel(t, p);
        } else if (scene === 'myth_bust') {
          K.room();
          K.man({ x: 540, y: 1200, s: 1.35, eyes: 'wide', mouth: 'flat', brow: 0.9, arm: K.ARM.point, finger: Math.sin(lt * 11) * 0.25 });
          K.redX(540, 740, eob(seg(lt, 0.1, 0.45)) * 0.85, 0.95);
        } else if (scene === 'clock_pass') {
          K.room();
          K.stopwatch(540, 730, 1.35 * eob(seg(lt, 0, 0.35)), lt * 5.2);
          K.man({ x: 540, y: 1460, s: 1.1, eyes: 'closed', mouth: 'flat' });
        } else if (scene === 'cosmos' || scene === 'ocean_mystery') {
          K.cosmosBg(t, scene === 'ocean_mystery' ? '#0C5E8C' : '#E86A33');
          K.man({ x: 250, y: 1420, s: 0.72, eyes: 'wide', mouth: 'o', brow: 1 });
        } else {
          // outro_twist or default
          K.room();
          K.man({
            x: 540, y: 1180, s: 1.48,
            eyes: 'n', mouth: 'smirk', smirk: true, brow: 0.7,
            arm: K.ARM.point, finger: Math.sin(lt * 10) * 0.28
          });
          K.warning(840, 560, eob(seg(lt, 0.2, 0.55)) * 0.68);
        }

        if (pillTxt && !globalThis.__CLEAN_FRAME) {
          const popSc = eob(seg(lt, 0.15, 0.42));
          const bgCol = /ALARM|DANGER|STOP|NO|HIGH|DEAD|TOXIC/i.test(pillTxt) ? C.red : C.ink;
          K.pill(pillTxt, 540, 320, 52, bgCol, C.white, popSc);
        }
      }
    });
  }

  return { shots: S, cues: CUES };
}
