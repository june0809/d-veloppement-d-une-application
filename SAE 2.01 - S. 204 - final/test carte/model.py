import sqlite3
import requests

# Chemin vers la base de données SQLite
DATABASE = "static/data/hubeau.db"

# Liste des API disponibles et deux tables suplémentaire
api = ["stations", "observations", "campagnes", "region", "dept"]

# Liste des départements avec leur code, nom et région
departements = [
    ("01", "Ain", "Auvergne-Rhône-Alpes"),
    ("02", "Aisne", "Hauts-de-France"),
    ("03", "Allier", "Auvergne-Rhône-Alpes"),
    ("04", "Alpes-de-Haute-Provence", "Provence-Alpes-Côte d'Azur"),
    ("05", "Hautes-Alpes", "Provence-Alpes-Côte d'Azur"),
    ("06", "Alpes-Maritimes", "Provence-Alpes-Côte d'Azur"),
    ("07", "Ardèche", "Auvergne-Rhône-Alpes"),
    ("08", "Ardennes", "Grand Est"),
    ("09", "Ariège", "Occitanie"),
    ("10", "Aube", "Grand Est"),
    ("11", "Aude", "Occitanie"),
    ("12", "Aveyron", "Occitanie"),
    ("13", "Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur"),
    ("14", "Calvados", "Normandie"),
    ("15", "Cantal", "Auvergne-Rhône-Alpes"),
    ("16", "Charente", "Nouvelle-Aquitaine"),
    ("17", "Charente-Maritime", "Nouvelle-Aquitaine"),
    ("18", "Cher", "Centre-Val de Loire"),
    ("19", "Corrèze", "Nouvelle-Aquitaine"),
    ("2A", "Corse-du-Sud", "Corse"),
    ("2B", "Haute-Corse", "Corse"),
    ("21", "Côte-d'Or", "Bourgogne-Franche-Comté"),
    ("22", "Côtes-d'Armor", "Bretagne"),
    ("23", "Creuse", "Nouvelle-Aquitaine"),
    ("24", "Dordogne", "Nouvelle-Aquitaine"),
    ("25", "Doubs", "Bourgogne-Franche-Comté"),
    ("26", "Drôme", "Auvergne-Rhône-Alpes"),
    ("27", "Eure", "Normandie"),
    ("28", "Eure-et-Loir", "Centre-Val de Loire"),
    ("29", "Finistère", "Bretagne"),
    ("30", "Gard", "Occitanie"),
    ("31", "Haute-Garonne", "Occitanie"),
    ("32", "Gers", "Occitanie"),
    ("33", "Gironde", "Nouvelle-Aquitaine"),
    ("34", "Hérault", "Occitanie"),
    ("35", "Ille-et-Vilaine", "Bretagne"),
    ("36", "Indre", "Centre-Val de Loire"),
    ("37", "Indre-et-Loire", "Centre-Val de Loire"),
    ("38", "Isère", "Auvergne-Rhône-Alpes"),
    ("39", "Jura", "Bourgogne-Franche-Comté"),
    ("40", "Landes", "Nouvelle-Aquitaine"),
    ("41", "Loir-et-Cher", "Centre-Val de Loire"),
    ("42", "Loire", "Auvergne-Rhône-Alpes"),
    ("43", "Haute-Loire", "Auvergne-Rhône-Alpes"),
    ("44", "Loire-Atlantique", "Pays de la Loire"),
    ("45", "Loiret", "Centre-Val de Loire"),
    ("46", "Lot", "Occitanie"),
    ("47", "Lot-et-Garonne", "Nouvelle-Aquitaine"),
    ("48", "Lozère", "Occitanie"),
    ("49", "Maine-et-Loire", "Pays de la Loire"),
    ("50", "Manche", "Normandie"),
    ("51", "Marne", "Grand Est"),
    ("52", "Haute-Marne", "Grand Est"),
    ("53", "Mayenne", "Pays de la Loire"),
    ("54", "Meurthe-et-Moselle", "Grand Est"),
    ("55", "Meuse", "Grand Est"),
    ("56", "Morbihan", "Bretagne"),
    ("57", "Moselle", "Grand Est"),
    ("58", "Nièvre", "Bourgogne-Franche-Comté"),
    ("59", "Nord", "Hauts-de-France"),
    ("60", "Oise", "Hauts-de-France"),
    ("61", "Orne", "Normandie"),
    ("62", "Pas-de-Calais", "Hauts-de-France"),
    ("63", "Puy-de-Dôme", "Auvergne-Rhône-Alpes"),
    ("64", "Pyrénées-Atlantiques", "Nouvelle-Aquitaine"),
    ("65", "Hautes-Pyrénées", "Occitanie"),
    ("66", "Pyrénées-Orientales", "Occitanie"),
    ("67", "Bas-Rhin", "Grand Est"),
    ("68", "Haut-Rhin", "Grand Est"),
    ("69", "Rhône", "Auvergne-Rhône-Alpes"),
    ("70", "Haute-Saône", "Bourgogne-Franche-Comté"),
    ("71", "Saône-et-Loire", "Bourgogne-Franche-Comté"),
    ("72", "Sarthe", "Pays de la Loire"),
    ("73", "Savoie", "Auvergne-Rhône-Alpes"),
    ("74", "Haute-Savoie", "Auvergne-Rhône-Alpes"),
    ("75", "Paris", "Île-de-France"),
    ("76", "Seine-Maritime", "Normandie"),
    ("77", "Seine-et-Marne", "Île-de-France"),
    ("78", "Yvelines", "Île-de-France"),
    ("79", "Deux-Sèvres", "Nouvelle-Aquitaine"),
    ("80", "Somme", "Hauts-de-France"),
    ("81", "Tarn", "Occitanie"),
    ("82", "Tarn-et-Garonne", "Occitanie"),
    ("83", "Var", "Provence-Alpes-Côte d'Azur"),
    ("84", "Vaucluse", "Provence-Alpes-Côte d'Azur"),
    ("85", "Vendée", "Pays de la Loire"),
    ("86", "Vienne", "Nouvelle-Aquitaine"),
    ("87", "Haute-Vienne", "Nouvelle-Aquitaine"),
    ("88", "Vosges", "Grand Est"),
    ("89", "Yonne", "Bourgogne-Franche-Comté"),
    ("90", "Territoire de Belfort", "Bourgogne-Franche-Comté"),
    ("91", "Essonne", "Île-de-France"),
    ("92", "Hauts-de-Seine", "Île-de-France"),
    ("93", "Seine-Saint-Denis", "Île-de-France"),
    ("94", "Val-de-Marne", "Île-de-France"),
    ("95", "Val-d'Oise", "Île-de-France")
]

# URL de base de l'API
api_url = "https://hubeau.eaufrance.fr/api/v1/ecoulement/"

# Classe Table pour gérer les opérations sur les tables de la base de données


class Table:

    @staticmethod
    def creer_table():
        conn = sqlite3.connect("static/data/hubeau.db")
        c = conn.cursor()

        # Création de la table stations
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY,
            code_station TEXT,
            libelle_station TEXT,
            uri_station TEXT,
            code_departement TEXT,
            libelle_departement TEXT,
            code_commune TEXT,
            libelle_commune TEXT,
            code_region TEXT,
            libelle_region TEXT,
            code_bassin TEXT,
            libelle_bassin TEXT,
            coordonnee_x_station REAL,
            coordonnee_y_station REAL,
            code_projection_station TEXT,
            libelle_projection_station TEXT,
            code_epsg_station TEXT,
            code_cours_eau TEXT,
            libelle_cours_eau TEXT,
            uri_cours_eau TEXT,
            etat_station TEXT,
            date_maj_station TEXT,
            latitude REAL,
            longitude REAL
        )
        """
        )
        print("La table stations a été créée avec succès !")

        # Création de la table observations
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY,
            code_station TEXT,
            libelle_station TEXT,
            uri_station TEXT,
            code_departement TEXT,
            libelle_departement TEXT,
            code_commune TEXT,
            libelle_commune TEXT,
            code_region TEXT,
            libelle_region TEXT,
            code_bassin TEXT,
            libelle_bassin TEXT,
            coordonnee_x_station REAL,
            coordonnee_y_station REAL,
            code_projection_station TEXT,
            libelle_projection_station TEXT,
            code_cours_eau TEXT,
            libelle_cours_eau TEXT,
            uri_cours_eau TEXT,
            code_campagne TEXT,
            code_reseau TEXT,
            libelle_reseau TEXT,
            uri_reseau TEXT,
            date_observation TEXT,
            code_ecoulement TEXT,
            libelle_ecoulement TEXT,
            latitude REAL,
            longitude REAL
        )
        """
        )
        print("La table observations a été créée avec succès !")

        # Création de la table campagnes
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS campagnes (
            id INTEGER PRIMARY KEY,
            code_campagne TEXT,
            date_campagne TEXT,
            nombre_modalite_ecoulement INTEGER,
            code_type_campagne INTEGER,
            libelle_type_campagne TEXT,
            code_reseau TEXT,
            libelle_reseau TEXT,
            uri_reseau TEXT,
            code_departement TEXT,
            libelle_departement TEXT
        )
        """
        )
        print("La table campagnes a été créée avec succès !")
        conn.commit()
        conn.close()

    @staticmethod
    def create_tables():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Création de la table region
        c.execute("""
            CREATE TABLE IF NOT EXISTS region (
                id INTEGER PRIMARY KEY,
                nom_region TEXT UNIQUE
            )
        """)

        # Création de la table dept
        c.execute("""
            CREATE TABLE IF NOT EXISTS dept (
                code_dept TEXT PRIMARY KEY,
                nom_dept TEXT,
                nom_region TEXT,
                FOREIGN KEY (nom_region) REFERENCES region (nom_region)
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def table_empty(table_name):
        conn = sqlite3.connect("static/data/hubeau.db")
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
        conn.close()
        return count == 0

    @staticmethod
    def insert_data(choix):
        table_name = api[choix]
        if not Table.table_empty(table_name):
            print(f"La table {table_name} contient déjà des données.")
            return

        url = f"{api_url}{table_name}"
        response = requests.get(url)

        if response.status_code not in [200, 206]:
            print(f"Erreur lors de la requête : {response.status_code}")
            return

        data = response.json().get("data", [])
        if not data:
            print(f"Aucune donnée trouvée pour {table_name}")
            return

        conn = sqlite3.connect("static/data/hubeau.db")
        c = conn.cursor()

        try:
            for item in data:
                if choix == 0:
                    # Insertion des données dans la table stations
                    c.execute(
                        """
                        INSERT INTO stations (
                            code_station, libelle_station, uri_station, code_departement, libelle_departement, 
                            code_commune, libelle_commune, code_region, libelle_region, code_bassin, libelle_bassin, 
                            coordonnee_x_station, coordonnee_y_station, code_projection_station, libelle_projection_station, 
                            code_epsg_station, code_cours_eau, libelle_cours_eau, uri_cours_eau, etat_station, date_maj_station, 
                            latitude, longitude) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            item.get("code_station"),
                            item.get("libelle_station"),
                            item.get("uri_station"),
                            item.get("code_departement"),
                            item.get("libelle_departement"),
                            item.get("code_commune"),
                            item.get("libelle_commune"),
                            item.get("code_region"),
                            item.get("libelle_region"),
                            item.get("code_bassin"),
                            item.get("libelle_bassin"),
                            item.get("coordonnee_x_station"),
                            item.get("coordonnee_y_station"),
                            item.get("code_projection_station"),
                            item.get("libelle_projection_station"),
                            item.get("code_epsg_station"),
                            item.get("code_cours_eau"),
                            item.get("libelle_cours_eau"),
                            item.get("uri_cours_eau"),
                            item.get("etat_station"),
                            item.get("date_maj_station"),
                            item.get("latitude"),
                            item.get("longitude"),
                        ),
                    )
                elif choix == 1:
                    # Insertion des données dans la table observations
                    c.execute(
                        """
                        INSERT INTO observations (
                        code_station, libelle_station, uri_station, code_departement,
                        libelle_departement, code_commune, libelle_commune, code_region,
                        libelle_region, code_bassin, libelle_bassin, coordonnee_x_station,
                        coordonnee_y_station, code_projection_station, libelle_projection_station,
                        code_cours_eau, libelle_cours_eau, uri_cours_eau, code_campagne, code_reseau,
                        libelle_reseau, uri_reseau, date_observation, code_ecoulement, libelle_ecoulement,
                        latitude, longitude)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            item.get("code_station"),
                            item.get("libelle_station"),
                            item.get("uri_station"),
                            item.get("code_departement"),
                            item.get("libelle_departement"),
                            item.get("code_commune"),
                            item.get("libelle_commune"),
                            item.get("code_region"),
                            item.get("libelle_region"),
                            item.get("code_bassin"),
                            item.get("libelle_bassin"),
                            item.get("coordonnee_x_station"),
                            item.get("coordonnee_y_station"),
                            item.get("code_projection_station"),
                            item.get("libelle_projection_station"),
                            item.get("code_cours_eau"),
                            item.get("libelle_cours_eau"),
                            item.get("uri_cours_eau"),
                            item.get("code_campagne"),
                            item.get("code_reseau"),
                            item.get("libelle_reseau"),
                            item.get("uri_reseau"),
                            item.get("date_observation"),
                            item.get("code_ecoulement"),
                            item.get("libelle_ecoulement"),
                            item.get("latitude"),
                            item.get("longitude"),
                        ),
                    )
                elif choix == 2:
                    # Insertion des données dans la table campagnes
                    c.execute(
                        """
                            INSERT INTO campagnes (
                                code_campagne, date_campagne, nombre_modalite_ecoulement, 
                                code_type_campagne, libelle_type_campagne, code_reseau, libelle_reseau, uri_reseau, 
                                code_departement, libelle_departement) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            item.get("code_campagne"),
                            item.get("date_campagne"),
                            item.get("nombre_modalite_ecoulement"),
                            item.get("code_type_campagne"),
                            item.get("libelle_type_campagne"),
                            item.get("code_reseau"),
                            item.get("libelle_reseau"),
                            item.get("uri_reseau"),
                            item.get("code_departement"),
                            item.get("libelle_departement"),
                        ),
                    )
            conn.commit()
            print(
                f"Les données de {table_name} ont été insérées avec succès !")
        except sqlite3.Error as e:
            print(
                f"Une erreur est survenue lors de l'insertion des données de {table_name} : {e}"
            )
        finally:
            conn.close()

    @staticmethod
    # Fonction pour insérer les régions dans la table region
    def insert_regions():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Utilisation d'un ensemble pour éviter les doublons de régions
        regions = set(dept[2] for dept in departements)

        for region in regions:
            c.execute(
                "INSERT OR IGNORE INTO region (nom_region) VALUES (?)", (region,)
            )

        conn.commit()
        conn.close()

    @staticmethod
    def insert_departements():
        # Insertion des données dans la table des départmeent
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        for dept in departements:
            c.execute(
                "INSERT OR IGNORE INTO dept (code_dept, nom_dept, nom_region) VALUES (?, ?, ?)", dept
            )

        conn.commit()
        conn.close()

    @staticmethod
    def drop_table(choix):
        conn = sqlite3.connect("static/data/hubeau.db")
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {api[choix]}")
        conn.commit()
        conn.close()
        print(f"La table {api[choix]} a été supprimée avec succès !")

    @staticmethod
    def delete_table_data(choix):
        conn = sqlite3.connect("static/data/hubeau.db")
        c = conn.cursor()
        try:
            c.execute(f"DELETE FROM {api[choix]}")
            conn.commit()
            print(f"Données de la table {api[choix]} supprimées avec succès !")
        except sqlite3.Error as e:
            print(
                f"Une erreur est survenue lors de la suppression des données de la table : {e}"
            )
        finally:
            conn.close()

    # -------------------------------------------------------
    # prendre toutes les données dans une table au choix
    @staticmethod
    def get_data(choix):
        conn = Table.get_db()
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM {api[choix]}"
        ) 
        rows = cur.fetchall()
        return rows

    # -------------------------------------------------------

# si on doit refaire la base entière
# --------------------------------------------------
# Table.creer_table()
# Table.create_tables()
# Table.insert_data(0)
# Table.insert_data(1)
# Table.insert_data(2)
# Table.insert_regions()
# Table.insert_departements()
