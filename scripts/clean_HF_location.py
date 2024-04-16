import pandas as pd
import geopandas as gpd
import numpy as np
from clean_shapefile import clean_sector # call this function to match sector name with the shape file sector

# define data path
facility_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/Health_Facilities.xlsx'
sector_shape_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Sector shapefile/clean_Sector.shp'
rbc_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/RBC/rbc.csv'
equip_disease_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases_to_Equipment/equipment_diseases_matching.csv'
survey_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Survey/survey.csv'
financial_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Viebeg Financial Data/financial.csv'
staff_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_Staff Data/staff_data.csv'

# read the data
def read_data(facility_path,sector_shape_file_path,rbc_file_path,survey_file_path,financial_file_path,equip_disease_file_path,staff_file_path):
    facility=pd.read_excel(facility_path,sheet_name='Health_Facilities')
    sector_shape_file=gpd.read_file(sector_shape_file_path)
    diseas_equip_match=pd.read_csv(equip_disease_file_path)
    rbc=pd.read_csv(rbc_file_path)
    survey=pd.read_csv(survey_file_path)
    financial=pd.read_csv(financial_file_path)
    staff=pd.read_csv(staff_file_path)
    return facility,sector_shape_file[['Province','District','Sector','Sect_ID']],rbc[['HEALTH FACILITY', 'EQUIPMENTS']],survey[['HEALTH FACILITY','EQUIPMENT','Of_Doctors','Of_Nurses','operation year','Patients_per_Month']],financial[['HEALTH FACILITY','EQUIPMENTS']],diseas_equip_match,staff[['HEALTH FACILITY','Of_Doctors', 'Of_Nurses']]

def cleanF_data(facility):
    facility1 = (
        facility
        .rename(columns={'long':'Longitude','lat':'Latitude','MOH name':'HEALTH FACILITY','district':'District','sector':'Sector','type':'FACILITY TYPE'})
        .drop(['source', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date'], axis=1)
        .assign(
            District=lambda x: x['District'].str.capitalize(),
            Sector=lambda x: x['Sector'].str.capitalize(),
            Latitude=lambda x: pd.to_numeric(x['Latitude'], errors='coerce')
        )
        .dropna(subset=['Latitude'])
        .drop_duplicates(subset=['HEALTH FACILITY'])
        .pipe(lambda df: df.assign(**{'FACILITY TYPE': df['FACILITY TYPE'].str.upper()}))
        .replace({
            'POLICLINIQUE': 'POLYCLINIC',
            'PRIVATE DIGITAL CLINIC': 'CLINIC',
            'PRIVATE SPECIALIZED CLINIC': 'CLINIC',
            'SPECIALISED HOSPITAL': 'HOSPITAL',
            'PRIVATE NUTRITION CABINET': 'CLINIC',
            'PRIVATE CLINIC': 'CLINIC',
            'MEDICAL CLINIC': 'CLINIC',
            'PRIVATE LABORATORY': 'LABORATORY'
        })
        
    )
    return facility1[~facility1['FACILITY TYPE'].isin(['PRISON','UNIVERSITY','CHURCH','BUSINESS', np.nan, 'SUPPLIER'])]

# Extract sector id and province from sector shape file on key 'district' and 'sector'
def adding_sect_id_province(facility2,sector_shape_file):
        facility2=facility2.merge(sector_shape_file,on=['District','Sector'])
        facility2['Sect_ID']=facility2['Sect_ID'].astype(np.int32)
        return facility2

# Extract equipment from rbc on key 'Health facility'
def adding_equip_from_rbc(facility3,rbc):
    return facility3.merge(rbc,on=['HEALTH FACILITY'],how='left')

def adding_equip_from_survey(facility4,survey):
        # Merge 'facility1' with the grouped 'survey' DataFrame using 'health facility' as the key
        facility5 = facility4.merge(survey, on='HEALTH FACILITY', how='left')

        # Fill NaN values in 'EQUIPMENT' with values from 'EQUIPMENTS'
        facility5['EQUIPMENT'].fillna(facility5['EQUIPMENTS'], inplace=True)

        # Drop the 'EQUIPMENT_y' column if needed
        facility5.drop(columns=['EQUIPMENTS'], inplace=True)
        return facility5

def adding_doctor_nurses_from_staff(facility4,staff):
        # Merge 'facility1' with the grouped 'survey' DataFrame using 'health facility' as the key
        facility5 = facility4.merge(staff, on='HEALTH FACILITY', how='left', suffixes=('', '_from_staff'))

        # Fill NaN values in 'EQUIPMENT' with values from 'EQUIPMENTS'
        facility5['Of_Doctors'].fillna(facility5['Of_Doctors_from_staff'], inplace=True)
        facility5['Of_Nurses'].fillna(facility5['Of_Nurses_from_staff'], inplace=True)

        # Drop the 'EQUIPMENT_y' column if needed
        facility5.drop(columns=['Of_Doctors_from_staff','Of_Nurses_from_staff'], inplace=True)
        return facility5

def adding_equip_from_sales(facility5,sales):
        # Merge 'facility2' with sales DataFrame using 'health facility' as the key
        facility6 =facility5.merge(sales, on='HEALTH FACILITY', how='left')
        # Fill NaN values in 'EQUIPMENT' with values from 'EQUIPMENTS'
        facility6['EQUIPMENT'].fillna(facility6['EQUIPMENTS'], inplace=True)

        # Drop the 'EQUIPMENTS' column if needed
        facility6=facility6.drop(columns=['EQUIPMENTS'],axis=1).drop_duplicates()

        return facility6

def adding_column_list_equip_per_hf(facility6):
        agg_df = facility6[~facility6['EQUIPMENT'].isnull()].groupby('HEALTH FACILITY')['EQUIPMENT'].agg(set).reset_index()
        agg_df['EQUIPMENT']=agg_df['EQUIPMENT'].apply(list)
        # Rename the aggregated column to 'EQUIPMENTS'
        agg_df.rename(columns={'EQUIPMENT': 'EQUIPMENTS'}, inplace=True)
        delimiter = ', '
        # Merge the aggregated data back into the original DataFrame
        agg_df['EQUIPMENTS'] =agg_df['EQUIPMENTS'] .apply(lambda x: delimiter.join(map(str, x)))
        # merge data with equipment list with the original data
        facility7 = (facility6
                .merge(agg_df, on='HEALTH FACILITY', how='left')
                .drop_duplicates()
                #.drop(facility3[((facility3['Sector'] == 'Rilima') |  #drop because No information on disease
             #(facility3['Sector'] == 'Mageregere') |
             #((facility3['District'] == 'Ruhango') & (facility3['Sector'] == 'Kinihira')))].index,axis=0)
         )

        return facility7

def adding_diseases(facility7,diseas_equip_match):
    facility7=facility7.merge(diseas_equip_match,on='EQUIPMENT',how='left').fillna('No Information')
    #facility7['EQUIPMENT'] = facility7['EQUIPMENT'].fillna('No Information')
    return facility7.drop_duplicates()

def main():
    facility,sector_shape_file,rbc,survey,sales,diseas_equip_match,staff=read_data(facility_path,sector_shape_file_path,rbc_file_path,survey_file_path,financial_file_path,equip_disease_file_path,staff_file_path)
    facility1=cleanF_data(facility)
    facility2=clean_sector(facility1)
    facility3=adding_sect_id_province(facility2,sector_shape_file)
    facility4=adding_equip_from_rbc(facility3,rbc)
    facility5=adding_equip_from_survey(facility4,survey)
    staff_df=adding_doctor_nurses_from_staff(facility5,staff)
    facility6=adding_equip_from_sales(staff_df,sales)
    facility7=adding_column_list_equip_per_hf(facility6)
    facility8=adding_diseases(facility7,diseas_equip_match)

    return facility8
if __name__ == "__main__":
    facility8 = main()
facility8.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facilities.csv',index=False)
