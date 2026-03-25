// ================================================================
// CONFIG — paste your Google Apps Script URL here
// ================================================================
const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzjKnNtWGyqyyrAjYtO6tn6zJRPYP4ctWZiHqAJYFHABKWVuYARoxyZcXUyVUhwO5m5/exec';

// ================================================================
// STATE
// ================================================================
let USER = { name: '', session: '' };
let localData = []; // offline fallback

// ================================================================
// BACKEND
// ================================================================
function send(paradox, action, value) {
    const entry = { session: USER.session, name: USER.name, paradox, action, value: String(value) };
    localData.push(entry);
    if (!SCRIPT_URL) return;
    fetch(SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify(entry)
    }).catch(() => {});
}

async function fetchData(session) {
    if (!SCRIPT_URL) return localData.filter(d => d.session === session);
    try {
        const r = await fetch(SCRIPT_URL + '?session=' + encodeURIComponent(session));
        return await r.json();
    } catch { return localData.filter(d => d.session === session); }
}

// ================================================================
// JOIN
// ================================================================
function joinSession() {
    const name = document.getElementById('inp-name').value.trim();
    const session = document.getElementById('inp-session').value.trim().toUpperCase();
    if (!name || !session) { document.getElementById('join-error').textContent = 'Please fill in both fields.'; return; }
    USER.name = name;
    USER.session = session;
    document.getElementById('join-screen').classList.add('hidden');
    document.getElementById('student-view').classList.remove('hidden');
    document.getElementById('user-badge').textContent = name;
    send('system', 'join', name);
    mhNew();
}

function openDashboard() {
    document.getElementById('join-screen').classList.add('hidden');
    document.getElementById('dash-join').classList.remove('hidden');
}

function startDashboard() {
    const session = document.getElementById('dash-session-input').value.trim().toUpperCase();
    if (!session) return;
    USER.session = session;
    document.getElementById('dash-join').classList.add('hidden');
    document.getElementById('dashboard-view').classList.remove('hidden');
    document.getElementById('dash-session').textContent = session;
    document.getElementById('dash-url').textContent = location.origin + location.pathname;
    refreshDashboard();
    setInterval(refreshDashboard, 5000);
}

// check URL params
(function() {
    const p = new URLSearchParams(location.search);
    if (p.has('dashboard')) {
        document.getElementById('join-screen').classList.add('hidden');
        if (p.get('session')) {
            document.getElementById('dash-session-input').value = p.get('session');
            document.getElementById('dash-join').classList.remove('hidden');
            startDashboard();
        } else {
            document.getElementById('dash-join').classList.remove('hidden');
        }
    }
})();

// ================================================================
// PARADOX I: BOY OR GIRL
// ================================================================
let bgRounds = [], bgRound = 0, bgCorrect = 0, bgBothCount = 0;
const BG_TOTAL = 20;

function bgGuess(val) {
    document.querySelectorAll('#bg-phase1 .choice-btn').forEach(b => {
        b.disabled = true;
        if (b.textContent === val) b.classList.add('selected');
        if (b.textContent === '1/3') b.classList.add('correct');
        if (b.textContent === val && val !== '1/3') b.classList.add('wrong');
    });
    send('boy_girl', 'guess', val);
    setTimeout(() => {
        document.getElementById('bg-phase2').classList.remove('hidden');
        bgGenerateRounds();
        bgShowRound();
    }, 1200);
}

function bgGenerateRounds() {
    bgRounds = [];
    while (bgRounds.length < BG_TOTAL) {
        const c1 = Math.random() < 0.5 ? 'M' : 'F';
        const c2 = Math.random() < 0.5 ? 'M' : 'F';
        if (c1 === 'M' || c2 === 'M') bgRounds.push([c1, c2]);
    }
}

function bgShowRound() {
    document.getElementById('bg-round').textContent = bgRound + 1;
    document.getElementById('bg-guess-btns').classList.remove('hidden');
    document.getElementById('bg-reveal').classList.add('hidden');
    document.getElementById('bg-next-btn').classList.add('hidden');
    document.getElementById('bg-family-icon').innerHTML = '&#128104;&#8205;&#128105;&#8205;&#128102;&#8205;&#10067;';
}

function bgRoundGuess(guessedBoth) {
    const [c1, c2] = bgRounds[bgRound];
    const actuallyBoth = c1 === 'M' && c2 === 'M';
    const correct = guessedBoth === actuallyBoth;
    if (correct) bgCorrect++;
    if (actuallyBoth) bgBothCount++;

    document.getElementById('bg-guess-btns').classList.add('hidden');
    const reveal = document.getElementById('bg-reveal');
    reveal.classList.remove('hidden', 'correct', 'wrong');

    const childStr = (c) => c === 'M' ? '&#128102; Boy' : '&#128103; Girl';
    const icon = c1 === 'M' && c2 === 'M' ? '&#128102;&#128102;' : c1 === 'F' && c2 === 'F' ? '&#128103;&#128103;' : '&#128102;&#128103;';
    document.getElementById('bg-family-icon').innerHTML = icon;

    reveal.classList.add(correct ? 'correct' : 'wrong');
    reveal.innerHTML = `${childStr(c1)} + ${childStr(c2)} &mdash; ${actuallyBoth ? 'BOTH BOYS!' : 'Not both boys.'} &mdash; You were <strong>${correct ? 'RIGHT' : 'WRONG'}</strong>`;

    document.getElementById('bg-score').textContent = bgCorrect;
    document.getElementById('bg-bothcount').textContent = bgBothCount;

    bgRound++;
    if (bgRound < BG_TOTAL) {
        document.getElementById('bg-next-btn').classList.remove('hidden');
    } else {
        send('boy_girl', 'game_result', JSON.stringify({ correct: bgCorrect, bothSeen: bgBothCount, total: BG_TOTAL }));
        setTimeout(bgShowResults, 1000);
    }
}

function bgNextRound() { bgShowRound(); }

function bgShowResults() {
    document.getElementById('bg-phase2').classList.add('hidden');
    document.getElementById('bg-phase3').classList.remove('hidden');
    const rate = (bgBothCount / BG_TOTAL * 100).toFixed(1);
    document.getElementById('bg-final-rate').textContent = rate + '%';
    document.getElementById('bg-results-text').textContent =
        `You guessed correctly ${bgCorrect}/${BG_TOTAL} times. "Both boys" appeared ${bgBothCount}/${BG_TOTAL} times (${rate}%).`;
}

// ================================================================
// PARADOX II: BIRTHDAY
// ================================================================
let bdGuessed = false, bdSubmitted = false;

function bdSubmitGuess() {
    const v = document.getElementById('bd-guess-input').value;
    if (!v) return;
    send('birthday', 'guess', v);
    bdGuessed = true;
    document.getElementById('bd-phase1').innerHTML = `<div class="result-box success text-center"><strong>Your guess: ${v} people.</strong> The answer is just <strong>23</strong>! Let's check with the class...</div>`;
    document.getElementById('bd-phase2').classList.remove('hidden');
}

function bdSubmitBirthday() {
    const inp = document.getElementById('bd-date-input');
    if (!inp.value) return;
    const d = new Date(inp.value);
    const mmdd = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
    send('birthday', 'birthday', mmdd);
    bdSubmitted = true;
    document.getElementById('bd-phase2').innerHTML = `<div class="result-box success text-center"><strong>Birthday submitted!</strong> (${mmdd}) Watch the board below as classmates add theirs.</div>`;
    document.getElementById('bd-phase3').classList.remove('hidden');
    bdPollBoard();
}

function bdPollBoard() {
    setInterval(async () => {
        const data = await fetchData(USER.session);
        const bdays = data.filter(d => d.paradox === 'birthday' && d.action === 'birthday');
        renderBdBoard(bdays);
    }, 4000);
}

function renderBdBoard(entries) {
    const board = document.getElementById('bd-board');
    const counts = {};
    entries.forEach(e => {
        const v = e.value;
        counts[v] = counts[v] || [];
        counts[v].push(e.name);
    });
    const dupes = Object.keys(counts).filter(k => counts[k].length > 1);
    board.innerHTML = entries.map(e => {
        const isMatch = dupes.includes(e.value);
        return `<span class="bd-tag ${isMatch ? 'match' : ''}">${e.name}: ${e.value}</span>`;
    }).join('');
    document.getElementById('bd-count').textContent = entries.length;

    const n = entries.length;
    let p = 1;
    for (let i = 0; i < Math.min(n, 365); i++) p *= (365 - i) / 365;
    document.getElementById('bd-theory-n').textContent = n;
    document.getElementById('bd-theory-p').textContent = ((1 - p) * 100).toFixed(1);

    const matchMsg = document.getElementById('bd-match-msg');
    if (dupes.length > 0) {
        matchMsg.classList.remove('hidden');
        matchMsg.className = 'result-box success';
        matchMsg.innerHTML = '<strong>Match found!</strong> ' + dupes.map(d => `<strong>${d}</strong>: ${counts[d].join(', ')}`).join(' &bull; ');
    } else if (n > 0) {
        matchMsg.classList.remove('hidden');
        matchMsg.className = 'result-box';
        matchMsg.innerHTML = `<strong>No match yet</strong> among ${n} people.`;
    }
}

// ================================================================
// PARADOX III: SIMPSON'S
// ================================================================
function spVote(phase, val) {
    send('simpson', 'vote_' + phase, val);
    if (phase === 'before') {
        document.getElementById('sp-phase1').innerHTML = `<div class="result-box text-center"><strong>You voted: ${val === 'yes' ? 'Yes, discrimination' : 'No discrimination'}.</strong> Now look at the department-level data below...</div>`;
        document.getElementById('sp-phase2').classList.remove('hidden');
    } else {
        document.getElementById('sp-phase2').classList.add('hidden');
        document.getElementById('sp-phase3').classList.remove('hidden');
    }
}

// ================================================================
// PARADOX IV: MONTY HALL
// ================================================================
let mh = { car: -1, pick: -1, opened: -1, phase: 'pick', stayW: 0, stayT: 0, swW: 0, swT: 0, total: 0 };

function mhNew() {
    mh.car = Math.floor(Math.random() * 3);
    mh.pick = -1; mh.opened = -1; mh.phase = 'pick';
    for (let i = 0; i < 3; i++) {
        const d = document.getElementById('mh-d' + i);
        d.className = 'door';
        d.querySelector('.icon').textContent = '?';
    }
    document.getElementById('mh-instruction').textContent = 'Pick a door!';
    document.getElementById('mh-instruction').style.color = 'var(--darkblue)';
    document.getElementById('mh-action-btns').classList.add('hidden');
    document.getElementById('mh-result').classList.add('hidden');
}

function mhPick(i) {
    if (mh.phase !== 'pick') return;
    mh.pick = i; mh.phase = 'decide';
    document.getElementById('mh-d' + i).classList.add('picked');

    const opts = [0, 1, 2].filter(d => d !== i && d !== mh.car);
    mh.opened = opts[Math.floor(Math.random() * opts.length)];
    const od = document.getElementById('mh-d' + mh.opened);
    od.classList.add('opened');
    od.querySelector('.icon').textContent = '🐐';

    document.getElementById('mh-instruction').textContent = `You picked Door ${i + 1}. The host opened Door ${mh.opened + 1} (goat!). Stay or switch?`;
    document.getElementById('mh-action-btns').classList.remove('hidden');
}

function mhDecide(choice) {
    if (mh.phase !== 'decide') return;
    mh.phase = 'done';
    document.getElementById('mh-action-btns').classList.add('hidden');

    let final;
    if (choice === 'stay') { final = mh.pick; mh.stayT++; }
    else { final = [0, 1, 2].find(d => d !== mh.pick && d !== mh.opened); mh.swT++; }

    const won = final === mh.car;
    if (choice === 'stay' && won) mh.stayW++;
    if (choice === 'switch' && won) mh.swW++;
    mh.total++;

    for (let i = 0; i < 3; i++) {
        const d = document.getElementById('mh-d' + i);
        d.classList.add('locked');
        d.querySelector('.icon').textContent = i === mh.car ? '🚗' : '🐐';
        if (!d.classList.contains('opened') && i !== mh.pick) d.classList.add('opened');
        if (i === mh.car && i === final) d.style.borderColor = 'var(--green)';
    }

    const res = document.getElementById('mh-result');
    res.classList.remove('hidden');
    res.style.color = won ? 'var(--green)' : 'var(--red)';
    res.textContent = won ? `You WON! (${choice})` : `You lost. (${choice}) Car was behind Door ${mh.car + 1}.`;

    send('monty_hall', choice, won ? 'win' : 'lose');
    mhUpdateStats();
}

function mhUpdateStats() {
    document.getElementById('mh-stay-w').textContent = mh.stayW;
    document.getElementById('mh-stay-t').textContent = mh.stayT;
    document.getElementById('mh-sw-w').textContent = mh.swW;
    document.getElementById('mh-sw-t').textContent = mh.swT;
    document.getElementById('mh-total-games').textContent = mh.total;
    if (mh.stayT > 0) {
        const p = (mh.stayW / mh.stayT * 100).toFixed(1);
        document.getElementById('mh-stay-p').textContent = p + '%';
        document.getElementById('mh-stay-bar').style.width = p + '%';
    }
    if (mh.swT > 0) {
        const p = (mh.swW / mh.swT * 100).toFixed(1);
        document.getElementById('mh-sw-p').textContent = p + '%';
        document.getElementById('mh-sw-bar').style.width = p + '%';
    }
}

// ================================================================
// PARADOX V: SIX DEGREES
// ================================================================
function sdSubmitGuess() {
    const v = document.getElementById('sd-guess-input').value;
    if (!v) return;
    send('six_degrees', 'guess', v);
    document.getElementById('sd-phase1').innerHTML = `<div class="result-box success text-center"><strong>Your guess: ${v} steps.</strong> The real answer is about <strong>6</strong> (or even less with social media: ~3.5)! Explore below...</div>`;
    document.getElementById('sd-phase2').classList.remove('hidden');
    sdCalc();
}

function sdCalc() {
    const k = parseInt(document.getElementById('sd-k').value) || 150;
    const tbody = document.getElementById('sd-tbody');
    let html = '', reach = 1;
    for (let s = 0; s <= 7; s++) {
        if (s > 0) reach *= k;
        const fmt = reach >= 1e9 ? (reach / 1e9).toFixed(1) + 'B' : reach >= 1e6 ? (reach / 1e6).toFixed(1) + 'M' : reach.toLocaleString();
        const pct = Math.min(reach / 8e9 * 100, 100);
        const over = reach >= 8e9;
        const bg = over ? '#16a34a' : '#2563eb';
        const rowStyle = over ? 'background:#dcfce7;font-weight:600' : '';
        html += '<tr style="' + rowStyle + '"><td>' + s + '</td><td>' + fmt + '</td><td><div class="progress-bar" style="height:16px"><div class="progress-fill" style="width:' + Math.max(pct, 0.5) + '%;background:' + bg + ';font-size:.7rem">' + (pct < 1 ? pct.toFixed(2) : pct.toFixed(0)) + '%</div></div></td></tr>';
    }
    tbody.innerHTML = html;
}

function sdNetwork() {
    const N = parseInt(document.getElementById('sd-n').value) || 50;
    const K = parseInt(document.getElementById('sd-e').value) || 4;
    const canvas = document.getElementById('sd-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight;
    const W = canvas.width, H = canvas.height;

    const adj = Array.from({ length: N }, () => new Set());
    for (let i = 0; i < N; i++)
        for (let j = 1; j <= Math.floor(K / 2); j++) { const ni = (i + j) % N; adj[i].add(ni); adj[ni].add(i); }
    for (let i = 0; i < N; i++)
        for (let j = 1; j <= Math.floor(K / 2); j++) {
            if (Math.random() < 0.3) {
                const ni = (i + j) % N; adj[i].delete(ni); adj[ni].delete(i);
                let t; do { t = Math.floor(Math.random() * N); } while (t === i || adj[i].has(t));
                adj[i].add(t); adj[t].add(i);
            }
        }

    const src = Math.floor(Math.random() * N);
    let dst; do { dst = Math.floor(Math.random() * N); } while (dst === src);
    const prev = Array(N).fill(-1), vis = Array(N).fill(false), q = [src]; vis[src] = true;
    while (q.length) { const u = q.shift(); if (u === dst) break; for (const v of adj[u]) if (!vis[v]) { vis[v] = true; prev[v] = u; q.push(v); } }
    const path = []; if (vis[dst]) { let c = dst; while (c !== -1) { path.unshift(c); c = prev[c]; } }
    const pathSet = new Set(path), pathEdges = new Set();
    for (let i = 0; i < path.length - 1; i++) { pathEdges.add(path[i] + '-' + path[i + 1]); pathEdges.add(path[i + 1] + '-' + path[i]); }

    const pos = Array.from({ length: N }, (_, i) => ({ x: W / 2 + (W / 3) * Math.cos(2 * Math.PI * i / N), y: H / 2 + (H / 3) * Math.sin(2 * Math.PI * i / N) }));
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < N; i++) for (const j of adj[i]) if (j > i) {
        const isP = pathEdges.has(i + '-' + j);
        ctx.beginPath(); ctx.moveTo(pos[i].x, pos[i].y); ctx.lineTo(pos[j].x, pos[j].y);
        ctx.strokeStyle = isP ? '#dc2626' : '#e2e8f0'; ctx.lineWidth = isP ? 3 : .5; ctx.stroke();
    }
    const r = Math.max(3, Math.min(8, 200 / N));
    for (let i = 0; i < N; i++) {
        ctx.beginPath(); ctx.arc(pos[i].x, pos[i].y, r, 0, 2 * Math.PI);
        ctx.fillStyle = i === src ? '#2563eb' : i === dst ? '#16a34a' : pathSet.has(i) ? '#f59e0b' : '#94a3b8';
        ctx.fill();
        if (i === src || i === dst) { ctx.lineWidth = 2; ctx.strokeStyle = i === src ? '#1e40af' : '#15803d'; ctx.stroke(); }
    }
    ctx.font = 'bold 11px sans-serif'; ctx.fillStyle = '#1e3a5f';
    ctx.fillText('START', pos[src].x + r + 3, pos[src].y - 4);
    ctx.fillText('END', pos[dst].x + r + 3, pos[dst].y - 4);

    const rd = document.getElementById('sd-net-result');
    rd.innerHTML = path.length ? `<div class="result-box success"><strong>Shortest path: ${path.length - 1} steps</strong> in a network of ${N} people.</div>` : `<div class="result-box warn"><strong>No path found</strong> — try increasing contacts.</div>`;
}

// ================================================================
// DASHBOARD
// ================================================================
async function refreshDashboard() {
    const data = await fetchData(USER.session);
    if (!data || data.error) return;

    // Students
    const names = [...new Set(data.filter(d => d.action === 'join').map(d => d.value))];
    document.getElementById('dash-count').textContent = names.length;
    document.getElementById('dash-students').innerHTML = names.length ?
        names.map(n => `<span class="tag">${n}</span>`).join('') :
        '<em style="color:var(--grey)">Waiting for students...</em>';

    // --- Paradox I: Boy/Girl guesses ---
    const bgG = data.filter(d => d.paradox === 'boy_girl' && d.action === 'guess');
    if (bgG.length) {
        const counts = {}; bgG.forEach(d => counts[d.value] = (counts[d.value] || 0) + 1);
        const total = bgG.length;
        let html = '';
        ['1/4', '1/3', '1/2', '2/3'].forEach(k => {
            const c = counts[k] || 0;
            const pct = (c / total * 100).toFixed(0);
            const color = k === '1/3' ? 'var(--green)' : 'var(--blue)';
            html += `<div class="dash-bar"><span class="label">${k} ${k === '1/3' ? '✓' : ''}</span><div class="bar"><div class="fill" style="width:${pct}%;background:${color}">${c} (${pct}%)</div></div></div>`;
        });
        document.getElementById('dash-bg-guesses').innerHTML = `<p style="font-size:.85rem;color:var(--grey);margin-bottom:.3rem">${total} responses</p>` + html;
    }

    // Game results
    const bgGames = data.filter(d => d.paradox === 'boy_girl' && d.action === 'game_result');
    if (bgGames.length) {
        let totalBoth = 0, totalRounds = 0;
        bgGames.forEach(d => {
            try { const v = JSON.parse(d.value); totalBoth += v.bothSeen; totalRounds += v.total; } catch {}
        });
        const avgRate = totalRounds > 0 ? (totalBoth / totalRounds * 100).toFixed(1) : '—';
        document.getElementById('dash-bg-games').innerHTML = `<div class="result-box"><strong>Class game results:</strong> "Both boys" appeared ${totalBoth}/${totalRounds} times = <strong>${avgRate}%</strong> (theory: 33.3%)</div>`;
    }

    // --- Paradox II: Birthday ---
    const bdGuesses = data.filter(d => d.paradox === 'birthday' && d.action === 'guess');
    if (bdGuesses.length) {
        const vals = bdGuesses.map(d => parseInt(d.value)).filter(v => !isNaN(v));
        const avg = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(0) : '—';
        const min = vals.length ? Math.min(...vals) : '—';
        const max = vals.length ? Math.max(...vals) : '—';
        document.getElementById('dash-bd-guesses').innerHTML = `<p><strong>${vals.length} guesses</strong> — Average: <strong>${avg}</strong>, Range: ${min}–${max} (Correct: <strong style="color:var(--green)">23</strong>)</p>`;
    }
    const bdBdays = data.filter(d => d.paradox === 'birthday' && d.action === 'birthday');
    if (bdBdays.length) {
        const counts = {};
        bdBdays.forEach(e => { counts[e.value] = counts[e.value] || []; counts[e.value].push(e.name); });
        const dupes = Object.keys(counts).filter(k => counts[k].length > 1);
        let html = '<p><strong>' + bdBdays.length + ' birthdays submitted</strong></p><div class="bd-board">';
        bdBdays.forEach(e => {
            const m = dupes.includes(e.value);
            html += `<span class="bd-tag ${m ? 'match' : ''}">${e.name}: ${e.value}</span>`;
        });
        html += '</div>';
        if (dupes.length) {
            html += '<div class="result-box success mt-1"><strong>Matches found!</strong> ';
            html += dupes.map(d => `<strong>${d}</strong>: ${counts[d].join(', ')}`).join(' &bull; ');
            html += '</div>';
        }
        document.getElementById('dash-bd-board').innerHTML = html;
    }

    // --- Paradox III: Simpson's ---
    const spBefore = data.filter(d => d.paradox === 'simpson' && d.action === 'vote_before');
    const spAfter = data.filter(d => d.paradox === 'simpson' && d.action === 'vote_after');
    if (spBefore.length || spAfter.length) {
        const bYes = spBefore.filter(d => d.value === 'yes').length;
        const bNo = spBefore.filter(d => d.value === 'no').length;
        const aYes = spAfter.filter(d => d.value === 'yes').length;
        const aNo = spAfter.filter(d => d.value === 'no').length;
        const bTot = bYes + bNo || 1; const aTot = aYes + aNo || 1;

        let html = '<p style="font-weight:600;margin-bottom:.5rem">Before seeing departments:</p>';
        html += `<div class="dash-bar"><span class="label">Yes</span><div class="bar"><div class="fill" style="width:${bYes/bTot*100}%;background:var(--red)">${bYes} (${(bYes/bTot*100).toFixed(0)}%)</div></div></div>`;
        html += `<div class="dash-bar"><span class="label">No</span><div class="bar"><div class="fill" style="width:${bNo/bTot*100}%;background:var(--green)">${bNo} (${(bNo/bTot*100).toFixed(0)}%)</div></div></div>`;

        if (spAfter.length) {
            html += '<p style="font-weight:600;margin:.8rem 0 .5rem">After seeing departments:</p>';
            html += `<div class="dash-bar"><span class="label">Still yes</span><div class="bar"><div class="fill" style="width:${aYes/aTot*100}%;background:var(--red)">${aYes} (${(aYes/aTot*100).toFixed(0)}%)</div></div></div>`;
            html += `<div class="dash-bar"><span class="label">Changed to no</span><div class="bar"><div class="fill" style="width:${aNo/aTot*100}%;background:var(--green)">${aNo} (${(aNo/aTot*100).toFixed(0)}%)</div></div></div>`;

            // Count mind-changers
            const beforeMap = {};
            spBefore.forEach(d => beforeMap[d.name] = d.value);
            let changed = 0;
            spAfter.forEach(d => { if (beforeMap[d.name] === 'yes' && d.value === 'no') changed++; });
            if (changed > 0) html += `<div class="result-box success mt-1"><strong>${changed} student${changed > 1 ? 's' : ''} changed their mind</strong> after seeing the department breakdown!</div>`;
        }
        document.getElementById('dash-sp').innerHTML = html;
    }

    // --- Paradox IV: Monty Hall ---
    const mhData = data.filter(d => d.paradox === 'monty_hall');
    if (mhData.length) {
        const stay = mhData.filter(d => d.action === 'stay');
        const sw = mhData.filter(d => d.action === 'switch');
        const stayW = stay.filter(d => d.value === 'win').length;
        const swW = sw.filter(d => d.value === 'win').length;
        const stayPct = stay.length ? (stayW / stay.length * 100).toFixed(1) : 0;
        const swPct = sw.length ? (swW / sw.length * 100).toFixed(1) : 0;

        let html = `<p style="font-size:.85rem;color:var(--grey);margin-bottom:.5rem">${mhData.length} total games played by the class</p>`;
        html += `<div class="dash-bar"><span class="label">STAY</span><div class="bar"><div class="fill" style="width:${stayPct}%;background:var(--red)">${stayW}/${stay.length} wins (${stayPct}%)</div></div></div>`;
        html += `<div class="dash-bar"><span class="label">SWITCH</span><div class="bar"><div class="fill" style="width:${swPct}%;background:var(--green)">${swW}/${sw.length} wins (${swPct}%)</div></div></div>`;
        html += `<p style="font-size:.85rem;color:var(--grey);margin-top:.3rem">Theory: Stay wins 33%, Switch wins 67%</p>`;
        document.getElementById('dash-mh').innerHTML = html;
    }

    // --- Paradox V: Six Degrees ---
    const sdG = data.filter(d => d.paradox === 'six_degrees' && d.action === 'guess');
    if (sdG.length) {
        const vals = sdG.map(d => parseInt(d.value)).filter(v => !isNaN(v));
        const avg = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1) : '—';
        const median = vals.length ? vals.sort((a, b) => a - b)[Math.floor(vals.length / 2)] : '—';
        let html = `<p><strong>${vals.length} guesses</strong> — Average: <strong>${avg}</strong>, Median: <strong>${median}</strong> (Answer: <strong style="color:var(--green)">~6</strong>)</p>`;
        // Simple histogram
        const buckets = { '1-5': 0, '6-10': 0, '11-50': 0, '51-100': 0, '101-1000': 0, '1000+': 0 };
        vals.forEach(v => {
            if (v <= 5) buckets['1-5']++;
            else if (v <= 10) buckets['6-10']++;
            else if (v <= 50) buckets['11-50']++;
            else if (v <= 100) buckets['51-100']++;
            else if (v <= 1000) buckets['101-1000']++;
            else buckets['1000+']++;
        });
        const maxB = Math.max(...Object.values(buckets), 1);
        Object.entries(buckets).forEach(([k, v]) => {
            if (v > 0) html += `<div class="dash-bar"><span class="label">${k}</span><div class="bar"><div class="fill" style="width:${v/maxB*100}%;background:var(--blue)">${v}</div></div></div>`;
        });
        document.getElementById('dash-sd').innerHTML = html;
    }
}
