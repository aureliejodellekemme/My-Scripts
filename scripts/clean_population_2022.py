import pandas as pd
import numpy as np
import geopandas as gpd


def read_data(file_path,sector_shape_file_path):
    """
    Reads data from an Excel file and returns an ExcelFile object.

    Parameters:
    - file_path (str): The path to the Excel file.
    - sector_shape_file_path (str): File path to the shapefile (GeoDataFrame) containing geographic sector shapes.

    Returns:
    - ExcelFile: An ExcelFile object containing the data from the specified file.
     - gpd.GeoDataFrame: Geographic sector shapes loaded from the shapefile, including columns: 'Province', 'District', 'Sector', 'Sect_ID'.
    """
    xls_obj = pd.ExcelFile(file_path)
    sector_shape_file=gpd.read_file(sector_shape_file_path)
    return xls_obj,sector_shape_file[['Province','District','Sector','Sect_ID']]

def read_population_data(xls_obj,sheet_name,col):
    """
    Reads population data from an ExcelFile object, drops specified columns, and removes unnecessary rows.

    Parameters:
    - xls_obj (ExcelFile): The ExcelFile object containing the data.
    - sheet_name (str): The name of the sheet containing population data.
    - col (str): The column to drop from the data.

    Returns:
    - DataFrame: A DataFrame containing cleaned population data.
    """
    return pd.read_excel(xls_obj, sheet_name=sheet_name).drop([col,'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'], axis=1).drop(0)

def create_district_list(pop_rwd):
    """
    Creates a list of indices corresponding to districts in population data.

    Parameters:
    - pop_rwd (DataFrame): The DataFrame containing population data.

    Returns:
    - list: A list of indices corresponding to districts in the population data.
    """
    index_row_to_drop=pop_rwd[pop_rwd['Unnamed: 1'].isin([np.nan, 'City of Kigali','Southern province','Western Province','Northern Province','Eastern Province'])].index
    remain=[index_row_to_drop[1]+1,index_row_to_drop[3]+1,index_row_to_drop[5]+1,index_row_to_drop[7]+1,index_row_to_drop[9]+1,13,29,
    40,53,67,82,97,115,125,138,151,167,181,194,207,221,240,256,276,296,312,330,352,369,384,399,412,425,440]
    lis_index=list(index_row_to_drop)+list(remain)
    return lis_index

def create_population_dataframe(pop_rwd,pop_Kgl,pop_South,pop_West,pop_North,pop_East, lis_index):
    """
    Creates a DataFrame for population data with additional columns for Province, District, and Sector.

    Parameters:
    - pop_rwd (DataFrame): The DataFrame containing raw population data.
    - pop_Kgl (DataFrame): DataFrame containing population data for Kigali City.
    - pop_South (DataFrame): DataFrame containing population data for Southern Province.
    - pop_West (DataFrame): DataFrame containing population data for Western Province.
    - pop_North (DataFrame): DataFrame containing population data for Northern Province.
    - pop_East (DataFrame): DataFrame containing population data for Eastern Province.
    - lis_index (list): List of indices to drop from the population data.

    Returns:
    - DataFrame: A DataFrame with columns for Province, District, Sector, Population, Male, and Female.
    """
    Rwd_pop_df=( pop_rwd
    .assign(Province=lambda x:['Kigali City'] * pop_Kgl.shape[0] + ['Southern Province'] * pop_South.shape[0] + ['Western Province'] * pop_West.shape[0]+['Northern Province']*pop_North.shape[0]+['Eastern Province']*pop_East.shape[0])
    .assign(District=['Nyarugenge'] * 13 + ['Gasabo'] * 16 + ['Kicukiro'] *11+['Nyanza']*13+['Gisagara']*14+
            ['Nyaruguru']*15+['Huye']*15+['Nyamagabe']*18+['Ruhango']*10+['Muhanga']*13+['Kamonyi']*13+['Karongi']*16+['Rutsiro']*14+['Rubavu']*13+['Nyabihu']*13+
            ['Ngororero']*14+['Rusizi']*19+['Nyamasheke']*16+['Rulindo']*20+['Gakenke']*20+['Musanze']*16+['Burera']*18+['Gicumbi']*22+
            ['Rwamagana']*17+['Nyagatare']*15+['Gatsibo']*15+['Kayonza']*13+['Kirehe']*13+['Ngoma']*15+['Bugesera']*16)
    .assign(Sector=pop_rwd.loc[0:12, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[13:28, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[29:39, 'Unnamed: 1'].values.tolist()+
        pop_rwd.loc[40:52, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[53:66, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[67:81, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[82:96, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[97:114, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[115:124, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[125:137, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[138:150, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[151:166, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[167:180, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[181:193, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[194:206, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[207:220, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[221:239, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[240:255, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[256:275, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[276:295, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[296:311, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[312:329, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[330:351, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[352:368, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[369:383, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[384:398, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[399:411, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[412:424, 'Unnamed: 1'].values.tolist()+pop_rwd.loc[425:439, 'Unnamed: 1'].values.tolist()+
            pop_rwd.loc[440:455, 'Unnamed: 1'].values.tolist())
    .rename(columns={'Unnamed: 2':'Population_per_Sector','Unnamed: 3':'Male_per_Sector','Unnamed: 4':'Female_per_Sector'})
    .drop(lis_index)
    .drop('Unnamed: 1',axis=1)

    )
    Rwd_pop_df=Rwd_pop_df[Rwd_pop_df.columns[-3:].tolist() + Rwd_pop_df.columns[:-3].tolist()]
    return Rwd_pop_df

def remove_spaces(Rwd_pop_df):
    """
    Removes leading and trailing spaces from the 'Sector' column of the DataFrame.

    Parameters:
    - Population_rwd (DataFrame): The DataFrame containing population data.

    Returns:
    - DataFrame: The DataFrame with leading and trailing spaces removed from the 'Sector' column.
    """
    Rwd_pop_df['Sector'] = Rwd_pop_df['Sector'].str.strip()
    return Rwd_pop_df

def group_population_data(Rwd_pop_df):
    """
    Groups population data by Province, District, and Sector, summing up the numerical columns.

    Parameters:
    - Rwd_pop_df (DataFrame): The DataFrame containing population data.

    Returns:
    - DataFrame: A grouped DataFrame with total population, male, and female counts for each sector, District, and Province.
    """
    Rwd_pop_df=Rwd_pop_df.groupby(by=['Province', 'District', 'Sector']).sum().reset_index()
    Rwd_pop_df['Population_per_District']=Rwd_pop_df.groupby(by=['Province', 'District'])['Population_per_Sector'].transform('sum')
    Rwd_pop_df['Male_per_District']=Rwd_pop_df.groupby(by=['Province', 'District'])['Male_per_Sector'].transform('sum')
    Rwd_pop_df['Female_per_District']=Rwd_pop_df.groupby(by=['Province', 'District'])['Female_per_Sector'].transform('sum')
    Rwd_pop_df['Population_per_Province']=Rwd_pop_df.groupby(by=['Province'])['Population_per_Sector'].transform('sum')
    Rwd_pop_df['Male_per_Province']=Rwd_pop_df.groupby(by=['Province'])['Male_per_Sector'].transform('sum')
    Rwd_pop_df['Female_per_Province']=Rwd_pop_df.groupby(by=['Province'])['Female_per_Sector'].transform('sum')
    return Rwd_pop_df

def adding_sector_id(Population_rwd,sector_shape_file):
    """
    Add sector identification (Sect_ID) to the diseases DataFrame by merging with sector_shape_file.

    Parameters:
    - Population_rwd (pd.DataFrame): DataFrame containing disease information, with columns 'Province', 'District', 'Sector', and other relevant data.
    - sector_shape_file (gpd.GeoDataFrame): GeoDataFrame containing geographic sector shapes, with columns 'Province', 'District', 'Sector', 'Sect_ID'.

    Returns:
    dataframe: Merged GeoDataFrame with disease information and sector identification (Sect_ID), based on common columns 'Province', 'District', 'Sector'.
    """
    return Population_rwd.merge(sector_shape_file,on=['Province','District','Sector'],how='left')


def main():
    """
    Reads population data from an Excel file, processes and combines it for various provinces, districts, and sectors.

    Returns:
    - DataFrame: A processed DataFrame containing grouped population data by Province, District, and Sector.
    """

    from clean_shapefile import clean_sector

    # Define the data path
    file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/PHC5-2022_Main_Indicators.xlsx'
    sector_shape_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Sector shapefile/clean_Sector.shp'
    xls_obj ,sector_shape_file= read_data(file_path,sector_shape_file_path)
    
    pop_Kgl = read_population_data(xls_obj,'Table 96','Table 96: City of Kigali population distribution by district and sector')
    pop_South = read_population_data(xls_obj,'Table 97','Table 97: Southern Province population distribution by district and sector')
    pop_West = read_population_data(xls_obj,'Table 98','Table 98: Western Province population distribution by district and sector')
    pop_North = read_population_data(xls_obj,'Table 99','Table 99: Northern Province population distribution by district and sector')
    pop_East = read_population_data(xls_obj,'Table 100','Table 100: Eastern Province population distribution by district and sector')
    
    #pop_rwd = pd.concat([pop_Kgl,pop_South, pop_West, pop_North, pop_East])

    pop_rwd = pop_rwd.reset_index(drop=True)

    lis_index = create_district_list(pop_rwd)
   
    Rwd_pop_df = create_population_dataframe(pop_rwd,pop_Kgl,pop_South,pop_West,pop_North,pop_East, lis_index)

    Rwd_pop_df = remove_spaces(Rwd_pop_df)

    Rwd_pop_df=clean_sector(Rwd_pop_df)
    
    Population_rwd = group_population_data(Rwd_pop_df)
    #Population_rwd=adding_sector_id(Population_rwd,sector_shape_file)

    return Population_rwd

if __name__ == "__main__":
    Population_rwd = main()
Population_rwd.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/2022_Population_Rwanda.csv',index=False)
