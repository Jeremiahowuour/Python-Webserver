import socket
import mimetypes
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on port {SERVER_PORT} ...")

def build_response(status_code, content, content_type="text/html"):
    status_messages = {
        200: "OK",
        404: "Not Found",
        405: "Method Not Allowed"
    }

    header = f"HTTP/1.1 {status_code} {status_messages[status_code]}\n"
    header += f"Content-Type: {content_type}\n"
    header += f"Content-Length: {len(content)}\n"
    header += "Connection: close\n\n"

    return header.encode() + content


while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(2000).decode()

    if not request:
        client_socket.close()
        continue

    print(request)

    # Parse request
    headers = request.split('\n')
    first_line = headers[0].split()

    method = first_line[0]
    path = first_line[1]

    # Only allow GET
    if method != "GET":
        response = build_response(405, b"<h1>405 - Method Not Allowed</h1>")
        client_socket.sendall(response)
        client_socket.close()
        continue

    # (/) should return index.html
    if path == "/":
        path = "/index.html"

    # Remove leading slash
    filepath = path.lstrip("/")

    # File exists?
    if not os.path.exists(filepath):
        response = build_response(404, b"<h1>404 - File Not Found</h1>")
        client_socket.sendall(response)
        client_socket.close()
        continue

    # Determine MIME type
    mimetype, _ = mimetypes.guess_type(filepath)
    if mimetype is None:
        mimetype = "application/octet-stream"

    # Open and read file
    with open(filepath, "rb") as f:
        content = f.read()

    # Build response
    response = build_response(200, content, mimetype)

    # Send
    client_socket.sendall(response)
    client_socket.close()
