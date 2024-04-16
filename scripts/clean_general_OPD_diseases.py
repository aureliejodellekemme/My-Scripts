import pandas as pd
import numpy as np
import warnings
from datetime import datetime as dt

def consolidate_opd_diseases(xls_obj,years):

    """
    Processes disease data from an Excel file object to create a structured DataFrame.

    This function iterates over each sheet in the provided Excel file object, extracting
    and reformating data related to disease cases. It handles data across different age 
    and gender categories, specifically for males and females both under and above 5 years old.
    The function cleans and restructures this data into a more readable and accessible format.

    Parameters:
    - xls_obj (ExcelFile): An Excel file object containing multiple sheets with disease data.
                           Each sheet is expected to have a set of numerical columns representing
                           different diseases and their case counts categorized by gender and age.
    - years (int or str): A value representing the year(s) to which the data pertains. This is used
                          in naming the columns for total cases.

    Returns:
    - DataFrame: A pandas DataFrame containing the processed data. The DataFrame includes columns for
                 disease names and total cases for each gender and age category (Male/Female, Under/Above 5 years).
                 Each row corresponds to data from a specific sheet in the original Excel file.
                 The original numerical columns from the input data are dropped, and duplicate rows are removed.

    Notes:
    - The function expects specific formatting in the input Excel sheets, particularly in the naming and
      arrangement of the columns related to disease cases.
    - Null values in the input data are handled by assigning a zero count to the respective category.
    - The function may raise errors if the input Excel file does not adhere to the expected format.

    """

    disease_data = pd.DataFrame()
    for sheet in xls_obj.sheet_names:
        dpm = pd.read_excel(xls_obj, sheet_name=sheet)
        numerical_cols = dpm.columns[6:]
        # Initialize empty lists to store values for different columns
        disease_label = []
        Male5_under, Male5_above= [], []
        Female5_under, Female5_above = [], []

        # Iterate over each row in the DataFrame
        for _, row in dpm.iterrows():
            # Initialize values for the current row
            disease_values = []
            less_than_5_Male, greater_than_5_Male= [], []
            less_than_5_Female, greater_than_5_Female= [], []
            # Iterate over each numerical column
            for col in numerical_cols:
                #col_var=col.capitalize()
                disease_name=col.capitalize().split("5")[0].strip()
                #gender_age=col.capitalize().split("5")[-1].strip()
                if not pd.isna(row[col]):
                    new_disease_name = disease_name.replace(' female <', '').replace(' female >=', '').replace(' male <', '').replace(' male >=', '')
                    disease_values.append(new_disease_name)
                   
                    if disease_name.endswith(' male <'):
                        less_than_5_Male.append(row[col])
                    elif disease_name.endswith(' male >='):
                        greater_than_5_Male.append(row[col])
                    elif disease_name.endswith('female <'):
                        less_than_5_Female.append(row[col])
                    elif disease_name.endswith('female >='):
                        greater_than_5_Female.append(row[col])
                    
                else:
                    # Handle the case where row[col] is null   
                    new_disease_name = (disease_name
                                        .replace(' female <', '').replace(' female >=', '') # renaming diseases on general opd data
                                        .replace(' male <', '').replace(' male >=', '')
                                        .replace(' cases received in OPD ', '') # renaming diseases  on malaria data
                    )
                    disease_values.append(new_disease_name)

                    if disease_name.endswith(' male <'):
                        less_than_5_Male.append(0)
                    elif disease_name.endswith(' male >='):
                        greater_than_5_Male.append(0)
                    elif disease_name.endswith('female <'):
                        less_than_5_Female.append(0)
                    elif disease_name.endswith('female >='):
                        greater_than_5_Female.append(0)

            disease_label.append(list(dict.fromkeys(disease_values)))
            #print(disease_label)
            # Append values to respective lists
        
            Male5_under.append(less_than_5_Male)
            Male5_above.append(greater_than_5_Male)
            Female5_under.append(less_than_5_Female)
            Female5_above.append(greater_than_5_Female)
        # Create new Series with the aligned lists
        disease_values_series = pd.Series(disease_label, name='DISEASES').explode()
        Male5_under_series = pd.Series(Male5_under, name=f'Male_Under_{years}y_Total_Cases').explode()
        Male5_above_series = pd.Series(Male5_above, name=f'Male_Above_{years}y_Total_Cases').explode()
        Female5_under_series = pd.Series(Female5_under, name=f'Female_Under_{years}y_Total_Cases').explode()
        Female5_above_series = pd.Series(Female5_above, name=f'Female_Above_{years}y_Total_Cases').explode()
        Female5_under_series = pd.Series(Female5_under, name=f'Female_Under_{years}y_Total_Cases').explode()
        #print(disease_values_series,Male5_above_series)
        #Concatenate the DataFrames
        df_concat = pd.concat([dpm.reset_index(drop=True),disease_values_series, Female5_under_series.astype(int), Female5_above_series.astype(int),
                        Male5_under_series.astype(int), Male5_above_series.astype(int)], axis=1)
        df_concat = df_concat.drop(numerical_cols, axis=1).drop_duplicates() # drop initial columns
        # Reset the index of the DataFrame
        df_concat.reset_index(drop=True, inplace=True)
       
        # set it as dataframe
        disease_data = pd.concat([disease_data, df_concat], ignore_index=True)
        
    return disease_data

def disease_count(moh_data,years):
    
    """
    Aggregates disease case data by gender, age group, and geographical divisions in the moh_data DataFrame.

    This function adds several columns to the moh_data DataFrame, each representing aggregate case counts
    across different categories and geographical hierarchies (province, district, sector). It computes total 
    case counts for males, females, and combined, across different age groups (under and above a specified number 
    of years) and time periods (annually and monthly).

    Parameters:
    - moh_data (DataFrame): A pandas DataFrame containing detailed disease case data, including columns for gender,
                            age groups, and geographical divisions (Province, District, Sector).
    - years (int or str): A value representing the age threshold used for categorizing case counts into 'under' and 'above' age groups.

    Returns:
    - DataFrame: The modified moh_data DataFrame with additional columns for aggregated case counts. These include total
                 cases by gender and age group at sector, district, and province levels, both on an annual and monthly basis.
                 The function also removes duplicate rows after the aggregation.

    Notes:
    - The function expects the moh_data DataFrame to contain specific columns related to disease cases, gender, age groups,
      and geographical divisions. The presence of columns like 'Male_Under_{years}y_Total_Cases', 'Female_Above_{years}y_Total_Cases',
      'Province', 'District', 'Sector', and 'Period' is essential for the proper functioning of this function.
    - The 'Period' column should be in a datetime format to facilitate monthly and annual aggregations.
    - The function may raise errors if the moh_data DataFrame does not adhere to the expected format or if essential columns are missing.

    """
    
    moh_data[f'Under_{years}y_Total_Cases']=moh_data[f'Male_Under_{years}y_Total_Cases']+moh_data[f'Female_Under_{years}y_Total_Cases']
    moh_data[f'Above_{years}y_Total_Cases']=moh_data[f'Male_Above_{years}y_Total_Cases']+moh_data[f'Female_Above_{years}y_Total_Cases']
    
    moh_data['Male_Total_Cases']=moh_data[f'Male_Under_{years}y_Total_Cases']+moh_data[f'Male_Above_{years}y_Total_Cases']
    moh_data['Female_Total_Cases']=moh_data[f'Female_Under_{years}y_Total_Cases']+moh_data[f'Female_Above_{years}y_Total_Cases']

    moh_data['Total_Cases']=moh_data['Female_Total_Cases']+moh_data['Male_Total_Cases']


    moh_data['Total_Male_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Total_Female_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Female_Total_Cases'].transform('sum')

    moh_data['Total_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Total_Male_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Total_Female_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Female_Total_Cases'].transform('sum')

    moh_data['Total_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Total_Male_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Total_Female_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Female_Total_Cases'].transform('sum')

    moh_data['Total_Cases_per_Province'] = moh_data.groupby(
        by=['Province', moh_data['Period'].dt.year, 'DISEASES']
    )['Total_Cases'].transform('sum')

    # Calculate cases per Month

    moh_data['Monthly_Male_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Monthly_Female_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Female_Total_Cases'].transform('sum')

    moh_data['Monthly_Total_Cases_per_Sector'] = moh_data.groupby(
        by=['Province', 'District', 'Sector', 'Period', 'DISEASES']
    )['Total_Cases'].transform('sum')


    moh_data['Monthly_Male_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Monthly_Female_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Female_Total_Cases'].transform('sum')


    moh_data['Monthly_Total_Cases_per_District'] = moh_data.groupby(
        by=['Province', 'District', 'Period', 'DISEASES']
    )['Total_Cases'].transform('sum')

    moh_data['Monthly_Male_Cases_per_Province'] = moh_data.groupby(
        by=['Province', 'Period', 'DISEASES']
    )['Male_Total_Cases'].transform('sum')

    moh_data['Monthly_Female_Cases_per_Province'] = moh_data.groupby(
        by=['Province', 'Period', 'DISEASES']
    )['Female_Total_Cases'].transform('sum')

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
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/New Data/Priority health problems in General OPD.xlsx'
    file_path_moh = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facility_data.csv'
    from clean_chronic_diseases import read_data
    xls_obj = read_data(file_path)
    disease_data = consolidate_opd_diseases(xls_obj,'5')
    from clean_chronic_diseases import clean_data
    cleaned_data = clean_data(disease_data)
    
    facility_data = pd.read_csv(file_path_moh)
    from clean_MOH import add_facility_type
    moh_data = add_facility_type(cleaned_data, facility_data)
    moh_data1=disease_count(moh_data,'5')
    from clean_shapefile import clean_sector
    moh_data2=clean_sector(moh_data1)

    return moh_data2

if __name__ == "__main__":
    moh_data2 = main()
    moh_data2.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/general_OPD_diseases.csv',index=False)
 