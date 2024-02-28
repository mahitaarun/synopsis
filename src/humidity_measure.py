from flask import Flask
from prometheus_client import Counter, Histogram, Summary, Gauge, generate_latest
from flask import Response

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
REQUEST_SIZE = Summary('http_request_size_bytes', 'HTTP request size', ['method', 'endpoint'])
RESPONSE_SIZE = Summary('http_response_size_bytes', 'HTTP response size', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('active_http_requests', 'Active HTTP requests')

@app.route('/')
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.labels(method='GET', endpoint='/').time():
        # Your application logic here
        return 'Hello, World!'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True)

