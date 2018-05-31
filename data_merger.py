import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

class DataMerger():
    """
    It firstly clean the data then merge it into one CSV file named “clinicservicelocations.csv”.
    """

    # PATH Constants
    CLINICS_PATH = "/clinics.csv"
    SERVICES_PATH = "/services.csv"
    CLINIC_SERVICES_PATH = "/clinicservices.csv"
    CLINIC_LOCATIONS_PATH = "/cliniclocations.xml"
    EMAIL_DEFAULT_DOMAIN = "@myclinic.com.au"
    DEFAULT_FOLDER_LOCATION = "./data"

    def data_read(self, folder_location="Not Provided"):
        """
        Input --> folder_location

        Output --> clinics_df, cliniclocations_df, services_df, clinicservices_df

        This function reads all csv and xml files from ./data(if not provided) folder and return dataframe of each file
        """
        if folder_location == "Not Provided":
            folder_location = self.DEFAULT_FOLDER_LOCATION


        clinics_df = pd.read_csv(folder_location + self.CLINICS_PATH)
        clinicservices_df = pd.read_csv(folder_location + self.CLINIC_SERVICES_PATH)
        services_df = pd.read_csv(folder_location + self.SERVICES_PATH)
        cliniclocations_df = self.xml_to_df(folder_location + self.CLINIC_LOCATIONS_PATH)
        return clinics_df, cliniclocations_df, services_df, clinicservices_df

    def xml_to_df(self, path):
        """
        Input --> path of xml_file

        Output --> cliniclocations_df
        
        This function reads xml files from path and return dataframe
        """
        tree = ET.parse(path)
        root = tree.getroot()
        clinics = []
        for child in root:
            clinic = {
                "ClinicID": int(child[0].text),
                "Lat": float(child[1].text),
                "Lon": float(child[2].text)
            }
            clinics.append(clinic)
        cliniclocations_df = pd.DataFrame(clinics)
        return cliniclocations_df

    def email_repair(self, email):
        cleaned_email = "".join(email.split())
        if (len(cleaned_email.split('@')) < 2):
            cleaned_email += self.EMAIL_DEFAULT_DOMAIN
        return cleaned_email

    def data_cleansing(self, clinics_df):
        clinics_df['Email'] = clinics_df['Email'].map(lambda x: self.email_repair(x))
        return clinics_df

    
    def data_merge(self,clinics_df, cliniclocations_df, services_df, clinicservices_df):

        clinicservices = []
        clinic_service_locations = []
        for index, row in clinicservices_df.iterrows():
            clinic_df = clinics_df.loc[clinics_df['ClinicID']==row['ClinicID']]
            service_df = services_df.loc[services_df['ServiceID']==row['ServiceID']]
            cliniclocation_df = cliniclocations_df.loc[cliniclocations_df['ClinicID']==row['ClinicID']]
            clinic_service_location = {
                "ClinicServicesID": row['ClinicServiceID'],
                "ServiceID":row['ServiceID'],
                "Service":service_df.iloc[0]['Service'],
                "ClinicID":row['ClinicID'],
                "Clinic":clinic_df.iloc[0]['Name'],
                "Suburb":clinic_df.iloc[0]['Suburb'],
                "State":clinic_df.iloc[0]['State'],
                "Email":clinic_df.iloc[0]['Email'],
                "Lat":cliniclocation_df.iloc[0]['Lat'],
                "Lon":cliniclocation_df.iloc[0]['Lon']
            }
            clinic_service_locations.append(clinic_service_location)
        
        clinicservicelocations_df = pd.DataFrame(clinic_service_locations, index=None)
        return clinicservicelocations_df

    def df_to_csv(self, clinicservicelocations_df, file_name):
        clinicservicelocations_df.to_csv(self.DEFAULT_FOLDER_LOCATION + "/" + file_name, index=False)

    def main(self):
        clinics_df, cliniclocations_df, services_df, clinicservices_df = self.data_read()
        cleaned_clinics_df = self.data_cleansing(clinics_df)
        clinic_service_locations_df = self.data_merge(cleaned_clinics_df, cliniclocations_df, services_df, clinicservices_df)
        self.df_to_csv(clinic_service_locations_df, "clinicservicelocations.csv")



if __name__ == "__main__":
    DataMerger().main()
    