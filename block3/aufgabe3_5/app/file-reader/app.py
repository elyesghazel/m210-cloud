from flask import Flask
app = Flask(__name__)

@app.route('/')
def read_file():
    # Liest die Datei bei jedem Seitenaufruf neu aus
    with open('/data/data.txt', 'r') as f:
        content = f.read()
    return f'Inhalt der Datei: {content}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
