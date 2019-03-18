import xml.etree.ElementTree as ET
import logging
from constantes import SCHEME_URI, PURL, CRITICAL_LOG, DOI_PANGLOSS, FOLDER_METADATA_RECORD, FOLDER_URL_DOI_RECORD

logging.basicConfig(filename=CRITICAL_LOG, level=logging.INFO)


class Record:
    """
    Classe qui génère des objets record pour une ressource du fichier de métadonnées Cocoon

    Contient la méthode __init__ qui est constructeur d'objet de la classe Record

    Contient la methode buildMetadataResource qui génère le fichier XML selon le modèle DOI pour chaque ressource

    Contient la methode generateFileUrlDoiResource qui génère le fichier texte contenant le nom DOI et le lien URL de la ressource
    """

    def __init__(self, doiIdentifiant, identifiantOAI, publisherInstitution, format, annee, taille, titre,
                 codeXmlLangTitre, titresSecondaire, droits, licence, contributeursDoi, droitAccess,
                 codeLangue, labelLangue, sujets, labelType, typeRessourceGeneral, isRequiredBy,
                 requires, identifiant_Ark_Handle, lienAnnotation, abstract, tableDeMatiere, descriptionsOlac,
                 labelLieux, longitudeLatitude, pointCardinaux, url):
        """
        Constructeur d'objet de la classe Record

        Contient des attributs avec des valeurs par défaut (setSpec, publisher, hostingInstitution)
        Contient aussi des attributs avec des valeurs issues des éléments composant la balise record

        :param doiIdentifiant: identifiant DOI présent dans la balise <dc:identifier>
        :type doiIdentifiant : str
        :param identifiantOAI: identifiant OAI présent dans la balise <oai:identifier>`
        :type identifiantOAI: str
        :param publisherInstitution: valeur par défaut
        :type publisherInstitution: str
        :param format: format de la ressource. Elémént présent dans la balise <dc:format>
        :type format: list
        :param annee: année de publication. Elément présent dans la balise <dcterms:available>
        :type annee: str
        :param taille: dimension de la ressource. Elément présent dans la baise <dcterms:extent>
        :type taille: str
        :param titre: titre de la ressource. Elément présent dans la balise <dc:title>
        :type titre: str
        :param codeXmlLangTitre: code XML du titre. Attribut de la balise <dc:title>
        :type codeXmlLangTitre: str
        :param titresSecondaire: titre alternatif de la ressource. Elément présent dans la balise <dcterms:alternative>
        :type titresSecondaire: list
        :param droits: personne qui détient les droits sur la ressource. Elément présent dans la balise <dc:rights>
        :type droits: str
        :param licence: type de licence concernant les droits. Elément présent dans la balise <dcterms:licence>
        :type licence: str
        :param contributeursDoi: nom des contributeurs de la ressource. Eléments convertis à partir de la liste des contributeurs
        :type contributeursDoi: list
        :param droitAccess: description des droits d'acces à la ressource. Elément présent dans la balise <dcterms:accessRights>
        :type droitAccess: str
        :param codeLangue: le code de la langue principale de la ressource. Elément présent dans l'attribut olac:code de la balise <dc:subject>
        :type codeLangue: list
        :param labelLangue: l'intitulé de la langue principale de la ressource et l'attribut xml:lang. Elément présent dans la balise <dc:subject>
        :type labelLangue: list
        :param sujets: les mots clés et les attribut xml:lang. Elément présent dans la balise <dc:subject>
        :type sujets: list
        :param labelType: le type de la ressource. Elément présent dans l'attribut olac:code de la balise <dc:type> où xsi:type = olac:discourse-type
        :type labelType: str
        :param typeRessourceGeneral: type général de la ressource. Elément présent dans la balise où xsi:type = dcterms:DCMIType
        :type typeRessourceGeneral: str
        :param isRequiredBy: l'URI de la ressource qui appelle la ressource actuelle. Elément présent dans la balise <dcterms:isRequiredBy>
        :type isRequiredBy: list
        :param requires: l'URI de la ressource qui est appellé par la ressource actuelle. Elément présent dans la balise <dcterms:requires>
        :type requires: list
        :param identifiant_Ark_Handle: les identifiants ark et handle.Elément présent dans la balise <dc:identifier>
        :type identifiant_Ark_Handle: list
        :param lienAnnotation: lien URL des fichiers d'annotations en XML
        :type lienAnnotation: str
        :param abstract: le résumé descriptif. Elémént présent dans la balise <dcterms:abstract>
        :type abstract: list
        :param tableDeMatiere:sommaire. Elément présent dans la balise <dcterms:tableOfContents>
        :type tableDeMatiere: list
        :param descriptionsOlac: description de la ressource. Elément présent dans la balise <dc:description>
        :type descriptionsOlac: list
        :param labelLieux: le nom du lieu. Elément présent dans la balise <dcterms:spatial>
        :type labelLieux: list
        :param longitudeLatitude: les 2 valeurs de la longitude et latitude. Eléments présents dans la balise <dcterms:Point>
        :type longitudeLatitude: list
        :param pointCardinaux: les 4 valeurs des points cardinaux. Eléments présents dans la balise <dcterms:Box>
        :type pointCardinaux: list
        :param url: le lien URL de la ressource sur le site Pangloss de Lacito
        :type url: str
        """
        # self.doiIdentifiant = doiIdentifiant.replace('https://doi.org/','')
        self.doiIdentifiant = doiIdentifiant
        self.identifiantOAI = identifiantOAI
        self.setSpec = "Linguistique"
        self.publisher = "Pangloss"
        self.publisherInstitution = publisherInstitution
        self.hostingInstitution = ["COllections de COrpus Oraux Numériques", "Huma-Num",
                                   "Langues et Civilisations à Tradition Orale",
                                   "Centre Informatique National de l'Enseignement Supérieur"]
        self.format = format
        self.annee = annee
        self.relatedIdPangloss = DOI_PANGLOSS
        self.taille = taille
        self.titre = titre
        self.codeXmlLangTitre = codeXmlLangTitre
        self.titresSecondaire = titresSecondaire
        self.droits = droits
        self.licence = licence
        self.contributeursDoi = contributeursDoi
        self.droitAccess = droitAccess
        self.codeLangue = codeLangue
        self.labelLangue = labelLangue
        self.sujets = sujets
        self.labelType = labelType
        self.typeRessourceGeneral = typeRessourceGeneral
        self.isRequiredBy = isRequiredBy
        self.requires = requires
        self.identifiant_Ark_Handle = identifiant_Ark_Handle
        self.lienAnnotation = lienAnnotation
        self.abstract = abstract
        self.tableDeMatiere = tableDeMatiere
        self.descriptionsOlac = descriptionsOlac
        self.labelLieux = labelLieux
        self.longitudeLatitude = longitudeLatitude
        self.pointCardinaux = pointCardinaux
        self.url = url

    def buildMetadataResource(self):
        """
        Fonction qui génère le fichier XML à partir des attributs de la classe Record
        :return: le fichier XML contenant les métadonnées selon le format DOI pour une ressource
        :rtype file
        """


        racine = ET.Element("resource", xmlns="http://datacite.org/schema/kernel-4")
        racine.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        racine.set("xsi:schemaLocation",
                               "http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.1/metadata.xsd")

        # l'identifiant DOI
        # création de la balise identifier pour l'identifiant DOI
        if self.doiIdentifiant:
            identifier = ET.SubElement(racine, "identifier", identifierType="DOI")
            identifier.text = self.doiIdentifiant
        else:
            message = "La balise IDENTIFIER pour le record {} est obligatoire!!".format(self.identifiantOAI)
            logging.info(message)

        # les titres
        # creation de la balise titre
        if self.titre:
            titles = ET.SubElement(racine, "titles")
            title = ET.SubElement(titles, "title")
            title.text = self.titre
            # ajoute l'attribut xml:lang pour le titre s'il en contient un
            if self.codeXmlLangTitre:
                title.set("xml:lang", self.codeXmlLangTitre)
        else:
            message = "La balise TITLE pour le record {} est obligatoire!!".format(self.identifiantOAI)
            logging.info(message)

        # Le deuximèe titre s'il existe
        if self.titresSecondaire:
            # parcourt les listes imbriquées de la liste titresSecondaire
            # pour chaque liste
            for groupe in self.titresSecondaire:
                titreS = ET.SubElement(titles, "title")
                # si le premier élément de la liste imbriquée existe, il s'agit de l'attribut xml:lang,
                # donc il faut l'ajouter comme attribut à la balise titre
                # le deuxième élement de la liste est le titre
                if groupe[0] is not None:
                    titreS.text = groupe[1]
                    titreS.set("xml:lang", groupe[0])
                # sinon, si le premier élement est None, donc le titre est rajouté à la balise sans attribut xml:lang
                else:
                    titreS.text = groupe[1]

        # les createurs et contributeurs
        # création des deux éléments parents creators et contributors
        creators = ET.SubElement(racine, "creators")
        contributors = ET.SubElement(racine, "contributors")
        # déclare une variable booléenne à False
        booleen = False
        # pour chaque liste du type (nom personne, rôle) dans la liste globale
        for personneRole in self.contributeursDoi:
            # si le rôle est ‘researcher’, crée la balise creatorName et contributorName
            if "Researcher" in personneRole[1]:
                creator = ET.SubElement(creators, "creator")
                creatorName = ET.SubElement(creator, "creatorName", nameType="Personal")
                creatorName.text = personneRole[0]
                contributor = ET.SubElement(contributors, "contributor", contributorType='Researcher')
                contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
                contributorName.text = personneRole[0]
                # la condition est satisfaite, la balise creator a été créee et le booléen passe à True
                booleen = True
            # sinon si le rôle est ‘DataCurator’, 'Other', 'DataCollector, 'ContactPerson', 'Editor', 'Sponsor' crée la balise contributorName
            elif "DataCurator" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='DataCurator')
                contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
                contributorName.text = personneRole[0]
            elif "Other" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='Other')
                contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
                contributorName.text = personneRole[0]
            elif "DataCollector" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='DataCollector')
                contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
                contributorName.text = personneRole[0]
            elif "ContactPerson" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='ContactPerson')
                contributorName = ET.SubElement(contributor, "contributorName")
                contributorName.text = personneRole[0]
            elif "Editor" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='Editor')
                contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
                contributorName.text = personneRole[0]
            elif "Sponsor" in personneRole[1]:
                contributor = ET.SubElement(contributors, "contributor", contributorType='Sponsor')
                contributorName = ET.SubElement(contributor, "contributorName")
                contributorName.text = personneRole[0]
        # si la condition n’est pas satisfaite, car la balise creator n’a pas été créée,
        # le booléen est False et dans ce cas, c’est le contributor avec le rôle ContactPerson qui va devenir creator.
        if not booleen:
            for personneRole in self.contributeursDoi:
                if "ContactPerson" in personneRole[1]:
                    creator = ET.SubElement(creators, "creator")
                    creatorName = ET.SubElement(creator, "creatorName")
                    creatorName.text = personneRole[0]
                    booleen = True
        # si le booléen est toujours False, crée un log pour préciser que la balise Creator est obligatoire
        if not booleen :
            message = "La balise CREATOR pour le record {} est obligatoire!!".format(self.identifiantOAI)
            logging.info(message)

        # laboratroire = role producteur
        for institution in self.publisherInstitution:
            contributor = ET.SubElement(contributors, "contributor", contributorType="Producer")
            contributorName = ET.SubElement(contributor, "contributorName", nameType="Organizational")
            contributorName.text = institution

        # etablissement = role Hosting Institution
        for institution in self.hostingInstitution:
            contributor = ET.SubElement(contributors, "contributor", contributorType="HostingInstitution")
            contributorName = ET.SubElement(contributor, "contributorName", nameType="Organizational")
            contributorName.text = institution

        # contributeur = role droit
        if self.droits:
            contributor = ET.SubElement(contributors, "contributor", contributorType='RightsHolder')
            contributorName = ET.SubElement(contributor, "contributorName")
            contributorName.text = self.droits

        # les droits d'accès
        if self.droitAccess:
            rightsList = ET.SubElement(racine, "rightsList")
            rights = ET.SubElement(rightsList, "rights")
            rights.text = self.droitAccess

        # licence
        if self.licence:
            licencedoi = ET.SubElement(rightsList, "rights", rightsURI=self.licence)
            licencedoi.text = "Creative Commons Attribution-NonCommercial 2.5 Generic"

        # le publisher
        publisher = ET.SubElement(racine, "publisher")
        publisher.text = self.publisher

        # année de publication
        if self.annee:
            publicationYear = ET.SubElement(racine, "publicationYear")
            publicationYear.text = self.annee[:4]
        else:
            message = "La balise PUBLICATIONYEAR pour le record {} est obligatoire!!".format(self.identifiantOAI)
            logging.info(message)

        # la langue
        if self.codeLangue:
            # prend la première valeur de la liste
            language = ET.SubElement(racine, "language")
            language.text = self.codeLangue[0]

        # les mots clés
        subjects = ET.SubElement(racine, "subjects")

        subject = ET.SubElement(subjects, "subject")
        subject.text = self.setSpec

        if self.labelLangue:
            for label in self.labelLangue:
                # crée la balise subject avec l'attribut OLAC et la valeur du schema uri
                subject = ET.SubElement(subjects, "subject", subjectScheme="OLAC",
                                        schemeURI=SCHEME_URI)

                # vérifie que la liste contient un attribut xml:lang.
                if label[0] is not None:
                    #  ajoute le label de la langue comme mot clé
                    subject.text = label[1]
                    # ajoute l'attribut xml
                    subject.set("xml:lang", label[0])
                # si le premier élément de la liste imbriquée est None, ajoute le label de la lague sans attribut xml:lang
                else:
                    subject.text = label[1]

        # si la liste sujets existe
        if self.sujets:
            for mot in self.sujets:
                # si le mot est une chaine de caractères, cela veut dire qu'il n'a pas d'attribut xml:lang
                # la balise subject sera composée uniquement du mot clé.
                if isinstance(mot, str):
                    subject = ET.SubElement(subjects, "subject")
                    subject.text = mot
                # sinon, le mot clé est une liste imbriquée composée d'un attribut xml:lang et du mot clé.
                else:
                    # crée la balise subject
                    subject = ET.SubElement(subjects, "subject")
                    # ajoute le contenu de la balise
                    subject.text = mot[1]
                    # ajoute l'attribut xml:lang
                    subject.set("xml:lang", mot[0])

        # le type de ressource
        if self.labelType:
            resourceType = ET.SubElement(racine, "resourceType", resourceTypeGeneral=self.typeRessourceGeneral)
            resourceType.text = self.labelType
        else:
            message = "La balise RESOURCETYPE pour le record {} est obligatoire!!".format(self.identifiantOAI)
            logging.info(message)

        # les dates
        dates = ET.SubElement(racine, "dates")
        date = ET.SubElement(dates, "date", dateType="Available")
        date.text = self.annee

        # les identifiants
        # crée la balise parente alternateIdentifiers
        alternateIdentifiers = ET.SubElement(racine, "alternateIdentifiers")
        # crée la balise enfant alternateIdentifier avec comme attribut alternateIdentifierType="internal ID"
        alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                            alternateIdentifierType="internal ID")
        # le contenu de la balise est l'identifiant oai
        alternateIdentifier.text = self.identifiantOAI

        # procédure similaire pour les identifiants purl, ark et handle
        alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                            alternateIdentifierType="PURL")
        alternateIdentifier.text = PURL + self.identifiantOAI[21:]

        if self.identifiant_Ark_Handle:
            for identifiant in self.identifiant_Ark_Handle:
                alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                                    alternateIdentifierType=identifiant[0])
                alternateIdentifier.text = identifiant[1]

        # les identifiants de relation
        if self.isRequiredBy or self.requires or self.relatedIdPangloss:
            # crée la balise parente relatedIdentifiers
            relatedIdentifiers = ET.SubElement(racine, "relatedIdentifiers")

        if self.isRequiredBy:
            # crée la balise enfant relatedIdentifier
            for identifiantRel in self.isRequiredBy:
                relatedIdentifier = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="PURL",
                                                  relationType="IsRequiredBy")
                relatedIdentifier.text = PURL + identifiantRel[21:]

        if self.requires:
            for identifiantRequires in self.requires:
                relatedIdentifier = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="PURL",
                                                  relationType="Requires")
                relatedIdentifier.text = PURL + identifiantRequires[21:]

        idPangloss = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="DOI",
                                   relationType="IsPartOf")
        idPangloss.text = self.relatedIdPangloss

        # le format
        if self.format:
            formats = ET.SubElement(racine, "formats")
            for element in self.format:
                format = ET.SubElement(formats, "format")
                format.text = element

        if self.taille:
            sizes = ET.SubElement(racine, "sizes")
            size = ET.SubElement(sizes, "size")
            size.text = self.taille

        # les descriptions, représentées par trois listes
        if self.abstract or self.tableDeMatiere or self.descriptionsOlac:
            descriptions = ET.SubElement(racine, "descriptions")

        if self.abstract:
            for element in self.abstract:
                # si la descritpion est une chaine de caractères, cela veut dire qu'il n'a pas d'attribut xml:lang
                if isinstance(element, str):
                    description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                    # la balise description sera composée uniquement du mot clé.
                    description.text = element
                # sinon, la description est une liste imbriquée composée d'un attribut xml:lang et du texte de la description.
                else:
                    description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                    # ajoute le deuxième élément de la liste (le texte de la description) au contenu de la balise
                    description.text = element[1]
                    # ajoute le deuxième élément de la liste (l'attribut xml:lang) au contenu de la balise
                    description.set("xml:lang", element[0])

        # procédure similaire au traitement de la liste abstract
        if self.tableDeMatiere:
            for element in self.tableDeMatiere:
                if isinstance(element, str):
                    description = ET.SubElement(descriptions, "description", descriptionType="TableOfContents")
                    description.text = element
                else:
                    description = ET.SubElement(descriptions, "description", descriptionType="TableOfContents")
                    description.text = element[1]
                    description.set("xml:lang", element[0])

        # procédure similaire au traitement de la liste abstract
        if self.descriptionsOlac:
            for element in self.descriptionsOlac:
                if isinstance(element, str):
                    # si le mot Equipment fait partie du contenu de la balise description, alors cet élément aura l'attribut TechnicalInfo
                    if "Equipment" in element:
                        description = ET.SubElement(descriptions, "description", descriptionType="TechnicalInfo")
                        description.text = element

                    # sinon si la balise abstract existe, alors la balise description aura l'attribut Other, si elle n'existe pas, l'attribut Abstract
                    elif self.abstract:
                        description = ET.SubElement(descriptions, "description", descriptionType="Other")
                        description.text = element
                    else:
                        description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                        description.text = element
                # la même chose, mais pour le cas où abstract contient l'attribut xml-lang
                else:
                    if "Equipment" in element[1]:
                        description = ET.SubElement(descriptions, "description", descriptionType="TechnicalInfo")
                        description.text = element[1]
                        description.set("xml:lang", element[0])

                    elif self.abstract:
                        description = ET.SubElement(descriptions, "description", descriptionType="Other")
                        description.text = element[1]
                        description.set("xml:lang", element[0])
                    else:
                        description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                        description.text = element[1]
                        description.set("xml:lang", element[0])

        # les lieux géographiques
        if self.labelLieux:
            geoLocations = ET.SubElement(racine, "geoLocations")
            for element in self.labelLieux:
                geoLocation = ET.SubElement(geoLocations, "geoLocation")
                geoLocationPlace = ET.SubElement(geoLocation, "geoLocationPlace")
                geoLocationPlace.text = element

            if self.longitudeLatitude:
                geoLocationPoint = ET.SubElement(geoLocation, "geoLocationPoint")
                pointLongitude = ET.SubElement(geoLocationPoint, "pointLongitude")
                pointLongitude.text = self.longitudeLatitude[0]
                pointLatitude = ET.SubElement(geoLocationPoint, "pointLatitude")
                pointLatitude.text = self.longitudeLatitude[1]

            if self.pointCardinaux:
                geoLocationBox = ET.SubElement(geoLocation, "geoLocationBox")
                westBoundLongitude = ET.SubElement(geoLocationBox, "westBoundLongitude")
                westBoundLongitude.text = self.pointCardinaux[0]
                eastBoundLongitude = ET.SubElement(geoLocationBox, "eastBoundLongitude")
                eastBoundLongitude.text = self.pointCardinaux[1]
                southBoundLatitude = ET.SubElement(geoLocationBox, "southBoundLatitude")
                southBoundLatitude.text = self.pointCardinaux[2]
                northBoundLatitude = ET.SubElement(geoLocationBox, "northBoundLatitude")
                northBoundLatitude.text = self.pointCardinaux[3]

        # génération du fichier XML en format DOI
        tree = ET.ElementTree(racine)
        # le nom du fichier est l'identifiant OAI réduit
        tree.write(FOLDER_METADATA_RECORD + self.identifiantOAI[21:] + ".xml", encoding="UTF-8", xml_declaration=True,
                   default_namespace=None, method="xml")

        # vérifie que le fichier XML est créé
        if FOLDER_METADATA_RECORD + self.identifiantOAI[21:] + ".xml":
            return FOLDER_METADATA_RECORD + self.identifiantOAI[21:] + ".xml"
        else:
            return None

    def generateFileUrlDoiResource(self):
        """
        Fonction qui génère un fichier texte
        :return: fichier texte contenant le lien URL et le DOI de la ressource
        :rtype file
        """
        with open(FOLDER_URL_DOI_RECORD + self.identifiantOAI[21:] + ".txt", "w") as fichierUrl:
            url = "url= " + self.url
            doi = "doi= " + self.doiIdentifiant
            fichierUrl.write(doi + "\n" + url)

        # vérifie que le fichier text est créé ou pas
        if FOLDER_URL_DOI_RECORD + self.identifiantOAI[21:] + ".txt":
            return FOLDER_URL_DOI_RECORD + self.identifiantOAI[21:] + ".txt"
        else:
            return None
