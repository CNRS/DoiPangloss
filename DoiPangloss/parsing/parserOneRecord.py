# --------Parsing XML ------------------#
import xml.etree.ElementTree as ET
from constantes import NAMESPACES, DOI_PANGLOSS, DOI_PREFIX, EASTLING_PLAYER, SHOW_TEXT, SHOW_OTHER, IDREF
import re

tree = ET.parse("../data/lacito_verif.xml")
root = tree.getroot()

# --------Parse.py header--------#

# savoir si le record contient un identifiant doi
for identifiant in root.findall('.//dc:identifier', NAMESPACES):
    if "https://doi.org/" in identifiant.text:
        doiIdentifiant = identifiant.text[4:]

if root.find('*/identifier', NAMESPACES) is not None:
    identifiantOAI = root.find('*/identifier').text
    identifiant = DOI_PREFIX + identifiantOAI[21:]

else:
    identifiant = ""
    print("La balise identifiant n'existe pas")

setSpec = "Linguistique"

# --------Parse.py metadata-OLAC--------#

olac = root.find('*/olac:olac', NAMESPACES)

#extrait les publisher
publisherInstitution = []

for institution in olac.findall('dc:publisher', NAMESPACES):
    nomInstitution = institution.text
    publisherInstitution.append(nomInstitution)


# récupérer le contentnu de la balise titre
if olac.find("dc:title", NAMESPACES) is not None:
    titreElement = olac.find("dc:title", NAMESPACES)
    titre = titreElement.text
    # récupérer la valeur de l'attribut xml:lang du titre
    codeXmlLangTitre = titreElement.get('{http://www.w3.org/XML/1998/namespace}lang')
else:
    titre = ""
    print("La balise Titre n'existe pas")


# récupérer le titre alternatif et la langue dans une liste
titresSecondaire = []

for titreAlternatif in olac.findall('dcterms:alternative', NAMESPACES):
    titreLabel = titreAlternatif.text
    codeXmlLangTitreSecond = titreAlternatif.get("{http://www.w3.org/XML/1998/namespace}lang")
    titreLangList = [codeXmlLangTitreSecond, titreLabel]
    titresSecondaire.append(titreLangList)


# droit d'accès
droitAccess=""
if olac.find("dcterms:accessRights", NAMESPACES) is not None:
    droitAccess = olac.find("dcterms:accessRights", NAMESPACES).text


if olac.find('dc:format', NAMESPACES) is not None:
    format = olac.find('dc:format', NAMESPACES).text.split("/")
else:
    format =[]


if olac.find("dcterms:available", NAMESPACES) is not None:
    annee = olac.find("dcterms:available", NAMESPACES).text
else:
    annee =""


if olac.find("dcterms:extent", NAMESPACES) is not None:
    taille = olac.find("dcterms:extent", NAMESPACES).text
else:
    taille = ""


droits=''
if olac.find("dc:rights", NAMESPACES) is not None:
    droitsComplet = olac.find("dc:rights", NAMESPACES).text
    if re.match("Copyright [^A-Z]*", droitsComplet):
        droits = re.sub("Copyright [^A-Z]*", '', droitsComplet)
    else:
        print("Il y a une autre forme de droits")
        droits = ""


# les contributeurs. On extrait d'abord les valeurs et les rôles des contributeurs Olac
contributeursOlac = []
for contributor in olac.findall('dc:contributor', NAMESPACES):
    role = contributor.get('{http://www.language-archives.org/OLAC/1.1/}code')
    nomPrenom = contributor.text
    contributorList = [nomPrenom, role]
    contributeursOlac.append(contributorList)


contributeursDoi = []
for elem in contributeursOlac:
    if "transcriber" in elem[1] or "annotator" in elem[1] or "translator" in elem[1] or "compiler" in elem[1]:
        # transforme les rôles Olac en Contributor Type
        listeCurator =[elem[0], "DataCurator"]
        # si la liste n'est pas dans la liste globale contributeursDoi, l'ajouter à la liste
        if listeCurator not in contributeursDoi:
            contributeursDoi.append(listeCurator)
    elif "interpreter" in elem[1] or "recorder" in elem[1] or "interviewer" in elem[1]:
        listeCollector = [elem[0], "DataCollector"]
        if listeCollector not in contributeursDoi:
            contributeursDoi.append(listeCollector)
    elif "performer" in elem[1] or "responder" in elem[1] or "singer" in elem[1] or "speaker" in elem[1]:
        listeOther = [elem[0], "Other"]
        if listeOther not in contributeursDoi:
            contributeursDoi.append(listeOther)
    elif "depositor" in elem[1]:
        listeContactPerson = [elem[0], "ContactPerson"]
        contributeursDoi.append(listeContactPerson)
    elif "researcher" in elem[1]:
        listeResearcher = [elem[0], "Researcher"]
        contributeursDoi.append(listeResearcher)
    elif "editor" in elem[1]:
        listeEditor = [elem[0], "Editor"]
        contributeursDoi.append(listeEditor)
    elif "sponsor" in elem[1]:
        listeSponsor = [elem[0], "Sponsor"]
        contributeursDoi.append(listeSponsor)


# récupère le code de la langue principale de la ressource. On crée une liste parce que la balise subject est répétable
codeLangue = []
# récupère le label de la langue principale de la ressource
labelLangue = []
# récupère des mots-clés sous forme de chaine de caractères et des listes de mot-clé et xml:lang
sujets = []

for sujet in olac.findall('dc:subject', NAMESPACES):
    sujetAttribut = sujet.attrib

    # si la balise subject n'a pas d'attributs, la valeur de l'élement est ajouté à la liste de mots-cles
    if not sujetAttribut :
        sujets.append(sujet.text)
    else:
        # si la balise subject contient l'attribut type et la valeur olac:langue, recupérer les diférents informations sur les langues
        for cle, valeur in sujetAttribut.items():
            if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:language":
                # récupère le code de la langue et l'ajoute à la liste de code
                code = sujetAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')
                codeLangue.append(code)
                # récupére dans une liste la valeur de l'attribut xml:lang et le label de la langue et l'ajoute à la liste de label
                label = sujet.text
                codeXmlLangLabel = sujetAttribut.get('{http://www.w3.org/XML/1998/namespace}lang')
                listeAttribXmlLabel = [codeXmlLangLabel, label]
                labelLangue.append(listeAttribXmlLabel)
            # si la balise subject contient l'attribut xml:lang, récupére dans une liste la valeur de l'attribut et le contenu de l'élément
            if cle == "{http://www.w3.org/XML/1998/namespace}lang" and "{http://www.w3.org/2001/XMLSchema-instance}type" not in sujetAttribut:
                codeXmlLangSujet = valeur
                motCle = sujet.text
                listeAttribMot = [codeXmlLangSujet, motCle]
                # ajout de la liste attribut langue et mot clé à la liste de mots clés
                sujets.append(listeAttribMot)
print (labelLangue)
# Le type de ressource: récupère les informations des balises dc:type
# liste qui récupère le contenu de la balise type et la valeur de l'attribut olac:code et qui vont être affectés à l'élément type en sortie

labelType = ""
typeRessourceGeneral = ""
bool = False
for element in olac.findall("dc:type", NAMESPACES):
    typeAttribut = element.attrib
    if not typeAttribut:
        sujets.append(element.text)
    else:
        for cle, valeur in typeAttribut.items():
            if cle == '{http://www.w3.org/XML/1998/namespace}lang':
                codeXmlLangSujet = valeur
                motCle = element.text
                listeAttribMot = [codeXmlLangSujet, motCle]
                sujets.append(listeAttribMot)
            elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:DCMIType":
                # variable qui récupère le type de ressource general qui va être affecté à l'attribut typeRessourceGeneral en sortie
                if element.text == "MovingImage":
                    typeRessourceGeneral = "Audiovisual"
                else:
                    typeRessourceGeneral = element.text
            # on récupère le contenu de l'atttribut olac:code de la balise dc:type qui a comme valeur d'attribut olac:discourse-type,sinon afficher "(:unkn)"
            elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:discourse-type":
                labelType = typeAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')
                bool = True
if not bool:
    labelType = "(:unkn)"
    bool = True


isRequiredBy = []
for ressource in olac.findall('dcterms:isRequiredBy', NAMESPACES):
    isRequiredBy.append(ressource.text)

requires = []
for ressource in olac.findall('dcterms:requires', NAMESPACES):
    requires.append(ressource.text)


idPangloss = DOI_PANGLOSS

identifiant_Ark_Handle = []
for identifiantAlternatif in olac.findall('dc:identifier', NAMESPACES):
    identifiantAttribut = identifiantAlternatif.attrib

    for cle, valeur in identifiantAttribut.items():
        if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:URI":
            if "ark" in identifiantAlternatif.text:
                identifiantType = "ARK"
                lienArk = identifiantAlternatif.text
                listeIdLienArk = [identifiantType, lienArk]
                identifiant_Ark_Handle.append(listeIdLienArk)
            if "handle" in identifiantAlternatif.text:
                identifiantType = "Handle"
                lienHandle = identifiantAlternatif.text
                listeIdLienHandle = [identifiantType, lienHandle]
                identifiant_Ark_Handle.append(listeIdLienHandle)

lienAnnotation = ""
for identifiantAnnotation in olac.findall('dc:identifier', NAMESPACES):
    # extraire le lien du fichier xml contenant l'annontation
    if ".xml" in identifiantAnnotation.text:
        lienAnnotation = identifiantAnnotation.text
        break

# ajouter le code pour créer une balise licence

# récupère la description de la balise abstract sous la forme d'une liste avec le contenu de la balise
# et/ou avec une liste contenant l'attribut langue et le contenu de la balise
abstract = []
for contenu in olac.findall("dcterms:abstract", NAMESPACES):
    # récupère les attributs et valeurs d'attributs sous la forme d'un dictionnaire
    abstractAttrib = contenu.attrib
    # si la balise ne contient pas d'attributs, alors ajouter le contenu de l'élément à la liste
    if not abstractAttrib:
        abstract.append(contenu.text)
    # si la balise contient d'attributs (attributs xml:lang d'office), créer une liste avec le code de la langue et le contenu de la balise
    else:
        langueAbstract = abstractAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
        texteAbstract = contenu.text
        listeLangueContenu = [langueAbstract, texteAbstract]
        abstract.append(listeLangueContenu)

# récupérer le contenu de la balise tableOfContent
tableDeMatiere = []
for contenu in olac.findall("dcterms:tableOfContents", NAMESPACES):
    # récupère les attributs et valeurs de la balise sous la forme d'un dictionnaire
    tableAttrib = contenu.attrib
    # si la balise ne contient pas d'attributs, alors ajouter le contenu à la liste
    if not tableAttrib:
        tableDeMatiere.append(contenu.text)
    # si la balise contient d'attributs (attributs xml:lang d'office), créer une liste avec le code de la langue et le contenu de la balise
    else:
        langueTable = tableAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
        texteTable = contenu.text
        listeLangueContenu = [langueTable, texteTable]
        tableDeMatiere.append(listeLangueContenu)

# récupérer la description
descriptionsOlac = []
for texte in olac.findall("dc:description", NAMESPACES):
    descriptionAttrib = texte.attrib
    if not descriptionAttrib:
        contenuDescription = texte.text
        descriptionsOlac.append(contenuDescription)
    else:
        langueDescription = descriptionAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
        texteDescription = texte.text
        listeLangueContenu = [langueDescription, texteDescription]
        descriptionsOlac.append(listeLangueContenu)


# liste qui récupère les labels du lieu
labelLieux = []
longitudeLatitude = []
pointCardinaux = []
for lieu in olac.findall('dcterms:spatial', NAMESPACES):
    lieuAttrib = lieu.attrib
    if not lieuAttrib:
        labelLieux.append(lieu.text)
    for cle, valeur in lieuAttrib.items():
        if cle == '{http://www.w3.org/XML/1998/namespace}lang':
            labelLieux.append(lieu.text)

        # récupère les 2 points de la longitude et latitude en une seule chaine de caractères pour le cas où l'attribut est Point
        if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:Point":
            pointLieux = lieu.text

            # transforme la chaine en une liste avec deux élémentscomme suit: 'east=valeur', 'north=valeur'
            long_lat = pointLieux.split(";")

            # élimine l'espace en trop du contenu texte des deux éléments de la liste (north et east)
            point1sansEspaces = long_lat[0].strip()
            point2sansEspaces = long_lat[1].strip()

            # condition pour régler le problème d'ordre des éléments nord et sud. Récupération des valeurs chiffrées de la longitude et de la latitude
            if "east" in point1sansEspaces:
                longitude = point1sansEspaces[5:]
                latitude = point2sansEspaces[6:]
            else:
                longitude = point2sansEspaces[5:]
                latitude = point1sansEspaces[6:]

            longitudeLatitude.append(longitude)
            longitudeLatitude.append(latitude)


        # récupère les 4 points de la longitude et latitude en une seule chaine de caractères pour le cas où l'attribut est Box
        elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:Box":
            boxLieux = lieu.text
            # transforme la chaine en une liste avec quatre éléments : southlimit, northlimit, eastlimit, westlimit
            sudNordEstWest = boxLieux.split(';')

            # supression des espaces pour les quatres points
            sudSansEspace = sudNordEstWest[0].strip()
            nordSansEspace = sudNordEstWest[1].strip()
            estSansEspace = sudNordEstWest[2].strip()
            westSansEspace = sudNordEstWest[3].strip()

            # récupère uniquement la valeur chiffrée des quatre points
            sud = sudSansEspace[11:]
            nord = nordSansEspace[11:]
            est = estSansEspace[10:]
            west = westSansEspace[10:]
            pointCardinaux.append(west)
            pointCardinaux.append(est)
            pointCardinaux.append(sud)
            pointCardinaux.append(nord)

url = ""
if typeRessourceGeneral == "Audiovisual" or typeRessourceGeneral == "Sound":
    url = SHOW_TEXT + identifiantOAI[21:]
elif typeRessourceGeneral == "Text" and format[0] == "image" and requires:
    for lienRequires in requires:
        if "SOUND" not in lienRequires:
            url = EASTLING_PLAYER + lienRequires[21:]
elif typeRessourceGeneral == "Text" and format[0] == "text" and requires:
    for lienRequires in requires:
        url = SHOW_TEXT + lienRequires[21:] + IDREF + identifiantOAI[21:]
elif typeRessourceGeneral == "Text" and format[0] == "application" and requires:
    for lienRequires in requires:
        url = SHOW_OTHER + lienRequires[21:] + IDREF + identifiantOAI[21:]
elif typeRessourceGeneral == "Collection":
    url = 'http://lacito.vjf.cnrs.fr/pangloss/index.html'

print(url)

# --------Building XML ------------------#

racine = ET.Element("resource", xmlns="http://datacite.org/schema/kernel-4")
racineXmlns = racine.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
racineXsi = racine.set("xsi:schemaLocation", "http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.1/metadata.xsd")

# l'identifiant DOI
if identifiant:
    identifier = ET.SubElement(racine, "identifier", identifierType="DOI")
    identifier.text = identifiant
else:
    print("La balise IDENTIFIER est obligatoire!!")

# les titres
if titre:
    titles = ET.SubElement(racine, "titles")
    title = ET.SubElement(titles, "title")
    title.text = titre
    if codeXmlLangTitre:
        title.set("xml:lang", codeXmlLangTitre)
else:
    print("La Balise TITLE est obligatoire")

if titresSecondaire:
    for groupe in titresSecondaire:
        titreS = ET.SubElement(titles, "title")
        if groupe [0] is not None:
            titreS.text = groupe[1]
            titreS.set("xml:lang", groupe[0])
        else:
            titreS.text = groupe[1]


# les createurs et contributeurs
creators = ET.SubElement(racine, "creators")
contributors = ET.SubElement(racine, "contributors")

booleen = False
for personneRole in contributeursDoi:
    if "Researcher" in personneRole[1]:
        creator = ET.SubElement(creators, "creator")
        creatorName = ET.SubElement(creator, "creatorName", nameType="Personal")
        creatorName.text = personneRole[0]
        contributor = ET.SubElement(contributors, "contributor", contributorType='Researcher')
        contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
        contributorName.text = personneRole[0]
        booleen = True
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
        contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
        contributorName.text = personneRole[0]
    elif "Editor" in personneRole[1]:
        contributor = ET.SubElement(contributors, "contributor", contributorType='Editor')
        contributorName = ET.SubElement(contributor, "contributorName", nameType="Personal")
        contributorName.text = personneRole[0]
    elif "Sponsor" in personneRole[1]:
        contributor = ET.SubElement(contributors, "contributor", contributorType='Sponsor')
        contributorName = ET.SubElement(contributor, "contributorName")
        contributorName.text = personneRole[0]

if not booleen:
    for personneRole in contributeursDoi:
        if "ContactPerson" in personneRole[1]:
            creator = ET.SubElement(creators, "creator")
            creatorName = ET.SubElement(creator, "creatorName", nameType="Personal")
            creatorName.text = personneRole[0]
            booleen = True
if not booleen:
    print("La balise CREATOR est obligatoire!")


if publisherInstitution:
    for institution in publisherInstitution:
        contributor = ET.SubElement(contributors, "contributor", contributorType="Producer")
        contributorName = ET.SubElement(contributor, "contributorName", nameType="Organizational")
        contributorName.text = institution

hostingInstitution = ["COllections de COrpus Oraux Numériques", "Huma-Num",
                      "Langues et Civilisations à Tradition Orale",
                      "Centre Informatique National de l'Enseignement Supérieur"]
for institution in hostingInstitution:
    contributor = ET.SubElement(contributors, "contributor", contributorType="HostingInstitution")
    contributorName = ET.SubElement(contributor, "contributorName", nameType="Organizational")
    contributorName.text = institution

# contributeur = role droit
if droits:
    contributor = ET.SubElement(contributors, "contributor", contributorType='RightsHolder')
    contributorName = ET.SubElement(contributor, "contributorName")
    contributorName.text = droits


# les droits d'accès

if droitAccess:
    if 'Access restricted' in droitAccess:
        print("Pour consulter la ressource il est nécessaire d'avoir un mot de passe")
    else:
        rightsList = ET.SubElement(racine, "rightsList")
        rights = ET.SubElement(rightsList, "rights")
        rights.text = droitAccess


# le publisher
publisher = ET.SubElement(racine, "publisher")
publisher.text = "Pangloss"

# année de publication
if annee:
    publicationYear = ET.SubElement(racine, "publicationYear")
    publicationYear.text = annee[:4]
else:
    print("La balise PUBLICATIONYEAR est obligatoire")


# la langue
if codeLangue:
    # prend la première valeur de la liste avec les codes des langues
    language = ET.SubElement(racine, "language")
    language.text = codeLangue[0]

# les mots clés
subjects = ET.SubElement(racine, "subjects")

subject = ET.SubElement(subjects, "subject")
subject.text = setSpec

if labelLangue:
    for label in labelLangue:
        subject = ET.SubElement(subjects, "subject", subjectScheme="OLAC",
                                schemeURI="http://search.language-archives.org/index.html")
        subject.text = label[1]
        # vérifier que la liste contient un attribut xml:lang.
        if label[0] is not None:
            subject.set("xml:lang", label[0])
            subject.text = label[1]
        else:
            subject.text = label[1]


if sujets:
    for mot in sujets:
        if isinstance(mot, str):
            subject = ET.SubElement(subjects, "subject")
            subject.text = mot
        else:
            subject = ET.SubElement(subjects, "subject")
            subject.text = mot[1]
            subject.set("xml:lang", mot[0])


# le type de ressource
if labelType:
    resourceType = ET.SubElement(racine, "resourceType", resourceTypeGeneral=typeRessourceGeneral)
    resourceType.text = labelType
else:
    print("La balise RESOURCETYPE est obligatoire")


# les dates
dates = ET.SubElement(racine, "dates")
date = ET.SubElement(dates, "date", dateType="Available")
date.text = annee


alternateIdentifiers = ET.SubElement(racine, "alternateIdentifiers")
alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                    alternateIdentifierType="internal_ID")
alternateIdentifier.text = identifiantOAI
alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier",
                                    alternateIdentifierType="PURL")
alternateIdentifier.text = "http://purl.org/poi/crdo.vjf.cnrs.fr/"+identifiantOAI[21:]

if identifiant_Ark_Handle:
    for identifiant in identifiant_Ark_Handle:
        alternateIdentifier = ET.SubElement(alternateIdentifiers, "alternateIdentifier", alternateIdentifierType=identifiant[0])
        alternateIdentifier.text = identifiant[1]

if isRequiredBy or requires or idPangloss:
    relatedIdentifiers = ET.SubElement(racine, "relatedIdentifiers")

if isRequiredBy:
    for identifiantRel in isRequiredBy:
        relatedIdentifier = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="PURL",
                                      relationType="IsRequiredBy")
        relatedIdentifier.text = "http://purl.org/poi/crdo.vjf.cnrs.fr/"+identifiantRel[21:]

if requires:
    for identifiantRequires in requires:
        relatedIdentifier = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="PURL",
                                      relationType="Requires")
        relatedIdentifier.text = "http://purl.org/poi/crdo.vjf.cnrs.fr/"+identifiantRequires[21:]

idPangloss = ET.SubElement(relatedIdentifiers, "relatedIdentifier", relatedIdentifierType="DOI",
                                      relationType="IsPartOf")
idPangloss.text = DOI_PANGLOSS

if format:
    formats = ET.SubElement(racine, "formats")
    for element in format:
        format = ET.SubElement(formats, "format")
        format.text = element

if taille:
    sizes = ET.SubElement(racine, "sizes")
    size = ET.SubElement(sizes, "size")
    size.text = taille

if abstract or tableDeMatiere or descriptionsOlac:
    descriptions = ET.SubElement(racine, "descriptions")

if abstract:
    for element in abstract:
        # si la liste est composée d'une liste et d'une chaine de carractère, on récupère la chaine avec isistance()
        if isinstance(element, str):
            description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
            description.text = element
        else:
            description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
            description.text = element[1]
            description.set("xml:lang", element[0])

if tableDeMatiere:
    for element in tableDeMatiere:
        if isinstance(element, str):
            description = ET.SubElement(descriptions, "description", descriptionType="TableOfContents")
            description.text = element
        else:
            description = ET.SubElement(descriptions, "description", descriptionType="TableOfContents")
            description.text = element[1]
            description.set("xml:lang", element[0])

if descriptionsOlac:
    for element in descriptionsOlac:
        if isinstance(element, str):
            # si le mot Equipment fait partie du contenu de la balise description, alors cet élément aura l'attribut TechnicalInfo
            if "Equipment" in element:
                description = ET.SubElement(descriptions, "description", descriptionType="TechnicalInfo")
                description.text = element

            # sinon si la balise abstract existe, alors la balise description aura l'attribut Other, si elle n'existe pas, l'attribut Abstract
            elif abstract:
                description = ET.SubElement(descriptions, "description", descriptionType="Other")
                description.text = element
            else:
                description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                description.text = element
            #la même chose, mais pour le cas où abstract contient l'attribut xml-lang
        else:
            if "Equipment" in element[1]:
                description = ET.SubElement(descriptions, "description", descriptionType="TechnicalInfo")
                description.text = element[1]
                description.set("xml:lang", element[0])

            elif abstract:
                description = ET.SubElement(descriptions, "description", descriptionType="Other")
                description.text = element[1]
                description.set("xml:lang", element[0])
            else:
                description = ET.SubElement(descriptions, "description", descriptionType="Abstract")
                description.text = element[1]
                description.set("xml:lang", element[0])

if labelLieux:
    geoLocations = ET.SubElement(racine, "geoLocations")
    for element in labelLieux:
        geoLocation = ET.SubElement(geoLocations, "geoLocation")
        geoLocationPlace = ET.SubElement(geoLocation, "geoLocationPlace")
        geoLocationPlace.text = element

    if longitudeLatitude:
        geoLocationPoint = ET.SubElement(geoLocation, "geoLocationPoint")
        pointLongitude = ET.SubElement(geoLocationPoint, "pointLongitude")
        pointLongitude.text = longitudeLatitude[0]
        pointLatitude = ET.SubElement(geoLocationPoint, "pointLatitude")
        pointLatitude.text = longitudeLatitude[1]

    if pointCardinaux:
        geoLocationBox = ET.SubElement(geoLocation, "geoLocationBox")
        westBoundLongitude = ET.SubElement(geoLocationBox, "westBoundLongitude")
        westBoundLongitude.text = pointCardinaux[0]
        eastBoundLongitude = ET.SubElement(geoLocationBox, "eastBoundLongitude")
        eastBoundLongitude.text = pointCardinaux[1]
        southBoundLatitude = ET.SubElement(geoLocationBox, "southBoundLatitude")
        southBoundLatitude.text = pointCardinaux[2]
        northBoundLatitude = ET.SubElement(geoLocationBox, "northBoundLatitude")
        northBoundLatitude.text = pointCardinaux[3]



tree = ET.ElementTree(racine)
tree.write("../data/sortie.xml", encoding="UTF-8", xml_declaration=True, default_namespace=None, method="xml")


