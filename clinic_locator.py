from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import json

app = Flask(__name__)
DEFAULT_FOLDER_LOCATION = "./data"
cliniclocations_df = pd.read_csv(DEFAULT_FOLDER_LOCATION + "/clinicservicelocations.csv")
services_df = pd.read_csv(DEFAULT_FOLDER_LOCATION + "/services.csv")

def find_clinic(service_id):
    if service_id == 0:
        clinics = cliniclocations_df.drop_duplicates('ClinicID', keep='first')
        print(clinics)
    else:
        clinics = cliniclocations_df.loc[cliniclocations_df['ServiceID'] == service_id]
    clinics.drop(['ClinicID', 'ClinicServicesID', 'ServiceID'], axis=1, inplace=True)
    clinics_dict =  clinics.to_dict('records')
    return clinics_dict

@app.route("/getclinics")
def getclinics():
    service_id = int(request.args.get('serviceid'))
    clinics_dict = find_clinic(service_id)
    clinics_json = json.dumps(clinics_dict)
    return clinics_json

@app.route("/getservices")
def getServices():
    services_dict = services_df.to_dict('records')
    services_json = json.dumps(services_dict)
    return services_json

@app.route("/")
def homePage():
    return render_template('clinic_map.html')


if __name__ == '__main__':
    app.run(debug=True)
