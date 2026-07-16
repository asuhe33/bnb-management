"""
Flask 网关层
- 托管 frontend 静态资源
- /api/* 反向代理到 FastAPI (http://localhost:8000)
- 统一通过 5000 端口对外提供服务
"""
import os

import requests
from flask import Flask, send_from_directory, request, Response

app = Flask(__name__, static_folder="static", static_url_path="")

FASTAPI_BASE = os.environ.get("FASTAPI_URL", "http://localhost:8000")


def _proxy(method: str, path: str) -> Response:
    """将请求转发到 FastAPI"""
    url = f"{FASTAPI_BASE}/{path}"
    headers = {
        k: v
        for k, v in request.headers
        if k.lower() not in ("host", "content-length")
    }
    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=30,
        )
    except requests.ConnectionError:
        return Response(
            '{"detail":"后端 API 服务未启动"}',
            status=502,
            mimetype="application/json",
        )

    # 过滤 hop-by-hop 响应头
    excluded = {"transfer-encoding", "connection", "keep-alive"}
    headers = [
        (k, v) for k, v in resp.headers.items() if k.lower() not in excluded
    ]
    return Response(resp.content, status=resp.status_code, headers=headers)


@app.route("/api/", defaults={"path": ""})
@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy_api(path):
    return _proxy(request.method, f"api/{path}")


# 静态资源
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # SPA 路由 fallback
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
