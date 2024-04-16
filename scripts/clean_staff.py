import pandas as pd

staff_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_Staff Data/3_Staffing.xlsx'

def read_survey(staff_file_path):
    return pd.read_excel(staff_file_path)

mapping_columns_names={'Doctors_Specialist':'Doctors_Specialist(Female)','Unnamed: 6':'Doctors_Specialist(Male)',
       'Doctors_Generalist':'Doctors_Generalist(Female)', 'Unnamed: 8':'Doctors_Generalist(Male)',
        'Dental Surgeons':'Dental Surgeons(Female)','Unnamed: 10':'Dental Surgeons(Male)',
        'Nurses':'Nurses(Female)','Unnamed: 12':'Nurses(Male)','Mental Health Nurses':'Mental Health Nurses(Female)','Unnamed: 14':'Mental Health Nurses(Male)',
        'Midwives':'Midwives(Female)','Unnamed: 16':'Midwives(Male)', 'Dentist therapist':'Dentist therapist(Female)','Unnamed: 18':'Dentist therapist(Male)',
        'Pharmacists':'Pharmacists(Female)','Unnamed: 20':'Pharmacists(Male)','Ophthalmology clinical Officers':'Ophthalmology clinical Officers(Female)','Unnamed: 22':'Ophthalmology clinical Officers(Male)',
        'Ophthalmology clinical Officers':'Ophthalmology clinical Officers(Female)','Unnamed: 22':'Ophthalmology clinical Officers(Male)',
         'Non Physician Anesthetists':'Non Physician Anesthetists(Female)','Unnamed: 24':'Non Physician Anesthetists(Male)',
         'Nutritionist':'Nutritionist(Female)','Unnamed: 26':'Nutritionist(Male)',
         'Medical Imagery Technologists':'Medical Imagery Technologists(Female)','Unnamed: 28':'Medical Imagery Technologists(Male)',
         'Environmental Health officers':'Environmental Health officers(Female)','Unnamed: 30':'Environmental Health officers(Male)',
         'Biomedical technician':'Biomedical technician(Female)','Unnamed: 32':'Biomedical technician(Male)',
         'Physiotherapist':'Physiotherapist(Female)','Unnamed: 34':'Physiotherapist(Male)',
         'Health Information System Staff':'Health Information System Staff(Female)','Unnamed: 36':'Health Information System Staff(Male)',
         'Social_Worker':'Social_Worker(Female)','Unnamed: 38':'Social_Worker(Male)',
         'Clinical psychologist':'Clinical psychologist(Female)','Unnamed: 40':'Clinical psychologist(Male)',
         'Administrative and Support Personnel':'Administrative and Support Personnel(Female)','Unnamed: 42':'Administrative and Support Personnel(Male)',
         'Lab technicians':'Lab technicians(Female)','Unnamed: 44':'Lab technicians(Male)','Health Facility':'HEALTH FACILITY'
        }
def clean_rename_column(staff_df):
    staff_df1=(staff_df
            .rename(columns=mapping_columns_names)
            .drop(0)
            .assign(Of_Doctors=lambda x: x['Doctors_Specialist(Female)'].fillna(0) + x['Doctors_Specialist(Male)'].fillna(0) + x['Doctors_Generalist(Female)'].fillna(0) + x['Doctors_Generalist(Male)'].fillna(0))
            .assign(Of_Nurses=lambda x: x['Nurses(Female)'].fillna(0) + x['Nurses(Male)'].fillna(0))

            )
    return staff_df1

def main():
    staff_df=read_survey(staff_file_path)
    staff_df1=clean_rename_column(staff_df)

    return staff_df1

if __name__=="__main__":
    staff_df1=main()

staff_df1.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_Staff Data/staff_data.csv',index=False)
