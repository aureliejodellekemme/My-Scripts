import pandas as pd
import numpy as np
import warnings
from datetime import datetime as dt
def read_data(file_path):
    xls_obj = pd.ExcelFile(file_path)
    return xls_obj

def read_facility_type_data(xls_obj):
    df=pd.read_excel(xls_obj, sheet_name=xls_obj.sheet_names[0])[['HEALTH FACILITY', 'FACILITY TYPE']]
    return df

def consolidate_diseases(xls_obj,n,m):
    """
    Consolidate disease data from multiple sheets in an Excel file.

    This function reads data from multiple sheets in an Excel file and consolidates it into a single DataFrame.
    Each sheet in the Excel file is expected to contain data related to diseases, with numerical columns representing
    the number of cases for different diseases.

    Parameters:
    xls_obj (pandas.ExcelFile): An ExcelFile object containing multiple sheets of disease data.

    Returns:
    pandas.DataFrame: A DataFrame has been created to consolidate disease data, featuring two columns: 
    'DISEASES' for disease names and 'NUMBER OF CASES' for the corresponding case counts. This DataFrame 
    also includes initial columns such as "PROVINCE," "SUB DISTRICT," "DISTRICT," "SECTOR," "HEALTH FACILITY," 
    and "PERIOD." Additionally, the "FACILITY TYPE" has been added to the DataFrame using the "HEALTH FACILITY" from  
    the first sheet as a key variable. To enhance the data, two new columns, "YEAR" and "QUARTER," have been generated based on 
    the "PERIOD" variable. 

    Note:
    - If a numerical value is missing (NaN) in a sheet, it is treated as 0 cases for the respective disease.
    - The 'DISEASES' column is created by combining the column names representing diseases.
    - The 'NOMBER OF CASES' column contains the corresponding disease cases aligned with the 'DISEASES' column.
    """
    disease_data = pd.DataFrame()
    # Create a list of numerical column names
    for sheet in xls_obj.sheet_names[n:m]:
        dpm = pd.read_excel(xls_obj, sheet_name=sheet)
        numerical_cols = dpm.columns[6:]
        # Initialize empty lists to store values for 'disease' and 'disease_cases' columns
        disease_values = []
        disease_cases_values = []
        # Iterate over each row in the DataFrame
        for _, row in dpm.iterrows():
            # Initialize 'disease' and 'disease_cases' values for the current row
            diseases = []
            disease_cases = []
            # Iterate over each numerical column
            for col in numerical_cols:
                if not pd.isna(row[col]): # Check if the value in the numerical column is not NaN
                    # Append the column name to 'diseases' list and the value to 'disease_cases' list
                    diseases.append(col)
                    disease_cases.append(row[col])
                    # Append the column name to 'diseases' list, the 0 to 'disease_cases' list
                if pd.isna(row[col]): 
                    diseases.append(col)
                    disease_cases.append(0)
             # Check if 'diseases' list is empty 
            if not diseases:
                # Append sheet name to diseases list and Nan to disease_cases list
                diseases.append(sheet)
                disease_cases.append(np.nan)
           
            # Append 'diseases' and 'disease_cases' values to the respective lists
            disease_values.append(diseases)
            disease_cases_values.append(disease_cases)
        # Create new Series with the aligned lists
        disease_series = pd.Series(disease_values, name='DISEASES').explode()
        disease_cases_series = pd.Series(disease_cases_values, name='NOMBER OF CASES').explode()
        # Reset the index of the DataFrames
        #dpm = dpm.reset_index(drop=True)
        #disease_series = disease_series.reset_index(drop=True)
        #disease_cases_series = disease_cases_series.reset_index(drop=True)
        # Concatenate the DataFrames
        df_concat = pd.concat([dpm, disease_series, disease_cases_series], axis=1)
        df_concat = df_concat.drop(numerical_cols, axis=1) # drop initial columns
        # set it as dataframe
        disease_data = pd.concat([disease_data, df_concat], ignore_index=True)
    
    return disease_data

def clean_data(data):
    """
    Clean and preprocess a DataFrame containing disease data.

    Parameters:
    data (DataFrame): A DataFrame containing disease data with various columns, including 'PROVINCE', 'DISTRICT', 'SECTOR',
                     'HEALTH FACILITY', 'PERIOD', 'SUB DISTRICT', 'NOMBER OF CASES', and more.

    Returns:
    DataFrame: A cleaned and preprocessed DataFrame with the following transformations:
        1. Filtering out specific 'DISTRICT' values ('Kigali City', 'West', 'South', 'East', 'North').
        2. Modifying 'DISTRICT' values to keep only the first part of the name to align with the format in sector shape file.
        3. Adding 'ern Province' to 'PROVINCE' values that are not 'Kigali City' to have the format Southern Province etc...
        4. Renaming columns to 'Province', 'District', and 'Sector'.
        5. Dropping rows with missing values in the 'NOMBER OF CASES' column because it is the case where disease names do not exist.
        6. Dropping the 'SUB DISTRICT' column as it is the same as DISTRICT.
        7. Generating 'YEAR' and 'QUARTER' columns based on the 'PERIOD' column. That might be helpful to visualize a certain period of time
        8. Converting 'NOMBER OF CASES' to integer type. 
        9. Cleaning sector names based on specified replacements and capitalizing sector names. To align with sector shape file format

    Note: The input DataFrame 'data' is the data generated from the "consolidate_diseases" function and it is modified in place,
      and the cleaned DataFrame is returned as the result.
    """
    
    data = data[~data['DISTRICT'].isin(['Kigali City', 'West', 'South', 'East', 'North'])] # filter out wrong name of district
    data['DISTRICT'] = data['DISTRICT'].str.split(' ').str[0] # Collect the first name in district value
    data.loc[data['PROVINCE'] != 'Kigali City', 'PROVINCE'] += 'ern Province' # Add suffix to have Northern Province etc..
    
    cleaned_data = (data.rename(columns={'PROVINCE': 'Province', 'DISTRICT': 'District', 'SECTOR': 'Sector'})# Capitalize columns name to have same format as other data source
                    .dropna(subset=['NOMBER OF CASES']) # drop null values in disease cases as the reflect the name of the sheet and not disease
                    .drop('SUB DISTRICT', axis=1))# Drop su district as same as district
    
    cleaned_data['NOMBER OF CASES'] = cleaned_data['NOMBER OF CASES'].astype(int)# convert diseases case ti integer
    return cleaned_data

def add_facility_type(data, facility_data):
    """
    Adds a 'FACILITY TYPE' column to the input data by merging it with facility_data based on the 'HEALTH FACILITY' column.
    The 'FACILITY TYPE' is determined based on the suffix of the 'HEALTH FACILITY' name.

    Parameters:
    data (pandas.DataFrame): The main data to which the 'FACILITY TYPE' column will be added.
    facility_data (pandas.DataFrame): The data containing information about the facilities which is the first sheet.

    Returns:
    pandas.DataFrame: A new DataFrame with the 'FACILITY TYPE' column added based key variable 'HEALTH FACILITY',
    and for the not matching one we added based on the facility suffix.
    """

    moh_data = data.merge(facility_data, on=['HEALTH FACILITY'], how='left') # add type of facility to the data
    # Add type of facility to facilities not in facility_data by using the two last character of the name as reference
    # Create conditions for each facility type
    condition_health_center = moh_data['HEALTH FACILITY'].str.endswith(('CS', 'VCT','(Mobile VCT)'))
    condition_health_post = moh_data['HEALTH FACILITY'].str.endswith(('HP','PS','ost','econdaire','secondare'))
    condition_ngo = moh_data['HEALTH FACILITY'].str.endswith(('coeur','Friendly Center','RULINDO','Rwanda','Region'))
    condition_individual = moh_data['HEALTH FACILITY'].str.endswith(('Assurance','IBN.SINA'))
    condition_individual_prison = moh_data['HEALTH FACILITY'].str.endswith(('Prison'))
    

    # Use the conditions to fill NaN values in the "FACILITY TYPE" column
    moh_data.loc[condition_health_center, 'FACILITY TYPE'] = 'HEALTH CENTER'
    moh_data.loc[condition_health_post, 'FACILITY TYPE'] = 'HEALTH POST'
    moh_data.loc[condition_ngo, 'FACILITY TYPE'] = 'NGO'
    moh_data.loc[condition_individual, 'FACILITY TYPE'] = 'INDIVIDUAL'
    moh_data.loc[condition_individual_prison, 'FACILITY TYPE'] = 'PRISON'
    type_facility=moh_data.pop('FACILITY TYPE')
    moh_data.insert(5,'FACILITY TYPE',type_facility)
    return moh_data.drop_duplicates()
# Number of cases per location, year and diseases
def disease_count(moh_data):
    """
    Calculate the total number of cases for each disease at different levels (Sector, District, Province).

    Parameters:
    - moh_data (pd.DataFrame): Input data containing information about cases, diseases, and location.

    Returns:
    pd.DataFrame: The input data with additional columns representing the total cases per Sector, District, and Province.
    """
    # Calculate cases per Sector
    moh_data['CASES_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')

    # Calculate cases per District
    moh_data['CASES_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')

    # Calculate cases per Province
    moh_data['CASES_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['PERIOD'].dt.year, 'DISEASES']
    )['NOMBER OF CASES'].transform('sum')

    return moh_data.drop_duplicates()


def main():
    """
    The main function for processing MOH Data data.

    Reads data from a specified Excel file, consolidates disease information, cleans the data,
    and adds a 'FACILITY TYPE' column based on facility information. The resulting data is returned.

    Returns:
    pandas.DataFrame: Processed moh_data that will be exported as csv file.
    """
    # upload and read the data with pandas.read_excel() and applied the previous functions to process the data
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/OPD_HMIS Data_Part 1.xlsx'
    
    xls_obj = read_data(file_path)
    facility_data = read_facility_type_data(xls_obj)
    facility_data.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facility_data.csv',index=False)
    disease_data = consolidate_diseases(xls_obj,1,len(xls_obj.sheet_names)-1)
    cleaned_data = clean_data(disease_data)
    
    moh_data = add_facility_type(cleaned_data, facility_data)
    #moh_data1=disease_count(moh_data)
    from clean_shapefile import clean_sector
    moh_data2=clean_sector(moh_data)

    return moh_data2

if __name__ == "__main__":
    moh_data2 = main()
moh_data2.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/moh_data.csv',index=False)
 