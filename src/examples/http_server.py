import http.server
import ssl
import socketserver

PORT = 443

class SecureHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(("", PORT), SecureHTTPRequestHandler) as httpd:
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='/etc/letsencrypt/live/dev2.monitor.eco.br/fullchain.pem',
                                   keyfile='/etc/letsencrypt/live/dev2.monitor.eco.br/privkey.pem',
                                   ssl_version=ssl.PROTOCOL_TLS)
    print("Serving HTTPS on port", PORT)
    httpd.serve_forever()