# 🧠 Projeto de Observabilidade - Flask App

Este projeto é uma arquitetura completa de observabilidade para uma aplicação Flask que simula jogadas de dado. Ele reúne métricas, logs e traces utilizando ferramentas open source modernas como Prometheus, Grafana, Jaeger, OpenTelemetry e Redis.

## 🔧 Tecnologias Utilizadas

- **Flask** — Aplicação principal (simula jogadas de dado)
- **Prometheus** — Coleta de métricas
- **Grafana** — Visualização de métricas e dashboards
- **Jaeger** — Tracing distribuído via OpenTelemetry
- **Redis** — Armazena histórico das jogadas de dado
- **cAdvisor** — Métricas de containers Docker
- **Node Exporter** — Métricas do host
- **OpenTelemetry Collector** — Coleta e exporta métricas/traces

## 📊 Dashboard de Observabilidade

O Grafana carrega automaticamente o dashboard `Observabilidade - Flask App` com as seguintes visualizações:

### 🎲 Métricas de Aplicação

- **Requisições por segundo**
- **Erros 5xx**
- **Tempo de resposta P95**
- **Histograma de resposta**
- **Requisições por status**
- **Jogadas de dado por valor**
- **Top 5 valores mais jogados**

### 🧩 Tracing (via Jaeger)

- **GET /**, **GET /metrics**, **GET /health**, **GET /history**
- **LPUSH** e **LRANGE** em Redis

### 🖥️ Infraestrutura

- **Tráfego de rede da interface eth0**
- **Espaço em disco**

## 🚀 Subindo o projeto

### Pré-requisitos

- Docker + Docker Compose
- Git

### Comandos

```bash
# Clone o repositório
git clone https://github.com/allysonchristiann/projeto-observabilidade.git
cd projeto-observabilidade

# Suba todos os serviços
docker compose up -d
```

### Acesso aos serviços

| Serviço       | URL                     |
|---------------|--------------------------|
| Flask App     | http://localhost:5000    |
| Prometheus    | http://localhost:9090    |
| Grafana       | http://localhost:3000    |
| Jaeger        | http://localhost:16686   |
| cAdvisor      | http://localhost:8080    |

**Login do Grafana:**  
Usuário: `admin`  
Senha: `admin`

## 📈 Prometheus

Arquivo de configuração: [`prometheus/prometheus.yml`](prometheus/prometheus.yml)  
Regras de alertas: [`prometheus/rules.yml`](prometheus/rules.yml)

Inclui alertas como:

- Alta taxa de erros 500
- Ausência de requisições
- Falhas frequentes

## 🔍 OpenTelemetry + Tracing

- O `otel-collector.yaml` define a coleta de traces da aplicação e o envio ao Jaeger.
- Todas as rotas da aplicação Flask são automaticamente instrumentadas.

## 📁 Estrutura do Projeto

```
projeto-observabilidade/
├── build/                     # Código da aplicação Flask
│   └── app.py
├── compose.yml                # Compose de todos os serviços
├── grafana/
│   ├── dashboards/            # Dashboard JSON
│   └── provisioning/          # Provisionamento automático
│       ├── dashboards/
│       └── datasources/
├── prometheus/
│   ├── prometheus.yml
│   └── rules.yml
├── otel-collector.yaml        # Configuração do Otel Collector
├── send-requests.sh           # Script de simulação de carga
└── README.md                  # Este arquivo
```