from flask import *
import sqlite3
import random
import model
from model import Table

app = Flask(__name__)

# Chemin vers la base de données SQLite
DATABASE = "static\data\hubeau.db"

# Fonction pour obtenir la connexion à la base de données


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# Fonction pour fermer la connexion à la base de données à la fin de la requête
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Route pour afficher les stations avec filtres sur la région, le département, la date de début et la date de fin
@app.route("/stations")
def stations():
    region = request.args.get("region")
    departement = request.args.get("departement")
    debut = request.args.get("debut")
    fin = request.args.get("fin")

    conn = get_db()
    c = conn.cursor()

    # Construction de la requête SQL pour filtrer les stations
    query = "SELECT * FROM stations WHERE 1=1 "
    params = []

    if "region" in request.args and request.args["region"]:
        query += "AND libelle_region = ? "
        params.append(request.args["region"])

    if "departement" in request.args and request.args["departement"]:
        query += "AND libelle_departement = ? "
        params.append(request.args["departement"])

    if "debut" in request.args and request.args["debut"]:
        query += "AND date_maj_station >= ? "
        params.append(request.args["debut"])

    if "fin" in request.args and request.args["fin"]:
        query += "AND date_maj_station <= ? "
        params.append(request.args["fin"])

    c.execute(query, params)
    stations = c.fetchall()

    # Récupération des données des régions et départements pour les filtres
    c.execute("SELECT * FROM region")
    regions = c.fetchall()

    c.execute("SELECT * FROM dept")
    departements = c.fetchall()
    conn.close()

    return render_template(
        "stations.html",
        stations=stations,
        regions=regions,
        departements=departements,
        title="Stations",
    )

# Route pour afficher les observations avec filtres sur la région, le département, la date de début et la date de fin
@app.route("/observations")
def observations():
    conn = get_db()
    c = conn.cursor()

    query = "SELECT * FROM observations WHERE 1=1 "
    params = []

    if "region" in request.args and request.args["region"]:
        query += "AND libelle_region = ? "
        params.append(request.args["region"])

    if "departement" in request.args and request.args["departement"]:
        query += "AND libelle_departement = ? "
        params.append(request.args["departement"])

    if "debut" in request.args and request.args["debut"]:
        query += "AND date_observation >= ? "
        params.append(request.args["debut"])

    if "fin" in request.args and request.args["fin"]:
        query += "AND date_observation <= ? "
        params.append(request.args["fin"])

    c.execute(query, params)
    observations = c.fetchall()

    c.execute("SELECT * FROM region ORDER BY 'nom_region'")
    regions = c.fetchall()

    c.execute("SELECT * FROM dept")
    departements = c.fetchall()

    conn.close()

    return render_template(
        "observations.html",
        observations=observations,
        regions=regions,
        departements=departements,
        title="Observations",
    )

# Route pour afficher les régions et les campagnes
@app.route("/regions")
def regions():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    campagnes = Table.get_data(2)
    region = Table.get_data(3)
    c.close()
    return render_template(
        "regions.html",
        title="Campagnes",
        region=region,
    )

# Route pour récupérer les départements en fonction de la région sélectionnée
@app.route("/dept", methods=["POST"])
def dept():
    region = request.form.get("region")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM dept WHERE nom_region = ?", (region,))
    departements = c.fetchall()
    c.close()
    return render_template(
        "dept.html",
        title="Départements",
        region=departements,
        reg=region
    )

# Route pour récupérer les campagnes en fonction du département sélectionné
@app.route("/campagnes", methods=["POST"])
def campagnes():
    dept = request.form.get("nom_dept")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM campagnes WHERE libelle_departement = ?", (dept,))
    campagnes = c.fetchall()
    c.close()
    return render_template(
        "campagnes.html",
        title="Campagnes",
        campagnes=campagnes,
        dept=dept
    )

# Route de redirection vers la page des régions
@app.route("/retour")
def retour_dept():
    return redirect(url_for('regions'))

# Page de contact
@app.route("/contacts")
def contacts():
    return render_template("contact.html", title="Contact")

# Route pour gérer l'envoi du formulaire de contact
@app.route("/send")
def envoyer():
    pass

# Route pour retourner 50 stations aléatoires
@app.route("/random_stations")
def random_stations():
    stations = Table.get_data(0)
    if not stations:
        return jsonify({"error": "No stations found"}), 404

    random_stations = random.sample(stations, 50)
    station_data = [
        {
            "name": station[2],
            "latitude": station[-2],
            "longitude": station[-1],
            "code": station[1],
            "commune": station[7],
        }
        for station in random_stations
    ]
    return jsonify(station_data)

# Route pour retourner 50 observations aléatoires
@app.route("/random_observations")
def random_observations():
    observations = Table.get_data(1)
    if not observations:
        return jsonify({"error": "No observations found"}), 404

    random_observations = random.sample(observations, 50)
    observation_data = [
        {
            "name": observation[2],
            "latitude": observation[-2],
            "longitude": observation[-1],
            "code": observation[1],
            "commune": observation[7],
        }
        for observation in random_observations
    ]
    return jsonify(observation_data)


# Exécution de l'application Flask
if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
