import requests

# l'adresse pour retrouver tous les DOI de Datacite sur lesquels il faut appliquer les filtres
ENDPOINTALLDOI= 'https://api.datacite.org/works'

# dictionnaire avec 2 paramètres à passer à l'appel de l'URL : data-center-id et page[number]
# pour tester le code avant la création des DOI pour Lacito, remplacer INIST.LACITO par un autre code institutionnel par exemple "inist.garnier"
param = {"data-center-id":"INIST.LACITO", "page[number]": 1}

response = requests.get(ENDPOINTALLDOI, params=param)
donnee = response.json()

# tant que la clé "data" du json a du contenu
while donnee["data"] != [] :
    # passer à la page suivante et faire une nouvelle requête GET
    param["page[number]"] = param["page[number]"]+1
    response = requests.get(ENDPOINTALLDOI, params=param)

    # si la réponse est différente de 200 sortir de la boucle.
    if (response.status_code != 200):
        print (str(response.status_code) + " " + response.text)
        break

    # sinon, extraire les 25 objets DOI pour chaque page
    else:
        donnee = response.json()
        panglossDois = donnee["data"]

        #pour chaque objet DOI d'une page
        for element in panglossDois :
            # extraire le doi qui se trouve au niveau de l'"id" dans "data"
            doiPangloss = element["id"]
            print (doiPangloss)