# Tarefa 6 — Desvios em Relação às Trajetórias de Pouso e Decolagem
## Relatório Preliminar de Estado — Sandbox Regulatório de Vertiporto (SJC/SBSJ)

**Versão:** 0.1 — Preliminar  
**Data:** 20 de maio de 2026  
**Equipe ITA — VertiMob**

---

## 1. Objetivo

A Tarefa 6 quantifica os desvios entre as trajetórias de pouso e decolagem efetivamente voadas — obtidas por simulação — e as trajetórias nominais definidas pelas normas EASA PTS-VPT-DSN (Subpart 2) e FAA EB-105A para o vertiporto SBSJ (São José dos Campos). O resultado esperado são envelopes probabilísticos de desvio lateral (e_y) e vertical (e_z) por fase de voo e por condição meteorológica, expressos nos percentis operacionais P95 e P99.

O interesse regulatório da ANAC reside na viabilidade do dimensionamento de FATO, TLOF e superfícies de limitação de obstáculos (OLS) com base em dados de dispersão de trajetória realistas, e não apenas nos envelopes conservadores prescritos pelas normas estrangeiras. O sandbox regulatório do ITA fornece o ambiente de simulação controlado que permite produzir esses dados antes da operação real.

A Tarefa 6 insere-se na camada de simulação do projeto: sucede a geração e validação dos cenários BlueSky (Tarefa 5) e precede a análise de conformidade regulatória e o dimensionamento de áreas de proteção (Tarefa 7). Os produtos desta tarefa — parquets de e_y e e_z estratificados, distribuições ajustadas e envelopes probabilísticos — são insumos diretos para o relatório técnico final apresentado à ANAC.

---

## 2. Estado atual das simulações

A Tabela 1 sintetiza o estado dos artefatos necessários para a execução completa da Tarefa 6.

**Tabela 1 — Estado dos artefatos da Tarefa 6**

| Artefato | Estado | Observação |
|---|---|---|
| Cenários BlueSky (.scn) com rampa regulatória | Disponível (8 cenários) | 4 EASA + 4 FAA; orientações 0° e 180°; rotas SBGR e Taubaté |
| CSVs de trajetória nominal | Disponível (2 arquivos) | EASA: 1.948 linhas; FAA: 1.180 linhas |
| Script gerador (`gerar_scenarios_rampas.py`) | Disponível e funcional | Perfis ATDIST, VAC, STATELOG e UAMMETRICS configurados |
| Dashboard Taipy (`app/pages/trajetorias.py`) | Disponível e operacional | Exibe perfis nominais EASA vs. FAA |
| Cenários legados Peres (.scn) | Disponível (4 cenários) | Sem rampa regulatória; uso apenas como referência VAC |
| **Logs de telemetria STATELOG** | **Ausente — BLOQUEADOR CRÍTICO** | BlueSky nunca executado; sem logs, o Monte Carlo é inviável |
| Perturbações atmosféricas nos cenários | Ausente | Nenhum cenário modela vento, turbulência ou variação de temperatura |
| Caracterização meteorológica SBSJ | Ausente | Envelope de vento sazonal (DJF/JJA/MAM/SON) não definido |
| Parametrização BADA-H do tipo "EVTOL" | Não verificada | Referenciado nos .scn; parâmetros de desempenho não documentados |
| Simulações Monte Carlo | Ausente | Zero iterações executadas; nenhuma dispersão quantificada |
| Dados de e_y e e_z | Ausente | Dependem dos logs de simulação |
| Envelopes probabilísticos | Ausente | Dependem do Monte Carlo |

O bloqueador crítico é a ausência total de logs de simulação: os 8 cenários BlueSky estão completamente especificados em disco, mas nunca foram executados no simulador. Toda análise de desvios e o Monte Carlo dependem da execução desses cenários e da captura dos respectivos STATELOG.

---

## 3. Caracterização das trajetórias nominais

### 3.1 Parâmetros geométricos (EASA Subpart 2 vs. FAA EB-105A)

A Tabela 2 compara os parâmetros geométricos das rampas nominais, calculados a partir dos CSVs de centerline com o método de regressão linear simples (`alt_m ~ distance_along_m`), excluindo as zonas de transição de cada norma.

**Tabela 2 — Parâmetros geométricos das rampas nominais (trecho ativo)**

| Dimensão | EASA Subpart 2 | FAA EB-105A | Razão EASA/FAA |
|---|---|---|---|
| Extensão horizontal total | 1.010,0 m | 602,848 m | 1,675 |
| Trecho ativo (excluindo zona de transição) | 970,0 m | 586,6 m | 1,655 |
| Delta altitude total | 152,000 m (498,7 ft AGL) | 73,456 m (240,9 ft AGL) | 2,069 |
| Altitude de entrada da rampa | 791,541 m MSL | 712,997 m MSL | — (diff: +78,5 m) |
| Gradiente de descida | 12,50% (7,125°) | 12,50% (7,125°) | 1,000 |
| R² da regressão linear | 1,000000 | 1,000000 | — |
| Resíduo máximo da regressão | 0,000 m | 0,0005 m | — |
| Curvatura horizontal | Reta (planar) | Curva (Path Curved) | — |
| Zona de transição próxima ao pad | 0–38 m; salto abrupto (76,9%) | 0–15,2 m; gradiente zero (0%) | — |
| Pontos de centerline por rampa | 974 | 590 | 1,651 |
| Desvio lateral estrutural e_y (máx.) | 0,000 m | 82,1 m | — |

**Sítio de referência:** TLOF/FATO -23.231441°, -45.862719° | Altitude pad: 639,541 m MSL | EPSG:31983

### 3.2 Perfil de velocidades de aproximação

As velocidades operacionais não constam nos CSVs; são definidas exclusivamente pelos perfis ATDIST do script `gerar_scenarios_rampas.py`. A Tabela 3 apresenta os 7 gatilhos de cada norma.

**Tabela 3 — Perfis ATDIST de velocidade de aproximação**

| Dist. ao pad (NM) | Alt. AGL (ft) — EASA | Vel. (kt) | VS (fpm) | Alt. AGL (ft) — FAA | Vel. (kt) | VS (fpm) |
|---|---|---|---|---|---|---|
| 5,00 | 984 | 60 | 500 | 984 | 60 | 500 |
| 2,00 | 657 | 40 | 500 | 507 | 40 | 500 |
| 0,60 | 504 | 30 | 400 | — | — | — |
| 0,38 | — | — | — | 250 | 30 | 400 |
| 0,30 | 275 | 15 | 300 | — | — | — |
| 0,20 | — | — | — | 148 | 15 | 300 |
| 0,10 | 92 | 5 | 200 | 74 | 5 | 200 |
| 0,05 | 50 | 5 | 100 | 50 | 5 | 100 |
| 0,002 | 0 | 0 | 50 | 0 | 0 | 50 |

*Células com "—" indicam ausência de gatilho naquela distância para a norma respectiva. Os gatilhos de entrada (5,0 NM) e de toque (0,05 e 0,002 NM) são idênticos em ambas as normas.*

### 3.3 Interpretação técnica

Conforme demonstrado na Tabela 2, as duas normas adotam gradiente de descida idêntico (12,50%), o que permite isolar o efeito da extensão horizontal e da curvatura na análise de desvios. A rampa EASA é 1,68 vezes mais longa e inicia 78,5 m acima da FAA, o que implica espação de risco substancialmente maior em altitude: o eVTOL permanece exposto à rampa por mais tempo e em cota mais elevada, ampliando a janela de atuação de perturbações atmosféricas. Para o dimensionamento de OLS, o envelope EASA exigirá superfícies de proteção mais extensas.

A curvatura horizontal da rota FAA "Path Curved" introduz um desvio lateral estrutural de até 82,1 m em relação à linha reta início-fim do trecho ativo (Tabela 2). Esse componente é determinístico e geométrico, não estocástico: sua origem está na curvatura da rota prescrita pela norma, não em perturbação. Conforme demonstrado na Tabela 3, os perfis de desaceleração das duas normas divergem nos gatilhos intermediários (0,38 NM/0,30 NM e 0,20 NM/0,30 NM), o que implica regimes de energia distintos na fase de rampa — diferença que afetará a sensibilidade do eVTOL a perturbações laterais nessa fase.

---

## 4. Framework metodológico para análise de desvios (Monte Carlo)

### 4.1 Variáveis estocásticas de entrada

A Tabela 4 apresenta o contrato de variáveis de entrada para o Monte Carlo. As distribuições específicas serão definidas pelo agente `meteorologist` após análise dos dados METAR históricos do SBSJ e aprovação de ADR.

**Tabela 4 — Variáveis estocásticas de entrada do Monte Carlo**

| Variável | Símbolo | Unidade | Distribuição candidata | Fonte / Observação |
|---|---|---|---|---|
| Velocidade de vento | V_w | kt | Weibull(c, scale) | Comportamento físico assimétrico; parâmetros a definir via METAR SBSJ |
| Direção do vento | θ_w | graus | von Mises(μ, κ) | Variável circular; κ baixo equivale a regime isotrópico |
| Componente de proa | V_proa | kt | Normal(μ, σ) | Projeção escalar de V_w sobre o eixo de aproximação |
| Componente de través | V_traves | kt | Normal(0, σ) | Simétrica em regime sem vento predominante |
| Temperatura | T | °C | Normal(μ_T, σ_T) | Efeito em densidade-altitude; μ_T e σ_T a definir via METAR |
| Semente por iteração | seed_i | int | Determinística | Rastreabilidade individual de cada simulação |

[AMBÍGUO] Os parâmetros numéricos de todas as distribuições dependem de ADR aprovada pelo `meteorologist` com base nos dados METAR do SBSJ. Nenhum valor pode ser adotado antes dessa análise.

### 4.2 Métricas de dispersão

Para cada célula de estratificação (regulação × orientação × rota × fase × cenário meteorológico), calcular:

**Estatísticas de e_y e e_z:**
- Média (μ) e desvio padrão (σ)
- Percentis: P50, P90, P95, P99 e P99,9
- Máximo absoluto (envelope bounding)
- Intervalo de confiança 95% por bootstrap (N_bootstrap ≥ 10.000; implementação: `scipy.stats.bootstrap`)

**Métricas de envelope probabilístico:**
- Raio de contenção lateral R95: distância que engloba 95% das trajetórias
- Elipsoide 2σ no plano (e_y, e_z)
- Fração de conformidade: percentual de trajetórias dentro do envelope nominal EASA/FAA

**Testes de aderência (obrigatórios antes de qualquer ajuste de distribuição):**
- Kolmogorov-Smirnov (KS): `scipy.stats.kstest`, α = 0,05
- Anderson-Darling (AD): `scipy.stats.anderson`, α = 0,05; prioritário para extremos de cauda
- Shapiro-Wilk: `scipy.stats.shapiro`, α = 0,05; apenas para N < 5.000

Mau ajuste deve ser registrado explicitamente — não silenciado. Critério de seleção de distribuição: AIC/BIC mínimo entre candidatas com p-valor KS > 0,05.

### 4.3 Dimensionamento amostral

A Tabela 5 apresenta os valores analíticos de N mínimo para estimativa de quantis por bootstrap, com distribuição assumida como normal.

**Tabela 5 — N mínimo por cenário para estimativa de quantis (bootstrap, IC 95%)**

| Quantil-alvo | Erro máx. relativo | N mínimo (analítico) |
|---|---|---|
| P95 | 10% | 1.715 simulações/cenário |
| P99 | 10% | 5.354 simulações/cenário |
| P95 | 5% | 6.859 simulações/cenário |

**Tabela 6 — Plano amostral por fase de execução**

| Fase | N/cenário | Justificativa |
|---|---|---|
| Piloto (validação) | 100 | Verificar STATELOG e convergência básica |
| Nominal | 500 | P95 com erro ~14%; aceitável para primeira análise |
| Produção | 1.000 | P95 com erro ~10%; P99 subestimado |
| Completo | 5.000 | Rigoroso para P99; necessário para relatório final |

O N recomendado de 1.000 simulações/cenário — adotado como referência inicial — é pragmaticamente adequado para P95, mas insuficiente para P99 com erro < 10% (exigiria N ≥ 5.354, conforme Tabela 5). O relatório final deverá declarar esse caveat explicitamente. O N total estimado para a fase de produção (N = 1.000) é de 48.000 simulações (8 cenários × 6 condições meteorológicas × 1.000 iterações). Critério de convergência: variação do P95 < 1% entre blocos consecutivos de 100 simulações.

---

## 5. Observação crítica: desvio lateral estrutural FAA

A rota FAA "Path Curved" apresenta curvatura horizontal mensurável no CSV, com desvio lateral estrutural (e_y_struct) de até **82,1 m** em relação à linha reta entre o início e o fim do trecho ativo (comprimento do arco: 586,6 m; comprimento da linha reta: 554,4 m; direção: 121,3° no plano local). O P95 desse componente é 81,7 m e a média é 48,1 m.

Esse valor supera amplamente o bound regulatório da safety area FAA (27,4 m, equivalente a 90 ft de meia-largura). A superação não representa violação operacional: o e_y_struct é determinístico e geométrico, decorrente da curvatura prescrita pela própria norma FAA EB-105A, e não de perturbação atmosférica ou erro de controle.

A implicação metodológica é obrigatória: ao calcular e_y a partir dos logs de simulação para a rota FAA, o statistician deve decompor o desvio lateral em componente estrutural (e_y_struct, geométrico, calculado ponto a ponto como distância perpendicular à reta início-fim) e componente estocástico (e_y_stoch = e_y − e_y_struct). Apenas e_y_stoch representa perturbação real e deve ser submetido ao ajuste de distribuição e à comparação com envelopes regulatórios. A omissão dessa decomposição resultaria em distribuições ajustadas que refletem a geometria da rota, não a dispersão induzida por perturbações.

---

## 6. Próximas ações (prioridade)

1. **Verificar o tipo "EVTOL" no BlueSky:** confirmar que os parâmetros de desempenho BADA-H estão carregados no ambiente de execução. Se o tipo não for reconhecido pelo simulador, o comando `CRE` falhará e nenhum log será gerado.
2. **Verificar disponibilidade do plugin UAMMETRICS:** todos os cenários requerem `PLUGIN LOAD UAMMETRICS`; sua presença no ambiente BlueSky não foi confirmada.
3. **Executar cenário nominal (sem perturbação) para cada uma das 8 configurações:** verificar que o STATELOG produz saída não vazia e que as colunas `lat`, `lon`, `distflown`, `alt`, `cas`, `tas`, `gs` estão presentes.
4. **Extrair e processar dados METAR históricos do SBSJ** (mínimo 5 anos) para os 4 regimes sazonais (DJF, JJA, MAM, SON) e definir os parâmetros das distribuições de vento e temperatura via ADR.
5. **Definir envelope de vento operacional** para os rumos de aproximação 0° e 180°: componentes de proa, través e cauda, com estatísticas por regime sazonal.
6. **Escrever script de execução em lote** (`run_montecarlo.py`): variação de semente por iteração, injeção de perturbações atmosféricas via comandos BlueSky, consolidação de logs em DataFrame parquet por cenário.
7. **Calcular e_y e e_z** a partir dos logs brutos, com decomposição estrutural/estocástica para a rota FAA, e entregar parquet estruturado ao statistician conforme contrato de variáveis (Seção 4.1).
8. **Executar ajuste de distribuições e geração de envelopes probabilísticos** (statistician), seguido de verificação de conformidade regulatória com dimensionamento de FATO/TLOF/OLS.

---

## 7. Limitações e premissas declaradas

- **Terra-plana no BlueSky:** as altitudes nos .scn são AGL (pad = 0 ft). A altitude MSL real do pad (639,541 m) e a topografia do vale do Paraíba não são modeladas. O e_z calculado a partir dos logs será relativo ao pad, não absoluto em MSL. A interpolação do perfil nominal (CSVs em MSL) deve ser convertida para AGL antes do cálculo dos resíduos.
- **Tipo "EVTOL" não verificado:** os parâmetros de desempenho do eVTOL nos cenários BlueSky não foram confirmados. Se o modelo não existir no simulador, os cenários falham silenciosamente.
- **Plugin UAMMETRICS não verificado:** necessário para métricas UAM; disponibilidade no ambiente de execução não confirmada.
- **Meteorologia não caracterizada:** os cenários atmosféricos DJF/JJA/MAM/SON e crítico ainda não estão parametrizados. O Monte Carlo completo (48.000 simulações) depende dessa etapa.
- **Distribuições sem ADR aprovada:** as distribuições candidatas estão especificadas (Seção 4.1), mas os parâmetros numéricos dependem de ADR do `meteorologist` baseada em dados reais do SBSJ.
- **N = 1.000 insuficiente para P99:** o plano amostral de produção (N = 1.000/cenário) é adequado para P95 (erro ~10%), mas subestima P99. O relatório final deve declarar esse caveat.
- **Cenários Peres classificados como legados:** os 4 cenários Peres não contêm waypoints de rampa regulatória e não integram a análise da Tarefa 6. São mantidos para referência histórica do procedimento VAC SBSJ.
- **`saida_gerador.txt` vazio (0 bytes):** indica que a saída do script gerador não foi capturada. Não é bloqueador (os .scn existem e estão corretos), mas o ambiente de execução não está documentado.
- **Estratificação obrigatória:** resultados agregados sem estratificação por regulação × orientação × rota × fase × cenário meteorológico não são aceitos como produto da Tarefa 6.

---

*Documento produzido por cadeia de agentes IA: especialista-trajetoria → statistician → technical_writer. Conteúdo técnico baseado em dados reais dos CSVs e cenários BlueSky do projeto.*
