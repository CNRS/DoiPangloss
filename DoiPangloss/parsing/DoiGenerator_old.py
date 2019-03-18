import xml.etree.ElementTree as ETree
import re
from constantes import NAMESPACES
from apiDatacite.API_Get_DataCite_DOI import extractDoiOai

# --------utilisations des trois méthodes suivantes pour crééer le nom DOI à l'aide d'un compteur et retour du dernier numéro --------# --------#

def extractDoiIdentifiantFromRecord(record):
    """
    Fonction qui extrait le nom DOI depuis la balise dc:identifier du fichier de métadonnées
    :param record: élément de la classe 'xml.etree.ElementTree.Element'
    :return: le nom DOI
    :rtype str
    """
    doiIdentifiant = ""
    for identifiant in record.findall('.//dc:identifier', NAMESPACES):
        if "doi:" in identifiant.text:
            doiIdentifiant = identifiant.text[4:]
    return doiIdentifiant


def getLastDoiNumberFromRecord(file):
    """
    Fonction qui parcourt la liste contenant tous les identifiants DOI et retourne la valeur chiffrée du dernier doi
    :param file: le fichier de métadonnées à parcourir
    :type file: file
    :return: le dernier doi
    :rtype int
    """

    lastDoi = 0
    listAllDoiIdentifier = []

    tree = ETree.parse(file)
    root = tree.getroot()

    for record in root.findall(".//oai:record", NAMESPACES):

        # appel de la fonction extractDoiIdentifiantFromRecord pour extraire uniquement le DOI
        doiIdentifiant = extractDoiIdentifiantFromRecord(record)

        if doiIdentifiant != "":
            listAllDoiIdentifier.append(doiIdentifiant)

    for doi in listAllDoiIdentifier:
        # puisqu'un doi aura ce type de structure "doi:10.5072/PANGLOSS-0000003",
        # il faut récupérer uniquement les 7 derniers chiffres
        number = int(doi[-7:])

        if lastDoi < number:
            lastDoi = number

    return lastDoi

    
def getLastDoiNumberFromDataCite():
    """
    Fonction qui parcourt la liste contenant tous les identifiants DOI extraite à partir du DataCite et retourne la valeur chiffrée du dernier doi
    :return: le dernier doi
    :rtype int
    """

    lastDoi = 0
    listAllDoiIdentifier = []
    dicoDoiOai = {}
    expression = r"^[0-9]{7}$"
    
    
    
    dicoDoiOai = extractDoiOai()
    
    
    # for doi in dicoDoiOai.values():
        # print ('CONTENU : ', doi)
    
   
    for doi in dicoDoiOai.keys():
        
        if re.search(expression, doi[-7:]) is not None:
            # print (doi)
            listAllDoiIdentifier.append(doi)
    
    for doi in listAllDoiIdentifier:
        # puisqu'un doi aura ce type de structure "doi:10.5072/PANGLOSS-0000003",
        # il faut récupérer uniquement les 7 derniers chiffres
        number = int(doi[-7:])
        if lastDoi < number:
            lastDoi = number
    # print("lastDoi = ", lastDoi)        
    return lastDoi

def incrementDoi(lastDoiNumber):
    """
    Fonction qui incrémente de 1 le dernier numéro DOI et ajoute autant de zero pour arriver à un numéro composé de 7 chiffres
    :param lastDoiNumber: le dernier numéro doi
    :type lastDoiNumber: str
    :return: le numéro DOI incrémenté avec les zeros (chaine) et le dernier numéro DOI (integer)
    :rtype str, int
    """
    lastDoiNumber += 1
    # transforme le numéro en chaine de caractères pour connaître la longueur du numéro
    # à savoir le nombre de chiffres qui le compose
    doiNumber = str(lastDoiNumber)
    # trouve le nombre de zeros à rajouter au doi. Un numéro doi peut être formé de maximum 7 chiffres
    # donc le nombre de zeros est obtenu par la différence entre 7 et le chiffre représenant la taille du dernier numéro doi
    difference = 7 - len(doiNumber)
    # on itère sur les éléments en partant de 0 jusqu'à la différence entre 7 et le nombre de chiffres du dernier doi
    for i in range(0, difference):
        # on rajoute un 0 sous forme de chaine de caractère pour chaque élément trouvé
        # on concatène avec le numéro doi déja incrémété de 1 par rapport au dernier
        doiNumber = "0" + doiNumber

    return doiNumber, lastDoiNumber