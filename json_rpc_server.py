from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonrpcserver import method, dispatch
import psutil, datetime
from psutil._common import bytes2human
import json
import sysdata

@method
def get_sys_state():
    return sysdata.get_system_json()



class RpcServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()
        response = dispatch(request)
        # Return response
        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(str(response).encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 5000), RpcServer).serve_forever()
