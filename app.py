import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

@st.cache_data
def read_data():
    data = pd.read_parquet("shnik_mini.parquet")
    return data

def get_statistics(data, anun, azganun=None, haeranun=None):
    new_data = data[data["anun"] == anun]
    if azganun:
        new_data = new_data[new_data["azganun"] == azganun]
    if haeranun:
        new_data = new_data[new_data["haeranun"] == haeranun]

    return new_data



def get_plots(new_data):
    d = new_data.groupby(["marz"])["anun"].count().reset_index()
    d=d.sort_values(by="anun",ascending=True)
    plot_bar = px.bar(y=d["marz"].tolist(),x=d["anun"].tolist(),orientation='h')
    plot_bar=plot_bar.update_layout(xaxis_title="count",yaxis_title="marz")

    d=new_data.groupby(["tari"])["anun"].count()
    plot_bar2 = px.bar(x=d.index,y=d.values)
    plot_bar2 = plot_bar2.update_layout(xaxis_title="Year born",yaxis_title="count")

    return plot_bar, plot_bar2


data = read_data()

form = st.form(key="my_form")
anun = form.text_input("anun","")
azganun = form.text_input("azganun","")
haeranun = form.text_input("haeranun","")
submit_button = form.form_submit_button(label="Submit")

if submit_button:
    if anun:
        new_data = get_statistics(data, anun, azganun, haeranun)

        st.write(new_data.head(100))

        plot_1, plot_2 = get_plots(new_data)
        st.plotly_chart(plot_1)
        st.plotly_chart(plot_2)

