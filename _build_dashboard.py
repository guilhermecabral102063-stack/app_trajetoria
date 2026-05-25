import math, json

TLOF_LAT = -23.231441
TLOF_LON = -45.862719
GATE_KM   = 20.0
STEP_S    = 5.0

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(a))

def to_local(lat, lon):
    dx = (lon - TLOF_LON) * math.cos(math.radians(TLOF_LAT)) * 111319.0
    dy = (lat - TLOF_LAT) * 111319.0
    return round(dx, 1), round(dy, 1)

logs = [
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\EASA\Outputs\STATELOG_scenario_EASA_R1_0_SBGR_SJK_20260521_15-04-25.log',   'EASA_R1', 'EASA', 'R1', '0°', 'SBGR → SJK'),
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\EASA\Outputs\STATELOG_scenario_EASA_R2_180_SBGR_SJK_20260521_15-06-18.log',  'EASA_R2', 'EASA', 'R2', '180°','SBGR → SJK'),
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\EASA\Outputs\STATELOG_scenario_EASA_R3_0_TAUBATE_SJK_20260521_15-07-24.log', 'EASA_R3', 'EASA', 'R3', '0°', 'Taubaté → SJK'),
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\EASA\Outputs\STATELOG_scenario_EASA_R4_180_TAUBATE_SJK_20260521_15-08-00.log','EASA_R4', 'EASA', 'R4', '180°','Taubaté → SJK'),
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\FAA\output\STATELOG_scenario_FAA_R1_0_SBGR_SJK_20260521_16-02-13.log',       'FAA_R1',  'FAA',  'R1', '0°', 'SBGR → SJK'),
    (r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Bluesky\Scenarios\FAA\output\STATELOG_scenario_FAA_R2_180_SBGR_SJK_20260521_16-03-51.log',     'FAA_R2',  'FAA',  'R2', '180°','SBGR → SJK'),
]

all_trajs = []
for path, tid, reg, config, orient, route in logs:
    with open(path) as f:
        lines = [l for l in f if not l.startswith('#') and l.strip()]
    pts_x, pts_y, pts_z = [], [], []
    last_t = -9999
    for l in lines:
        p = l.strip().split(',')
        t      = float(p[0])
        lat    = float(p[2])
        lon    = float(p[3])
        alt_ft = float(p[5])
        alt_m  = round(alt_ft * 0.3048, 1)
        dist_km = haversine_km(lat, lon, TLOF_LAT, TLOF_LON)
        if dist_km > GATE_KM:
            continue
        if (t - last_t) < STEP_S and len(pts_x) > 0:
            continue
        last_t = t
        dx, dy = to_local(lat, lon)
        pts_x.append(dx)
        pts_y.append(dy)
        pts_z.append(alt_m)
    all_trajs.append({'id':tid,'reg':reg,'config':config,'orient':orient,'route':route,'x':pts_x,'y':pts_y,'z':pts_z})
    print(f'{tid}: {len(pts_x)} pts')

trajs_js = json.dumps(all_trajs, separators=(',',':'))
print(f'TRAJS JS: {len(trajs_js)//1024} KB')

# ── Read current dashboard ────────────────────────────────────────────────────
with open(r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Aplicativo - Trajetória\dashboard.html', encoding='utf-8') as f:
    html = f.read()

# ── 1. Plotly CDN ─────────────────────────────────────────────────────────────
html = html.replace(
    '</style>\n</head>',
    '</style>\n<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>\n</head>'
)

# ── 2. Extra CSS ──────────────────────────────────────────────────────────────
traj_css = """
/* -- Trajectory selector -- */
.traj-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}
.traj-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--soft);
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
  user-select: none;
}
.traj-pill:hover { background: #e8eef6; border-color: #b0bec5; color: var(--ink); }
.traj-pill.active-easa { background: #dbeafe; border-color: #93c5fd; color: #1e3a8a; }
.traj-pill.active-faa  { background: #ede9fe; border-color: #c4b5fd; color: #4c1d95; }
.traj-pill .reg-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.dot-easa { background: #2563eb; }
.dot-faa  { background: #7c3aed; }
#plot3d { width: 100%; height: 480px; border-radius: 18px; overflow: hidden; }
.plot-note { font-size: 0.78rem; color: var(--quiet); margin-top: 8px; }
"""
html = html.replace('/* -- Responsive -- */', traj_css + '\n/* -- Responsive -- */')

# ── 3. Sidebar nav ────────────────────────────────────────────────────────────
html = html.replace(
    '    <a href="#cenarios">Cenários</a>\n    <a href="#proximos">Próximos Passos</a>',
    '    <a href="#cenarios">Cenários</a>\n    <a href="#trajetorias">Trajetórias 3D</a>'
)

# ── 4. STATELOG card 0 -> 6 ───────────────────────────────────────────────────
html = html.replace(
    '<div class="val pending">0</div>\n      <div class="lbl">STATELOGs executados</div>',
    '<div class="val">6</div>\n      <div class="lbl">STATELOGs executados</div>'
)

# ── 5. Update table STATELOG column for executed logs ────────────────────────
done_rows = [
    ('<td>1</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R1</td><td>0°</td><td>SBGR → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>1</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R1</td><td>0°</td><td>SBGR → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
    ('<td>2</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R1</td><td>0°</td><td>Taubaté → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>2</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R1</td><td>0°</td><td>Taubaté → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
    ('<td>3</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R2</td><td>180°</td><td>SBGR → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>3</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R2</td><td>180°</td><td>SBGR → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
    ('<td>4</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R2</td><td>180°</td><td>Taubaté → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>4</td><td><span class="tag tag-easa">EASA Subpart 2</span></td><td>R2</td><td>180°</td><td>Taubaté → SJK</td><td>1 010</td><td>152,0</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
    ('<td>5</td><td><span class="tag tag-faa">FAA EB-105A</span></td><td>R1</td><td>0°</td><td>SBGR → SJK</td><td>602,8</td><td>73,5</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>5</td><td><span class="tag tag-faa">FAA EB-105A</span></td><td>R1</td><td>0°</td><td>SBGR → SJK</td><td>602,8</td><td>73,5</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
    ('<td>7</td><td><span class="tag tag-faa">FAA EB-105A</span></td><td>R2</td><td>180°</td><td>SBGR → SJK</td><td>602,8</td><td>73,5</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-no">Pendente</span></td>',
     '<td>7</td><td><span class="tag tag-faa">FAA EB-105A</span></td><td>R2</td><td>180°</td><td>SBGR → SJK</td><td>602,8</td><td>73,5</td><td>12,5%</td><td><span class="tag tag-ok">Criado</span></td><td><span class="tag tag-ok">Executado</span></td>'),
]
for old, new in done_rows:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f'WARNING: row not found: {old[:60]}')

# ── 6. Remove Proximos Passos section ────────────────────────────────────────
import re
html = re.sub(
    r'\s*<!-- 4\. Pr[^\n]*-->\s*<a id="proximos"></a>.*?</div>\s*\n',
    '\n',
    html,
    flags=re.DOTALL
)

# ── 7. Trajetórias 3D section + JS ───────────────────────────────────────────
traj_section = (
    "\n  <!-- 4. Trajetórias 3D -->\n"
    "  <a id=\"trajetorias\"></a>\n"
    "  <div class=\"section-title\">Trajetórias 3D — Abordagem Final</div>\n"
    "  <div class=\"reference-card\" style=\"padding:24px 28px;\">\n"
    "    <div class=\"traj-selector\" id=\"trajSelector\"></div>\n"
    "    <div id=\"plot3d\"></div>\n"
    "    <p class=\"plot-note\">Origem: Portão Caçapava / Portão Jacareí (≤ 20 km do TLOF). Altitude AGL em metros (referência BlueSky flat-earth). Eixos X/Y em metros a partir do TLOF.</p>\n"
    "  </div>\n\n"
    "<script>\nconst TRAJS = " + trajs_js + ";\n\n"
    "const REG_COLOR = { EASA: '#2563eb', FAA: '#7c3aed' };\n"
    "const REG_LABEL = { EASA: 'EASA Subpart 2', FAA: 'FAA EB-105A' };\n\n"
    "let activeIdx = 0;\n\n"
    "function buildSelector() {\n"
    "  const el = document.getElementById('trajSelector');\n"
    "  TRAJS.forEach((t, i) => {\n"
    "    const pill = document.createElement('button');\n"
    "    pill.className = 'traj-pill';\n"
    "    pill.dataset.idx = i;\n"
    "    pill.innerHTML = '<span class=\"reg-dot dot-' + t.reg.toLowerCase() + '\"></span>' + REG_LABEL[t.reg] + ' ' + t.config + ' ' + t.orient + ' — ' + t.route;\n"
    "    pill.addEventListener('click', () => select(i));\n"
    "    el.appendChild(pill);\n"
    "  });\n"
    "  select(0);\n"
    "}\n\n"
    "function select(idx) {\n"
    "  activeIdx = idx;\n"
    "  document.querySelectorAll('.traj-pill').forEach((p, i) => {\n"
    "    p.classList.remove('active-easa', 'active-faa');\n"
    "    if (i === idx) p.classList.add('active-' + TRAJS[i].reg.toLowerCase());\n"
    "  });\n"
    "  renderPlot(TRAJS[idx]);\n"
    "}\n\n"
    "function renderPlot(t) {\n"
    "  const color = REG_COLOR[t.reg];\n"
    "  const trace = {\n"
    "    type: 'scatter3d', mode: 'lines',\n"
    "    x: t.x, y: t.y, z: t.z,\n"
    "    line: { color, width: 4 },\n"
    "    name: REG_LABEL[t.reg] + ' ' + t.config,\n"
    "    hovertemplate: 'X: %{x:.0f} m<br>Y: %{y:.0f} m<br>Alt: %{z:.1f} m<extra></extra>'\n"
    "  };\n"
    "  const tlof = {\n"
    "    type: 'scatter3d', mode: 'markers',\n"
    "    x: [0], y: [0], z: [0],\n"
    "    marker: { color: '#e53e3e', size: 8, symbol: 'diamond' },\n"
    "    name: 'TLOF/FATO',\n"
    "    hovertemplate: 'TLOF — SJC<extra></extra>'\n"
    "  };\n"
    "  const layout = {\n"
    "    paper_bgcolor: '#ffffff',\n"
    "    scene: {\n"
    "      xaxis: { title: 'Leste (m)', gridcolor: '#dfe6ee', zerolinecolor: '#b0bec5' },\n"
    "      yaxis: { title: 'Norte (m)', gridcolor: '#dfe6ee', zerolinecolor: '#b0bec5' },\n"
    "      zaxis: { title: 'Altitude AGL (m)', gridcolor: '#dfe6ee', zerolinecolor: '#b0bec5' },\n"
    "      bgcolor: '#f7f9fb',\n"
    "      camera: { eye: { x: 1.5, y: -1.8, z: 0.9 } }\n"
    "    },\n"
    "    margin: { l: 0, r: 0, t: 10, b: 0 },\n"
    "    legend: { x: 0.01, y: 0.99, bgcolor: 'rgba(255,255,255,0.85)', bordercolor: '#dfe6ee', borderwidth: 1 },\n"
    "    font: { family: 'Inter, Segoe UI, system-ui, sans-serif', size: 11, color: '#526078' }\n"
    "  };\n"
    "  Plotly.react('plot3d', [trace, tlof], layout, { responsive: true, displayModeBar: false });\n"
    "}\n\n"
    "buildSelector();\n"
    "</script>\n"
)

html = html.replace("</div><!-- /content -->", traj_section + "</div><!-- /content -->")

with open(r'C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Aplicativo - Trajetória\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'dashboard.html written: {len(html)//1024} KB')
