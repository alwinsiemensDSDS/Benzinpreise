import streamlit as st
import tankstellen_api as tanker_api
import pandas as pd
import plotly.express as px
import st_aggrid

st.set_page_config(page_title="Spritpreise in ihrer Nähe!", page_icon="⛽", layout="wide")
st.title("Spritpreise in ihrer Nähe!⛽")

# User Input Form
sprit_sorte = st.selectbox("", tanker_api.sprittypes.keys())
radius = st.number_input("Umkreis (km)", min_value=0, max_value=25, step=1, value = 3)
place = st.text_input("Ortsbeschreibung", placeholder="Lemgo")
dataframe_loaded = False

# retrieve dataframe with stations from api
if(place != "" and radius > 0.0 and radius < 25.0 and sprit_sorte != ""):
    dataframe = tanker_api.get_all_tankstellen_in_specific_radius_json(place, radius, sprit_sorte)
    if(not dataframe.empty):
        dataframe = dataframe.dropna()
        dataframe_loaded = True
    else:
        st.error("Error: Leider wurden keine Daten gefunden! Bitte ändern sie ihre Eingaben.")

if(dataframe_loaded):
    # Key Values from dataframe
    with st.container():
        lowestprice_colum, nearestprice_colum = st.columns(2)
        with lowestprice_colum:
            
            lowest_price_dataset:pd.DataFrame = dataframe[dataframe["price"] == dataframe["price"].min()]
            
            st.info("Günstigster Preis")

            price_formatted = "{:.2f} €".format(lowest_price_dataset["price"].values[0])

            st.metric(label=lowest_price_dataset["name"].values[0],value=price_formatted)
            st.dataframe(lowest_price_dataset[["name", "place", "street", "isOpen"]], hide_index=True)

        with nearestprice_colum:

            nearest_price_dataset:pd.DataFrame = dataframe[dataframe["dist"] == dataframe["dist"].min()]

            st.info("Nächster Preis")

            price_formatted = "{:.2f} €".format(nearest_price_dataset["price"].values[0])
            st.metric(label=nearest_price_dataset["name"].values[0],value=price_formatted, delta=None)
            st.dataframe(nearest_price_dataset[["name", "place", "street", "isOpen"]], hide_index=True)

    # Visuals from Dataframe
    with st.container():
        st.write("---")

        st.info("Kartenansicht")

        map = px.scatter_mapbox(dataframe, lat = "lat", lon = "lng", hover_name= "name", color="price", size= "price", color_continuous_scale="oxy", zoom=10, hover_data = ["street"])
        map.update_layout(mapbox_style="open-street-map", autosize=True)
        map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(map)

        st.write("---")

        st.info("Tabellenansicht")
        st.write("Klicke die einzelnen Spalten an um zu filtern.")

        tableview = dataframe.drop(columns=["id", "lat", "lng"])

        st_aggrid.AgGrid(tableview, columns_auto_size_mode=st_aggrid.ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)
else:
    st.info("Bitte geben Sie ihre gewünschten Parameter ein.")