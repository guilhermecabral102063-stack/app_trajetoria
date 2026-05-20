from taipy.gui import Markdown

home_page = Markdown("""
<|container|

# App Trajetória
### Gêmeo Digital — Vertiporto de São José dos Campos (SJC/SBSJ)

---

## Objetivo

Modelagem e visualização de trajetórias de aeronaves eVTOL durante operações de
pouso e decolagem no vertiporto de SJC, com comparação entre os padrões regulatórios
**EASA Subpart 2** e **FAA EB-105A**.

---

## Descrição do sistema

O aplicativo permite a simulação e análise de perfis de rampa de aproximação e decolagem
de aeronaves eVTOL. Os dados são gerados a partir de cenários no simulador BlueSky e
visualizados com gráficos padronizados em Matplotlib.

As trajetórias cobrem o trecho en-route (SBGR → SJK / Taubaté → SJK) e o procedimento
de rampa preciso com waypoints de altitude e velocidade conforme cada regulamentação.

---

## Integrantes responsáveis

| Nome | Instituição |
|------|-------------|
| Guilherme Henrique Coelho Cabral | ITA |

---

## Navegação

<|navbar|>

<|Trajetórias EASA vs. FAA|button|on_action=navigate_trajetorias|class_name=plain|>
<|Comparativo|button|class_name=plain|>
<|Sobre|button|class_name=plain|>

|>
""")
