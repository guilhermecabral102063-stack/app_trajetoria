# Analise Estatistica -- Tarefa 6

**Data:** 2026-05-20 | **Agente:** statistician | **Destino:** technical_writer  
**Normas:** EASA PTS-VPT-DSN Subpart 2 / FAA AC 150/5390-2D + EB-105A  
**CSVs lidos:** `trajetorias_rampas_vertiporto_EASA_Subpart_2.csv` (1.948 linhas) | `trajetorias_rampas_vertiporto_FAA_eb_105a.csv` (1.180 linhas)  
**Ponto de referencia:** TLOF/FATO -23.231441, -45.862719 | Altitude pad: 639,541 m MSL | EPSG:31983

---

## 1. Estatisticas Descritivas das Trajetorias Nominais

Todos os valores referem-se ao subconjunto `point_type == centerline`. R1/R2 sao simetricos (mesmos valores numericos, orientacoes opostas); idem P1/P2.

### 1.1 Variavel `distance_along_m`

| Rampa | n | media (m) | sigma (m) | min (m) | max (m) | P25 (m) | P50 (m) | P75 (m) | P95 (m) |
|-------|---|-----------|-----------|---------|---------|---------|---------|---------|---------|
| EASA R1 (0 deg) | 974 | 523,462 | 281,382 | 0,000 | 1.010,000 | 280,250 | 523,500 | 766,750 | 961,350 |
| EASA R2 (180 deg) | 974 | 523,462 | 281,382 | 0,000 | 1.010,000 | 280,250 | 523,500 | 766,750 | 961,350 |
| FAA P1 (0 deg) | 590 | 308,492 | 170,403 | 0,000 | 602,848 | 161,354 | 308,507 | 455,677 | 573,414 |
| FAA P2 (180 deg) | 590 | 308,492 | 170,403 | 0,000 | 602,848 | 161,354 | 308,507 | 455,677 | 573,414 |

> Nota: distribuicao uniforme esperada (amostragem a passo ~1 m). sigma/media ~ 0,538 (EASA) e 0,552 (FAA), consistente com distribuicao uniforme teorica (sigma/media = 1/sqrt(3) ~ 0,577 para U[0,L]).

### 1.2 Variavel `alt_m` (MSL, metros)

| Rampa | n | media (m) | sigma (m) | min (m) | max (m) | P25 (m) | P50 (m) | P75 (m) | P95 (m) |
|-------|---|-----------|-----------|---------|---------|---------|---------|---------|---------|
| EASA R1 (0 deg) | 974 | 730,697 | 35,232 | 639,541 | 791,541 | 700,322 | 730,729 | 761,135 | 785,460 |
| EASA R2 (180 deg) | 974 | 730,697 | 35,232 | 639,541 | 791,541 | 700,322 | 730,729 | 761,135 | 785,460 |
| FAA P1 (0 deg) | 590 | 676,205 | 21,295 | 639,541 | 712,997 | 657,810 | 676,205 | 694,601 | 709,318 |
| FAA P2 (180 deg) | 590 | 676,205 | 21,295 | 639,541 | 712,997 | 657,810 | 676,205 | 694,601 | 709,318 |

### 1.3 Pontos de controle da rampa ativa

**EASA (trecho ativo: 40--1.010 m):**

| dist (m) | alt MSL (m) | AGL pad (m) | AGL pad (ft) |
|----------|-------------|-------------|--------------|
| 40,0 | 670,291 | 30,750 | 100,9 |
| 200,0 | 690,291 | 50,750 | 166,5 |
| 400,0 | 715,291 | 75,750 | 248,5 |
| 600,0 | 740,291 | 100,750 | 330,5 |
| 800,0 | 765,291 | 125,750 | 412,6 |
| 1.010,0 | 791,541 | 152,000 | 498,7 |

**FAA (trecho ativo: 16--603 m):**

| dist (m) | alt MSL (m) | AGL pad (m) | AGL pad (ft) |
|----------|-------------|-------------|--------------|
| 16,2 | 639,666 | 0,125 | 0,4 |
| 100,1 | 650,159 | 10,618 | 34,8 |
| 200,1 | 662,650 | 23,109 | 75,8 |
| 300,0 | 675,142 | 35,601 | 116,8 |
| 400,0 | 687,635 | 48,094 | 157,8 |
| 499,9 | 700,129 | 60,588 | 198,8 |
| 601,8 | 712,872 | 73,331 | 240,6 |

---

## 2. Regressao do Perfil de Altitude

**Metodo:** regressao linear simples `alt_m ~ distance_along_m` (scipy.stats.linregress), excluindo zona de transicao (EASA: dist < 40 m; FAA: dist < 16 m).

| Rampa | n_reg | coef (m/m) | intercepto (m) | R^2 | grad (%) | grad (graus) | max |resid| (m) |
|-------|-------|-----------|---------------|-----|----------|--------------|---------------------|
| EASA R1 | 971 | 0,125000 | 665,2910 | 1,000000 | 12,500% | 7,125 | 0,0000 |
| EASA R2 | 971 | 0,125000 | 665,2910 | 1,000000 | 12,500% | 7,125 | 0,0000 |
| FAA P1 | 588 | 0,125000 | 637,6407 | 1,000000 | 12,500% | 7,125 | 0,0005 |
| FAA P2 | 588 | 0,125000 | 637,6407 | 1,000000 | 12,500% | 7,125 | 0,0005 |

**Interpretacao:**
- Perfil de altitude e perfeitamente linear em ambas as normas no trecho ativo (R^2 = 1,000000 EASA; 1,000000 FAA -- residuo maximo 0,5 mm, atribuivel a arredondamento numerico).
- Gradiente identico: 0,1250 m/m = 12,50% = 7,125 deg em ambas as normas.
- Os dois interceptos diferem (665,29 vs 637,64 m) porque a rampa FAA e mais curta e inicia mais proximo ao nivel do pad.
- **Nao ha nao-linearidade para modelar**: a variancia da regressao e zero (trajetoria nominal deterministica). O desvio residual relevante aparecera apenas apos execucao das simulacoes Monte Carlo.

**Zona de transicao EASA (0--40 m):**
- 3 pontos: dist=0 m (alt=639,541), dist=38 m (alt=670,041), dist=40 m (alt=670,291).
- Gradiente abrupto: (670,291 - 639,541) / 40 = 0,7688 m/m = 76,88% -- zona hover/FATO, nao e rampa.

**Zona plana FAA (0--16 m):**
- 2 pontos: dist=0 m e dist=15,2 m, ambos com alt=639,541 m -- gradiente zero, zona de flare sobre o TLOF.

---

## 3. Comparativo EASA vs. FAA

| Dimensao | EASA Subpart 2 | FAA EB-105A | Razao EASA/FAA |
|----------|---------------|-------------|----------------|
| Extensao horizontal total | 1.010,0 m | 602,848 m | 1,675 |
| Trecho ativo (excl. transicao) | 970,0 m | 586,6 m | 1,655 |
| Delta altitude total | 152,000 m (498,7 ft) | 73,456 m (240,9 ft) | 2,069 |
| Altitude de entrada | 791,541 m MSL | 712,997 m MSL | -- (diff: +78,5 m) |
| Gradiente de descida | 12,50% (7,125 deg) | 12,50% (7,125 deg) | 1,000 |
| n pontos centerline | 974 | 590 | 1,651 |
| Passo medio entre pontos | 1,038 m | 1,024 m | 1,014 |
| Curvatura horizontal | reta (planar) | curva (Path Curved) | -- |
| Zona de transicao | 3 pts, 0--40 m, salto abrupto | 2 pts, 0--15,2 m, nivel | -- |
| Desvio lateral estrutural (e_y_struct) | 0,000 m (reta) | max 82,1 m; P95 81,7 m; media 48,1 m | -- |
| R^2 perfil vertical | 1,000000 | 1,000000 | -- |
| max residuo regressao | 0,000 m | 0,0005 m | -- |

**Implicacoes para o Monte Carlo:**

1. **EASA exige envelope maior em altitude**: com delta-alt 2,07x maior e extensao 1,68x maior, o espaco de risco e substancialmente mais amplo que o FAA.
2. **FAA gera e_y estrutural de ate 82 m**: a curvatura da rota FAA cria desvio lateral entre a linha reta inicio-fim e a trajetoria real. O statistician devera decompor e_y em componente estrutural (geometrico, deterministico) e componente estocastico (perturbacoes). Esta decomposicao e **obrigatoria** antes do ajuste de distribuicao.
3. **Mesma inclinacao**: o gradiente identico de 12,5% permite comparar regimes de desaceleracao EASA vs. FAA com a mesma referencia angular, isolando apenas o efeito do comprimento e da curvatura horizontal.

---

## 4. Framework Monte Carlo -- Contrato de Implementacao

### 4.1 Variaveis Estocasticas de Entrada

| Variavel | Simbolo | Unidade | Tipo | Distribuicao candidata | Justificativa |
|----------|---------|---------|------|----------------------|---------------|
| Velocidade de vento | V_w | kt | continua | Weibull(c, scale) | comportamento fisico assimetrico |
| Direcao do vento | theta_w | graus | circular | von Mises(mu, kappa) | variavel circular; kappa baixo = isotrópico |
| Componente proa | V_proa | kt | continua | Normal(mu, sigma) | projecao escalar de V_w sobre o eixo de aproximacao |
| Componente traves | V_traves | kt | continua | Normal(0, sigma) | simetrico em regime sem vento predominante |
| Temperatura | T | degC | continua | Normal(mu_T, sigma_T) | efeito em densidade-altitude |
| Semente por iteracao | seed_i | int | deterministica | -- | rastreabilidade |

> Nota: distribuicoes especificas serao definidas pelo meteorologist apos analise METAR SBSJ. O statistician implementa os fits apos ADR aprovada -- nao decide a distribuicao.

**Variaveis de saida a calcular por iteracao (contrato com especialista-trajetoria):**

| Variavel | Descricao | Formula |
|----------|-----------|---------|
| e_y(t) | Desvio cross-track | dist. perpendicular ao centerline nominal (CSVs de referencia) |
| e_z(t) | Desvio vertical | alt_simulada(t) - alt_nominal(dist_pad(t)) interpolada no CSV |
| dist_pad_m | Distancia ao pad | convertida de dist_flown relativa ao WPT POUSO_FINAL |
| fase_voo | Segmento | cruzeiro / pre-rampa / rampa / hover / pouso por dist ao pad |
| e_y_struct | Componente estrutural (FAA) | distancia ponto-a-linha(reta inicio->fim) da rota curva |
| e_y_stoch | Componente estocastico | e_y - e_y_struct |

### 4.2 Metricas de Dispersao a Calcular

Por celula de estratificacao (regulacao x orientacao x rota x fase x cenario_met):

**Estatisticas de e_y e e_z:**

| Metrica | Simbolo | Descricao |
|---------|---------|-----------|
| Media | mu | tendencia central |
| Desvio padrao | sigma | dispersao |
| P50, P90, P95, P99, P99,9 | -- | quantis operacionais |
| Maximo absoluto | max|e| | envelope bounding |
| IC 95% bootstrap | [q_low, q_hi] | N_bootstrap >= 10.000 (scipy.stats.bootstrap) |

**Metricas de envelope probabilistico:**

| Metrica | Descricao |
|---------|-----------|
| R95 | raio de contencao lateral que engloba 95% das trajetorias |
| Elipsoide 2-sigma | volume no plano (e_y, e_z) |
| Fracao de conformidade | % trajetorias dentro do envelope nominal EASA/FAA |

### 4.3 Testes de Aderencia

Aplicar obrigatoriamente antes de qualquer ajuste de distribuicao:

| Teste | Implementacao | Nivel alfa | Uso |
|-------|--------------|------------|-----|
| Kolmogorov-Smirnov | `scipy.stats.kstest` | 0,05 | geral; comparacao bilateral |
| Anderson-Darling | `scipy.stats.anderson` | 0,05 | sensivel as caudas; prioritario para extremos |
| Shapiro-Wilk | `scipy.stats.shapiro` | 0,05 | apenas N < 5.000; normalidade |

Diagnosticos visuais complementares (minimo): histograma com PDF ajustada, QQ-plot, PIT histogram, residual plot vs. distancia ao pad.

**Criterio de aderencia:** p-valor KS > 0,05 E estatistica AD < critico 5%. Mau ajuste e registrado explicitamente -- nao silenciado.

### 4.4 Distribuicoes Candidatas por Variavel

| Variavel | Distribuicoes candidatas | Prioridade | Justificativa fisica |
|----------|------------------------|------------|---------------------|
| e_y (desvio lateral) | Normal(0,sigma), Laplace(0,b) | Normal primeiro | simetria esperada; Laplace para caudas pesadas |
| |e_y| (magnitude lateral) | Rayleigh(sigma), Half-normal, Weibull | Rayleigh para vento isotrópico | magnitude nao-negativa |
| e_z (desvio vertical) | Normal(mu,sigma), Logistica(mu,s) | Normal primeiro | perturbacoes simetricas em torno da rampa |
| e_y fase hover | Normal(mu!=0, sigma) | -- | viés de controle possivel; mu != 0 e hipotese a testar |
| e_y fase rampa FAA | GMM 2-3 componentes | -- | bimodalidade por curvatura horizontal |
| V_w | Weibull(c, scale) | -- | padrao fisico estabelecido para vento |

**Selecao de distribuicao:** AIC/BIC minimo entre candidatas com p-valor KS > 0,05. Distribuicao escolhida sera registrada em ADR pelo meteorologist.

### 4.5 Dimensionamento Amostral

**Calculo analitico de N minimo (regra de bootstrap para quantis):**

Para IC 95% com erro relativo < 10% no quantil estimado, assumindo distribuicao normal:

| Quantil-alvo | Erro max | N minimo (analitico) |
|--------------|----------|---------------------|
| P95 | 10% | 1.715 simulacoes/cenario |
| P99 | 10% | 5.354 simulacoes/cenario |
| P95 | 5% | 6.859 simulacoes/cenario |

**Recomendacao pratica (balanco custo-computacional):**

| Fase | N/cenario | Justificativa |
|------|-----------|---------------|
| Piloto (validacao) | 100 | verificar STATELOG e convergencia basica |
| Nominal | 500 | aceitavel para P95 (erro ~14%) |
| Producao | 1.000 | pragmatico; P95 com erro ~10%; P99 subestimado |
| Completo | 5.000 | rigoroso para P99; recomendado para relatorio final |

**N total estimado:**

| Configuracao | Calculo | Total |
|-------------|---------|-------|
| Minimo (N=500) | 8 cenarios x 6 cond_met x 500 | 24.000 simulacoes |
| Recomendado (N=1.000) | 8 cenarios x 6 cond_met x 1.000 | 48.000 simulacoes |
| Completo (N=5.000) | 8 cenarios x 6 cond_met x 5.000 | 240.000 simulacoes |

**Criterio de convergencia:** variacao do P95 < 1% entre blocos consecutivos de 100 simulacoes. Avaliacao em N = {100, 200, 300, ..., N_max}.

**Estratificacao obrigatoria (resultados agregados nao aceitos):**

| Dimensao | Niveis |
|----------|--------|
| Regulacao | EASA, FAA |
| Configuracao | R1/P1 (0 deg), R2/P2 (180 deg) |
| Rota de origem | SBGR, Taubate |
| Fase de voo | cruzeiro, pre-rampa, rampa, hover, pouso |
| Cenario meteorologico | nominal, DJF, JJA, MAM, SON, critico |
| Semente | por iteracao (rastreabilidade individual) |

---

## 5. Envelope Nominal Estimado (Geometria Apenas)

**Aviso:** na ausencia de logs de simulacao, os valores abaixo sao estimativas geometricas conservadoras para planejamento do framework Monte Carlo. Nao substituem analise probabilistica real.

### 5.1 Desvio lateral estrutural FAA (componente deterministico)

A rota FAA Path Curved tem curvatura horizontal mensuravel no CSV. Distancia de cada ponto da rota ativa (dist >= 16 m) a linha reta entre inicio e fim:

| Metrica | e_y_struct (m) |
|---------|----------------|
| Maximo absoluto | 82,1 m |
| P95 | 81,7 m |
| Media | 48,1 m |
| Comprimento linha reta inicio->fim | 554,4 m |
| Comprimento do arco | 586,6 m |
| Direcao da linha reta | 121,3 deg (plano local) |

**Consequencia direta:** ao calcular e_y a partir dos logs, o statistician DEVE subtrair e_y_struct por ponto antes de ajustar qualquer distribuicao estocastica para a rota FAA. Caso contrario, a distribuicao ajustada refletira a geometria da rota, nao a perturbacao.

### 5.2 Estimativa conservadora de dispersao esperada

| Fase | Variavel | Estimativa P95 | Base da estimativa |
|------|----------|---------------|--------------------|
| Rampa | e_z | EASA +/-11,4 m; FAA +/-5,5 m | 7,5% do delta-alt respectivo |
| Hover | e_z | +/- 3 m | referencia operacional UAM (sem dado local) |
| Rampa | e_y (estocastico) | +/- 27,4 m | FAA safety area half-width (90 ft = 27,4 m) como bound superior |
| Rampa EASA | e_y | +/- 27,4 m (bound) | sem dado; mesmo bound FAA aplicado conservadoramente |

> Estas estimativas serao substituidas pelos valores reais calculados a partir dos logs de simulacao. Usar apenas para dimensionamento preliminar de escalas em graficos e definicao de limites de alertas no dashboard.

---

## Resumo Executivo

As trajetorias nominais EASA e FAA sao **perfeitamente deterministicas** no trecho ativo (R^2 = 1,000000, residuo maximo 0,5 mm): nao ha variancia para modelar neste estagio. O gradiente de descida e identico em ambas as normas (0,1250 m/m = 12,5%), diferindo apenas na extensao (EASA 1,68x maior) e no delta de altitude (EASA 2,07x maior). A curvatura horizontal da rota FAA gera um desvio lateral estrutural de ate **82,1 m** que precisa ser isolado antes de qualquer ajuste de distribuicao estocastica. O framework Monte Carlo esta completamente especificado (contrato de variaveis, metricas, testes, dimensionamento amostral), mas **nenhuma simulacao foi executada**: o bloqueador critico e a ausencia total de logs do BlueSky.

---

## Artefatos Produzidos

- `C:\Users\Guilherme Cabral\Desktop\Projeto - Vertimob\Aplicativo - Trajetória\analise_statistician.md` -- este documento

---

## Pendencias / Riscos

1. **BLOQUEADOR CRITICO:** Nenhum log de simulacao BlueSky existe. Toda analise probabilistica (e_y, e_z, envelopes, Monte Carlo) esta bloqueada ate a execucao dos 8 cenarios nominais.
2. **N recomendado vs. rigor estatistico:** N=1.000/cenario e pragmatico mas insuficiente para P99 com erro < 10% (exigiria N >= 5.354). O relatorio final devera declarar esse caveat explicitamente.
3. **e_y estrutural FAA (82 m):** Valor muito superior ao bound regulatorio (27,4 m safety area). Isso indica que a rota FAA Curved se afasta consideravelmente da linha reta inicio-fim -- e esperado pela geometria curva, mas **o componente estocastico sera muito menor**. A decomposicao estrutural/estocastico e obrigatoria.
4. **Distribuicoes sem ADR aprovada:** O statistician registra as candidatas mas nao pode escolher sem ADR do meteorologist. Bloqueio parcial na camada de ajuste de distribuicao.
5. **Caracterizacao meteorologica SBSJ ausente:** Os cenarios DJF/JJA/MAM/SON/critico nao estao parametrizados. Monte Carlo completo (48.000 simulacoes) depende disso.
6. **Premissa terra-plana BlueSky:** e_z calculado a partir dos logs sera relativo ao pad (AGL), nao absoluto MSL. O statistician deve garantir que a interpolacao do perfil nominal (dos CSVs, em MSL) seja convertida para AGL antes de calcular os residuos.
7. **Tipo EVTOL no BlueSky:** Nao confirmado. Se o modelo de performance nao existir, os cenarios falham na criacao da aeronave e nenhum log e gerado.

---

## Proximo Passo Sugerido

Executar os 8 cenarios BlueSky em modo nominal (sem perturbacao atmosferica), capturar os logs STATELOG e confirmar que a aeronave EVTOL e reconhecida pelo simulador -- isso destrava toda a cadeia estatistica da Tarefa 6.
