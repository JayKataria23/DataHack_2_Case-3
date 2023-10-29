import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Lawyer Dashboard", page_icon="/Users/jaykataria/Desktop/Data hack/jay/lawyantra.png", layout="wide")

df=pd.read_csv("/Users/jaykataria/Desktop/Data hack/jay/pages/lawyer_matrix_data.csv")
df=df.iloc[:, 1:]

st.sidebar.header("Please Filter Here:")
city=st.sidebar.multiselect(
    "Select the City:",
    options=df["city"].unique(),
    default=df["city"].unique()
)
jurisdiction=st.sidebar.multiselect(
    "Select the Jurisdiction level:",
    options=df["jur"].unique(),
    default=df["jur"].unique()
)
demographic=st.sidebar.multiselect(
    "Select your Demographic:",
    options=df["demo"].unique(),
    default=df["demo"].unique()
)

df_selection = df.query(
    "city == @city & jur == @jurisdiction & demo == @demographic"
)

st.title("Lawyantra Lawyer Dashboard")
st.markdown("##")
st.dataframe(df_selection)

average_rating = round(df_selection["feed"].mean())
star_rating = ":star:"*int(average_rating)
average_rate = round(df_selection["rate"].mean())

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Price per hour USD:")
    st.subheader(f"US $ {average_rate}")

st.markdown("---")

li=[]
for i in df_selection.columns[13:]:
    li.append(df_selection.groupby(i)["exp"].max()[1])
