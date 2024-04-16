with open("clean_equipment_disease_matching.py") as f:
    exec(f.read())
moh_data=pd.read_csv(r'C:\Users\Olive\Documents\viebeg\research\data\manual\moh_data.csv')
#Extracting 2022
moh_data=moh_data[moh_data['Year']==2022]
#counting number of diseases cases per sector
moh_data['NOMBER OF CASES']=moh_data.groupby(by=['Province','District','Sector','DISEASES'])['NOMBER OF CASES'].transform('sum')
merg_equip_diseas=moh_data.merge(disease_equip_data,on='DISEASES')
# counting health facility
merg_equip_diseas['# Of HEALTH FACILITY'] = merg_equip_diseas.groupby(['Province','District','Sector'])['HEALTH FACILITY'].transform('nunique')
# county type of facility
cross_tab = pd.crosstab([merg_equip_diseas['Province'], merg_equip_diseas['District'], merg_equip_diseas['Sector'],merg_equip_diseas['HEALTH FACILITY']],merg_equip_diseas['FACILITY TYPE'],values=merg_equip_diseas['FACILITY TYPE'],
    aggfunc=pd.Series.unique)
cross_tabS=cross_tab.copy()
cross_tabS.columns = [f'# Of {col}' for col in cross_tabS.columns]
cross_tabS=cross_tabS.reset_index()
cross_tabS=cross_tabS.groupby(['Province','District','Sector']).count()
cross_tabS=cross_tabS.fillna(0).astype(int)

cross_tab.columns = [f'# Of {col} Per HF' for col in cross_tab.columns]
cross_tabHF=cross_tab.reset_index()
#print(cross_tabHF)
cross_tabHF=cross_tabHF.groupby(['Province','District','Sector','HEALTH FACILITY']).count()
cross_tabHF=cross_tabHF.fillna(0).astype(int)
cross_tabS=cross_tabS.drop('HEALTH FACILITY',axis=1)
MOH_equip_deseas = merg_equip_diseas.merge(cross_tabS, left_on=['Province','District','Sector'], right_index=True)
MOH_equip_deseas = MOH_equip_deseas.merge(cross_tabHF,left_on=['Province','District','Sector','HEALTH FACILITY'], right_index=True)