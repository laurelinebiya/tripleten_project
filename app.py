import streamlit as st
import pandas as pd
import plotly.express as px

df=pd.read_csv('kc_house_data.csv')
df=df.drop(df.columns[0], axis=1)

st.header('Housing Market in King County, USA')

st.write('###### Filter data below to see listings by zipcode:')

unique_zipcodes=df['zipcode'].unique()

chosen_unique_zipcode=st.selectbox('Select zipcode',sorted(unique_zipcodes))


yr_built_min, yr_built_max =int(df['yr_built'].min()),int(df['yr_built'].max())

year_range = st.slider("Choose construction year:",value=(yr_built_min, yr_built_max),min_value=yr_built_min, max_value=yr_built_max)

actual_range = list(range(year_range[0],year_range[1]+1))

filtered_df=df[(df['zipcode']==chosen_unique_zipcode) & (df.yr_built.isin(list(actual_range)))]

st.table(filtered_df.head(50))

st.header('Price analysis')
st.write('###### Elements that influence house prices. We will check how distibution of price varies depending on bedrooms, bathrooms, floors and presence of areas with a good view.')

list_for_hist=['bedrooms','bathrooms','floors','view']
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)
fig1 = px.histogram(df, x="price", color=choice_for_hist)

fig1.update_layout(
title="<b> Split of price by {}</b>".format(choice_for_hist))
st.plotly_chart(fig1)

df['age']=2023-df['yr_built']
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'
df['age_category']=  df['age'].apply(age_category)

st.write("###### Now we can check how price is affected by square footage for living, square footage of the lot or above square footage.")

list_for_scatter=['sqft_living','sqft_lot','sqft_above']
choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig2 = px.scatter(df, x="price", y=choice_for_scatter, color="age_category",
                  hover_data=['yr_built'])

fig2.update_layout(
title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)