#IMPORT LIBARIES
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import yfinance as yf

str.title('S&P 500 STOCK PRIC APP')

st.write("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, matplotlib, yfinance
* **Data source:** [Wikipedia](https://www.wikipedia.org/).
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Parameters')

# WEB SCRAPPING OF S&P 500 data with Pandas
@st.cache

def read_data():
    url =   'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url,header=0)
    df = html[0]
    return df

df = read_data()
sector = df.groupby('GICS Sector')


# SIDEBAR SELECTIONS SECTION
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

#FILTERING DATA
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)


#DOWNLOAD S&P 500 DATA
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f' <a href = "data:file/csv; base64,{b64}" download = "SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color = 'skyblue', alpha = 0.3)
    plt.plot(df.Date, df.Close, color = 'skyblue', alpha = 0.8)
    plt.xticks(rotation=90)
    plt.title('symbol', fontweight = 'bold')
    plt.xlabel('Date',fontweight = 'bold')
    plt.ylabel('Closing Proice', fontweight = 'bold')
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 5)


if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
