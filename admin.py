import pandas as pd
import streamlit as st
from io import StringIO


st.title("Admin Page")

df=pd.read_csv("/Users/jaykataria/Desktop/Data hack/jay/pages/LawyerInfo.csv")

st.dataframe(df)

st.subheader("Load more data")

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
    dataframe = pd.read_csv(uploaded_file)
    newdf=pd.concat([df, dataframe])
    newdf.to_csv("LawyerInfo.csv")