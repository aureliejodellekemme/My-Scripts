import geopandas as gpd
import pandas as pd
import numpy as np

#define data path

file_path=r"C:\Users\HP ELITEBOOK\Documents\VIEBEG_MEDICAL\research\data\manual\2018_shapefiles\rwa_sector\Sector.shp"

def read_data(file_path):
    return gpd.read_file(file_path)

def clean_data(data):
    data1= (data
     .rename(columns={'Name':'Sector'})
     .replace('Iburengerazuba','Western Province')
     .drop([4,107,412],axis=0)
     .drop(['Prov_ID','Dist_ID'],axis=1)
     .assign(Sect_ID=lambda x: x['Sect_ID'].astype(np.int32))
    )
    return data1

#,'Gashari':'Gishari','Gishari':'Gishari (Karongi District)'
def clean_sector(data1):
    sector_replacements = {
        'Bugesera': {'Nyarugenge':'Nyarugenge (Bugesera District)'},
        'Gatsibo': {'Kageyo':'Kageyo (Gatsibo District)', 'Murambi':'Murambi (Gatsibo District)',
                    'Remera':'Remera (Gatsibo District)', 'Rugarama':'Rugarama (Gatsibo District)', 'Rwimbogo':'Rwimbogo (Gatsibo District)'},
        'Kayonza':{'Mukarange':'Mukarange (Kayonza District)','Murundi':'Murundi (Kayonza District)'},
        'Kirehe':{'Kigarama':'Kigarama (Kirehe  District)','Nyamugali':'Nyamugari'},
        'Ngoma':{'Murama':'Murama (Ngoma  District)','Remera':'Remera (Ngoma  District)'},
        'Nyagatare': {'Karama':'Karama (Nyagatare District)','Rukomo':'Rukomo (Nyagatare District)','Musheli':'Musheri','Mimuli':'Mimuri'},
        'Rwamagana':{'Gishari':'Gishari (Rwamagana District)','Musha':'Musha (Rwamagana  District)','Nyakaliro':'Nyakariro','Gishali':'Gishari','Musheri':'Musheli'},
        'Burera':{'Cyanika':'Cyanika (Burera  District)'},
        'Gicumbi':{'Kageyo':'Kageyo (Gicumbi  District)','Muko':'Muko (Gicumbi  District)','Nyamiyaga':'Nyamiyaga (Gicumbi  District)','Rukomo':'Rukomo (Gicumbi  District)'},
        'Musanze':{'Nyange':'Nyange (Musanze District)','Remera':'Remera (Musanze  District)'},
        'Rulindo':{'Kinihira':'Kinihira (Rulindo District)','KINIHIRA':'Kinihira (Rulindo District)','Murambi':'Murambi (Rulindo District)',
                   'Tumba':'Tumba (Rulindo District)','Ngoma':'Ngoma (Rulindo District)','shyrongi':'Shyorongi'},
        'Karongi':{'Murambi':'Murambi (Karongi District)','Gashari':'Gashaki (Karongi District)'},
        'Huye':{'Karama':'Karama (Huye District)','Kigoma':'Kigoma (Huye District)','Ngoma':'Ngoma (Huye District)','Tumba':'Tumba (Huye District)'},
        'Kamonyi':{'Karama':'Karama (Kamonyi District)','Rugalika':'Rugarika'},
        'Nyamagabe':{'Mbazi':'Mbazi (Nyamagabe District)','Kibirizi':'Kibirizi (Nyamagabe District)','Cyanika':'Cyanika (Nyamagabe District)'},
        'Nyaruguru':{'Muganza':'Muganza (Nyaruguru District)','Nyagisozi':'Nyagisozi (Nyaruguru District)','Ngoma':'Ngoma (Nyaruguru District)'},
        'Ruhango':{'Kinazi':'Kinazi (Ruhango  District)','Kinihira':'Kinihira (Ruhango District)','Kabagali':'Kabagari'},
        'Rusizi':{'Muganza':'Muganza (Rusizi District)'},
        'Rutsiro':{'Mukura':'Mukura (Rutsiro  District)','Ruhango':'Ruhango (Rutsiro  District)'},
        'Gakenke':{'Nemba':'Nemba (Gakenke  District)'},
        'Burera':{'Nemba':'Nemba (Burera  District)','Rusarabuye':'Rusarabuge'},
        'Gisagara':{'Kibirizi':'Kibirizi (Gisagara  District)','Mukingo':'Mukingo (Gisagara  District)','Musha':'Musha (Gisagara  District)'},
        'Ngororero':{'Kageyo':'Kageyo (Ngororero  District)'},
        'Nyanza':{'Kibilizi':'Kibirizi','Mukingo':'Mukingo (Nyanza  District)','Busasamana':'Busasamana (Nyanza  District)'},
        'Rubavu':{'Nyakiriba':'Nyakiliba','Busasamana':'Busasamana (Rubavu  District)'}

    }
    # apply the process to the data to edit the sector name to be the same format as sector shape file
    for district, replacements in sector_replacements.items():
        
        mask = data1['District'] == district
        data1.loc[mask, 'Sector'] = data1.loc[mask, 'Sector'].replace(replacements)
    
    data1['Sector'] = data1['Sector'].str.capitalize()                        

    return data1

def main():
    data=read_data(file_path)
    data1=clean_data(data)
    sector_shape_file=clean_sector(data1)

    return sector_shape_file

if __name__ == "__main__":
    sector_shape_file = main()

#sector_shape_file.to_file('C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Sector shapefile/clean_Sector.shp')