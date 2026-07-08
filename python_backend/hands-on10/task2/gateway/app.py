"""
API Gateway (Hands-On 10 / Task 2, step 102) - a single entry point on
port 5000 that forwards requests to the correct backend service based on
URL prefix:

    /api/courses/*      -> Course Service   (http://127.0.0.1:5001)
    /api/departments/*  -> Course Service   (http://127.0.0.1:5001)
    /api/students/*     -> Student Service  (http://127.0.0.1:5002)

This is intentionally a THIN proxy that just demonstrates the routing
concept. A real API Gateway (e.g. Kong, AWS API Gateway, or a hand-rolled
one used in production) would also handle:
  - authentication / JWT validation in one place instead of per-service
  - rate limiting
  - TLS termination
  - request/response logging and metrics
  - circuit breaking when a backend is down
None of that is implemented here - just routing, so the concept is clear
without those production concerns getting in the way.
"""

import requests
from flask import Flask, Response, request

app = Flask(__name__)

COURSE_SERVICE_URL = "http://127.0.0.1:5001"
STUDENT_SERVICE_URL = "http://127.0.0.1:5002"

# Ordered so the most specific prefix is checked... in this case prefixes
# don't overlap, but this is the natural place to add more services later.
ROUTES = {
    "/api/courses": COURSE_SERVICE_URL,
    "/api/departments": COURSE_SERVICE_URL,
    "/api/students": STUDENT_SERVICE_URL,
}

# Headers that must NOT be forwarded as-is between hops (hop-by-hop headers).
EXCLUDED_HEADERS = {"content-encoding", "content-length", "transfer-encoding", "connection"}


def resolve_target(path: str):
    for prefix, base_url in ROUTES.items():
        if path.startswith(prefix):
            return base_url
    return None


@app.get("/health")
def health():
    return {"service": "api-gateway", "status": "ok"}


@app.route(
    "/<path:path>",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
def proxy(path):
    full_path = f"/{path}"
    target_base = resolve_target(full_path)

    if target_base is None:
        return {"error": {"code": 404, "message": f"No service registered for path {full_path}"}}, 404

    target_url = f"{target_base}{full_path}"

    try:
        upstream_response = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != "host"},
            params=request.args,
            data=request.get_data(),
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        return {"error": {"code": 503, "message": f"Upstream service at {target_base} is unavailable"}}, 503
    except requests.exceptions.Timeout:
        return {"error": {"code": 503, "message": f"Upstream service at {target_base} timed out"}}, 503

    response_headers = [
        (k, v) for k, v in upstream_response.raw.headers.items() if k.lower() not in EXCLUDED_HEADERS
    ]
    return Response(upstream_response.content, upstream_response.status_code, response_headers)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
