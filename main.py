# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta


# Import Data
df = pd.read_excel('data/Online Retail.xlsx', 
                   dtype = {'StockCode':str,'CustomerID':str })         

# Sidebar Controls for Dynamic Dashboard
with st.sidebar:
    st.subheader('Settings')

    # Filtering Data based on Periods
    rad_periods = st.radio('Choose Periods', 
             options= ['Last Week', 'Last Month', 'Last Quarter',
                       'Last Year', 'All Data'])
    
    match(rad_periods):

        case 'Last Week':
            st.write('Last Week Selected')
            last_date = df['InvoiceDate'].max()
            first_date = last_date - timedelta(7)
            df = df.loc[df['InvoiceDate'].between(first_date, last_date)]


        case 'Last Month':
            st.write('Last Month Selected')
        case 'Last Quarter':
            st.write('Last Quarter Selected')
        case 'Last Year':
            st.write('Last Year Selected')
        case _:
            st.write('All Data Selected')

    
st.header('Retail Dashboard')



# Main Dashboard Window
cols1 = st.columns(3)

with cols1[0]:
    st.write('Top 10 quantity')
    fig = plt.figure()
    ax = fig.add_subplot()
    quantity = df['StockCode'].value_counts().head(10)
    ax.bar(quantity.index,quantity.values)

    ax.set_xlabel('Quantity')
    ax.set_ylabel('InvoiceDate')
    ax.set_title('Top 10 Quantity')
    plt.xticks(rotation = 90)
    st.write(fig)

with cols1[1]:
    st.write('Top 10 Price')
    fig = plt.figure()
    ax = fig.add_subplot()
    UnitPrice = df['StockCode'].value_counts().head(10)
    ax.bar(UnitPrice.index, UnitPrice.values)

    ax.set_xlabel('StockCode')
    ax.set_ylabel('UnitPrice')
    ax.set_title('Top 10 Price')
    plt.xticks(rotation = 90)
    for index, value in enumerate(UnitPrice.values):
        ax.text(index -0.3,value+0.2, value)
    st.write(fig)

with cols1[2]:
    st.write('Top 10 Customer')
    fig = plt.figure()
    ax = fig.add_subplot()
    Customer = df['CustomerID'].value_counts().head(10)
    ax.bar(Customer.index.astype(str), Customer.values)

    ax.set_xlabel('CustomerID')
    ax.set_ylabel('count')
    ax.set_title('Top 10 Customer')
    plt.xticks(rotation=90)
    for index, value  in enumerate(Customer.values):
        ax.text(index-0.3, value +0.4, value)
    st.write(fig)


cols2 = st.columns([0.5, 0.4 ])
with cols2[0]:
    st.write('Top 10 months')
    df['month'] = df['InvoiceDate'].dt.month
    df.head()
    
    fig = plt.figure()
    ax = fig.add_subplot()

    unitprice = df['UnitPrice'].groupby(df['month']).sum()
    ax.bar(unitprice.index, unitprice.values)

    ax.set_xlabel('Month')
    ax.set_ylabel('Price')
    ax.set_title('Monthly Price')
    plt.xticks(rotation = 90)
    st.write(fig)

with cols2[1]:
    st.write('Top Countries')
    
    grouped_df_countriees = df.groupby('Country')['UnitPrice'].sum().reset_index()
    top_5_countriees =  grouped_df_countriees.nlargest(6,'UnitPrice')
    total_other_countriees = grouped_df_countriees['UnitPrice'].sum()-top_5_countriees['UnitPrice'].sum()
    other_df_countriees =  pd.DataFrame({'Country':['Others'], 'UnitPrice':[total_other_countriees]})

    df_countries = pd.concat([top_5_countriees, other_df_countriees ]).reset_index(drop =True)
    df_countries.drop(0,axis=0,inplace = True )

    fig = plt.figure(dpi=120)
    ax = fig.add_subplot()

    ax.pie(df_countries['UnitPrice'], autopct='%1.0f%%', 
           labels = df_countries['Country'])

    ax.set_title('Top countries')
    st.write(fig)


    





