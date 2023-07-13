from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "Service_A"})
    )
)

agent_host: str = "localhost"
agent_port: int = 6831

jaeger_exporter = JaegerExporter(
    agent_host_name=agent_host,
    agent_port=agent_port,
)

span_processor = BatchSpanProcessor(jaeger_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)


tracer = trace.get_tracer(__name__)
