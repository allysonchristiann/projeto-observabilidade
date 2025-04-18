# Projeto de Observabilidade com Flask, Prometheus, Grafana, Jaeger e OpenTelemetry

Este projeto demonstra uma arquitetura completa de observabilidade para uma aplicação Flask que simula jogadas de dado. Utilizamos:

- **Prometheus** para métricas
- **Grafana** para visualização
- **Jaeger** para traces
- **OpenTelemetry** para instrumentação
- **Redis** para armazenamento das jogadas
- **Docker Compose** para orquestração dos serviços

---

## 📦 Como rodar o projeto do zero

> Requisitos: Docker e Docker Compose

```bash
# 1. Clone o repositório
git clone https://github.com/allysonchristiann/projeto-observabilidade.git
cd projeto-observabilidade

# 2. Suba todos os containers com build automático da aplicação Flask
docker compose up --build -d
```

---

## 🔍 Acessos rápidos

- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Usuário: `admin` | Senha: `admin`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Jaeger**: [http://localhost:16686](http://localhost:16686)
- **Aplicação Flask**: [http://localhost:5000](http://localhost:5000)

---

## 📊 Dashboards no Grafana

O Grafana já vem configurado com painéis automáticos:

- Requisições por segundo
- Erros 5xx
- Tempo de resposta P95
- Tempo de resposta por rota
- Status por código HTTP
- Métricas do Redis
- Traces por endpoint (via Jaeger)
- Métricas de infraestrutura (CPU, disco, rede)

---

## 🧠 Arquitetura

Todos os serviços são orquestrados via `docker compose` e estão configurados no arquivo `compose.yml`.

---

## 🐛 Possíveis problemas na primeira instalação

- **Erro de pull da imagem `server`**:
  Isso é esperado caso o build ainda não tenha sido feito. Use sempre `docker compose up --build -d`.

- **Timeout ao baixar imagens (como `grafana/grafana`)**:
  Pode ocorrer por problemas temporários de rede. Basta executar novamente `docker compose up --build`.

---

Atualizado em: 18/04/2025 02:14:00
