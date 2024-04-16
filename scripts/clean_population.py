import pandas as pd, numpy as np,geopandas as gpd,streamlit as st
xls_obj=pd.ExcelFile('C:/Users/Olive/Documents/viebeg/research/data/manual/PHC5-2022_Main_Indicators.xlsx')
# dpm={}
# sheet_list=xls_obj.sheet_names[96:]
# for sheet in sheet_list:
#     dpm[sheet]=pd.read_excel(xls_obj,sheet_name=sheet)
# Cleaning Provinces sheet
pop_Kgl=( pd.read_excel(xls_obj,sheet_name='Table 96')
    .drop(['Table 96: City of Kigali population distribution by district and sector','Unnamed: 5','Unnamed: 6','Unnamed: 7'],axis=1)
    .drop(0)
)
st.write(pop_Kgl.head())
pop_South=(pd.read_excel(xls_obj,sheet_name='Table 97')
    .drop(['Table 97: Southern Province population distribution by district and sector','Unnamed: 5','Unnamed: 6','Unnamed: 7'],axis=1)
    .drop(0)
)  
pop_West=(pd.read_excel(xls_obj,sheet_name='Table 98')
    .drop(['Table 98: Western Province population distribution by district and sector','Unnamed: 5','Unnamed: 6','Unnamed: 7'],axis=1)
    .drop(0)
)  
pop_North=(pd.read_excel(xls_obj,sheet_name='Table 99')
    .drop(['Table 99: Northern Province population distribution by district and sector','Unnamed: 5','Unnamed: 6','Unnamed: 7'],axis=1)
    .drop(0)
)  
pop_East=(pd.read_excel(xls_obj,sheet_name='Table 100')
    .drop(['Table 100: Eastern Province population distribution by district and sector','Unnamed: 5','Unnamed: 6','Unnamed: 7'],axis=1)
    .drop(0)
) 
# Appending all Provinces in a single sheet
pop_rwd=pop_Kgl.append([pop_South,pop_West,pop_North,pop_East])
# Restructuring the data by Province, District, and Sector
pop_rwd=pop_rwd.reset_index(drop=True)
index_row_to_drop=pop_rwd[pop_rwd['Unnamed: 1'].isin([np.nan, 'City of Kigali','Southern province','Western Province','Northern Province','Eastern Province'])].index
remain=[index_row_to_drop[1]+1,index_row_to_drop[3]+1,index_row_to_drop[5]+1,index_row_to_drop[7]+1,index_row_to_drop[9]+1,13,29,
    40,53,67,82,97,115,125,138,151,167,181,194,207,221,240,256,276,296,312,330,352,369,384,399,412,425,440]
lis_index=list(index_row_to_drop)+list(remain)
Rwd_pop_df=( pop_rwd.copy()
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
    .rename(columns={'Unnamed: 2':'Population','Unnamed: 3':'Male','Unnamed: 4':'Female'})
    .drop(lis_index)
    .drop('Unnamed: 1',axis=1)

)
Rwd_pop_df=Rwd_pop_df[Rwd_pop_df.columns[-3:].tolist() + Rwd_pop_df.columns[:-3].tolist()]
# Grouping data by Sector
Population_rwd=Rwd_pop_df.groupby(by=['Province','District','Sector']).sum().reset_index()
# Remove spaces in values
Population_rwd['Sector']=Population_rwd['Sector'].str.strip() 

