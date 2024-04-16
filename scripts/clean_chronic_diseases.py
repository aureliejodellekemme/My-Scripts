import pandas as pd
import numpy as np
import warnings
from datetime import datetime as dt
def read_data(file_path):
    xls_obj = pd.ExcelFile(file_path)
    return xls_obj


def consolidate_chronic_diseases(xls_obj,years):
    """
    Process data from an Excel file and generate a DataFrame with specific columns.

        Parameters:
        - xls_obj (ExcelFile or str): The Excel file or path to the Excel file containing the data.
        - sheet (str): The name of the sheet in the Excel file.

        Returns:
        - pd.DataFrame: A DataFrame containing processed data with columns representing diseases,
                       gender, age groups, and corresponding case counts.

        The function reads data from the specified sheet in the Excel file and performs data
        processing to extract information related to diseases, gender, and age groups. It then
        creates a new DataFrame with organized columns and returns the result.

        Note:
        - The input Excel file (xls_obj) should be formatted appropriately with relevant data.
        - The returned DataFrame includes columns such as 'DISEASES', 'Male less than 39 - New',
          'Female less than 39 - New', 'Male less than 39 - Old', 'Female less than 39 - Old',
          'Male greater than 40 - New', 'Female greater than 40 - New', 'Male greater than 40 - Old',
          and 'Female greater than 40 - Old'.
        - The function handles missing values by replacing them with zero in the generated DataFrame.
    """
    disease_data = pd.DataFrame()
    for sheet in xls_obj.sheet_names:
        dpm = pd.read_excel(xls_obj, sheet_name=sheet)
        numerical_cols = dpm.columns[6:]
        # Initialize empty lists to store values for different columns
        disease_label = []
        Male39_new, Male40_new, Male39_old, Male40_old = [], [], [], []
        Female39_new, Female40_new, Female39_old, Female40_old = [], [], [], []

        # Iterate over each row in the DataFrame
        for _, row in dpm.iterrows():
            # Initialize values for the current row
            disease_values = []
            less_than_39_Male_New, greater_than_40_Male_New = [], []
            less_than_39_Female_New, greater_than_40_Female_New = [], []
            less_than_39_Male_Old, greater_than_40_Male_Old = [], []
            less_than_39_Female_Old, greater_than_40_Female_Old = [], []
            # Iterate over each numerical column
            for col in numerical_cols:
                #col_var=col.capitalize()
                disease_name=col.capitalize().split("cases")[0].strip()
                gender_age=col.capitalize().split("cases")[-1].strip()
                if not pd.isna(row[col]):
                    new_disease_name = disease_name.replace('_new', '').replace('_old', '')
                    disease_values.append(new_disease_name)
                   
                    if disease_name.endswith('new'):
                        if gender_age.startswith('male 0-39y') or gender_age.startswith('under 20yrs, male'):
                            less_than_39_Male_New.append(row[col])
                        elif gender_age.startswith('male >=40y') or gender_age.startswith('20yrs and above, male'):
                            greater_than_40_Male_New.append(row[col])
                        elif gender_age.startswith('female 0-39y') or gender_age.startswith('under 20yrs, female'):
                            less_than_39_Female_New.append(row[col])
                        elif gender_age.startswith('female >=40y') or gender_age.startswith('20yrs and above, female'):
                            greater_than_40_Female_New.append(row[col])

                    elif disease_name.endswith('old'):
                        if gender_age.startswith('male 0-39y') or gender_age.startswith('under 20yrs, male'):
                            less_than_39_Male_Old.append(row[col])
                        elif gender_age.startswith('male >=40y') or gender_age.startswith('20yrs and above, male'):
                            greater_than_40_Male_Old.append(row[col])
                        elif gender_age.startswith('female 0-39y') or gender_age.startswith('under 20yrs, female'):
                            less_than_39_Female_Old.append(row[col])
                        elif gender_age.startswith('female >=40y') or gender_age.startswith('20yrs and above, female'):
                            greater_than_40_Female_Old.append(row[col])
                #if pd.isna(row[col]):
                else:
                    # Handle the case where row[col] is null
                    new_disease_name = disease_name.replace('_new', '').replace('_old', '')
                    disease_values.append(new_disease_name)

                    if disease_name.endswith('new'):
                        if gender_age.startswith('male 0-39y') or gender_age.startswith('under 20yrs, male'):
                            less_than_39_Male_New.append(0)
                        elif gender_age.startswith('male >=40y') or gender_age.startswith('20yrs and above, male'):
                            greater_than_40_Male_New.append(0)
                        elif gender_age.startswith('female 0-39y') or gender_age.startswith('under 20yrs, female'):
                            less_than_39_Female_New.append(0)
                        elif gender_age.startswith('female >=40y') or gender_age.startswith('20yrs and above, female'):
                            greater_than_40_Female_New.append(0)

                    elif disease_name.endswith('old'):
                        if gender_age.startswith('male 0-39y') or gender_age.startswith('under 20yrs, male'):
                            less_than_39_Male_Old.append(0)
                        elif gender_age.startswith('male >=40y') or gender_age.startswith('20yrs and above, male'):
                            greater_than_40_Male_Old.append(0)
                        elif gender_age.startswith('female 0-39y') or gender_age.startswith('under 20yrs, female'):
                            less_than_39_Female_Old.append(0)
                        elif gender_age.startswith('female >=40y') or gender_age.startswith('20yrs and above, female'):
                            greater_than_40_Female_Old.append(0)

            disease_label.append(list(dict.fromkeys(disease_values)))
            #print(disease_label)
            # Append values to respective lists
        
            Male39_new.append(less_than_39_Male_New)
            Male40_new.append(greater_than_40_Male_New)
            Female39_new.append(less_than_39_Female_New)
            Female40_new.append(greater_than_40_Female_New)

            Male39_old.append(less_than_39_Male_Old)
            Male40_old.append(greater_than_40_Male_Old)
            Female39_old.append(less_than_39_Female_Old)
            Female40_old.append(greater_than_40_Female_Old)

        # Create new Series with the aligned lists
        disease_values_series = pd.Series(disease_label, name='DISEASES').explode()
        Male39_new_series = pd.Series(Male39_new, name=f'Male_Under_{years}y_New_Cases').explode()
        Female39_new_series = pd.Series(Female39_new, name=f'Female_Under_{years}y_New_Cases').explode()
        Male39_old_series = pd.Series(Male39_old, name=f'Male_Under_{years}y_Old_Cases').explode()
        Female39_old_series = pd.Series(Female39_old, name=f'Female_Under_{years}y_Old_Cases').explode()
        Male40_new_series = pd.Series(Male40_new, name=f'Male_Above_{years}y_New_Cases').explode()
        Female40_new_series = pd.Series(Female40_new, name=f'Female_Above_{years}y_New_Cases').explode()
        Male40_old_series = pd.Series(Male40_old, name=f'Male_Above_{years}y_Old_Cases').explode()
        Female40_old_series = pd.Series(Female40_old, name=f'Female_Above_{years}y_Old_Cases').explode()
    
        #Concatenate the DataFrames
        df_concat = pd.concat([dpm.reset_index(drop=True),disease_values_series, Female39_new_series.astype(int), Female40_new_series.astype(int), Male39_new_series.astype(int), Male40_new_series.astype(int),
                        Female39_old_series.astype(int), Female40_old_series.astype(int), Male39_old_series.astype(int), Male40_old_series.astype(int)], axis=1)
        df_concat = df_concat.drop(numerical_cols, axis=1).drop_duplicates() # drop initial columns
        # Reset the index of the DataFrame
        df_concat.reset_index(drop=True, inplace=True)
       
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
        4. Renaming columns to 'Health Facility'.
        5. Dropping the 'SUB DISTRICT' column as it is the same as DISTRICT.
        6. Cleaning sector names based on specified replacements and capitalizing sector names. To align with sector shape file format

    Note: The input DataFrame 'data' is the data generated from the "consolidate_diseases" function and it is modified in place,
      and the cleaned DataFrame is returned as the result.
    """
    
    data = data[~data['District'].isin(['Kigali City', 'West', 'South', 'East', 'North'])] # filter out wrong name of district
    data['District'] = data['District'].str.split(' ').str[0] # Collect the first name in district value
    data.loc[data['Province'] != 'Kigali City', 'Province'] += 'ern Province' # Add suffix to have Northern Province etc..
    
    cleaned_data = (data
                    .rename(columns={'Health Facility':'HEALTH FACILITY'})
                    .drop('Sub District', axis=1))# Drop su district as same as district
    return cleaned_data


def disease_count(moh_data,years):
    """
    Update the given DataFrame 'moh_data' by aggregating age and gender categories.

    Parameters:
    - moh_data (pandas.DataFrame): The input DataFrame containing columns for various age and gender categories.

    The function calculates and adds the following columns to the DataFrame:
    - 'Male - New', 'Female - New': Sum of corresponding age groups for males and females in the 'New' category.
    - 'Male - Old', 'Female - Old': Sum of corresponding age groups for males and females in the 'Old' category.
    - 'Male - Total', 'Female - Total': Total count of males and females by combining 'New' and 'Old' categories.
    - 'Male less than 39 - Total', 'Female less than 39 - Total': Total count of males and females below 39 years old.
    - 'Male greater than 40 - Total', 'Female greater than 40 - Total': Total count of males and females aged 40 or above.

    Returns:
    None: The function modifies the input DataFrame in-place.
    """
    
    moh_data[f'Male_Under_{years}y_Total_Cases']=moh_data[f'Male_Under_{years}y_New_Cases']+moh_data[f'Male_Under_{years}y_Old_Cases']
    moh_data[f'Female_Under_{years}y_Total_Cases']=moh_data[f'Female_Under_{years}y_New_Cases']+moh_data[f'Female_Under_{years}y_Old_Cases']
    
    moh_data[f'Male_Above_{years}y_Total_Cases']=moh_data[f'Male_Above_{years}y_New_Cases']+moh_data[f'Male_Above_{years}y_Old_Cases']
    moh_data[f'Female_Above_{years}y_Total_Cases']=moh_data[f'Female_Above_{years}y_New_Cases']+moh_data[f'Female_Above_{years}y_Old_Cases']
    moh_data['Male_New_Cases']=moh_data[f'Male_Under_{years}y_New_Cases']+moh_data[f'Male_Above_{years}y_New_Cases']
    moh_data['Female_New_Cases']=moh_data[f'Female_Under_{years}y_New_Cases']+moh_data[f'Female_Above_{years}y_New_Cases']
    
    moh_data['Male_Old_Cases']=moh_data[f'Male_Under_{years}y_Old_Cases']+moh_data[f'Male_Above_{years}y_Old_Cases']
    moh_data['Female_Old_Cases']=moh_data[f'Female_Under_{years}y_Old_Cases']+moh_data[f'Female_Above_{years}y_Old_Cases']
    
    moh_data['Male_Total_Cases']=moh_data['Male_New_Cases']+moh_data['Male_Old_Cases']
    moh_data['Female_Total_Cases']=moh_data['Female_New_Cases']+moh_data['Female_Old_Cases']
    moh_data['Total_New_Cases']=moh_data['Male_New_Cases']+moh_data['Female_New_Cases']
    moh_data['Total_Old_Cases']=moh_data['Male_Old_Cases']+moh_data['Female_Old_Cases']

    moh_data['Total_Cases']=moh_data['Female_Total_Cases']+moh_data['Male_Total_Cases']


    moh_data['Total_New_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Total_Old_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Old_Cases'].transform('sum')

    moh_data['Total_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Total_New_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Total_Old_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Old_Cases'].transform('sum')

    moh_data['Total_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Total_New_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Total_Old_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Old_Cases'].transform('sum')

    moh_data['Total_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    # Calculate cases per Month

    moh_data['Monthly_New_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Monthly_Old_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Total_Old_Cases'].transform('sum')

    moh_data['Monthly_Total_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Total_Cases'].transform('sum')


    moh_data['Monthly_New_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Monthly_Old_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Total_Old_Cases'].transform('sum')


    moh_data['Monthly_Total_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Monthly_New_Cases_per_Province'] = moh_data.groupby(
        by=['Province', 'Period', 'DISEASES']
    )['Total_New_Cases'].transform('sum')

    moh_data['Monthly_Old_Cases_per_Province'] = moh_data.groupby(
        by=['Province', 'Period', 'DISEASES']
    )['Total_Old_Cases'].transform('sum')

    moh_data['Monthly_Total_Cases_per_Province'] = moh_data.groupby(
        by=['Province', 'Period', 'DISEASES']
    )['Total_Cases'].transform('sum')

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
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/New Data/Chronic Diseases.xlsx'
    file_path_moh = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facility_data.csv'
    
    xls_obj = read_data(file_path)
    disease_data = consolidate_chronic_diseases(xls_obj,'39' )
    cleaned_data = clean_data(disease_data)
    facility_data = pd.read_csv(file_path_moh)
    from clean_MOH import add_facility_type
    moh_data = add_facility_type(cleaned_data, facility_data)
    moh_data1=disease_count(moh_data,'39')
    from clean_shapefile import clean_sector
    moh_data2=clean_sector(moh_data1)

    return moh_data2

if __name__ == "__main__":
    moh_data2 = main()
    moh_data2.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/Chronic-Diseases.csv',index=False)
 