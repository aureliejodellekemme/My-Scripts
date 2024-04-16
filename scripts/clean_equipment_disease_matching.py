# importing libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
 #################################  END  ###############################
# define data path
equip_disease_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases_to_Equipment/Copy of equipment_disease_matching.xlsx'
# read data
def read_equip_diseas(equip_disease_file_path):
    return pd.read_excel(equip_disease_file_path, sheet_name='Sheet1')

# clean data
def clean_equip_diseas(disease):
    disease_match=(disease
        .drop(['Disease','Internal equipment','RBC Equipment not in Internal Equipment'],axis=1)
        .rename(columns={'Unnamed: 1':'DISEASES'})
        .drop(0)
        .reset_index(drop=True)
    )
    return disease_match

def createequipment(diseas):

    # Create a list of numerical column names
    numerical_cols = diseas.columns[1:]

    # Initialize empty lists to store values for 'disease' and 'disease_cases' columns
    disease_values = []
    disease_cases_values = []

    # Iterate over each row in the DataFrame
    for _, row in diseas.iterrows():
        # Initialize 'disease' and 'disease_cases' values for the current row
        diseases = []
        disease_cases = []

        # Iterate over each numerical column
        for col in numerical_cols:
            # Check if the value in the numerical column is not NaN or zero
            if not pd.isna(row[col]):
                # Append the column name to 'diseases' list
                diseases.append(col)
                # Append the value to 'disease_cases' list
                disease_cases.append(row[col])

        # Check if 'diseases' list is empty (all numerical values are missing or zero)
        if not diseases:
            diseases.append('No equipments')
            disease_cases.append('No equipments')

        # Append 'diseases' and 'disease_cases' values to the respective lists
        disease_values.append(diseases)
        disease_cases_values.append(disease_cases)

    # Create new Series with the aligned lists
    disease_series = pd.Series(disease_values, name='DISEASES').explode()
    disease_cases_series = pd.Series(disease_cases_values, name='EQUIPMENT').explode()
    diseas.reset_index(drop=True)
    disease_cases_series.reset_index(drop=True)
    #print(disease_cases_series)
    # Concatenate the new series with the original DataFrame
    df_concat = pd.concat([diseas, disease_cases_series], axis=1)
    #drop unsed columns
    df_concat=df_concat.drop(numerical_cols, axis=1)
    return df_concat

def main():
    disease=read_equip_diseas(equip_disease_file_path)
    disease_match=clean_equip_diseas(disease)
    df_concat=createequipment(disease_match)
    return df_concat.drop_duplicates()
if __name__ == "__main__":
    equip_diseas = main()
equip_diseas.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases_to_Equipment/equipment_diseases_matching.csv',index=False)