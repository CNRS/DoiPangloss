import os, shutil
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import xml.etree.ElementTree as ETree
from parsing.DoiGenerator import getLastDoiNumberFromRecord, incrementDoi, getLastDoiNumberFromDataCite
from parsing.Parse import parseRecord
from apiDatacite.API_DataCite_Metadata import sendMetadataResource, sendMetadataPhrase
from apiDatacite.API_DataCite_DOI import sendUrlDoiResource, sendUrlDoiPhrase
from apiDatacite.API_Get_DataCite_Json import createDicoDoiOai
from constantes import NAMESPACES, PARSE_FILE, DOI_PREFIX, FOLDER_METADATA_RECORD, FOLDER_URL_DOI_RECORD, FOLDER_METADATA_PHRASE, FOLDER_URL_DOI_PHRASE
from parsing.parserAnnotation import parsePhrasesFromAnnotation
from objects.Phrase import Phrase


def addDOI():
    
    # appel de la fonction getLastDoiNumberFromRecord pour obtenir le dernier numero DOI
    last_doi_number_cocoon = getLastDoiNumberFromRecord(PARSE_FILE)

    # appel de la fonction getLastDoiNumberFromRecord pour obtenir le dernier numero DOI
    last_doi_number = getLastDoiNumberFromDataCite()

    print ('Lancement de la procédure d\'ajout de doi....')
   
    num = 0
  
    
##    if last_doi_number_cocoon != last_doi_number:
##        print ('Certains DOI ne sont pas intégrés dans cocoon')
##    else:
##        print ('DOI à jour dans cocoon')
    
    resume_add = open("resume_add.txt", "w", encoding="utf-8")
    
    # parsing du fichier xml Cocoon
    for index, record in enumerate(root.findall(".//oai:record", NAMESPACES)):

        num = num + 1
    
        # appel de la fonction parseRecord pour parser chaque record et créer un objet record
        objetRecord = parseRecord(record)

        
        
        # si les droits d'acces à la ressources sont conditionnés par un mot de passe, ne pas créer de DOI
        # if 'Access restricted' in objetRecord.droitAccess:
            # continue
        

        # --------gestion de la reprise après le premier lancement--------#
        oaiCocoon = objetRecord.identifiantOAI
        doiCocoon = objetRecord.doiIdentifiant.replace("doi:","")
        
        dicoDoiOai = {}
        doiExists = True    
        dicoDoiOai = createDicoDoiOai()
        
        
        print ('Ressource ', index+1, ' : ', oaiCocoon)
        
        # si la ressource a déjà un doi affecté
        if objetRecord.doiIdentifiant != "":
            doiExists = True
            print (len(dicoDoiOai))
            if doiCocoon in dicoDoiOai and oaiCocoon == dicoDoiOai[doiCocoon]:
                print ('Doi déjà créé pour cette ressource : '+ objetRecord.doiIdentifiant+'\n')
                resume_add.write ('Doi déjà créé pour cette ressource : '+ objetRecord.doiIdentifiant+'\n')
            # on ne fait rien car le doi existe dans cocoon mais pas dans datacite ! Problème !
            else:
                print (oaiCocoon,' : ', dicoDoiOai[doiCocoon])
                print ('ATTENTION :  Doi déjà créé pour cette ressource mais ne décrit pas la même ressource que dans datacite et dans cocoon (pas le même oai) : '+objetRecord.doiIdentifiant, ' !!!!\n')
                print ('ATTENTION :  Mise à jour et écrasement \n')
                resume_add.write ('!ATTENTION :  Doi déjà créé pour cette ressource mais ne décrit pas la même ressource que dans datacite et dans cocoon (pas le même oai) : '+ objetRecord.doiIdentifiant+ ' !!!!\n')
                resume_add.write ('ATTENTION :  Mise à jour et écrasement \n')
            
        
        # si la ressource n a pas de doi affecté
        else:
            # on vérifie que cet oai n\'a pas un doi dans datacite et que celui ci n\'aurait juste pas encore été intégré dans cocoon
            if (oaiCocoon in dicoDoiOai.values()):
                
                print ('ATTENTION :  Doi pas encore créé pour cette ressource mais l\'oai de cette ressource a déjà un doi affecté dans datacite '+ oaiCocoon+ ' !!!!\n')
              
                resume_add.write ('ATTENTION :  Doi pas encore créé pour cette ressource mais l\'oai de cette ressource a déjà un doi affecté dans datacite '+ oaiCocoon+ ' !!!!\n')
                
                doiExists = True
                # break
            
            else:
                print (oaiCocoon +' -> Création et affectation d\'un doi....\n')
                resume_add.write (oaiCocoon +' -> Création et affectation d\'un doi....\n')
                doiExists = False

        if doiExists == False:
            # appel de la fonction incrementDoi pour créer le nouveau DOI en faisant une incrémentation de 1 à partir du dernier DOI
            doiNumber, last_doi_number = incrementDoi(last_doi_number)
            # atttribue à l'objet record créée le numéro doi complet avec le prefixe,
            # en utilisant une nouvelle affectation à l'attribut identifiant de l'objet.
            objetRecord.doiIdentifiant = DOI_PREFIX+doiNumber
            # appel de la methode buildMetadataResource de la classe Record pour générer le fichier xml
            fichier_xmlRessource = objetRecord.buildMetadataResource()

            # appel de la méthode generateFileUrlDoiResource pour créer les fichiers avec les url et les DOI
            fichier_textRessource = objetRecord.generateFileUrlDoiResource()

            
            # appel des fonctions pour interroger l'API de Datacite et enregistrer le fichier de metadonnées et le fichier texte avec l'url et le doi pour les ressources
            if fichier_xmlRessource:
                sendMetadataResource(fichier_xmlRessource, objetRecord.doiIdentifiant)

            if fichier_textRessource:
                sendUrlDoiResource(fichier_textRessource, objetRecord.doiIdentifiant)
         
                
     

        # limite le nombre d'itérations sur les record et crée un nombre limité de fichiers et de DOI.
        # mettre en commentaire pour faire fonctionner l'application sur la totalité du fichier Cocoon et créer tous les DOI
        # if index == 4:
           # break

    
    
    resume_add.close()
    
    print ('Procédure de création terminée !')
    
def updateDOI():
    
    # appel de la fonction getLastDoiNumberFromRecord pour obtenir le dernier numero DOI
    last_doi_number_cocoon = getLastDoiNumberFromRecord(PARSE_FILE)

    # appel de la fonction getLastDoiNumberFromRecord pour obtenir le dernier numero DOI
    last_doi_number = getLastDoiNumberFromDataCite()

    print ('Lancement de la procédure de mise à jour de doi....')
    
##    if last_doi_number_cocoon != last_doi_number:
##        print ('Certains DOI ne sont pas intégrés dans cocoon')
##    else:
##        print ('DOI à jour dans cocoon')
    
    num = 0
    
    
    resume_update = open("resume_update.txt", "w", encoding="utf-8")
    
    
    
    # parsing du fichier xml Cocoon
    for index, record in enumerate(root.findall(".//oai:record", NAMESPACES)):
        
        num = num + 1
        
        # appel de la fonction parseRecord pour parser chaque record et créer un objet record
        objetRecord = parseRecord(record)

        
        # si les droits d'acces à la ressources sont conditionnés par un mot de passe, ne pas créer de DOI
        # if 'Access restricted' in objetRecord.droitAccess:
            # continue
        

        # --------gestion de la reprise après le premier lancement--------#
        oaiCocoon = objetRecord.identifiantOAI
        doiCocoon = objetRecord.doiIdentifiant.replace("doi:","")
       
        # print ('Création du dictionnaire des doi')
        dicoDoiOai = {}
        doiExists = False    
        dicoDoiOai = createDicoDoiOai()
        
        print ('Ressource ', index+1, ' : ', oaiCocoon)
        
        # si la ressource à mettre à jour a bien un doi affecté dans cocoon
        if objetRecord.doiIdentifiant != "":
          
            # si la ressource a le meme doi et oai que dans le datacite (si on met bien à jour la meme ressource vs si on ecrase une ressource par une autre)
            if doiCocoon in dicoDoiOai and oaiCocoon == dicoDoiOai[doiCocoon]:  
                print ('Ressource '+ objetRecord.doiIdentifiant+' : déjà enregistré dans le datacite (et même oai) \n')
                resume_update.write ('Ressource '+ objetRecord.doiIdentifiant+' : déjà enregistrée dans le datacite (et même oai) \n')
                doiExists = True
            else:   
                print ('Doi déjà existant dans le datacite mais correspond à une autre ressource (oai différent). Procédure d\'écrasement.... : '+ doiCocoon+'\n')
                resume_update.write ('Doi déjà existant dans le datacite mais correspond à une autre ressource (oai différent). Procédure d\'écrasement.... : '+ doiCocoon+'\n')
                doiExists = True
            # continue
            
        if doiExists == True:
            print (' -> Procédure de mise à jour de : '+oaiCocoon+'....\n' )
            resume_update.write (' -> Procédure de mise à jour de : '+ oaiCocoon+ '....\n' )
            # appel de la methode buildMetadataResource de la classe Record pour générer le fichier xml
            fichier_xmlRessource = objetRecord.buildMetadataResource()

            # appel de la méthode generateFileUrlDoiResource pour créer les fichiers avec les url et les DOI
            fichier_textRessource = objetRecord.generateFileUrlDoiResource()

            
            # appel des fonctions pour interroger l'API de Datacite et enregistrer le fichier de metadonnées et le fichier texte avec l'url et le doi pour les ressources
            if fichier_xmlRessource:
                sendMetadataResource(fichier_xmlRessource, objetRecord.doiIdentifiant)

            if fichier_textRessource:
                sendUrlDoiResource(fichier_textRessource, objetRecord.doiIdentifiant)
         
                 

        

        # limite le nombre d'itérations sur les record et crée un nombre limité de fichiers et de DOI.
        # mettre en commentaire pour faire fonctionner l'application sur la totalité du fichier Cocoon et créer tous les DOI
        # if index == 4:
            # break 
    
    resume_update.close()
    
    print ('Procédure de mise à jour terminée !')
    
    
    
    
    
    
    
    

if __name__ == "__main__":

    print ('Démarrage....')

    # Récupération du paramétre au lancement du programme
    if len(sys.argv) == 1:
        print("Paramètre manquant. Renseigner add pour traiter uniquement les nouvelles ressources ou update pour faire des mises à jour de ressources ayant deja un doi")
    else:
        parameter = sys.argv[1]

        # Teste si le paramètre est correctement renseigné
        if parameter != 'update' and parameter != 'add':
            print("Paramètre manquant. Renseigner add pour traiter uniquement les nouvelles ressources ou update pour faire des mises à jour de ressources ayant deja un doi")

        else:
            # suppression d'un dossier et de son contenu s'il existe
            if os.path.isdir(FOLDER_METADATA_RECORD) and os.path.exists(FOLDER_METADATA_RECORD):
                shutil.rmtree(FOLDER_METADATA_RECORD)
                
            if os.path.isdir(FOLDER_URL_DOI_RECORD) and os.path.exists(FOLDER_URL_DOI_RECORD):
                shutil.rmtree(FOLDER_URL_DOI_RECORD)
            
            if os.path.isdir(FOLDER_METADATA_PHRASE) and os.path.exists(FOLDER_METADATA_PHRASE):
                shutil.rmtree(FOLDER_METADATA_PHRASE)
            
            if os.path.isdir(FOLDER_URL_DOI_PHRASE) and os.path.exists(FOLDER_URL_DOI_PHRASE):
                shutil.rmtree(FOLDER_URL_DOI_PHRASE)

            
            # cree des repertoires s'il n'existent pas
            os.mkdir(FOLDER_METADATA_RECORD)
            os.mkdir(FOLDER_URL_DOI_RECORD)
            os.mkdir(FOLDER_METADATA_PHRASE)
            os.mkdir(FOLDER_URL_DOI_PHRASE)



           


            # --------Parse.py OAI-PMH avec etree--------#
            print ('Parsing....')
            tree = ETree.parse(PARSE_FILE)
            root = tree.getroot()

          
            
            if parameter == "add":
                addDOI()
            if parameter == "update":
                updateDOI()

