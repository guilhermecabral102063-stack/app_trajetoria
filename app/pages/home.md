<|part|class_name=app-shell|

<|layout|columns=260px 1fr|class_name=app-layout|

<|part|class_name=sidebar|

<|part|class_name=sidebar-brand|
VertiMob · ITA · ANAC
|>

<|part|class_name=sidebar-title|
Trajetória eVTOL
|>

<|part|class_name=sidebar-sub|
Vertiporto SJC/SBSJ — Sandbox Regulatório
|>

<|part|class_name=sidebar-nav|
[Pipeline](#pipeline)

[Estado Atual](#estado)

[Cenários](#cenarios)

[Trajetórias 3D](#trajetorias)
|>

|>

<|part|class_name=content-area|

<|part|class_name=topbar|
<span class="topbar-title">Desvios de Trajetória de Pouso — eVTOL SBSJ</span>
<span class="topbar-note">EASA Subpart 2 vs. FAA EB-105A · Simulação BlueSky (TU Delft, GPL v3)</span>
|>

<a id="pipeline"></a>

<div class="section-title">Pipeline — Tarefa 6</div>

<div class="hero-card" style="padding:18px 22px;">
  <div class="pipeline">
    <div class="pipeline-step step-done">
      <span class="num">1</span>
      <span class="label">Definição dos Cenários</span>
      <span class="badge">Concluído</span>
    </div>
    <div class="pipeline-step step-done">
      <span class="num">2</span>
      <span class="label">Geração das Rampas (CSV)</span>
      <span class="badge">Concluído</span>
    </div>
    <div class="pipeline-step step-active">
      <span class="num">3</span>
      <span class="label">Execução BlueSky (.scn)</span>
      <span class="badge">Em andamento</span>
    </div>
    <div class="pipeline-step step-pending">
      <span class="num">4</span>
      <span class="label">Análise dos Desvios e_y / e_z</span>
      <span class="badge">Pendente</span>
    </div>
    <div class="pipeline-step step-pending">
      <span class="num">5</span>
      <span class="label">Monte Carlo</span>
      <span class="badge">Pendente</span>
    </div>
  </div>
</div>

<a id="estado"></a>

<div class="section-title">Estado Atual</div>

<|layout|columns=1fr 1fr 1fr 1fr|class_name=cards-grid|

<div class="info-card">
  <div class="val">8</div>
  <div class="lbl">Arquivos .scn criados</div>
</div>

<div class="info-card">
  <div class="val">4</div>
  <div class="lbl">Rampas nominais definidas</div>
</div>

<div class="info-card">
  <div class="val">6</div>
  <div class="lbl">STATELOGs executados</div>
</div>

<div class="info-card">
  <div class="val pending">0</div>
  <div class="lbl">Corridas Monte Carlo</div>
</div>

|>

<a id="cenarios"></a>

<div class="section-title">Cenários</div>

<div class="reference-card">
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Regulamento</th>
          <th>Config.</th>
          <th>Orient.</th>
          <th>Rota</th>
          <th>Extensão (m)</th>
          <th>Δ Alt (m)</th>
          <th>Gradiente</th>
          <th>.scn</th>
          <th>STATELOG</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td><td><span class="tag tag-easa">EASA Subpart 2</span></td>
          <td>R1</td><td>0°</td><td>SBGR → SJK</td>
          <td>1 010</td><td>152,0</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>2</td><td><span class="tag tag-easa">EASA Subpart 2</span></td>
          <td>R1</td><td>0°</td><td>Taubaté → SJK</td>
          <td>1 010</td><td>152,0</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>3</td><td><span class="tag tag-easa">EASA Subpart 2</span></td>
          <td>R2</td><td>180°</td><td>SBGR → SJK</td>
          <td>1 010</td><td>152,0</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>4</td><td><span class="tag tag-easa">EASA Subpart 2</span></td>
          <td>R2</td><td>180°</td><td>Taubaté → SJK</td>
          <td>1 010</td><td>152,0</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>5</td><td><span class="tag tag-faa">FAA EB-105A</span></td>
          <td>R1</td><td>0°</td><td>SBGR → SJK</td>
          <td>602,8</td><td>73,5</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>6</td><td><span class="tag tag-faa">FAA EB-105A</span></td>
          <td>R1</td><td>0°</td><td>Taubaté → SJK</td>
          <td>602,8</td><td>73,5</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-wait">Pendente</span></td>
        </tr>
        <tr>
          <td>7</td><td><span class="tag tag-faa">FAA EB-105A</span></td>
          <td>R2</td><td>180°</td><td>SBGR → SJK</td>
          <td>602,8</td><td>73,5</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-ok">Executado</span></td>
        </tr>
        <tr>
          <td>8</td><td><span class="tag tag-faa">FAA EB-105A</span></td>
          <td>R2</td><td>180°</td><td>Taubaté → SJK</td>
          <td>602,8</td><td>73,5</td><td>12,5%</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-wait">Pendente</span></td>
        </tr>
        <tr>
          <td>9–12</td><td><span class="tag tag-peres">Peres (legado)</span></td>
          <td>VAC SBSJ</td><td>Var.</td><td>Var.</td>
          <td>—</td><td>—</td><td>—</td>
          <td><span class="tag tag-ok">Criado</span></td>
          <td><span class="tag tag-wait">Pendente</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<a id="trajetorias"></a>

<div class="section-title">Trajetórias — Abordagem Final</div>

<|part|class_name=reference-card traj-card|

<|part|class_name=traj-selector|
<|EASA · R1 · 0° — SBGR → SJK|button|on_action=sel_0|class_name={pill_0}|>
<|EASA · R2 · 180° — SBGR → SJK|button|on_action=sel_1|class_name={pill_1}|>
<|EASA · R1 · 0° — Taubaté → SJK|button|on_action=sel_2|class_name={pill_2}|>
<|EASA · R2 · 180° — Taubaté → SJK|button|on_action=sel_3|class_name={pill_3}|>
<|FAA · R1 · 0° — SBGR → SJK|button|on_action=sel_4|class_name={pill_4}|>
<|FAA · R2 · 180° — SBGR → SJK|button|on_action=sel_5|class_name={pill_5}|>
|>

<|layout|columns=2fr 1fr|class_name=traj-layout|

<|part|

<|layout|columns=1fr auto|class_name=chart-header-row|
<div class="chart-label" style="margin-bottom:0;">Trajetória de Aproximação</div>
<|{map_toggle_lbl}|button|on_action=toggle_map_style|class_name=map-toggle-btn|>
|>
<|chart|figure={map_fig}|>
<div class="chart-label" style="margin-top:16px;">Perfil de Altitude AGL</div>
<|chart|figure={profile_fig}|>

|>

<|part|

<div class="chart-label">Vista FATO/TLOF — SJC/SBSJ</div>
<|chart|figure={fato_fig}|>
<div class="fato-info">
  <strong>FATO/TLOF — Ponto de Toque</strong><br/>
  Sim. O marcador vermelho indica a coordenada exata de pouso do eVTOL. O STATELOG BlueSky confirma alt = 0 ft AGL nessa posição ao final de cada simulação.<br/><br/>
  Lat: −23.231441°<br/>
  Lon: −45.862719°<br/>
  Alt MSL: 639,5 m<br/>
  Alt BlueSky (flat-earth): 0 ft AGL
</div>

|>

|>

|>

|>

|>

|>
