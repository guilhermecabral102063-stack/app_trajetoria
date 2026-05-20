# app-trajetoria

Aplicativo de Trajetória — módulo do Gêmeo Digital do Vertiporto de São José dos Campos (SJC/SBSJ).

## Objetivo

Modelagem, simulação e visualização de trajetórias de aeronaves eVTOL durante operações de pouso e decolagem no vertiporto de SJC, com comparação entre padrões regulatórios EASA e FAA.

## Tecnologias

- [Taipy](https://taipy.io/) — interface gráfica e navegação
- [Matplotlib](https://matplotlib.org/) — visualização de trajetórias
- [Docker](https://www.docker.com/) — containerização

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

MIT — veja [LICENSE](LICENSE)
