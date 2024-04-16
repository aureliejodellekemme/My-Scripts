import pandas as pd

def read_data(file_path):
    """
    Reads data from an Excel file and returns an ExcelFile object.

    Parameters:
    - file_path (str): The path to the Excel file.

    Returns:
    - ExcelFile: An ExcelFile object containing the data from the specified file.
    """
    xls_obj = pd.read_excel(file_path)
    return xls_obj


old_val=('Kibirizi', 'Mimuli' ,'Gishari', 'Musheli', 'Nyakariro','Kabagari', 'Rugalika', 'Nyakiliba','Nyamugali', 'Rusarabuge')
new_val=('Kibilizi', 'Mimuri','Gishali','Musheri', 'Nyakaliro','Kabagali', 'Rugarika', 'Nyakiriba','Nyamugari','Rusarabuye')

def create_population_dataframe(xls_obj):
   
    rwd_pop_2020 = (xls_obj
        .drop([0,1,2,3,4,5,6,7,8,9,20,21,37,38,49,50,51,52,53,64,65,79,80,95,96,111,112,
            130,131,141,142,155,156,169,170,171,172,173,187,188,202,203,216,217,230,231,
            245,246,265,266,282,283,284,285,286,304,305,325,326,342,343,361,362,384,385,386,387,388,
            403,404,419,420,435,436,449,450,463,464,479,480])
        .assign(
        Province=(
            ['Kigali City'] * 35 +
            ['Southern Province'] * 101 +
            ['Western Province'] * 96 +
            ['Northern Province'] * 89 +
            ['Eastern Province'] * 95
        ))
        
        .assign(
        District=(
            ['Nyarugenge'] * 10 + ['Gasabo'] * 15 + ['Kicukiro'] * 10 + ['Nyanza'] * 10 + ['Gisagara'] * 13 +
            ['Nyaruguru'] * 14 + ['Huye'] * 14 + ['Nyamagabe'] * 17 + ['Ruhango'] * 9 + ['Muhanga'] * 12 + ['Kamonyi'] * 12 +
            ['Karongi'] * 13 + ['Rutsiro'] * 13 + ['Rubavu'] * 12 + ['Nyabihu'] * 12 + ['Ngororero'] * 13 + ['Rusizi'] * 18 +
            ['Nyamasheke'] * 15 + ['Rulindo'] * 17 + ['Gakenke'] * 19 + ['Musanze'] * 15 + ['Burera'] * 17 + ['Gicumbi'] * 21 +
            ['Rwamagana'] * 14 + ['Nyagatare'] * 14 + ['Gatsibo'] * 14 + ['Kayonza'] * 12 + ['Kirehe'] * 12 + ['Ngoma'] * 14 +
            ['Bugesera'] * 15
        ))
                    
        .assign(Sector=lambda x: x['Unnamed: 0'].str.split(' ').str[1].str.strip())
        .rename(columns={'Table 2.1: Distribution of the resident population by Province, District and Sector and by Urban/rural areas and Sex':'2020_Population_per_Sector',
                        'Unnamed: 2':'2020_Male_per_Sector', 'Unnamed: 3':'2020_Female_per_Sector', 'Unnamed: 4':'2020_Urban_Population_per_Sector', 'Unnamed: 5':'2020_Urban_Male_per_Sector',
                        'Unnamed: 6':'2020_Urban_Female_per_Sector', 'Unnamed: 7':'2020_Rural_Population_per_Sector', 'Unnamed: 8':'2020_Rural_Male_per_Sector',
                        'Unnamed: 9':'2020_Rural_Female_per_Sector' })
        .drop('Unnamed: 0',axis=1)[['Province','District', 'Sector','2020_Population_per_Sector', '2020_Male_per_Sector',
                                    '2020_Female_per_Sector', '2020_Urban_Population_per_Sector', '2020_Urban_Male_per_Sector',
                                    '2020_Urban_Female_per_Sector', '2020_Rural_Population_per_Sector',
                                    '2020_Rural_Male_per_Sector', '2020_Rural_Female_per_Sector']]
    )

    return rwd_pop_2020



def main():
    file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/'
    from clean_shapefile import clean_sector
    xls_obj=read_data(file_path+'2020_Population Rwanda Sector.xlsx')
    rwd_pop_2020=create_population_dataframe(xls_obj)
    rwd_pop_2020_df=clean_sector(rwd_pop_2020)

    return rwd_pop_2020_df

if __name__ == "__main__":
    rwd_pop_2020_df = main()
rwd_pop_2020_df.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Population/2020_Population_Rwanda.csv',index=False)
