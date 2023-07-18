from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from env import SERVICE_LETTER
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: f"Service_{SERVICE_LETTER}"})
    )
)

agent_host: str = "localhost"
agent_port: int = 6831

jaeger_exporter = JaegerExporter(
    agent_host_name=agent_host,
    agent_port=agent_port,
)

tempo_exporter = OTLPSpanExporter(
    endpoint="http://127.0.0.1:4317"
)

jaeger_span_processor = BatchSpanProcessor(jaeger_exporter)
tempo_span_processor = BatchSpanProcessor(tempo_exporter)


tracer = trace.get_tracer_provider()

tracer.add_span_processor(jaeger_span_processor)
tracer.add_span_processor(tempo_span_processor)


tracer = trace.get_tracer(__name__)
