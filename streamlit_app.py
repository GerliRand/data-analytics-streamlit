import streamlit as st
import pandas as pd 

@st.cache_data
def load_espoo():
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/c7f38065-41cf-4ec1-a1bb-774ac3029e4e", encoding="latin-1")

@st.cache_data
def load_compare():
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/b8c0c3b2-d37b-4e4d-be4f-671e1f2a48c2", encoding="latin-1")

df_espoo = load_espoo()
df_compare = load_compare()

# Data cleaning function
def clean_data(df):
    # Fixed: ï»¿"Month" to Month
    df.columns = df.columns.str.replace('ï»¿', '').str.replace('"', '').str.strip()
    #st.write(df.columns) # checking column names

    # Convert Month column from format (2010M01) to datetime
    df["Month"] = df["Month"].str.replace('*','')
    df["Month"] = pd.to_datetime(df["Month"], format="%YM%m")

    # Create new columns year and month 
    df["Year"] = df["Month"].dt.year
    df["Month_num"] = df["Month"].dt.month
    
    return df

df_espoo = clean_data(df_espoo)
df_compare = clean_data(df_compare)

# Checking datatypes and missing values
#st.write(df_espoo.dtypes)
#st.write(df_espoo.isna().sum())


st.markdown('''
# Monthly hotel capacity and nights spent by municipality 01.2010 - 02.2026

## Data in Espoo
            ''')

st.dataframe(df_espoo) # show the data (table)

st.markdown('### Hotel statistics in Espoo (01.2010 - 02.2026)')
option = st.selectbox(
    "Select metric: ",
    ("Espoo Domestic nights",
     "Espoo Foreign nights",
     "Espoo Nights spent",
     "Espoo Average price per night")
)

# Checking the selected value
#st.write("Choosed: ", option)

# Line chart
st.line_chart(df_espoo, x="Month", y=option)

st.divider()

# Bar chart 
st.markdown('### Yearly total nights in Espoo 01.2010 - 12.2025')
# Counting total nights per year
yearly = df_espoo.groupby("Year")["Espoo Nights spent"].sum()
yearly = yearly[yearly.index != 2026] # remove 2026 data, because it is incomplete 
st.bar_chart(yearly)