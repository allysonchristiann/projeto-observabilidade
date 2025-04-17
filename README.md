### 📌 Projeto de Observabilidade - Flask + OpenTelemetry

Este projeto tem como objetivo implementar uma stack de observabilidade completa utilizando:

- Aplicação Python (Flask)
- OpenTelemetry (para métricas, logs e traces)
- Prometheus (coleta de métricas)
- Grafana (dashboard)
- Jaeger (tracing)
- Docker Compose

---

## ⚠️ Principais Erros e Soluções Durante a Implementação

### 🧱 Etapa: OpenTelemetry Collector

- **Erro**: o container `otel-collector` reiniciava constantemente.
- **Motivo**: uso do `exporter: logging` que está deprecated.
- **Solução**:
  - Substituído por exporters válidos como `otlp`, `prometheus` e `jaeger`.
  - Corrigido o `receivers` e `pipelines` no `otel-collector-config.yaml`.

### 🐍 Etapa: Instrumentação da aplicação Flask

- **Erro**: métricas não apareciam no Prometheus.
- **Motivo**: a aplicação Flask não estava expondo o endpoint `/metrics`.
- **Solução**: incluímos:
  ```python
  from prometheus_client import start_http_server
  start_http_server(8000)
  ```
  no `app.py`.

### 📊 Etapa: Dashboards e Visualização

- **Problema**: dashboards no Grafana estavam “feios” e pouco informativos.
- **Solução**:
  - Criamos um novo dashboard do zero com:
    - Latência média por endpoint
    - Status da aplicação
    - Requisições por segundo
    - Erros 5xx
    - Service Map (via Jaeger)
    - Tempo de resposta P95

---

## ✅ Melhorias implementadas

- Logging estruturado com `trace_id` e `span_id`
- Métrica customizada: tempo de resposta
- Dashboard Jaeger para dependências
- Histogramas no Grafana
- Anotações com eventos
- Healthcheck com alerta real via Prometheus

---

## ✅ Componentes

| Componente        | Porta | Função                            |
|------------------|-------|-----------------------------------|
| Flask App         | 5000  | API principal simulando dados    |
| Prometheus        | 9090  | Coleta métricas do Collector     |
| Grafana           | 3000  | Visualização de métricas         |
| Jaeger UI         | 16686 | Visualização de traces           |
| Otel Collector    | 4317  | Recebe spans e métricas          |

---

# Clone o repositório
git clone https://github.com/allysonchristiann/projeto-observabilidade.git
cd projeto-observabilidade

# Suba todos os serviços
docker compose up -d

# Inicie as requisições automáticas
chmod +x send-requests.sh
nohup ./send-requests.sh > output.log 2>&1 &

---

## 📊 Acessos e Endpoints

| Serviço   | URL                                      |
|-----------|-------------------------------------------|
| API       | http://localhost:5000/roll-dice           |
| Prometheus| http://localhost:9090                     |
| Grafana   | http://localhost:3000                     |
| Jaeger    | http://localhost:16686                    |

---

## 💬 Comandos de teste

Enviar requisições automáticas para gerar observabilidade:
```bash
chmod +x send-requests.sh
nohup ./send-requests.sh > output.log 2>&1 &
```

---

## 👀 O que observar nos dashboards

- **Tempo de resposta médio (P95)**
- **Service Map** via Jaeger
- **Logs com trace_id e span_id**
- **Falhas (status 500) e alertas no Prometheus**
- **Histogramas reais de resposta**
- **Requisições por segundo e status da aplicação**

