import socket
import json
from urllib.parse import urlparse
import threading

HOST = "0.0.0.0"
PORT = 8080

def http_response(body, status="200 OK"):
    body_bytes = json.dumps(body).encode('utf-8')
    return (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode('utf-8') + body_bytes

def handle_client(conn, addr):
    try:
        conn.settimeout(5.0)  # ← FONDAMENTALE: non bloccare per sempre
        
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk

        if not data:
            return

        header_part, body_already_read = data.split(b"\r\n\r\n", 1)
        header_text = header_part.decode('utf-8', errors='ignore')

        lines = header_text.split("\r\n")
        method, full_path, _ = lines[0].split()
        path = urlparse(full_path).path

        content_length = 0
        for line in lines:
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        body_bytes = body_already_read
        while len(body_bytes) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body_bytes += chunk

        body_text = body_bytes.decode('utf-8', errors='ignore').strip()

        if path == "/flags" and method == "PUT":
            print(f"[*] PUT /flags da {addr} ({len(body_text)} bytes)")
            try:
                flags = json.loads(body_text)
                if not isinstance(flags, list):
                    flags = [str(flags)]

                results = []
                for f in flags:
                    results.append({
                        "flag": f,
                        "status": "RESUBMIT",
                        "msg": f"[{f}] flag RESUBMIT"
                    })

                print(f"[+] Risposto con RESUBMIT per {len(flags)} flag.")
                conn.sendall(http_response(results))

            except json.JSONDecodeError as e:
                print(f"[!] Errore JSON: {e}")
                conn.sendall(http_response({"error": "Malformed JSON", "details": str(e)}, "400 Bad Request"))
        else:
            conn.sendall(http_response({"message": "Server pronto", "path": path}))

    except socket.timeout:
        print(f"[!] Timeout connessione da {addr}")
    except Exception as e:
        print(f"[!] Errore: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(10)
        print(f"[*] Emulator attivo su http://0.0.0.0:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                # ← Ogni connessione in un thread separato
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    start_server()
