import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def histogramme():
    return render_template("histogramme.html")

@app.get("/atelier-data")
def atelier_data():

    def get_humidity(lat, lon):
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=relative_humidity_2m"
            "&timezone=auto"
        )

        data = requests.get(url).json()
        humidity = data.get("hourly", {}).get("relative_humidity_2m", [])[:24]

        low = sum(1 for h in humidity if h < 40)
        normal = sum(1 for h in humidity if 40 <= h <= 70)
        high = sum(1 for h in humidity if h > 70)

        return {"low": low, "normal": normal, "high": high}

    lille = get_humidity(50.6330, 3.0573)
    lyon = get_humidity(45.7640, 4.8357)

    return jsonify({
        "lille": lille,
        "lyon": lyon
    })

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
