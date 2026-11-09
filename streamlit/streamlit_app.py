import streamlit as st
import streamlit_folium as stf
import pandas as pd
import geopandas as gpd
import folium
from h3 import h3

def load_data():
    uploaded_file = st.file_uploader("Upload a GeoJSON or CSV file", type=["geojson", "csv"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "geojson":
            df = gpd.read_file(uploaded_file)
        elif file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        return df

def plot_h3_data(df, column, zoom):
    h3_set = set(df[column])
    m = folium.Map()

    for h3_index in h3_set:
        bounds = h3.h3_to_geo_boundary(h3_index, resolution=zoom)
        polygon = folium.GeoJson(bounds, style_function=lambda x: {'fillColor': 'blue', 'color': 'black'})
        polygon.add_to(m)

    m.fit_bounds(m.get_bounds())
    return m

def main():
    st.title("H3 Streamlit App")

    df = load_data()

    if df is not None:
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select a layer to visualize", columns)

        zoom_level = st.slider("Select H3 zoom level", min_value=0, max_value=15, value=8)

        aggregation_options = ["Sum", "Mean", "Count"]
        selected_aggregation = st.selectbox("Select aggregation method", aggregation_options)

        if st.button("Plot"):
            plot = plot_h3_data(df, selected_column, zoom_level)
            stf.st_folium(plot, width=800, height=600)

if __name__ == "__main__":
    main()