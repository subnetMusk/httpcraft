import os
import glob
from httpcraft import HttpCraft
import mimetypes

def run_test():
    hc = HttpCraft("http://127.0.0.1:5050")
    paths = ["/test/json", "/test/html", "/test/image", "/test/binary"]
    
    response_dir = os.path.join(os.path.dirname(__file__), "responses")
    os.makedirs(response_dir, exist_ok=True)

    for path in paths:
        exchange = hc.get(path)

        # Ricava l'estensione dal Content-Type
        ctype = exchange.response.raw_headers.get("Content-Type", "").split(";")[0].strip().lower()
        ext = mimetypes.guess_extension(ctype) or ".bin"

        # Costruisce il nome file con estensione corretta
        filename = f"{exchange.timestamp.replace(':', '').replace(' ', '_')}_{exchange.request.path.strip('/').replace('/', '_')}{ext}"
        filepath = os.path.join(response_dir, filename)

        hc.save_response_to_file(exchange, filepath=filepath)

    print("\n[✔] Salvataggi completati. Verifico i file...\n")

    found = glob.glob(os.path.join(response_dir, "*"))
    for f in found:
        print(f" - {f} ({os.path.getsize(f)} bytes)")

    print("\n[ℹ] Puoi ispezionare i file nella cartella 'responses/' e poi cancellarli.")

if __name__ == "__main__":
    run_test()
