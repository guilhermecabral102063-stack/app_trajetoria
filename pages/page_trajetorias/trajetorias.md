<|menu|lov={menu_items}|on_action=on_menu|label=Menu|width=260px|>

<|part|class_name=page-content-wide|

# Trajetórias de Aproximação

<|part|class_name=traj-selector|

<|R1 · 0° SBGR-SJK|button|on_action=sel_0|class_name={pill_0}|>

<|R2 · 180° SBGR-SJK|button|on_action=sel_1|class_name={pill_1}|>

<|R1 · 0° Taubate-SJK|button|on_action=sel_2|class_name={pill_2}|>

<|R2 · 180° Taubate-SJK|button|on_action=sel_3|class_name={pill_3}|>

|>

<|layout|columns=1 1|class_name=traj-layout|

<|part|

<|layout|columns=1 auto|class_name=chart-header-row|

## Mapa de trajetória

<|{map_toggle_lbl}|button|on_action=toggle_map_style|class_name=map-toggle-btn|>

|>

<|chart|figure={map_fig}|>

|>

<|part|

## Perfil de altitude

<|chart|figure={profile_fig}|>

|>

|>

## Localização do FATO/TLOF — SJC/SBSJ

<|chart|figure={fato_fig}|>

## Simulação 3D — Mapbox

<|{video_html}|text|raw=True|>

|>