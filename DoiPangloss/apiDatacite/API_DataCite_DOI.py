import requests
from constantes import USERNAME, PASSWORD, ENDPOINTDOI, FILE_API_URL

def sendUrlDoiResource(filename, doi):
    """
    Fonction qui intérroge l'API de Datacite avec une requête http PUT

    Envoie le nom DOI et le fichier texte contenant le nom DOI et le lien URL de la ressource
    :param filename: le fichier text contenant le nom DOI et le lien URL de la ressource
    :type filename: file
    :param doi: nom DOI de la resosurce
    :type doi: str
    """
    
    # ouvre en mode lecture le fichier texte et élimine les espaces vide du début des chaines de caractères
    urlFile = open(filename, 'r', encoding='utf8').read().strip()
    # print ('urlFile ---------------------', urlFile, ' --------------------')
    # envoie la requête HTTP PUT.
    # La methode put prend comme paramètre le lien URL du web service, concaténé avec le nom DOI,
    # les informations d'autentificantion, le fichier texte et les headers

    response = requests.put(ENDPOINTDOI + doi, auth=(USERNAME, PASSWORD), data=urlFile.encode('utf-8'),
                            headers={'Content-Type': 'text/plain;charset=UTF-8'})

    # ouvre en mode écriture un fichier qui va enregistrer les réponses du serveur.
    file = open(FILE_API_URL, 'a')
    if response.status_code != 200:

        file.write(str(response.status_code) + " " + doi + " " + response.text + "\n")
        print(str(response.status_code) + " ******** " + response.text)



def sendUrlDoiPhrase(filename, doi, id):
    """
    Fonction qui intérroge l'API de Datacite avec une requête http PUT

    Envoye le nom DOI et le fichier texte contenant le nom DOI et le lien URL de la phrase et du mot
    :param filename: le fichier text contenant le nom DOI et le lien URL de la ressource
    :type filename: file
    :param doi: nom DOI de la phrase
    :type doi: str
    :param id: identifiant XML de la phrase ou du mot utilisé pour créer le nom du fichier texte qui enregistre les réponses à la requête HTTP
    :type id: str

    """
    # ouvre en mode lecture le fichier texte et élimine les espaces vide du début des chaines de caractères
    urlFile = open(filename, 'r', encoding='utf8').read().strip()
    # envoie la requête HTTP PUT.
    # La methode put prend comme paramètre le lien URL du web service, concaténé avec le nom DOI,
    # les informations d'autentificantion, le fichier texte et les headers
    response = requests.put(ENDPOINTDOI + doi, auth=(USERNAME, PASSWORD), data=urlFile.encode('utf-8'),
                            headers={'Content-Type': 'text/plain;charset=UTF-8'})
    # ouvre en mode écriture un fichier qui va enregistrer les réponses du serveur.
    file = open(FILE_API_URL, 'a')
    if response.status_code != 200:
        file.write(str(response.status_code) + " " + id + " " + response.text + "\n")
        print(str(response.status_code) + " " + response.text)
