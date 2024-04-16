import pandas as pd, numpy as np

def read_data(file_path):
    """
    Reads data from an Excel file and returns an ExcelFile object.

    Parameters:
    - file_path (str): The path to the csv file.

    Returns:
    - csv file: An csv object containing the data from the specified file.
    """
    rwd_pop_2022 =pd.read_csv(file_path)
    return rwd_pop_2022

def rename_2022_columns_and_merge(rwd_pop_2022,rwd_pop_2020):
    rwd_pop_2022_df=rwd_pop_2022.rename(columns={'Population_per_Sector':'2022_Population_per_Sector','Male_per_Sector':'2022_Male_per_Sector','Female_per_Sector':'2022_Female_per_Sector'})[['Province', 'District', 'Sector', 'Sect_ID','2022_Population_per_Sector','2022_Male_per_Sector','2022_Female_per_Sector']]
    merge_pop=rwd_pop_2022_df.merge(rwd_pop_2020,on=['Province','District','Sector'])
    return merge_pop

def add_2022_urbanization(merge_pop):
    
   
    merge_pop_df = merge_pop.assign(
    
    _2022_Urban_Population_per_Sector=lambda x: np.where(
        x['2020_Urban_Population_per_Sector'] != '-', 
        x['2022_Population_per_Sector'], 
        '-'
    ),
   
    _2022_Urban_Male_per_Sector=lambda x: np.where(
        x['2020_Urban_Male_per_Sector'] != '-', 
        x['2022_Male_per_Sector'], 
        '-'
    ),
     _2022_Urban_Female_per_Sector=lambda x: np.where(
        x['2020_Urban_Female_per_Sector'] != '-', 
        x['2022_Female_per_Sector'], 
        '-'
    ),
   
   _2022_Rural_Population_per_Sector=lambda x: np.where(
        x['2020_Urban_Population_per_Sector'] == '-', 
        x['2022_Population_per_Sector'], 
        '-'
    ),
   
    _2022_Rural_Male_per_Sector=lambda x: np.where(
        x['2020_Urban_Male_per_Sector'] == '-', 
        x['2022_Male_per_Sector'], 
        '-'
    ),
     _2022_Rural_Female_per_Sector=lambda x: np.where(
        x['2020_Urban_Female_per_Sector'] == '-', 
        x['2022_Female_per_Sector'], 
        '-'  
    
))

    
    return merge_pop_df

def main():
    file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/'
    rwd_pop_2022 =read_data(file_path +'2022_Population_Rwanda.csv')
    rwd_pop_2020 =read_data(file_path +'2020_Population_Rwanda.csv')
    
    merge_pop=rename_2022_columns_and_merge(rwd_pop_2022,rwd_pop_2020)
    merge_pop_df=add_2022_urbanization(merge_pop)
    return merge_pop_df

if __name__ == "__main__":
    merge_pop_df = main()
merge_pop_df.to_excel('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/2020__2022_Rwanda_Population.xlsx',index=False)
