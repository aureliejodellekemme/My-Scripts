import pandas as pd
import numpy as np

# define data path
survey_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Survey/Copy of Clinics Outreach Survey - Sheet1.csv'

def read_survey(survey_file_path):
    return pd.read_csv(survey_file_path)

# list of equipment
equipment_list=['Microbiology', 'Ultrasound', 'Dental x-ray', 'X-Ray Imaging Systems',
       'X-Ray Machine', 'Hematology Analyzer', 'Echography ', 'Anastesia Machine',
       'Dental Unit', 'Microscope', 'Microplate reader', 'Bio Chemistry',
       'Digital X-Ray', 'Real-Time PCR System', 'CT Scan',
       'Trolley 3D, Doppler ultrasonography', 'Ultrasonic scaler',
       'Colonoscope', 'Holter Monitor', 'ECG Machine', 'Electrosurgical Unit',
       'Echocardiography Machine', 'Endoscopy Machine', 'Operation Light ',
       'Electrolyte Analyzer', 'Audiometer machine','Magnetic Reasonable Machine', 
           'EEG Machine', 'Hemodialysis Unit', 'Mammography Machine',
       'Electromyography (EMG)', 'EEG Machine', 'Fluoroscopy ']

def fillna_with_NO(clinic_survey,equipment_list):
    for eqp in equipment_list:
        clinic_survey[eqp]= clinic_survey[eqp].str.upper()
        clinic_survey.loc[clinic_survey[eqp].isnull(), eqp]='NO'
    return clinic_survey

def clean_survey_data(clinic_survey):
    clinic_survey1 = (clinic_survey
    .drop(['Type of clinic','Coordinates of the clinic','Province','District','Sector','Cell','Village','Departments','Number equipment','Insurance types','Contact','Person i spoke with'],axis=1)
    .rename(columns={'Anastesia Machine':'Anesthesia Machine','Microbiology':'Microbiology Equipment','EEG Machine':'EEG Monitor','Fluoroscopy ':'Radiography/Fluoroscopy Equipment','cust_id':'ID','Ecography':'Echography','X_Ray':'X-Ray Machine','Name of clinic':'HEALTH FACILITY','Number of Doctors':'Of_Doctors','Number of Nurses':'Of_Nurses'})
    .replace('KIVU Specialist Clinic\r\n','KIVU Specialist Clinic')
    .assign(Patients_per_Month=lambda x: ((x['How many patients/ Day'].str.split('-').str[0].astype(int) + x['How many patients/ Day'].str.split('-').str[1].astype(int)) / 2) * 30)
    .assign(Patients_per_Month=lambda x:x['Patients_per_Month'].astype(np.int32))
    #.assign(Operation_Year=lambda x:x['operation year'].astype(np.int32))
                  .drop('How many patients/ Day',axis=1)
    .reset_index(drop=True)
     )
    return clinic_survey1

def createequipment(clinic_survey1,equipment_list):
   
    # Initialize empty lists to store values for 'disease' and 'equipment_cases' columns
    equipment_values = []
    equipment_cases_values = []

    # Iterate over each row in the DataFrame
    for _, row in clinic_survey1.iterrows():
        # Initialize 'equipment' and 'equipment_cases' values for the current row
        equipments = []
        equipment_cases = []

        # Iterate over each numerical column
        for col in equipment_list:
            # Check if the value in the numerical column is not NaN or zero
            if row[col]=='YES':
                # Append the column name to 'equipments' list
                equipments.append(col)
                # Append the value to 'disease_cases' list
                equipment_cases.append(row[col])

        # Check if 'equipments' list is empty (all numerical values are missing or zero)
        if not equipments:
            equipments.append(np.nan)
            equipment_cases.append(np.nan)

        # Append 'equipments' and 'equipment_cases' values to the respective lists
        equipment_values.append(equipments)
        equipment_cases_values.append(equipment_cases)

    # Create new Series with the aligned lists
    equipment_series = pd.Series(equipment_values, name='name').explode()
    equipment_cases_series = pd.Series(equipment_series, name='EQUIPMENT').explode()
    # Concatenate the new series with the original DataFrame
    df_concat = pd.concat([clinic_survey1, equipment_cases_series], axis=1).drop(equipment_list, axis=1).dropna(subset=['EQUIPMENT']).drop_duplicates()
    df_concat=df_concat.drop_duplicates()
    
    return df_concat


def main():
    clinic_survey=read_survey(survey_file_path)
    clean_survey=fillna_with_NO(clinic_survey,equipment_list)
    clean_survey1=createequipment(clean_survey,equipment_list)
    survey=clean_survey_data(clean_survey1)

    return survey

if __name__=="__main__":
    survey=main()
survey.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Survey/survey.csv',index=False)