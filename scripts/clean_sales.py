import pandas as pd
# define the path of the data

sales_file_path='C:/Users/HP ELITEBOOK/Documents/VIEBEG_MEDICAL/research/data/manual/Viebeg Financial Data/VIEBEG_Sales analysis dataset.xlsx'

# read sales data

def read_sales(sales_file_path):
    return pd.read_excel(sales_file_path, sheet_name='2018-2023sales by products')

def clean_sales_data(financial):
    sales=(financial[['Products name','Customer','EQUIPMENTS', 'Date', 'Qty', 'currency', 'Location_prov', 'Location_distr','Location_sec', 'type','Customer_id']]
        .loc[(financial['currency'] == 'RWF')]
        .loc[(financial['Customer'] != 'VIEBEG DRC')]
        .rename(columns={'Customer_id':'ID','Customer':'HEALTH FACILITY','Location_prov':'Province','Location_distr':'District','Location_sec':'Sector','type':'FACILITY TYPE'})
        .dropna(subset=['EQUIPMENTS'])
        .assign(District=lambda x: x['District'].str.capitalize(), Sector=lambda x: x['Sector'].str.capitalize(), Province=lambda x: x['Province'].str.split(' ').str[0].str.capitalize()+' '+ x['Province'].str.split(' ').str[1].str.capitalize())
    )

    return sales

def main():
    financial=read_sales(sales_file_path)
    sales=clean_sales_data(financial)

    return sales

if __name__== "__main__":
    sales=main()