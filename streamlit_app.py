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

st.markdown("### Hotel statistics in Espoo (01.2010 - 02.2026)")
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

st.text("Conclusion: Overall, the numer of overnight stays has shown a steady increasing trend since 2010. " \
"However a sharp decline occured in April 2020 because the Covid-19 pandemic. At the same time, " \
"hotel prices dropped in May 2020 and remained at a lower level until araound July 2021.")

st.divider()

# Bar chart 
st.markdown("### Yearly total nights in Espoo (01.2010 - 12.2025)")
# Counting total nights per year
yearly = df_espoo.groupby("Year")["Espoo Nights spent"].sum()
yearly = yearly[yearly.index != 2026] # remove 2026 data, because it is incomplete 
st.bar_chart(yearly)

st.text("Conclusion: The highest number of overnight stays in Espoo can be observed in 2022, 2023 and 2025." \
" In 2020, there was a significant decrease because the Covid-19 pandemic. However the number of overnight stays" \
"recovered remarkably quickly in the following years.")

st.divider()

# Line chart: Espoo Domestic vs Foreign
st.markdown("### In Espoo: Domestic VS Foregin (01.2010 - 02.2026)")
st.line_chart(df_espoo, x="Month", y=["Espoo Domestic nights", "Espoo Foreign nights"]) 

st.text("Conclusion: There are fewer foreign overnight stays compared to domestic ones. " \
"A clear drop can be seen in April 2020 due to the Covid-19 pandemic. After that, foreign overnight" \
"stays have not recovered as quickly as domestic ones. In addition, there is a clear seasonal pattern," \
"with higher numbers of overnight stays during the summer months.")

st.divider()

# Line chart: Compare Vantaa and Espoo prices
st.markdown("### Comparison: Espoo VS Vantaa (Hotels average price per night)")
st.line_chart(df_compare, x="Month", y=["Espoo Average price per night", "Vantaa Average price per night"])

st.text("Conclusion: The Covid-19 in 2020 appears to have had a stronger impact on hotel prices in Espoo, " \
"where prices dropped more significantly compared to Vantaa. There is also a noticeable peak in prices " \
"in Espoo around June 2025. In addition, a seasonal pattern can be observed, as prices tend to decrease during " \
"July each year. Additionally, it is interesting to observe that hotel prices in Vantaa are generally higher " \
"than in Espoo, which was somewhat unexpected.")

# Download CSV data
@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")

csv = convert_for_download(df_compare)

st.download_button(
    label="Download comparison data as CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    icon=":material/download:",
)