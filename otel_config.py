from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

def configure_opentelemetry(app):
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
    tracer_provider.add_span_processor(span_processor)
    
    FlaskInstrumentor().instrument_app(app)