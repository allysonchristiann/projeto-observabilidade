from flask import Flask, jsonify
from random import randint
import redis
import logging

from prometheus_flask_exporter import PrometheusMetrics

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# === OpenTelemetry Metrics ===
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider

# === Configuração do Tracing ===
resource = Resource.create({"service.name": "flask-dice-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
)

# === Configuração de Métricas OTLP ===
exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter("flask-dice-app")

# === Métrica OTLP personalizada ===
request_counter = meter.create_counter(
    "app_requests_total",
    unit="1",
    description="Contador de requisições da aplicação"
)

# === Aplicação Flask ===
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RedisInstrumentor().instrument()
metrics = PrometheusMetrics(app)

# === Métrica Prometheus (direta) ===
from prometheus_client import Counter
dice_rolls_total = Counter(
    'dice_rolls_total', 'Total de jogadas de dado', ['dice_value']
)

r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def roll_dice():
    request_counter.add(1, {"endpoint": "/"})
    dice_value = randint(1, 6)
    dice_rolls_total.labels(dice_value=str(dice_value)).inc()
    r.lpush('history', dice_value)
    app.logger.info(f'Jogada de dado: {dice_value}')
    return jsonify({'dice_value': dice_value})

@app.route('/history')
def history():
    request_counter.add(1, {"endpoint": "/history"})
    app.logger.info('Histórico de jogadas acessado.')
    return jsonify({'last_rolls': r.lrange('history', 0, 9)})

@app.route('/health')
def health():
    request_counter.add(1, {"endpoint": "/health"})
    return jsonify({'status': 'ok'})

@app.route('/fail')
def fail():
    request_counter.add(1, {"endpoint": "/fail"})
    app.logger.info('Falha proposital acionada.')
    1 / 0

@app.errorhandler(500)
def handle_500(error):
    trace_id = trace.get_current_span().get_span_context().trace_id
    span_id = trace.get_current_span().get_span_context().span_id
    app.logger.info(f"Erro 500: {error}", extra={"trace_id": trace_id, "span_id": span_id})
    return str(error), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
