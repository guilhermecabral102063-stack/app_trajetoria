# Análise do Especialista em Trajetória — Tarefa 6

**Data:** 2026-05-20
**Agente:** especialista-trajetoria
**Destino:** statistician (leitura via disco)
**Normas de referência:** EASA PTS-VPT-DSN (Subpart 2), FAA AC 150/5390-2D e EB-105A
**Sistema de coordenadas:** EPSG:31983 (UTM Zone 23S)
**Sítio:** Vertiporto SBSJ — TLOF/FATO: -23.231441, -45.862719 | Altitude pad: 639,5 m MSL

---

## 1. Inventário de cenários existentes

### 1.1 Cenários gerados pelo `gerar_scenarios_rampas.py` (8 cenários)

| Arquivo `.scn` | Regulação | Config | Orientação | Rota | WPTs Rampa | WPTs VAC |
|---|---|---|---|---|---|---|
| `scenario_EASA_R1_000_SBGR_SJK.scn` | EASA Subpart 2 | R1 | 0° | SBGR → SJK | 50 | 69 |
| `scenario_EASA_R1_000_TAUBATE_SJK.scn` | EASA Subpart 2 | R1 | 0° | Taubaté → SJK | 50 | 52 |
| `scenario_EASA_R2_180_SBGR_SJK.scn` | EASA Subpart 2 | R2 | 180° | SBGR → SJK | 50 | 69 |
| `scenario_EASA_R2_180_TAUBATE_SJK.scn` | EASA Subpart 2 | R2 | 180° | Taubaté → SJK | 50 | 52 |
| `scenario_FAA_P1_000_SBGR_SJK.scn` | FAA EB-105A | P1 | 0° | SBGR → SJK | 47 | 69 |
| `scenario_FAA_P1_000_TAUBATE_SJK.scn` | FAA EB-105A | P1 | 0° | Taubaté → SJK | 47 | 52 |
| `scenario_FAA_P2_180_SBGR_SJK.scn` | FAA EB-105A | P2 | 180° | SBGR → SJK | 47 | 69 |
| `scenario_FAA_P2_180_TAUBATE_SJK.scn` | FAA EB-105A | P2 | 180° | Taubaté → SJK | 47 | 52 |

### 1.2 Cenários legados Peres (4 cenários — sem rampa regulatória)

| Arquivo `.scn` | Tipo | WPTs Rampa |
|---|---|---|
| `scenario_Procedimento_VAC_SBSJ_31983_Peres_1.scn` | Legado/VAC | 0 |
| `scenario_Procedimento_VAC_SBSJ_31983_Peres_2.scn` | Legado/VAC | 0 |
| `scenario_Procedimento_VAC_SBSJ_31983_Peres_3.scn` | Legado/VAC | 0 |
| `scenario_Procedimento_VAC_SBSJ_31983_Peres_4.scn` | Legado/VAC | 0 |

Os cenários Peres não contêm waypoints de rampa regulatória (campo `DEFWPT *_W*` ausente). São cenários de procedimento VAC SBSJ anteriores à integração das rampas EASA/FAA.

**Total de cenários disponíveis:** 12 (8 com rampa regulatória + 4 legados)

---

## 2. Perfil das trajetórias nominais (EASA e FAA)

### 2.1 CSV EASA — `trajetorias_rampas_vertiporto_EASA_Subpart_2.csv`

**Colunas disponíveis:** `ramp_name`, `point_type`, `distance_along_m`, `offset_m`, `lat`, `lon`, `alt_m`, `x_local_m`, `y_local_m`, `easting_m`, `northing_m`

**Nota:** Não há campo de velocidade (`spd_kts`) no CSV. Velocidades são definidas exclusivamente no perfil ATDIST do script gerador (ver Seção 2.3).

| Parâmetro | Rampa R1 (0°) | Rampa R2 (180°) |
|---|---|---|
| Pontos totais (centerline) | 974 | 974 |
| Intervalo nominal entre pontos | 1 m (médio: 1,038 m) | 1 m (médio: 1,038 m) |
| Distância ao longo (m) | 0,000 a 1.010,000 | 0,000 a 1.010,000 |
| Altitude MSL (m) | 639,541 a 791,541 | 639,541 a 791,541 |
| Delta altitude (m) | 152,000 | 152,000 |
| Gradiente nominal (m/m) | 0,1250 (excluindo ponto 0) | 0,1250 (excluindo ponto 0) |
| Gradiente em % | 12,50% | 12,50% |
| R² linearidade (regressão) | 0,99945 | 0,99945 |
| Offset lateral (offset_m) | 0,000 (apenas centerline) | 0,000 (apenas centerline) |

**Particularidade do ponto dist=0:** O ponto de distância zero tem altitude 639,541 m (nível do pad), seguido de um salto para dist=38 m com altitude 670,041 m. Esse salto gera um gradiente espúrio de 0,803 m/m no trecho 0–38 m, que representa a zona de hover/transição sobre o FATO — não é a rampa de aproximação propriamente dita. O gradiente regulatório de 0,1250 m/m aplica-se ao trecho 38–1.010 m.

**Estrutura da rampa EASA:**
- Rampa linear (R² = 0,9994) de 1.010 m de extensão horizontal
- Variação de altitude de 152 m (791,5 m → 639,5 m MSL) = 499 ft AGL sobre o pad
- Ângulo de aproximação equivalente: arctan(152/1010) ≈ 8,57° (gradiente 12,5%)
- Denominação regulatória: "OFV omni planar" conforme PTS-VPT-DSN Subpart 2
- Não há curvatura horizontal: ambas as rampas (R1 e R2) são orientações simétricas da mesma rampa plana

### 2.2 CSV FAA — `trajetorias_rampas_vertiporto_FAA_eb_105a.csv`

**Colunas disponíveis:** idênticas ao CSV EASA (`ramp_name`, `point_type`, `distance_along_m`, `offset_m`, `lat`, `lon`, `alt_m`, `x_local_m`, `y_local_m`, `easting_m`, `northing_m`)

**Nota:** Não há campo de velocidade no CSV. Velocidades definidas no perfil ATDIST_FAA do script gerador.

| Parâmetro | Rampa P1 (0°) | Rampa P2 (180°) |
|---|---|---|
| Pontos totais (centerline) | 590 | 590 |
| Intervalo nominal entre pontos | ~1 m (médio: 1,024 m) | ~1 m (médio: 1,024 m) |
| Distância ao longo (m) | 0,000 a 602,848 | 0,000 a 602,848 |
| Altitude MSL (m) | 639,541 a 712,997 | 639,541 a 712,997 |
| Delta altitude (m) | 73,456 | 73,456 |
| Gradiente nominal (m/m) | 0,1250 (trecho ativo) | 0,1250 (trecho ativo) |
| Gradiente em % | 12,50% | 12,50% |
| R² linearidade (regressão) | 0,99999 | 0,99999 |
| Offset lateral (offset_m) | 0,000 (apenas centerline) | 0,000 (apenas centerline) |

**Particularidade zona plana inicial FAA:** O ponto dist=0 e o ponto dist=15,2 m têm altitude idêntica (639,541 m), caracterizando uma zona de gradiente zero (flare sobre o TLOF). O gradiente regulatório de 0,1250 m/m aplica-se ao trecho 15,2–602,8 m.

**Estrutura da rampa FAA:**
- Rampa com alta linearidade (R² = 0,99999 — virtualmente perfeita)
- 587,6 m de extensão da rampa ativa (excluindo zona plana)
- Variação de altitude de 73,456 m (713,0 m → 639,5 m MSL) = 241 ft AGL
- Ângulo de aproximação equivalente: arctan(73,456/602,848) ≈ 6,96° (gradiente 12,5%)
- Denominação regulatória: "Path Curved (Fig. 2-6)" conforme FAA EB-105A
- Denominada "Curved" por ter curvatura na rota horizontal — o perfil vertical é linear

### 2.3 Perfil de velocidades (ATDIST — definido no script, não nos CSVs)

As velocidades de aproximação estão definidas em `gerar_scenarios_rampas.py` e são idênticas para os dois formatos de rampa na fase de entrada/cruzeiro, diferindo nos pontos intermediários:

**Perfil ATDIST_EASA (7 gatilhos):**

| Distância ao pad (NM) | Altitude AGL (ft) | Velocidade (kt) | VS (fpm) |
|---|---|---|---|
| 5,0 | 984 | 60 | 500 |
| 2,0 | 657 | 40 | 500 |
| 0,6 | 504 | 30 | 400 |
| 0,3 | 275 | 15 | 300 |
| 0,1 | 92 | 5 | 200 |
| 0,05 | 50 | 5 | 100 |
| 0,002 | 0 | 0 | 50 |

**Perfil ATDIST_FAA (7 gatilhos):**

| Distância ao pad (NM) | Altitude AGL (ft) | Velocidade (kt) | VS (fpm) |
|---|---|---|---|
| 5,0 | 984 | 60 | 500 |
| 2,0 | 507 | 40 | 500 |
| 0,38 | 250 | 30 | 400 |
| 0,2 | 148 | 15 | 300 |
| 0,1 | 74 | 5 | 200 |
| 0,05 | 50 | 5 | 100 |
| 0,002 | 0 | 0 | 50 |

### 2.4 Diferenças estruturais entre EASA e FAA

| Dimensão | EASA Subpart 2 | FAA EB-105A | Implicação |
|---|---|---|---|
| Extensão da rampa | 1.010 m | 602,848 m | EASA ocupa 1,68× mais espaço horizontal |
| Delta altitude | 152,0 m (499 ft AGL) | 73,456 m (241 ft AGL) | EASA inicia aproximação 2,07× mais alto |
| Gradiente de descida | 12,50% | 12,50% | Idênticos — mesma inclinação angular |
| Zona de transição | 0–38 m (salto abrupto) | 0–15,2 m (nível) | Ambas têm zona especial perto do pad |
| Curvatura vertical | Linear com exceção no ponto 0 | Virtualmente linear (R²=0,99999) | FAA mais regular para modelagem |
| Curvatura horizontal | Reta (planar) | Curved (rota curva) | FAA pode gerar e_y estrutural |
| WPTs por cenário (amostrado) | 50 (a cada 20 m) | 47 (a cada 12 m) | Resolução lateral similar |
| Altitude de entrada | 791,5 m MSL | 713,0 m MSL | EASA requer mais capacidade de descida |
| Campo de velocidade no CSV | Ausente | Ausente | Velocidades apenas em ATDIST |

---

## 3. Estado atual das simulações

### 3.1 O que já existe

- **8 cenários BlueSky (.scn) com rampa regulatória** completamente gerados e parametrizados:
  - 4 cenários EASA (R1 e R2, rotas SBGR e Taubaté)
  - 4 cenários FAA (P1 e P2, rotas SBGR e Taubaté)
- **4 cenários legados Peres (.scn)** com procedimento VAC SBSJ completo (sem rampas regulatórias)
- **2 CSVs de rampa** com 974 (EASA) e 590 (FAA) pontos de centerline cada, cobrindo as 4 configurações de rampa
- **Script gerador** (`gerar_scenarios_rampas.py`) funcional, com lógica de amostragem, perfil ATDIST, rotas VAC e logging de telemetria (STATELOG + UAMMETRICS)
- **Dashboard Taipy** (`app/pages/trajetorias.py`) operacional para visualização dos perfis nominais (EASA vs. FAA, orientações 0° e 180°)
- **Logging de telemetria configurado** em todos os cenários: `STATELOG` captura `lat, lon, distflown, alt, cas, tas, gs` a cada 0,1 s simulado; `UAMMETRICS` ativado
- **Arquivo `saida_gerador.txt`** existe mas está vazio (0 bytes) — nenhuma saída de execução foi capturada

### 3.2 O que está faltando (gap crítico)

| Item faltante | Bloqueio que causa |
|---|---|
| **Logs de telemetria de simulação** (.log ou .csv do STATELOG) | Sem eles não há dados de trajetória real; Monte Carlo impossível |
| **Execução do BlueSky** para os 8 cenários | Os .scn existem mas nunca foram executados no simulador |
| **Perturbações atmosféricas** nos cenários | Nenhum cenário modela vento, turbulência ou variação de temperatura |
| **Caracterização meteorológica SBSJ** | Envelope de vento (DJF/JJA/MAM/SON) não está definido |
| **Parametrização BADA-H** explícita | O tipo "EVTOL" é referenciado nos .scn mas os parâmetros de desempenho não estão documentados no repositório |
| **Simulações Monte Carlo** | Zero iterações executadas; nenhuma dispersão quantificada |
| **Dados de e_y e e_z** | Não calculados — dependem dos logs de simulação |
| **Envelopes probabilísticos** | Não gerados — dependem do Monte Carlo |
| **Plano de instrumentação (Fase II)** | Não redigido |

---

## 4. Parâmetros para o statistician

Esta seção especifica o contrato de dados que o `statistician` precisará quando as simulações Monte Carlo forem executadas. O `statistician` deve aguardar a entrega dos logs de telemetria antes de iniciar qualquer análise.

### 4.1 Variáveis de saída esperadas por linha de log (STATELOG)

| Variável BlueSky | Nome analítico | Tipo | Unidade | Observação |
|---|---|---|---|---|
| `traf.id` | `acid` | string | — | Identificador da aeronave/cenário |
| `traf.lat` | `lat` | float | graus | WGS84 |
| `traf.lon` | `lon` | float | graus | WGS84 |
| `traf.distflown` | `dist_flown_nm` | float | NM | Distância acumulada voada |
| `traf.alt` | `alt_ft_agl` | float | ft (AGL BlueSky) | Altitude no modelo terra-plana |
| `traf.cas` | `cas_kts` | float | kt | Calibrated airspeed |
| `traf.tas` | `tas_kts` | float | kt | True airspeed |
| `traf.gs` | `gs_kts` | float | kt | Ground speed |

**Variáveis derivadas a calcular pelo statistician:**

| Variável derivada | Descrição | Fórmula |
|---|---|---|
| `e_y(t)` | Desvio lateral (cross-track error) | Distância perpendicular ao centerline nominal em cada instante |
| `e_z(t)` | Desvio vertical | `alt_simulada(t) - alt_nominal(dist(t))` interpolada no CSV |
| `dist_pad_m` | Distância ao pad em metros | Convertida de `dist_flown_nm` relativa ao waypoint POUSO_FINAL |
| `fase_voo` | Fase da trajetória | Segmentação por distância ao pad: cruzeiro, pré-rampa, rampa, hover, pouso |

### 4.2 Estratificação recomendada

A análise estatística deve obrigatoriamente estratificar os resultados nas seguintes dimensões — resultados agregados sem estratificação não são aceitos como produto da Tarefa 6:

| Dimensão | Níveis | Justificativa |
|---|---|---|
| Regulação | EASA, FAA | Geometrias de rampa distintas |
| Configuração de rampa | R1/P1 (0°), R2/P2 (180°) | Orientações simétricas, mas rotas de ingresso diferentes |
| Rota de origem | SBGR, Taubaté | Procedimentos VAC distintos (69 vs. 52 waypoints) |
| Fase de voo | Cruzeiro, pré-rampa, rampa, hover, pouso | Dispersão varia por fase |
| Cenário atmosférico | Nominal, DJF, JJA, MAM, SON, crítico | Ainda não definidos — aguardar caracterização met. |
| Semente Monte Carlo | Por iteração | Rastreabilidade individual de cada simulação |

### 4.3 Métricas de dispersão a calcular

Para cada célula de estratificação (regulação × orientação × rota × fase × cenário):

**Estatísticas descritivas de e_y e e_z:**
- Média (μ), desvio padrão (σ)
- Percentis: P50, P90, P95, P99, P99,9
- Máximo absoluto (bounding envelope)
- Intervalo de confiança 95% por bootstrap (N_bootstrap ≥ 10.000)

**Métricas de envelope probabilístico:**
- Raio de contenção 95% (R95) — distância lateral que contém 95% das trajetórias
- Volume probabilístico: elipsoide 2σ no plano (e_y, e_z)
- Fração de trajetórias dentro do envelope nominal EASA/FAA

**Testes de normalidade (obrigatórios antes de ajuste de distribuição):**
- Kolmogorov-Smirnov (KS) — nível de significância α = 0,05
- Anderson-Darling (AD) — sensível às caudas
- Shapiro-Wilk para N < 5.000

### 4.4 Distribuições a testar (por variável)

| Variável | Distribuições candidatas | Justificativa física |
|---|---|---|
| `e_y` (desvio lateral) | Normal, Rayleigh, Laplace | e_y ~ N(0,σ) para perturbações simétricas; Rayleigh para magnitude |
| `\|e_y\|` (magnitude lateral) | Rayleigh, Half-normal, Weibull | Magnitude é não-negativa |
| `e_z` (desvio vertical) | Normal, Logística | Perturbações verticais tendem a ser simétricas |
| Desvios por fase hover | Normal com μ≠0 (viés possível) | Controle hover pode ter offset sistemático |
| Desvios por fase rampa | Mistura gaussiana (GMM, 2-3 componentes) | Rota curva FAA pode gerar bimodalidade |

**Critério de seleção de distribuição:** AIC/BIC mínimo entre candidatas, com p-valor KS > 0,05.

### 4.5 Dimensionamento amostral Monte Carlo

Estimativa preliminar (a validar após primeiras simulações):
- **N mínimo por cenário:** 500 iterações (para P99 com IC 95% bootstrap com erro < 10%)
- **N recomendado:** 1.000 iterações por cenário
- **N total estimado:** 8 cenários × 6 condições met. × 1.000 = 48.000 simulações
- **Critério de convergência:** variação do P95 < 1% entre blocos de 100 simulações adicionais

---

## 5. Recomendações para o dashboard

### 5.1 O que o dashboard pode exibir com dados existentes (fase atual)

O dashboard Taipy em `app/pages/trajetorias.py` já implementa:

**Implementado:**
- Perfil altitude vs. distância para orientação 0° (EASA vs. FAA sobrepostos)
- Perfil altitude vs. distância para orientação 180° (EASA vs. FAA sobrepostos)
- Exportação em PDF e PNG (paleta azul pastel conforme padronização visual)

**A adicionar com dados existentes (CSVs — sem Monte Carlo):**

| Gráfico | Dados necessários | Disponibilidade |
|---|---|---|
| Mapa 2D das trajetórias no plano horizontal (lat/lon) | Colunas `lat`, `lon` dos CSVs | Disponível agora |
| Perfil de altitude vs. distância por orientação (separados) | CSVs | Disponível agora |
| Perfil de velocidade vs. distância ao pad | Tabelas ATDIST do script | Disponível agora (codificado) |
| Tabela comparativa EASA vs. FAA (extensão, delta-alt, gradiente) | Calculado | Disponível agora |
| Mapa UTM (EPSG:31983) com sobreposição das 4 rampas | Colunas `easting_m`, `northing_m` | Disponível agora |

**Nota técnica:** O campo `ramp_name` nos CSVs usa o caractere `°` (grau Unicode). A lógica `str.contains("(0°)")` no dashboard deve funcionar corretamente em Python 3 com codificação UTF-8. Verificar encoding na leitura do pandas.

### 5.2 O que será adicionado quando Monte Carlo estiver disponível

| Gráfico / Tabela | Dados necessários |
|---|---|
| Envelope probabilístico 2D (banda lateral P95, P99 em torno do centerline) | e_y por distância ao pad |
| Envelope probabilístico vertical (banda P95, P99) | e_z por distância ao pad |
| Histogramas de e_y e e_z por fase de voo | Logs de simulação + fase identificada |
| Comparativo de dispersão EASA vs. FAA (boxplot por fase) | Logs de simulação estratificados |
| Heatmap de densidade de ocupação do espaço aéreo | e_y, e_z, dist_pad para N simulações |
| Tabela de envelopes probabilísticos (P95, P99, bounding) | Saída do statistician |
| Indicadores de conformidade regulatória (% dentro do envelope nominal) | Comparação nominal × simulado |

---

## 6. Próximos passos operacionais

Lista priorizada das ações necessárias para executar a Tarefa 6 completa:

### Prioridade 1 — Desbloqueadores críticos (sem isso, nada avança)

1. **Instalar e configurar BlueSky** no ambiente de execução (Python, dependências, modelo EVTOL/BADA-H)
2. **Verificar o tipo de aeronave "EVTOL"** no BlueSky: confirmar se os parâmetros de desempenho estão carregados ou se precisam ser parametrizados via arquivo de performance (`.perf`)
3. **Executar cenário nominal (sem perturbação)** para cada uma das 8 configurações — verificar que o STATELOG produz saída não-vazia
4. **Capturar `saida_gerador.txt`** com stdout real da execução (arquivo existe mas está vazio)

### Prioridade 2 — Caracterização atmosférica (necessária antes do Monte Carlo)

5. **Extrair e processar dados METAR históricos do SBSJ** (mínimo 5 anos) para os 4 regimes sazonais (DJF, JJA, MAM, SON)
6. **Definir envelope de vento:** componentes de proa, través e cauda para os rumos de aproximação (0° e 180°)
7. **Definir cenários atmosféricos operacionais:** nominal (calmo), crítico (vento máximo operacional), e sazonais representativos
8. **Documentar premissas de temperatura e pressão** para cálculo de densidade-altitude

### Prioridade 3 — Implementação Monte Carlo

9. **Escrever script de execução em lote** (`run_montecarlo.py`) que:
   - Varia semente aleatória por iteração
   - Injeta perturbações de vento (via comandos `WS` ou `WIND` do BlueSky)
   - Executa cada cenário N vezes
   - Consolida logs em DataFrame parquet por cenário
10. **Calcular e_y e e_z** a partir dos logs brutos (comparação com centerline dos CSVs)
11. **Entregar parquet estruturado** ao statistician conforme contrato de dados (Seção 4)

### Prioridade 4 — Análise e entrega

12. **Ajuste de distribuições e envelopes probabilísticos** (pelo statistician)
13. **Geração de histogramas e volumes probabilísticos** (pelo especialista + statistician)
14. **Verificação de conformidade regulatória** com dimensionamento de FATO/TLOF/OLS
15. **Redação do relatório técnico final** da Tarefa 6

---

## Resumo executivo

Os 8 cenários BlueSky para a Tarefa 6 estão completamente especificados em disco (4 EASA + 4 FAA, cobri ndo as duas orientações e as duas rotas de origem), com telemetria configurada via STATELOG e UAMMETRICS. As rampas nominais EASA e FAA apresentam o mesmo gradiente de descida (12,50%), diferindo em extensão horizontal (1.010 m vs. 603 m) e em delta de altitude (152 m vs. 73 m), o que implica envelopes de proteção e regimes de deceleração estruturalmente distintos. O gap crítico é a ausência total de logs de simulação — os cenários nunca foram executados no BlueSky — o que bloqueia toda a análise de desvios e o Monte Carlo; a próxima ação imediata é a execução e verificação dos cenários nominais no simulador.

---

## Artefatos produzidos

- `C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Aplicativo - Trajetória\analise_especialista.md` — este documento

---

## Decisões tomadas

- **Gradiente nominal adotado:** 0,1250 m/m (12,50%) para ambas as normas, calculado a partir dos dados reais dos CSVs excluindo as zonas de transição (trecho 0–38 m EASA e 0–15,2 m FAA). Norma: EASA PTS-VPT-DSN Subpart 2 e FAA EB-105A.
- **Ponto de dist=0 excluído do gradiente:** O salto abrupto de altitude no ponto dist=0 dos CSVs representa a zona hover/FATO, não a rampa de aproximação. Gradiente calculado excluindo esse ponto.
- **Velocidades: fonte é o script, não o CSV:** Os CSVs não contêm campo de velocidade. As velocidades operacionais são as definidas em `ATDIST_EASA` e `ATDIST_FAA` no `gerar_scenarios_rampas.py` — essa é a fonte autoritativa.
- **Contrato de dados com o statistician:** Definido na Seção 4. O statistician não deve iniciar análises antes da entrega dos logs de simulação em formato parquet com as colunas especificadas.
- **Cenários Peres classificados como legados:** Os 4 cenários Peres não têm waypoints de rampa regulatória e não integram a análise da Tarefa 6. São mantidos para referência histórica do procedimento VAC SBSJ.

---

## Pendências / riscos

- **BLOQUEADOR CRÍTICO:** Nenhuma simulação BlueSky foi executada. Todos os produtos da Tarefa 6 (e_y, e_z, envelopes) dependem disso.
- **Tipo "EVTOL" no BlueSky:** Não confirmado se o modelo de performance está carregado. Se o tipo não for reconhecido, os cenários falharão na criação da aeronave (`CRE` command).
- **Plugin UAMMETRICS:** Requerido em todos os cenários (`PLUGIN LOAD UAMMETRICS`). Sua disponibilidade no ambiente BlueSky não foi verificada.
- **Caracterização meteorológica ausente:** Os cenários atmosféricos (nominal, DJF/JJA/MAM/SON, crítico) não estão definidos. Sem isso, o Monte Carlo não pode ser parametrizado.
- **Arquivo `saida_gerador.txt` vazio:** Indica que a saída do gerador de cenários não foi capturada. Não é bloqueador (os .scn existem e estão corretos), mas sugere ambiente de execução não documentado.
- **Premissa de terra-plana do BlueSky:** As altitudes nos .scn são AGL (pad = 0 ft). A altitude MSL real do pad (639,5 m) e a topografia do vale do Paraíba não são modeladas. Isso implica que e_z calculado a partir dos logs será relativo ao pad, não absoluto — o statistician deve ser avisado.
- **Curvatura horizontal FAA:** A rota FAA "Curved" gera e_y estrutural (viés lateral não-zero) mesmo sem perturbação, pela geometria da trajetória. O statistician deve separar o componente estrutural do estocástico.

---

## Próximo passo sugerido

Executar os 8 cenários BlueSky em modo nominal (sem perturbação atmosférica) para verificar funcionamento do STATELOG e UAMMETRICS, capturar os primeiros logs de telemetria e confirmar que a aeronave "EVTOL" é reconhecida pelo simulador — isso destrava toda a Tarefa 6.
