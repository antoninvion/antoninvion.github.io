import csv 
import json 
import re
from datetime import datetime 

# ----------------------------------Création des différentes fonctions qui nous seront utiles pour la transformation du fichier------------------------------------------                              
 


def conversionDate(date_str): # fonction qui permet de convertir la date du format iso en format français 
    try: 
        return datetime.fromisoformat(date_str).strftime("%d/%m/%Y")
    
    except (TypeError, ValueError): 
        return None 
    

def conversionTemps(date_str): # fonction qui permet d"extraire l'heure des dates de début et de fin 

    try: 
        return datetime.fromisoformat(date_str).strftime("%H:%M") 

    except (TypeError, ValueError): 
        return None 


def cleanText(text): # fonction qui permet d'éviter les retours à la ligne et efface les balises

     if isinstance(text, str): 

        to_clean = re.compile("<.*?>") #Prend comme valeur tout les élèment de forme : "<" + text + ">"

        cleantext = re.sub(to_clean, " ", text) #remplace tout ces élèment par un espace

        return cleantext.replace("\n", " ").replace("\r", " ")   

     return text 

#----------------------------------------------------- Transformation du fichier JSON en csv-----------------------------------------------------------------------------


# Ouverture Charger le fichier JSON 
try:
    with open("que-faire-a-paris-.json") as f:  # with open(...) permet de gérer automatiquement la fermeture du fichier, même en cas d'exception
        data = json.load(f) 


    # Construire la liste des résultats 
    event = [ 
        {
            "ID": cleanText(item.get("id")),  #.get() retourne None si la clé est absente, évitant ainsi une erreur d'exécution

            "URL": cleanText(item.get("url")), 

            "Titre": cleanText(item.get("title")),

            "Mots clés" :  " ".join(item.get("tags", [])) if isinstance(item.get("tags"), list) else "" , # permet de concatener les mots clés à la place d'obtenir une liste

            "Chapeau": cleanText(item.get("lead_text")), 

            "Description": cleanText(item.get("description")), 

            "Date de début": conversionDate(item.get("date_start")), 

            "Heure de début": conversionTemps(item.get("date_start")), 

            "Date de fin": conversionDate(item.get("date_end")), 

            "Heure de Fin": conversionTemps(item.get("date_end")), 

            "Nom du lieu": cleanText(item.get("address_name")), 

            "Adresse du lieu": cleanText(item.get("address_street")), 

            "Code Postal": cleanText(item.get("address_zipcode")), 

            "Ville": cleanText(item.get("address_city")), 

            "Coordonnées géographiques": cleanText(item.get("lat_lon")), 

            "Accès PMR": cleanText(item.get("pmr")), 

            "Accès mal voyant": cleanText(item.get("blind")),

            "Accès mal entendant": cleanText(item.get("deaf")), 

            "Transport": cleanText(item.get("transport")), 

            "Téléphone de contact": cleanText(item.get("contact_phone")), 

            "Email de contact": cleanText(item.get("contact_mail")), 

            "Url de contact": cleanText(item.get("contact_url")), 

            "Type d'accès": cleanText(item.get("access_type")), 

            "Détail du prix": cleanText(item.get("price_detail")), 

            "URL de l'image de couverture": cleanText(item.get("cover_url")) 
   
             } for item in data if isinstance(item, dict) ] # l'utilisation du if isinstance nous permet d'éviter des erreurs de lecture dans le cas où le fichier json contient une structure différente (chaine de caractères par exemple)

    # création du fichier csv 

    with open("que-faire-a-paris-.csv", "w", encoding="utf-8", newline="") as fichier:
            # Initialisation du writer CSV
            ecritCSV = csv.DictWriter(fichier,delimiter=";",fieldnames=event[0].keys()) 

            ecritCSV.writeheader() # On écrit la ligne d"en-tête avec le titre des colonnes 

            for ligne in event: 

                ecritCSV.writerow(ligne) 

    print("Fichier créé avec succès !\nVous pouvez dès à présent l'ouvrir dans excel !")
    fichier.close()
 


except FileNotFoundError:
    print("Fichier introuvable : que-faire-a-paris-.json")
except json.JSONDecodeError as e:
    print("Erreur dans le fichier JSON : " + str(e))
except Exception as e:
    print("Une erreur inattendue s'est produite : " + str(e))

 

 

