import pandas as pd, numpy as np,geopandas as gpd,warnings
import streamlit as st
import folium
warnings.filterwarnings('ignore')
from folium import plugins
from folium.plugins import MeasureControl
from streamlit_folium import folium_static, st_folium
from datetime import datetime as dt
#st.cache_data.clear()
st.cache_data() 
def load_data():
    with open("clean_HF_location.py") as f:
        exec(f.read())
    return final_data

def main():
    final_data=load_data()
    #page_bg_img = '''
    #<style>
    #body {
    #background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    #background-size: cover;
     #}
     #</style>
     #'''

    # st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("Mapping Healthcare Services in Rwanda")
    #st.caption("Visualizing Services Care in Rwanda")
    # Create a dropdown menu to select the disease
    selected_disease = st.sidebar.selectbox('Select a Disease', final_data['DISEASES'].unique())
    #st.write(final_data.columns )
    data=final_data[final_data['DISEASES'] == selected_disease]
    metric_title = f'{selected_disease} Prevalence in Rwanda'
    rwd_per_disease_pr = (((data['NOMBER OF CASES'].sum()) / data['Population'].sum()) * 100).round(2)
    st.metric(metric_title, rwd_per_disease_pr)
    map = folium.Map(location=[-1.9437057, 29.8805778], zoom_start=9, control_scale=True)
    plugins.Fullscreen(position='topright').add_to(map)
    # Create a GeoJson layer for the sectors
    sectors_layer = folium.FeatureGroup(name='Sectors')
    folium.GeoJson(
    data,
    name='Sectors',
    style_function=lambda feature: {
        'color': 'black',
        'fillColor': 'white',
        'weight': 1,
        'fillOpacity': 0.5
    }
    ).add_to(sectors_layer)
    sectors_layer.add_to(map)

    # Create a search control for sector search
    search = plugins.Search(
        layer=sectors_layer,
        geom_type='polygon',
        search_zoom=13,
        placeholder='Search a sector',
        collapsed=False,
        search_label='Sector'
    )

    # Add the Search control to the map
    map.add_child(search)
    # Create a choropleth map for the selected disease
    choropleth = folium.Choropleth(
        geo_data=data,
        data=data,
        columns=['Sect_ID', 'Disease_Prevalence(%)'],
        key_on='feature.properties.Sect_ID',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight=True,
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
        legend_name=f'{selected_disease} Prevalence (%)'
    )

    # Create a GeoJsonTooltip for the choropleth
    tooltip = folium.GeoJsonTooltip(
        fields=['District', 'Sector','Population','NOMBER OF CASES',
       ],
        aliases=['District', 'Sector','Population','NOMBER OF CASES',
       ],
        localize=True
    )
    choropleth.geojson.add_child(tooltip)
    choropleth.add_to(map)
    folium_static(map,width=600,height=500)

if __name__ == "__main__":
    main()


