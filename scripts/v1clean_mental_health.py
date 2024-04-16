import pandas as pd
import numpy as np
import warnings
from datetime import datetime as dt
def read_data(file_path):
    xls_obj = pd.ExcelFile(file_path)
    return xls_obj


def consolidate_mental_health(xls_obj,sheet):
    """
    Process Excel data and organize it into a new DataFrame.

    Parameters:
    - xls_obj (str or path): The Excel file or path containing the data.
    - sheet (str): The name of the sheet within the Excel file.

    Returns:
    - pd.DataFrame: A new DataFrame with processed data.

    This function reads an Excel file, extracts data from specified columns,
    and organizes it into a new DataFrame. It separates data based on disease
    categories, gender, and age groups (new and old).

    The function performs the following steps:
    1. Reads the Excel file and extracts data from the specified sheet.
    2. Iterates over each row in the DataFrame, extracting relevant information.
    3. Organizes data into lists for disease labels, new/old male, and new/old female.
    4. Creates new Series for each list and aligns them.
    5. Concatenates the new Series with the original DataFrame, dropping unnecessary columns.
    6. Removes duplicate rows and resets the index of the resulting DataFrame.

    """
    dpm = pd.read_excel(xls_obj, sheet_name=sheet)
    numerical_cols = dpm.columns[6:]
    # Initialize empty lists to store values for different columns
    disease_label = []
    Male_new, Male_old=[], []
    Female_new,Female_old=[], []

    # Iterate over each row in the DataFrame
    for _, row in dpm.iterrows():
        # Initialize values for the current row
        disease_values = []
        New_Male, Old_Male= [], []
        New_Female,Old_Female= [], []
        # Iterate over each numerical column
        for col in numerical_cols:
            #col_var=col.capitalize()
            disease_name=col.capitalize().split("cases")[0].strip()
            gender_age=col.capitalize().split("cases")[-1].strip()
            if not pd.isna(row[col]):
                new_disease_name = disease_name.replace('_new', '').replace('_old', '')
                disease_values.append(new_disease_name)

                if disease_name.endswith('new'):
                    if gender_age.startswith('male'):
                        New_Male.append(row[col])
                    elif gender_age.startswith('female'):
                        New_Female.append(row[col])
                    

                elif disease_name.endswith('old'):
                    if gender_age.startswith('male'):
                        Old_Male.append(row[col])
                    elif gender_age.startswith('female'):
                        Old_Female.append(row[col])

            #if pd.isna(row[col]):
            else:
                # Handle the case where row[col] is null
                new_disease_name = disease_name.replace('_new', '').replace('_old', '')
                disease_values.append(new_disease_name)

                if disease_name.endswith('new'):
                    if gender_age.startswith('male'):
                        New_Male.append(0)
                    elif gender_age.startswith('female'):
                        New_Female.append(0)
                elif disease_name.endswith('old'):
                    if gender_age.startswith('male'):
                        Old_Male.append(0)
                    elif gender_age.startswith('female'):
                        Old_Female.append(0)
        #print(disease_values)
        # Append unique disease values
        disease_label.append(list(dict.fromkeys(disease_values)))
        #print(disease_label)
        # Append values to respective lists
    
        Male_new.append(New_Male)
        Female_new.append(New_Female)
        Male_old.append(Old_Male)
        Female_old.append(Old_Female)


    # Create new Series with the aligned lists
    disease_values_series = pd.Series(disease_label, name='DISEASES').explode()
    Male_new_series = pd.Series(Male_new, name='Male - New').explode()
    Female_new_series = pd.Series(Female_new, name='Female - New').explode()
    Male_old_series = pd.Series(Male_old, name='Male - Old').explode()
    Female_old_series = pd.Series(Female_old, name='Female - Old').explode()

    #Concatenate the DataFrames
    df_concat = pd.concat([dpm.reset_index(drop=True),disease_values_series, Female_new_series.astype(int),
                           Male_new_series.astype(int), Female_old_series.astype(int), Male_old_series.astype(int),], axis=1)
    df_concat = df_concat.drop(numerical_cols, axis=1).drop_duplicates() # drop initial columns
    # Reset the index of the DataFrame
    df_concat.reset_index(drop=True, inplace=True)
    
    return df_concat


def disease_count(moh_data):
    """
    Update the given DataFrame 'moh_data' by aggregating age and gender categories.

    Parameters:
    - moh_data (pandas.DataFrame): The input DataFrame containing columns for various age and gender categories.

    The function calculates and adds the following columns to the DataFrame:
  
    - 'Male - Total', 'Female - Total': Total count of males and females by combining 'New' and 'Old' categories.
    Returns:
    None: The function modifies the input DataFrame in-place.
    """
    moh_data['Male - Total']=moh_data['Male - New']+moh_data['Male - Old']
    moh_data['Female - Total']=moh_data['Female - New']+moh_data['Female - Old']
    moh_data['Total - New']=moh_data['Male - New']+moh_data['Female - New']
    moh_data['Total - Old']=moh_data['Male - Old']+moh_data['Female - Old']

    moh_data['Total']=moh_data['Female - Total']+moh_data['Male - Total']

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
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/OPD_HMIS Data_Part 3.xlsx'
    file_path_moh = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facility_data.csv'
    
    xls_obj = read_data(file_path)
    disease_data = consolidate_mental_health(xls_obj,'Mental Health')
    from clean_chronic_diseases import clean_data
    cleaned_data = clean_data(disease_data)
    
    facility_data = pd.read_csv(file_path_moh)
    from clean_MOH import add_facility_type
    moh_data = add_facility_type(cleaned_data, facility_data)
    moh_data1=disease_count(moh_data)
    from clean_shapefile import clean_sector
    moh_data2=clean_sector(moh_data1)

    return moh_data2

if __name__ == "__main__":
    moh_data2 = main()
    moh_data2.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/Mental_health.csv',index=False)
 