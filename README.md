# app-trajetoria

Aplicativo de Trajetória — módulo do Gêmeo Digital do Vertiporto de São José dos Campos (SJC/SBSJ).

## Objetivo

Modelagem, simulação e visualização de trajetórias de aeronaves eVTOL durante operações de pouso e decolagem no vertiporto de SJC, com comparação entre padrões regulatórios EASA e FAA.

## Tecnologias

- [Taipy](https://taipy.io/) — interface gráfica e navegação
- [Matplotlib](https://matplotlib.org/) — visualização de trajetórias
- [Docker](https://www.docker.com/) — containerização
- [BlueSky](https://github.com/TUDelft-CNS-ATM/bluesky) — motor de simulação de tráfego aéreo (componente externo)

## Como executar localmente

```bash
pip install -r requirements.txt
python app/main.py
```

Acesse em: `http://localhost:5000`

## Como executar com Docker

```bash
docker build -t app-trajetoria .
docker run -p 5000:5000 app-trajetoria
```

## Estrutura

```
app-trajetoria/
├── app/
│   ├── main.py          # entrada principal Taipy
│   └── pages/
│       └── home.py      # página inicial
├── agents/
│   └── especialista-trajetoria.md
├── Dockerfile
├── requirements.txt
└── LICENSE
```

## Integrantes responsáveis

- Guilherme Henrique Coelho Cabral (ITA)

## Licença

Este aplicativo é distribuído sob a licença **MIT** — veja [LICENSE](LICENSE).

### Motor de simulação

As trajetórias exibidas neste aplicativo são geradas pelo **BlueSky ATC Simulator**, desenvolvido pela TU Delft e distribuído sob a licença **GNU GPL v3**.

> Hoekstra, J. M. e Ellerbroek, J. "BlueSky ATC Simulator Project: an Open Data and Open Source Approach". *Proceedings of the 7th ICRAT*, 2016.

O BlueSky é utilizado como ferramenta externa de simulação — seu código não é incorporado a este aplicativo. Os dados de saída (trajetórias em CSV e cenários `.scn`) são consumidos pela interface Taipy como arquivos independentes. As licenças dos dois componentes são, portanto, compatíveis nesta arquitetura.
