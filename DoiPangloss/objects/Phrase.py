import xml.etree.ElementTree as ET
import logging
from constantes import CRITICAL_LOG, FOLDER_METADATA_PHRASE, FOLDER_URL_DOI_PHRASE

logging.basicConfig(filename=CRITICAL_LOG,level=logging.INFO)



class Phrase:
    """
    Classe qui génère des objets phrases pour une phrase ou un mot des fichiers d'annotations

    Contient la méthode  __init__ qui est constructeur d'objet de la classe Phrase

    Contient la methode buildMetadataPhrase qui génère le fichier XML selon le modèle DOI pour chaque phrase ou mot

    Contient la methode generateFileUrlDoiPhrase qui construit le fichier texte contenant le nom DOI et le lien URL de la phrase ou du mot
    """

    def __init__(self, id, doiPhrase, affixe, objetRecord):
        """
        Constructeur d'objet de la classse Phrase

        :param id: identifient XML des phrases du fichier d'annotations
        :type id: str
        :param doiPhrase: DOI de la phrase ou du mot
        :type doiPhrase: str
        :param affixe: suffixe ou préfixe en fonction du placement des initiales S (pour sentence) et W (pour word)
        :type affixe: str
        :param objetRecord:
        :type objetRecord: object
        """
        self.id = id
        self.doiPhrase = doiPhrase
        self.affixe = affixe
        self.objetRecord = objetRecord

    def buildMetadataPhrase(self):
        """
        Fonction qui génère le fichier XML à partir des attributs de la classe Phrase
        :return: le fichier XML contenant les métadonnées selon le format DOI pour une phrase ou un mot
        :rtype file
        """

        racine = ET.Element("resource", xmlns="http://datacite.org/schema/kernel-4")
        racine.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        racine.set("xsi:schemaLocation",
                               "http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.2/metadata.xsd")

        # création de la balise identifier contenant le DOI
        if self.doiPhrase:
            identifier = ET.SubElement(racine, "identifier", identifierType="DOI")
            identifier.text = self.doiPhrase
        else:
            message = "La balise IDENTIFIER pour le record {} est obligatoire!!".format(self.id)
            logging.info(message)

         # les créateurs
         # création de la balise parente "creators"
        creators = ET.SubElement(racine, "creators")
        # déclare une variable booléenne à False
        booleen = False
        # pour chaque liste du type (nom personne, rôle) dans la liste globale contributeursDoi
        for personneRole in self.objetRecord.contributeursDoi:
            # si le rôle est ‘researcher’, crée la balise creator et la balise enfant creatorName
            if "Researcher" in personneRole[1]:
                creator = ET.SubElement(creators, "creator")
                creatorName = ET.SubElement(creator, "creatorName", nameType="Personal")
                creatorName.text = personneRole[0]
                # la condition est satisfaite, la balise creator a été créee et le booléen passe à True
                booleen = True
        # si la condition n’est pas satisfaite, car la balise creator n’a pas été créée,
        # le booléen est False et dans ce cas, c’est le contributor avec le rôle ContactPerson qui va devenir creator.
        if not booleen:
            for personneRole in self.objetRecord.contributeursDoi:
                if "ContactPerson" in personneRole[1]:
                    creator = ET.SubElement(creators, "creator")
                    creatorName = ET.SubElement(creator, "creatorName")
                    creatorName.text = personneRole[0]
                    booleen = True
        # si le booléen est toujours False, crée un log pour préciser que la balise Creator est obligatoire
        if not booleen:
            message = "La balise CREATOR pour le record {} est obligatoire!!".format(self.objetRecord.identifiantOAI)
            logging.info(message)

        # les titres
        # creation de la balise titre
        if self.objetRecord.titre:
            titles = ET.SubElement(racine, "titles")
            title = ET.SubElement(titles, "title")
            # le contenu de la balise titre est la concaténation de l'affixe et du titre du fichier d'annotations
            title.text = self.affixe + ':' + self.objetRecord.titre
            # ajoute l'attribut xml:lang pour le titre si l'objet record en contient un
            if self.objetRecord.codeXmlLangTitre:
                title.set("xml:lang", self.objetRecord.codeXmlLangTitre)
        else:
            message = "La balise TITLE pour le record {} est obligatoire!!".format(self.objetRecord.identifiantOAI)
            logging.info(message)

        # le publisher
        publisher = ET.SubElement(racine, "publisher")
        publisher.text = self.objetRecord.publisher

        # année de publication
        if self.objetRecord.annee:
            publicationYear = ET.SubElement(racine, "publicationYear")
            publicationYear.text = self.objetRecord.annee[:4]
        else:
            message = "La balise PUBLICATIONYEAR pour le record {} est obligatoire!!".format(self.objetRecord.identifiantOAI)
            logging.info(message)

        # la langue
        if self.objetRecord.codeLangue:
            # prend la première valeur de la liste avec les codes des langues
            language = ET.SubElement(racine, "language")
            language.text = self.objetRecord.codeLangue[0]

        # le type de ressource
        if self.objetRecord.labelType:
            resourceType = ET.SubElement(racine, "resourceType", resourceTypeGeneral=self.objetRecord.typeRessourceGeneral)
            resourceType.text = self.objetRecord.labelType
        else:
            message = "La balise RESOURCETYPE pour le record {} est obligatoire!!".format(self.objetRecord.identifiantOAI)
            logging.info(message)

        # l'identifiant alternatif représenté par l'attribut id de la balise XML <S> ou <W>
        alternateIdentifiers = ET.SubElement(racine, "alternateIdentifiers")
        alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                            alternateIdentifierType="xml_ID")
        alternateIdentifier.text = self.id

        # is Part of. La phrase est relié comment faisant partie de l'identifiant du fichier d'annotations
        if self.objetRecord.doiIdentifiant:
            relatedIdentifiers = ET.SubElement(racine, "relatedIdentifiers")
            isPartof = ET.SubElement(relatedIdentifiers, "relatedIdentifier",
                                     relatedIdentifierType="DOI",
                                     relationType="IsPartOf")
            isPartof.text = self.objetRecord.doiIdentifiant
        else:
            message = "La balise IDENTIFIER pour le record {} est obligatoire!!".format(
                self.objetRecord.identifiantOAI)
            logging.info(message)
        
        # génération du fichier XML en format DOI
        tree = ET.ElementTree(racine)
        # le nom du fichier est la concéténation de l'identifiant OAI réduit + l'id xml de la phrase ou du mot
        tree.write(FOLDER_METADATA_PHRASE + self.objetRecord.identifiantOAI[21:] + "." + self.id + ".xml", encoding="UTF-8", xml_declaration=True, default_namespace=None, method="xml")

        # vérifie que le fichier XML est créé
        if FOLDER_METADATA_PHRASE + self.objetRecord.identifiantOAI[21:]+"."+self.id+".xml":
            return FOLDER_METADATA_PHRASE + self.objetRecord.identifiantOAI[21:]+ "." +self.id + ".xml"
        else:
            return None


    def generateFileUrlDoiPhrase(self):
        """
        Fonction qui génère un fichier texte
        :return: fichier texte contenant le lien URL et le DOI de la phrase ou du mot
        :rtype file
        """
        with open(FOLDER_URL_DOI_PHRASE + self.objetRecord.identifiantOAI[21:]+"."+self.id +".txt", "w") as fichierUrlPhrase:
            # le lien URL des phrases ou des mots doit etre mis à jour.
            url = "url= " + self.objetRecord.url + "/#/" + self.id
            doi = "doi= " + self.doiPhrase
            fichierUrlPhrase.write(doi + "\n" + url)

        # vérifie que le fichier text est créé ou pas
        if FOLDER_URL_DOI_PHRASE + self.objetRecord.identifiantOAI[21:]+"."+self.id +".txt":
            return FOLDER_URL_DOI_PHRASE + self.objetRecord.identifiantOAI[21:]+"."+self.id +".txt"
        else:
            return None



