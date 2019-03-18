import requests
from constantes import USERNAME, PASSWORD, ENDPOINTMETADATA, FILE_API_METADATA

def sendMetadataResource(filename, doi):
    """
    Fonction qui intérroge l'API de Datacite avec une requête http POST

    Envoye le fichier de métadonnées de la ressource en XML respectant le modèle DOI
    :param filename: le fichier XML de métadonnées
    :type filename: file
    :param doi: nom DOI de la resosurce utilisé pour créer le nom du fichier texte qui enregistre les réponses à la requête HTTP
    :type doi: str

    """
    # ouvre en mode lecture le fichier XML
    metadata = open(filename, 'r', encoding='utf8').read()
    # envoie la requête HTTP POST.
    # La methode post prend comme paramètre le lien URL du web service,
    # les informations d'autentificantion, le fichier XML et les headers
    response = requests.post(ENDPOINTMETADATA, auth=(USERNAME, PASSWORD), data=metadata.encode('UTF-8'), headers={'Content-Type':'application/xml;charset=UTF-8'})
    file = open(FILE_API_METADATA, 'a')
    if response.status_code != 200:

        file.write(str(response.status_code) + " " + doi + " " + response.text + "\n")
        print(str(response.status_code) + " " + response.text)


def sendMetadataPhrase(filename, id):
    """
    Fonction qui intérroge l'API de Datacite avec une requête http POST

    Envoye le fichier de métadonnées de la phrase ou du mot en XML respectant le modèle DOI
    :param filename: le fichier XML de métadonnées
    :type filename: file
    :param id : ID xml de la phrase ou du mot utilisé pour créer le nom du fichier texte qui enregistre les réponses à la requête HTTP
    :type id: str

    """

    # ouvre en mode lecture le fichier XML
    metadata = open(filename, 'r', encoding='utf8').read()
    # envoie la requête HTTP POST.
    # La methode post prend comme paramètre le lien URL du web service,
    # les informations d'autentificantion, le fichier XML et les headers
    response = requests.post(ENDPOINTMETADATA, auth=(USERNAME, PASSWORD), data=metadata.encode('UTF-8'), headers={'Content-Type':'application/xml;charset=UTF-8'})
    file = open(FILE_API_METADATA, 'a')
    if response.status_code != 200:
        file.write(str(response.status_code) + " " + id + " " + response.text + "\n")
        # print(str(response.status_code) + " " + response.text)

