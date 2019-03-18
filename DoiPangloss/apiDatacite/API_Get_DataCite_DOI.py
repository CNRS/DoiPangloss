import requests, sys
from constantes import USERNAME, PASSWORD, ENDPOINTDOI, ENDPOINTMETADATA, NAMESPACES
import xml.etree.ElementTree as ET


def extractDoiOai():
    """
    Fonction qui intérroge l'API de Datacite avec une requête http GET

    Récupérer les noms DOI créés par Lacito.
    Récupère le fichier de métadonnées de chaque DOI
    Parse le fichier et retourne un dictionnaire
    :return: dictionnaire avec pour clé le nom OAI et pour valeur le nom DOI
    :rtype: dict

    """
    # envoie la requête HTTP GET.
    # La methode get prend comme paramètre le lien URL du web service et les informations d'authentification
    response = requests.get(ENDPOINTDOI, auth = (USERNAME, PASSWORD))
	
    # creation d'une liste qui va stocker tous les noms DOI
    listDOI = response.text.split("\n")
    
    
    dicoDoiOai ={}
    # pour chaque nom DOI de la liste
    for doi in listDOI:
        # envoie une requête GET pour récupérer le fichier de métadonnées du DOI demandé sous la forme d'une chaine de caractères.
        # print(1)
        responseDOI = requests.get (ENDPOINTMETADATA + doi, auth = (USERNAME, PASSWORD))
		
        xmlMetaData = responseDOI.text
        # print(2)
        # parse l'arbre XML contenant les métadonnées
        root = ET.fromstring(xmlMetaData)

        # vérifie l'existance de la balise alternateIdentifier contenant
        # l'attribut alternateIdentifierType="internal ID" à l'aide d'une expression XPath
        if root.find('.//doi:alternateIdentifier[@alternateIdentifierType="internal ID"]', NAMESPACES) is not None:
            # recupère le contenu de la balise qui représente l'identifiant oai.
            oaiFromDatacite = root.find('.//doi:alternateIdentifier[@alternateIdentifierType="internal ID"]', NAMESPACES).text
        else:
            oaiFromDatacite = ""
        
       
        #extraire l'identifiant doi de la balise identifier
        doiFromDatacite = root.find('.//doi:identifier', NAMESPACES).text

        # ajouter au dictionnaire l'identifiant doi comme clé et l'identifiant oai comme valeur
        dicoDoiOai [doiFromDatacite] = oaiFromDatacite
        # print(3)
        # print (dicoDoiOai)
        
    return dicoDoiOai