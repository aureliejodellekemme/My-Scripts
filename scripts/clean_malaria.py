import pandas as pd
import numpy as np
from datetime import datetime as dt

def main():
    """
    The main function for processing MOH Data data.

    Reads data from a specified Excel file, consolidates disease information, cleans the data,
    and adds a 'FACILITY TYPE' column based on facility information. The resulting data is returned.

    Returns:
    pandas.DataFrame: Processed moh_data that will be exported as csv file.
    """
    # upload and read the data with pandas.read_excel() and applied the previous functions to process the data
    file_path = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/MOH_OPD_HOSP/New Data/Malaria cases received in OPD.xlsx'
    file_path_moh = 'C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Facilities/facility_data.csv'
    from clean_chronic_diseases import read_data
    xls_obj = read_data(file_path)
    from clean_general_OPD_diseases import consolidate_opd_diseases
    disease_data = consolidate_opd_diseases(xls_obj,'5')
    from clean_chronic_diseases import clean_data
    cleaned_data = clean_data(disease_data)
    
    facility_data = pd.read_csv(file_path_moh)
    from clean_MOH import add_facility_type
    moh_data = add_facility_type(cleaned_data, facility_data)
    from clean_general_OPD_diseases import disease_count
    moh_data1=disease_count(moh_data,'5')
    from clean_shapefile import clean_sector
    moh_data2=clean_sector(moh_data1)

    return moh_data2

if __name__ == "__main__":
    moh_data2 = main()
    moh_data2.to_csv('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Diseases/Malaria.csv',index=False)
 