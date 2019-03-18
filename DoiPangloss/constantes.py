PARSE_FILE= "data/metadata_cocoon.xml"
FOLDER_METADATA_RECORD = "data/testRecord/"
FOLDER_URL_DOI_RECORD = "data/testURL_Record/"
FOLDER_METADATA_PHRASE= "data/testPhrase/"
FOLDER_URL_DOI_PHRASE = "data/testURL_Phrase/"
NAMESPACES = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms" : "http://purl.org/dc/terms/",
            "olac" : "http://www.language-archives.org/OLAC/1.1/",
            "xsi" : "http://www.w3.org/2001/XMLSchema-instance",
            "oai" : "http://www.openarchives.org/OAI/2.0/",
            "doi" : "http://datacite.org/schema/kernel-4"
        }

# DOI_PREFIX = "10.5072/pangloss-"
DOI_PREFIX = "10.24397/pangloss-"

SHOW_TEXT = "http://lacito.vjf.cnrs.fr/pangloss/corpus/show_text.php?id="
IDREF = "&idref="
SHOW_OTHER = "http://lacito.vjf.cnrs.fr/pangloss/corpus/show_other.php?id="
EASTLING_PLAYER = 'http://lacito.vjf.cnrs.fr/pangloss/corpus/eastling_player.php?idref='
SCHEME_URI = "http://search.language-archives.org/index.html"
PURL = "http://purl.org/poi/crdo.vjf.cnrs.fr/"
USERNAME = ""
PASSWORD = ""
ENDPOINTMETADATA = "https://mds.datacite.org/metadata/"
ENDPOINTDOI = "https://mds.datacite.org/doi/"
RESTDOI = "https://api.datacite.org/dois/"
CRITICAL_LOG = 'critical.log'
# chager le préfix pour la phase de production 10.24397
# DOI_PANGLOSS = "10.5072/Pangloss"
DOI_PANGLOSS = "10.24397/Pangloss"
FILE_API_URL = './data/apiUrl'
FILE_API_METADATA = './data/apiMetadonnees'