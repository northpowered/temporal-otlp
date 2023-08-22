from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from env import SERVICE_LETTER, TEMPO_ENDPOINT


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: f"Service_{SERVICE_LETTER}"}),
    )
)

tempo_exporter = OTLPSpanExporter(endpoint=TEMPO_ENDPOINT)

tempo_span_processor = BatchSpanProcessor(tempo_exporter)

tracer = trace.get_tracer_provider()

tracer.add_span_processor(tempo_span_processor)

tracer = trace.get_tracer(__name__)
