import requests
import json
from constantes import USERNAME, PASSWORD, ENDPOINTDOI, ENDPOINTMETADATA, NAMESPACES 
import xml.etree.ElementTree as ET

##NAMESPACES = {
##            "dc": "http://purl.org/dc/elements/1.1/",
##            "dcterms" : "http://purl.org/dc/terms/",
##            "olac" : "http://www.language-archives.org/OLAC/1.1/",
##            "xsi" : "http://www.w3.org/2001/XMLSchema-instance",
##            "oai" : "http://www.openarchives.org/OAI/2.0/",
##            "doi" : "http://datacite.org/schema/kernel-4"
##        }
##USERNAME = "INIST.LACITO"
##PASSWORD = "PANGLOSS_DOI"
##ENDPOINTDOI = "https://mds.datacite.org/doi/"

token = ""
DoiMetadata = ""



def createDicoDoiOai():
    """
    Fonction qui intérroge l'API de Datacite avec une requête http GET

    Récupérer les noms DOI.
    Récupère le fichier de métadonnées de chaque DOI
    Parse le fichier et retourne un dictionnaire
    :return: dictionnaire avec pour clé le nom OAI et pour valeur le nom DOI
    :rtype: dict

    """

    # l'adresse pour retrouver tous les DOI de Datacite sur lesquels il faut appliquer les filtres
    ENDPOINTALLDOI= 'https://api.datacite.org/works'

    # dictionnaire avec 2 paramètres à passer à l'appel de l'URL : data-center-id et page[number]
    # pour tester le code avant la création des DOI pour Lacito, remplacer INIST.LACITO par un autre code institutionnel par exemple "inist.garnier"
    param = {"data-center-id":"inist.lacito", "page[size]": 500, "page[number]": 1}

    response = requests.get(ENDPOINTALLDOI, params=param)
    donnee = response.json()
    number = 0
    
    # print (donnee["meta"])
    # tant que la clé "data" du json a du contenu
    dicoDoiOai ={}

    for i in range(donnee["meta"]["total-pages"]):

        # si la réponse est différente de 200 sortir de la boucle.
        if (response.status_code != 200):
            print (str(response.status_code) + " " + response.text)
            break
        
        # sinon, extraire les 25 objets DOI pour chaque page
        else:
            # donnee = response.json()
            dataciteMeta = json.loads(response.text)

            import base64

            for entry in dataciteMeta["data"]:
                oneXml = base64.b64decode(entry["attributes"]["xml"])


                root = ET.fromstring(oneXml)

                if root.find('.//doi:alternateIdentifier[@alternateIdentifierType="internal ID"]', NAMESPACES) is not None:
                    # recupère le contenu de la balise qui représente l'identifiant oai.
                    oaiFromDatacite = root.find('.//doi:alternateIdentifier[@alternateIdentifierType="internal ID"]', NAMESPACES).text
                else:
                    oaiFromDatacite = ""

                #extraire l'identifiant doi de la balise identifier
                doiFromDatacite = root.find('.//doi:identifier', NAMESPACES).text

                # ajouter au dictionnaire l'identifiant doi comme clé et l'identifiant oai comme valeur
                dicoDoiOai [doiFromDatacite] = oaiFromDatacite 

        number += 1
        # print ('nb pages : ', param["page[number]"], len(donnee["data"]))
        # passer à la page suivante et faire une nouvelle requête GET
        param["page[number]"] = param["page[number]"]+1
        response = requests.get(ENDPOINTALLDOI, params=param)

        
    return(dicoDoiOai)  

# print (len(createDicoDoiOai()))
