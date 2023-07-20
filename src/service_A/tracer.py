from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from env import SERVICE_LETTER, JAEGER_HOST, JAEGER_PORT, TEMPO_ENDPOINT


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: f"Service_{SERVICE_LETTER}"})
    )
)


jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_HOST,
    agent_port=JAEGER_PORT,
)

tempo_exporter = OTLPSpanExporter(endpoint=TEMPO_ENDPOINT)

jaeger_span_processor = BatchSpanProcessor(jaeger_exporter)
tempo_span_processor = BatchSpanProcessor(tempo_exporter)


tracer = trace.get_tracer_provider()

tracer.add_span_processor(jaeger_span_processor)
tracer.add_span_processor(tempo_span_processor)


tracer = trace.get_tracer(__name__)
