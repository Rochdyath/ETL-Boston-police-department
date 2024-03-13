import requests
import json
import matplotlib.pyplot as plt

# récupération des données
def extract_boston_salary():
    url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=31358fd1-849a-48e0-8285-e813f6efbdf1'
    response = requests.get(url)
    
    # vérifier que la requête a fonctionnée
    if (response.status_code != 200):
        raise Exception(f"extraction failed - status code: {response.status_code}")
    # récupérer les données en format json
    return response.json()["result"]["records"]

# vérifier qu'une chaîne est sous format "{int},{int},{...}.{int}"
def is_float(string):
    for c in string:
        if ((c >= '0' and c <= '9') or (c in ",.")): continue
        else: return -1
    return 1

# correction des champs selon notre besoin
def transform(records):
    for record in records:
        for key in record:
            value = record[key]
            # convertir les chaînes sous format "{int},{int},{...}.{int}" en float
            if (type(value) is str and is_float(value) == 1):
                record[key] = float(value.replace(',', ''))

# enregistrer les données dans un fichier json
def save_to_file(records, file_path):
    # créer le fichier ayant pour nom file_path
    with open(file_path, "w") as file:
        # enregistrer les données sous format json dans le fichier
        json.dump(records, file, indent=4)

# récupérer les titres des salariés de boston distinctement  
def get_all_title(records):
    titles = []
    for record in records:
        if record["TITLE"] not in titles: titles.append(record["TITLE"])
    return titles

# calculer la moyenne des salaires par titre
def aggregate_department_data(records, title):
    total = 0
    count = 0
    for record in records:
        if record["TITLE"] == title:
            total += record["TOTAL EARNINGS"]
            count += 1
    return total / count

# afficher une bar chart en utilisant une liste de valeurs numérique et des labels 
def bar_chart(numbers, labels):
    plt.bar(labels, numbers)
    # positionner les labels verticalement
    plt.xticks(rotation='vertical')
    # créer une marge en l'axe des absisses et la bordure inférieure de la fenêtre
    plt.subplots_adjust(bottom=0.3)
    # afficher le résultat
    plt.show()

# analyse des salaires de boston par poste
def analyse_boston_salary(records):
    titles = get_all_title(records)
    mean_salary = list()
    # récupérer la moyenne salaire par poste dans mean_salary
    for title in titles:
        mean_salary.append(aggregate_department_data(records, title))
    # afficher une bar chart représentative des
    bar_chart(mean_salary, titles)