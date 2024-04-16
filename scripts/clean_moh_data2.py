import pandas as pd

def read_data(file_path):
    xls_obj = pd.read_csv(file_path)
    return xls_obj

disease_cases_mapping = {
    'OPD_NCD_Diabetes - Type 2': ['OPD_NCD_Diabetes - Type 2_New Cases', 'OPD_NCD_Diabetes - Type 2_Old Cases'],
    'OPD_NCD_Hypertension': ['OPD_NCD_Hypertension_New Cases', 'OPD_NCD_Hypertension_Old Cases'],
    'OPD_NCD_Suspected Cancer': ['OPD_NCD_Suspected Cancer_New Cases', 'OPD_NCD_Suspected Cancer_Old Cases'],
    'OPD_Mental Depression': ['OPD_Mental Depression_New Cases', 'OPD_Mental Depression_Old Cases','OPD_ Mental Depression_New Cases'],
    'OPD_Mental Suicide_attempted': ['OPD_Mental Suicide_attempted_Old Cases', 'OPD_Mental Suicide_attempted_New Cases'],
    'OPD_NCD_Diabetes - Type 1': ['OPD_NCD_Diabetes - Type 1_Old Cases', 'OPD_NCD_Diabetes - Type 1_New Cases'],
    'OPD_NCD_Diabetes gestational': ['OPD_NCD_Diabetes gestational_New Cases', 'OPD_NCD_Diabetes gestational_Old Cases'],
    'OPD_NCD_Confirmed Cancer': ['OPD_NCD_Confirmed Cancer_New Cases', 'OPD_NCD_Confirmed Cancer_Old Cases'],
    'OPD_NCD_Other Chronic respiratory diseases': ['OPD_NCD_Other Chronic respiratory diseases_New cases', 'OPD_NCD_Other Chronic respiratory diseases_Old cases'],
    'OPD_Mental Schizophrenia and other psychoses': ['OPD_Mental Schizophrenia and other psychoses_New cases', 'OPD_Mental Schizophrenia and other psychoses_Old cases'],
    'OPD_NCD_Asthma': ['OPD_NCD_Asthma_New Cases', 'OPD_NCD_Asthma_Old cases'],
    'OPD_NCD_Renal failure': ['OPD_NCD_Renal failure_New cases', 'OPD_NCD_Renal failure_Old cases'],
    'OPD_NCD_Other chronic kidney diseases': ['OPD_NCD_Other chronic kidney diseases_New cases', 'OPD_NCD_Other chronic kidney diseases_Old cases'],
    'OPD_NCD_Other Cardiovascular diseases': ['OPD_NCD_Other Cardiovascular diseases Cardiovascular_New cases', 'OPD_NCD_Other Cardiovascular diseases Cardiovascular_Old cases'],
    'OPD_NCD_Rheumatic heart disease': ['OPD_NCD_Rheumatic heart disease_New cases', 'OPD_NCD_Rheumatic heart disease_Old cases'],
    'OPD_NCD_Cardiomyopathies': ['OPD_NCD_Cardiomyopathies_New cases', 'OPD_NCD_Cardiomyopathies_Old cases'],
    'OPD_NCD_Congenital heart disease': ['OPD_NCD_Congenital heart disease_New cases', 'OPD_NCD_Congenital heart disease_Old cases'],
    'OPD_NCD_Coronary artery disease': ['OPD_NCD_Coronary artery disease Cardiovascular_New cases', 'OPD_NCD_Coronary artery disease Cardiovascular_Old cases'],
    'OPD_NCD_Deep veinus thrombosis': ['OPD_NCD_Deep veinus thrombosis_New cases', 'OPD_NCD_Deep veinus thrombosis_Old cases'],
    'OPD_NCD_Heart failure': ['OPD_NCD_Heart failure_New cases', 'OPD_NCD_Heart failure_Old cases'],
    'OPD_NCD_Pericardial disease': ['OPD_NCD_Pericardial disease Cardiovascular_New cases', 'OPD_NCD_Pericardial disease Cardiovascular_Old cases'],
    'OPD_Mental Anxiety disorders': ['OPD_Mental Anxiety disorders_New cases', 'OPD_Mental Anxiety disorders_Old cases'],
    'OPD_Mental Somatoform disorders': ['OPD_Mental Somatoform disorders_New cases', 'OPD_Mental Somatoform disorders_Old cases'],
    'OPD_NCD_Other endocrine and metabolic diseases': ['OPD_NCD_Other endocrine and metabolic diseases_New cases', 'OPD_NCD_Other endocrine and metabolic diseases_Old cases'],
    'OPD_Mental Bipolar disorders': ['OPD_Mental Bipolar disorders_New cases', 'OPD_Mental Bipolar disorders_Old Cases'],
    'OPD_NCD_Pericardial disease': ['OPD_NCD_Pericardial disease Cardiovascular_New cases', 'OPD_NCD_Pericardial disease Cardiovascular_Old cases'],
    'OPD_Mental Epilepsy': ['OPD_Mental Epilepsy_New cases', 'OPD_Mental Epilepsy_Old Cases'],
    'MH_Acute and transient psychotic disorders': ['MH_Acute and transient psychotic disorders_New cases_OPD', 'MH_Acute and transient psychotic disorders_Old cases_OPD']
}

def clean_disease_names(df1):
    
    for disease, cases_types in disease_cases_mapping.items():
        #facility.loc[facility['DISEASES'].isin(cases_types), 'DISEASES'] = disease
        # Combine new and old cases Sect_IDs, then find unique Sect_IDs for each
        all_cases_ids = df1[df1['DISEASES'].isin(cases_types)]['Sect_ID'].unique()
        
        for sect_id in all_cases_ids:
            # Filter data for the Sect_ID and relevant disease cases
            common_data = df1[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(cases_types)]
            
            # Assuming you want to sum CASES for each disease category and recalculate Burden(%)
            total_cases = common_data['CASES_per_Sector'].sum()
            population = df1[df1['Sect_ID'] == sect_id]['Population_per_Sector'].iloc[0]  # Assuming population does not vary within Sect_ID
            burden=((total_cases/population)*100).round(2)
            # Update df1 for the current Sect_ID and disease types
            #df1.loc[(df1['Sect_ID'] == sect_id) & (df1['DISEASES'].str.endswith('New cases'))|(df1['DISEASES'].str.endswith('New Cases'))|(df1['DISEASES'].str.endswith('New cases_OPD')), 'New CASES'] = common_data['CASES']
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(cases_types), 'CASES_per_Sector'] = total_cases
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(cases_types), 'Disease_Burden(%)_per_Sector'] = burden
            #df1=df1[(~df1['DISEASES'].str.endswith('Old cases'))&(~df1['DISEASES'].str.endswith('Old Cases'))&(~df1['DISEASES'].str.endswith('Old cases_OPD'))]
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(cases_types), 'DISEASES'] = disease
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(['Dental caries_OPD']), 'DISEASES'] = 'Dental caries'
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(['OPD_Severe Malaria cases']), 'DISEASES'] = 'OPD_Severe Malaria'
            df1.loc[(df1['Sect_ID'] == sect_id) & df1['DISEASES'].isin(['Eye problem other_OPDDH']), 'DISEASES'] = 'Eye problem other'
            
    df1['DISEASES'] = df1['DISEASES'].str.split('_New cases').str[0]
    df1['DISEASES'] = df1['DISEASES'].str.split('_New Cases').str[0]
    df1['DISEASES'] = df1['DISEASES'].str.split('OPD New cases').str[0]
    df1['DISEASES'] = df1['DISEASES'].str.split('_new').str[0]
    df1['DISEASES'] = df1['DISEASES'].str.split('_Old cases').str[0]
    df1['DISEASES'] = df1['DISEASES'].str.split('_OPDnew').str[0]
    df1.loc[df1['DISEASES'].isin(['Dental caries_OPD']), 'DISEASES'] = 'Dental caries'
    df1.loc[df1['DISEASES'].isin(['OPD_Severe Malaria cases']), 'DISEASES'] = 'OPD_Severe Malaria'
    df1.loc[df1['DISEASES'].isin(['Eye problem other_OPDDH']), 'DISEASES'] = 'Eye problem other'
    df1.loc[df1['DISEASES'].isin(['OPD_NCD_Pericardial disease Cardiovascular']), 'DISEASES'] = 'Eye problem other'
    return df1.drop_duplicates()

def main():
    """
    The main function for processing MOH Data data.

    Reads data from a specified Excel file, consolidates disease information, cleans the data,
    and adds a 'FACILITY TYPE' column based on facility information. The resulting data is returned.

    Returns:
    pandas.DataFrame: Processed moh_data that will be exported as csv file.
    """
    # upload and read the data with pandas.read_excel() and applied the previous functions to process the data
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/diseases_data.csv'
    
    xls_obj = read_data(file_path)
    
    df1=clean_disease_names(xls_obj)
    

    return df1

if __name__ == "__main__":
    df1 = main()
    df1.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/diseases.csv',index=False)