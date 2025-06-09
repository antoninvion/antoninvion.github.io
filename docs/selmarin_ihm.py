from tkinter import *
from tkinter import messagebox, filedialog
import mysql.connector
import pandas as pd
from datetime import datetime
import os

from selmarin import lancer_insertion
from requetes_sql import requetes_sql

# Configuration initiale (sans base pour la création)
CONFIG_INIT = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

DB_NAME = "selmarin-tdb"

# Logs
historique_logs = []

# Fonction pour afficher les logs dans l'interface
def log_action(message):
    historique_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    zone_log.delete("1.0", END)
    zone_log.insert(END, "\n".join(historique_logs[-10:]))

# Fonction pour afficher les données d'une table

def afficher_table(nom_table):
    try:
        conn = mysql.connector.connect(**CONFIG_INIT, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nom_table}")
        colonnes = [desc[0] for desc in cursor.description]
        lignes = cursor.fetchall()
        df = pd.DataFrame(lignes, columns=colonnes)

        fenetre_table = Toplevel()
        fenetre_table.title(f"Contenu de la table {nom_table}")
        texte = Text(fenetre_table, wrap=NONE, font=("Courier", 10))
        texte.pack(fill=BOTH, expand=True)
        texte.insert(END, df.to_string(index=False))

        cursor.close()
        conn.close()
        log_action(f"✅ Table {nom_table} affichée.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
        log_action(f"❌ Erreur affichage table {nom_table} : {e}")

# Fonction pour créer la base de données et les tables

def creer_base_et_tables():
    try:
        conn_init = mysql.connector.connect(**CONFIG_INIT)
        cursor_init = conn_init.cursor()
        cursor_init.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET 'utf8'")
        cursor_init.close()
        conn_init.close()
        log_action("✅ Base créée ou déjà existante.")
    except Exception as e:
        messagebox.showerror("Erreur création base", str(e))
        log_action(f"❌ Erreur création base : {e}")
        return

    try:
        conn = mysql.connector.connect(**CONFIG_INIT, database=DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Saunier(
            numSau INT,
            nomSau VARCHAR(50) NOT NULL,
            prenomSau VARCHAR(50) NOT NULL,
            villeSau VARCHAR(50) NOT NULL,
            PRIMARY KEY(numSau)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produit(
            numPdt INT,
            libPdt VARCHAR(50) NOT NULL,
            stockPdt INT NOT NULL CHECK(stockPdt >= 0),
            PRIMARY KEY(numPdt),
            UNIQUE(libPdt)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Client(
            numCli INT,
            nomCli VARCHAR(50) NOT NULL,
            precisionCli VARCHAR(50) NOT NULL,
            villeCli VARCHAR(50) NOT NULL,
            PRIMARY KEY(numCli),
            UNIQUE(nomCli, villeCli)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sortie(
            numSort INT,
            dateSort DATETIME DEFAULT CURRENT_TIMESTAMP,
            numCli INT NOT NULL,
            PRIMARY KEY(numSort),
            FOREIGN KEY(numCli) REFERENCES Client(numCli)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Annee(
            annee INT,
            PRIMARY KEY(annee)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Entree(
            numEnt INT,
            dateEnt DATETIME DEFAULT CURRENT_TIMESTAMP,
            qteEnt DOUBLE NOT NULL CHECK(qteEnt > 0),
            numPdt INT NOT NULL,
            numSau INT NOT NULL,
            PRIMARY KEY(numEnt),
            FOREIGN KEY(numPdt) REFERENCES Produit(numPdt),
            FOREIGN KEY(numSau) REFERENCES Saunier(numSau)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Concerner(
            numPdt INT,
            numSort INT,
            qteSort INT NOT NULL CHECK(qteSort > 0),
            PRIMARY KEY(numPdt, numSort),
            FOREIGN KEY(numPdt) REFERENCES Produit(numPdt),
            FOREIGN KEY(numSort) REFERENCES Sortie(numSort)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Appartenir(
            numPdt INT,
            annee INT,
            prixAchat DOUBLE NOT NULL CHECK(prixAchat > 0),
            prixVente DOUBLE NOT NULL CHECK(prixVente > 0),
            PRIMARY KEY(numPdt, annee),
            FOREIGN KEY(numPdt) REFERENCES Produit(numPdt),
            FOREIGN KEY(annee) REFERENCES Annee(annee)
        ) ENGINE=InnoDB;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Base et tables créées.")
        log_action("✅ Tables créées avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur création tables", str(e))
        log_action(f"❌ Erreur création tables : {e}")
        
from tkinter import Toplevel, Label, Text, Button, END, BOTH, X, NONE, messagebox, ttk
import mysql.connector
import pandas as pd
from requetes_sql import requetes_sql

def executer_requete_predeterminee():
    fenetre_requetes = Toplevel()
    fenetre_requetes.title("Exécuter une requête prédéfinie")
    fenetre_requetes.geometry("800x600")

    Label(fenetre_requetes, text="Sélectionnez une requête :", font=("Arial", 12)).pack(pady=10)

    combo_requetes = ttk.Combobox(fenetre_requetes, values=list(requetes_sql.keys()), state="readonly", font=("Arial", 11))
    combo_requetes.pack(fill=X, padx=20, pady=10)

    texte_resultat = Text(fenetre_requetes, wrap=NONE, font=("Courier", 10))
    texte_resultat.pack(fill=BOTH, padx=20, pady=10, expand=True)

    def executer():
        texte_resultat.delete("1.0", END)
        cle_requete = combo_requetes.get()
        if not cle_requete:
            messagebox.showwarning("Sélection vide", "Veuillez sélectionner une requête.")
            return

        requete = requetes_sql[cle_requete]

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="selmarin-tdb")
            cursor = conn.cursor()
            cursor.execute(requete)

            if requete.strip().lower().startswith("select"):
                colonnes = [desc[0] for desc in cursor.description]
                lignes = cursor.fetchall()
                df = pd.DataFrame(lignes, columns=colonnes)
                texte_resultat.insert(END, df.to_string(index=False))
            else:
                conn.commit()
                texte_resultat.insert(END, f"✅ Requête exécutée avec succès : {cle_requete}")

            cursor.close()
            conn.close()
        except Exception as e:
            texte_resultat.insert(END, f"❌ Erreur : {e}")

    Button(fenetre_requetes, text="Exécuter", bg="#007BFF", fg="white", font=("Arial", 12), command=executer).pack(pady=10)

    
# Requête personnalisée

def executer_requete():
    fenetre_perso = Toplevel()
    fenetre_perso.title("Requête personnalisée")
    fenetre_perso.geometry("850x700")

    Label(fenetre_perso, text="Entrez votre requête SQL :", font=("Arial", 12)).pack(pady=10)
    champ_requete = Text(fenetre_perso, height=5, font=("Courier", 10))
    champ_requete.pack(padx=10, fill=X)

    Label(fenetre_perso, text="Mot de passe (requis pour DELETE, UPDATE, etc...) :", font=("Arial", 10)).pack(pady=5)
    champ_mdp = Entry(fenetre_perso, show="*", font=("Arial", 11))
    champ_mdp.pack(padx=10, fill=X)

    texte_resultat = Text(fenetre_perso, wrap=NONE, font=("Courier", 10))
    texte_resultat.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def exporter_csv(df):
        fen_export = Toplevel(fenetre_perso)
        fen_export.title("Exporter en CSV")
        Label(fen_export, text="Nom du fichier CSV :").pack(pady=5)
        entry_nom = Entry(fen_export, font=("Arial", 11))
        entry_nom.pack(padx=10)

        def sauvegarder():
            nom = entry_nom.get().strip()
            if not nom:
                messagebox.showwarning("Nom manquant", "Veuillez entrer un nom de fichier.")
                return
            nom_fichier = nom if nom.endswith(".csv") else f"{nom}.csv"
            chemin = os.path.join(os.getcwd(), nom_fichier)
            df.to_csv(chemin, index=False)
            messagebox.showinfo("Export", f"✅ Fichier exporté : {chemin}")
            fen_export.destroy()

        Button(fen_export, text="Exporter", bg="#28A745", fg="white", command=sauvegarder).pack(pady=5)

    def executer():
        texte_resultat.delete("1.0", END)
        requete = champ_requete.get("1.0", END).strip()
        mot_de_passe = champ_mdp.get().strip()

        if not requete:
            texte_resultat.insert(END, "❌ Aucune requête saisie.")
            return

        try:
            conn = mysql.connector.connect(**CONFIG_INIT, database=DB_NAME)
            cursor = conn.cursor()

            if requete.lower().startswith("select"):
                cursor.execute(requete)
                colonnes = [desc[0] for desc in cursor.description]
                lignes = cursor.fetchall()
                df = pd.DataFrame(lignes, columns=colonnes)
                texte_resultat.insert(END, df.to_string(index=False))
                log_action("✅ Requête SELECT exécutée")
                Button(fenetre_perso, text="Exporter CSV", bg="#28A745", fg="white", command=lambda: exporter_csv(df)).pack(pady=5)
            else:
                if mot_de_passe != "idr2025":
                    texte_resultat.insert(END, "❌ Mot de passe requis ou incorrect pour cette opération.")
                    log_action("❌ Tentative de requête sans mot de passe valide")
                    cursor.close()
                    conn.close()
                    return
                cursor.execute(requete)
                conn.commit()
                texte_resultat.insert(END, "✅ Requête exécutée avec succès.")
                log_action("✅ Requête sensible exécutée")

            cursor.close()
            conn.close()
        except Exception as e:
            texte_resultat.insert(END, f"❌ Erreur : {e}")
            log_action(f"❌ Erreur requête personnalisée : {e}")

    Button(fenetre_perso, text="Exécuter", font=("Arial", 12), bg="#007BFF", fg="white", command=executer).pack(pady=10)


# Interface requêtes prédéfinies (placeholder)
def interface_requetes(requetes_sql):
    messagebox.showinfo("Requêtes SQL", "Fonction à développer : interface requêtes prédéfinies.")


# Fonction d'insertion SQL spécifique
def inserer_donnees_initiales():
    requetes_insertion = """
    
    INSERT INTO SAUNIER(numSAU,nomSau,prenomSAU,villeSau)
    VALUES (1,"YVAN","Pierre","Ars-En-Ré"),
           (2,"PETIT","Marc","Loix");

    INSERT INTO CLIENT(numCLI,nomCli,precisionCli,villeCli)
    VALUES  (1,"CAVANA","Marie","LA ROCHELLE"),
            (2,"BURLET","Michel","LAGORD"),
            (3,"PEUTOT","Maurice","LAGORD"),
            (4,"ORGEVAL","Centrale d'achats","SURGERES");

    INSERT INTO PRODUIT(NUMPDT,libPdt,stockPdt)
    VALUES  (1,"Gros sel",2000),
            (2,"Fleur de sel",1000);
    
    INSERT INTO ENTREE(numENT,dateEnt,qteEnt,numSAU,numPdt)
    VALUES  (20241,"2024/06/16",1000,1,1),
            (20242,"2024/06/18",500,1,2),
            (20243,"2024/07/10",1500,2,2);

    INSERT INTO SORTIE(NUMSORT,dateSort,numCli)
    VALUES (20241,"2024/07/16",1),
           (20242,"2024/07/18",1),
           (20243,"2024/08/10",2);

    INSERT INTO CONCERNER(NUMSORT,NUMPDT,qteSort)
    VALUES (20241,1,300),
           (20241,2,500),
           (20242,1,200),
           (20243,1,100),
           (20243,2,500);

    INSERT INTO ANNEE(annee)
    VALUES (2023),
           (2024),
           (2025);

    INSERT INTO APPARTENIR(numpdt,annee,prixachat,prixvente)
    VALUES (1,2023,270,280),
           (2,2023,3900,9500),
           (1,2024,270,290),
           (2,2024,3800,10000),
           (1,2025,240,300),
           (2,2025,3500,9000);
    """

    try:
        conn = mysql.connector.connect(**CONFIG_INIT, database=DB_NAME)
        cursor = conn.cursor()

        for requete in requetes_insertion.strip().split(';'):
            if requete.strip():
                cursor.execute(requete)

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Succès", "Les données initiales ont été insérées.")
        log_action("✅ Données initiales insérées.")
    except Exception as e:
        messagebox.showerror("Erreur insertion", str(e))
        log_action(f"❌ Erreur insertion données initiales : {e}")


# --- Interface Principale ---
fenetre = Tk()
fenetre.title("Gestion Base de Données - Sel Marin")
fenetre.minsize(450, 650)
fenetre.configure(bg="#f0f0f0")

cadre = Frame(fenetre, bg="#f0f0f0")
cadre.pack(fill=BOTH, expand=True, padx=20, pady=20)

Label(cadre, text="Base de Données Sel Marin", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

Button(cadre, text="Créer Base + Tables", font=("Arial", 12), bg="#17a2b8", fg="white", command=creer_base_et_tables).pack(fill=X, pady=5)

# Nouveau bouton insertion données initiales
Button(cadre, text="Insérer Données Initiales", font=("Arial", 12), bg="#dc3545", fg="white", command=inserer_donnees_initiales).pack(fill=X, pady=5)


Button(cadre, text="Insertion CSV", font=("Arial", 12), bg="#28A745", fg="white", command=lancer_insertion).pack(fill=X, pady=5)
Button(cadre, text="10 Requêtes SQL", font=("Arial", 12), bg="#FFC107", fg="black", command=executer_requete_predeterminee).pack(fill=X, pady=5)
Button(cadre, text="Requête personnalisée", font=("Arial", 12), bg="#6f42c1", fg="white", command=executer_requete).pack(fill=X, pady=5)

# Boutons de visualisation des tables (sauf Annee)
for table in ["Saunier", "Produit", "Client", "Sortie", "Entree", "Concerner", "Appartenir"]:
    Button(cadre, text=f"Afficher {table}", font=("Arial", 12), bg="#007BFF", fg="white", command=lambda t=table: afficher_table(t)).pack(fill=X, pady=3)

Label(fenetre, text="Historique :", bg="#f0f0f0", font=("Arial", 11, "bold")).pack()
zone_log = Text(fenetre, height=6, bg="#e9ecef", font=("Courier", 9))
zone_log.pack(fill=BOTH, padx=20, pady=(0, 10), expand=False)

fenetre.mainloop()