with open("merge_moh_equip_disease.py") as f:
    exec(f.read())
with open("clean_population.py") as f:
    exec(f.read())
moh_equip_disease_pop=MOH_equip_deseas.merge(Population_rwd,on=['Province','District','Sector'],how='left').reset_index()
# Converting number of cases to numeric
moh_equip_disease_pop['NOMBER OF CASES']=pd.to_numeric(moh_equip_disease_pop['NOMBER OF CASES'])
#Computing the Prevalence
moh_equip_disease_pop=moh_equip_disease_pop[moh_equip_disease_pop['Year']==2022]
moh_equip_disease_pop['NOMBER OF CASES']=moh_equip_disease_pop.groupby(by=['Province','District','Sector','DISEASES'])['NOMBER OF CASES'].transform('sum')
moh_equip_disease_pop['Disease_Prevalence(%)']=(moh_equip_disease_pop['NOMBER OF CASES']/moh_equip_disease_pop['Population']*100).round(2)
