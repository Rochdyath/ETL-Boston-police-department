from process import extract_boston_salary, transform, save_to_file, analyse_boston_salary

# fonction principale de l'etl
def etl_boston_police_department():
    # extraction
    records = extract_boston_salary()
    
    # transformation
    transform(records)

    # sauvegarde
    save_to_file(records, "boston_salary.json")
    
    # analyse
    analyse_boston_salary(records)

try:
    etl_boston_police_department()
except Exception as error:
    print(error)