from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonrpcserver import method, dispatch
import psutil, datetime

@method
def get_sys_state():
    temperature = psutil.sensors_temperatures()
    cpus = psutil.cpu_percent(interval=2,percpu=True)
    users = psutil.users()
    user_str = []
    for user in users:
        since = datetime.datetime.fromtimestamp(user.started)
        user_str.append((f"User: <b>{user.name}</b> from <b>{user.host}</b> since <b>{since.strftime('%d-%m-%Y %H:%M:%S')}</b>"))
    resp_data = {
                    "temperature" : temperature['cpu_thermal'][0].current,
                    "cpus": 
                    {
                        "cpu_1" : cpus[0],
                        "cpu_2" : cpus[1],
                        "cpu_3" : cpus[2],
                        "cpu_4" : cpus[3]
                    },
                    "frequency" : psutil.cpu_freq(percpu=False).current,
                    "users" : user_str
                }
    return resp_data



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