import pandas as pd
from clean_shapefile import clean_sector # call this function to match sector name with the shape file sector
# define data path
rbc_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/RBC/MEMMS extract 19072022 RBC.xlsx'

# read the data
def readrbc_data(rbc_file_path):
    return pd.read_excel(rbc_file_path,sheet_name='MEMMS extract 19072021')

# process the data
def process_rbc_data(rbc_data):
    # Step 1: Select and rename columns
    rbc1 = rbc_data[['Type name_en', 'Subcategory', 'Status', 'Facility name_en',' ID', 'Catchment area', 'Facility type', 'Province', 'District', 'Sector']]
    rbc1 = rbc1.rename(columns={' ID':'ID','Type name_en': 'RBC_EQUIPMENT', 'Facility name_en': 'HEALTH FACILITY', 'Subcategory': 'EQUIPMENTS'})
    # Step 2: Modify 'District' column
    rbc1['District'] = rbc1['District'].str.split(' ').str[0]

    # Step 3: Update 'Province' column
    rbc1.loc[rbc1.Province != 'Kigali City', 'Province'] += 'ern Province'

    # Step 4: Capitalize 'Sector' column
    rbc1['Sector'] = rbc1['Sector'].str.capitalize()

    # Step 5: Select and reorder columns
    rbc2 = rbc1[['Province', 'District', 'Sector', 'ID','HEALTH FACILITY', 'Catchment area', 'Facility type', 'RBC_EQUIPMENT', 'EQUIPMENTS', 'Status']]

    return rbc2

def main():
    rbc_data=readrbc_data(rbc_file_path)
    rbc2=process_rbc_data(rbc_data)
    rbc3=clean_sector(rbc2)
    return rbc3
if __name__ == "__main__":
    rbc3 = main()


