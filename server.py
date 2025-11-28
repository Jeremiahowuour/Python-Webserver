# server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# --- 1. Define the Request Handler Class ---
#  handles incoming requests (GET, POST,)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    # --- 2. Implement the GET request handler ---
    # This method is automatically called when a client sends a GET request.
    def do_GET(self):
        
        # Requirement 2: Return "Hello, World!" when accessing '/'
        if self.path == '/':
            
            # 1. Send response code 200 (OK)
            self.send_response(200)
            
            # 2. Send headers (tell the client what kind of content is coming)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            
            # 3. Write the actual content (must be encoded to bytes)
            message = "Hello, World!"
            self.wfile.write(bytes(message, "utf8"))
            
        else:
            # Handle other paths (optional, but good practice)
            self.send_error(404, "File Not Found: %s" % self.path)

# --- 3. Define the Main Function to Run the Server ---
def run_server():
    # Requirement 1: Create a server that listens on localhost:8000
    host_name = "localhost" # 127.0.0.1
    server_port = 8000
    
    # Create the HTTP server instance
    web_server = HTTPServer((host_name, server_port), SimpleHTTPRequestHandler)
    print(f"✅ Server started successfully at http://{host_name}:{server_port}")
    print("Press Ctrl+C to stop the server.")

    # Start listening for requests
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    # Clean up and shut down
    web_server.server_close()
    print("❌ Server stopped.")

# --- 4. Run the main function ---
if __name__ == "__main__":
    run_server()