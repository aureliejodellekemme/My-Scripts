import pandas as pd
import numpy as np
from datetime import datetime as dt

# define data path
disease_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/moh_data.csv'
population_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/2022_Population_Rwanda.csv'


def read_data(disease_file_path,population_file_path):
    """
    Read and load data from CSV files for disease information, population statistics, and geographic sector shapes.

    Parameters:
    - disease_file_path (str): File path to the CSV file containing disease data.
    - population_file_path (str): File path to the CSV file containing population statistics.

    Returns:
    tuple: A tuple containing three elements:
        - pd.DataFrame: Disease data loaded from the CSV file.
        - pd.DataFrame: Population statistics loaded from the CSV file.
    """

    disease=pd.read_csv(disease_file_path)
    population=pd.read_csv(population_file_path)

    return disease,population

def disease_count(disease,population):
    """
    Calculate the total number of cases for each disease at different administrative levels (Sector, District, Province).

    Parameters:
    - disease (pd.DataFrame): Input data containing information about cases, diseases, and location.
    - population (pd.DataFrame): Input data containing population information for each Sector, District, and Province.

    Returns:
    pd.DataFrame: The input data with additional columns representing the total cases per Sector, District, and Province, 
                  along with calculated disease burden percentages at each administrative level.

    Notes:
    - The input 'disease' DataFrame is expected to have columns: 'Province', 'District', 'Sector', 'PERIOD', 'DISEASES', and 'NOMBER OF CASES'.
    - The input 'population' DataFrame is expected to have columns: 'Province', 'District', 'Sector', 'Population_per_Sector', 
      'Population_per_District', 'Population_per_Province'.
    
    The function performs the following steps:
    1. Calculates the total cases per Sector, District, and Province based on diseases and their occurrence.
    2. Merges the calculated cases with the 'population' DataFrame on the common columns 'Province', 'District', 'Sector'.
    3. Adjusts column data types for better representation.
    4. Computes disease burden percentages per Sector, District, and Province, rounded to two decimal places.

    Columns added to the output DataFrame:
    - 'CASES_per_Sector': Total cases per Sector.
    - 'CASES_per_District': Total cases per District.
    - 'CASES_per_Province': Total cases per Province.
    - 'Disease_Burden(%)_per_Sector': Disease burden percentage per Sector.
    - 'Disease_Burden(%)_per_District': Disease burden percentage per District.
    - 'Disease_Burden(%)_per_Province': Disease burden percentage per Province.
    """

    # Calculate cases per Sector
    disease['PERIOD'] = pd.to_datetime(disease['PERIOD'])
    disease['CASES_per_Sector'] = disease.groupby(
        by=['Province', 'District', 'Sector', disease['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')

    # Calculate cases per District
    disease['CASES_per_District'] = disease.groupby(
        by=['Province', 'District', disease['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')

    # Calculate cases per Province
    disease['CASES_per_Province'] = disease.groupby(
        by=['Province', disease['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')
    diseases=(disease
              .merge(population,on=['Province','District','Sector'])
              .replace('Shyorongi','Shyrongi')
              .assign(CASES_per_Sector=lambda x: x['CASES_per_Sector'].astype(np.int32),
                      CASES_per_District=lambda x: x['CASES_per_District'].astype(np.int32),
                      CASES_per_Province=lambda x: x['CASES_per_Province'].astype(np.int32),
                      Population_per_Sector=lambda x: x['Population_per_Sector'].astype(np.int32),
                      Population_per_District=lambda x: x['Population_per_District'].astype(np.int32),
                      Population_per_Province=lambda x: x['Population_per_Province'].astype(np.int32))
    )
    # diseases burden
    diseases['Disease_Burden(%)_per_Sector']=((diseases['CASES_per_Sector']/diseases['Population_per_Sector'])*100).round(2)
    diseases['Disease_Burden(%)_per_District']=((diseases['CASES_per_District']/diseases['Population_per_District'])*100).round(2)
    diseases['Disease_Burden(%)_per_Province']=((diseases['CASES_per_Province']/diseases['Population_per_Province'])*100).round(2)

    return diseases

def assign_98_where_burden_greater_than_100(diseases):
    diseases.loc[diseases['Disease_Burden(%)_per_Sector'] >= 100, 'Disease_Burden(%)_per_Sector'] = 98
    diseases.loc[diseases['Disease_Burden(%)_per_District'] >= 100, 'Disease_Burden(%)_per_District'] = 98
    diseases.loc[diseases['Disease_Burden(%)_per_Province'] >= 100, 'Disease_Burden(%)_per_Province'] = 98

    return diseases



def main():
    disease,population=read_data(disease_file_path,population_file_path)
    diseases=disease_count(disease,population)
    Diseases=assign_98_where_burden_greater_than_100(diseases)
    return Diseases

if __name__== "__main__":
    Diseases=main()
Diseases.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/diseases_data.csv',index=False)