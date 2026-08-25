# Importing
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from datetime import date

# --- REBRANDING: Page Config ---
st.set_page_config(page_title="SkyFare Predictor | Ankit Kumar", page_icon="✈️", layout="centered")

# Loading the Model
with open("model/best_model.pkl","rb") as file:
  best_model=pickle.load(file)
  
# Styling
st.markdown("""
            <style>
              h4 
              {
                  margin-bottom: 0px;
                  padding-bottom: 0px;
              }
              
              h6
              {
                margin-top:15px;
                padding-bottom: 0px;
                font-size:20px;
              }
              
              .stSlider > div > div > div > div 
              {
                   background: #00ADB5;
              }
              .stSlider > div > div > div > div > div
              {
                  background-color: #00ADB5;
              }
              
        
              .stSelectbox > div > div > div > div 
              {
                  font-weight: bold;
              }
              
              div.stButton > button , div.stButton > button:focus , div.stButton > button:active 
              {
                  background-color: #00ADB5;
                  color: white;
                  border: none;
                  outline:none;
              }
              div.stButton > button:hover
              {
                  background-color: white;
                  color: #00ADB5; 
                  border: none;
                  outline:none;
              }
              
              .stSpinner > div > div 
              {
                  color: white;
              }
            </style>
            """,unsafe_allow_html=True)
    
    
# --- REBRANDING: Custom Title and Developer Info ---
st.markdown("""
              <h1 style="text-align:center; color:white;">✈️ SkyFare Predictor</h1>
              <p style="text-align:center; color:#00ADB5; font-size:18px;">Built by <b>Ankit Kumar</b> | B.Tech CSE (Bioinformatics), VIT</p>
              <hr>
            """,unsafe_allow_html=True)

# Getting User Input
c1,c2=st.columns(2)
def input():
  with c1:
    st.markdown("""
                  <h4 style="color:#00ADB5;">Airline</h4>
                """,unsafe_allow_html=True)
    Airline=st.selectbox("",["IndiGo", "Air India", "Jet Airways", "SpiceJet", "Multiple carriers", "GoAir", "Vistara", "Air Asia", "Vistara Premium economy", "Jet Airways Business", "Multiple carriers Premium economy", "Trujet"])
    
    
    st.markdown("""
                  <h4 style="color:#00ADB5;">Origin</h4>
                """,unsafe_allow_html=True) 
    Source=st.selectbox("",["Banglore", "Kolkata", "Delhi", "Chennai", "Mumbai"])
  
    st.markdown("""
                  <h4 style="color:#00ADB5;">Ticket Type</h4>
                """,unsafe_allow_html=True)
    Passengers_Type=st.selectbox("",["Economy","Business"])
    
    st.markdown("""
                  <h4 style="color:#00ADB5;">Additional Info</h4>
                """,unsafe_allow_html=True)
    Additional_Info=st.selectbox("",["No info", "In-flight meal not included", "No check-in baggage included", "1 Short layover", "No Info", "1 Long layover", "Change airports", "Business class", "Red-eye flight", "2 Long layover"])
  
  with c2:
    st.markdown("""
                  <h4 style="color:#00ADB5;">Booking Date</h4>
                """,unsafe_allow_html=True)
    Date=st.date_input("",min_value=date.today())
    
    st.markdown("""
                  <h4 style="color:#00ADB5;">Destination</h4>
                """,unsafe_allow_html=True) 
    Destination=st.selectbox("",["New Delhi", "Banglore", "Cochin", "Kolkata", "Delhi", "Hyderabad"])
    
    column1,column2=st.columns(2)
    with column1:
      st.markdown("""
                  <h6 style="color:#00ADB5;">Adults</h4>
                """,unsafe_allow_html=True)
      Adults=st.number_input("",min_value=0,max_value=700,step=1)
    with column2:
      st.markdown("""
                  <h6 style="color:#00ADB5;">Children</h4>
                """,unsafe_allow_html=True)
      Children=st.number_input("",min_value=0,max_value=600,step=1)
    
    st.markdown("""
                  <h4 style="color:#00ADB5;">Max No. of Stops Preferred</h4>
                """,unsafe_allow_html=True)
    Total_Stops=st.number_input("",min_value=0,max_value=4,step=1)
    
        

  data={
          "Airline" : Airline,
          "Source" : Source,
          "Destination" : Destination,
          "Total_Stops" : Total_Stops,
          "Additional_Info" : Additional_Info,
          "Date" : Date.day,
          "Month" : Date.month,
          "Year" : Date.year,
       }
  return data,(Adults,Children),Passengers_Type

user_data,Total_pass,type=input()

# Mapping
air_rep={'IndiGo': 0, 'Air India': 1, 'Jet Airways': 2, 'SpiceJet': 3, 'Multiple carriers': 4, 'GoAir': 5, 'Vistara': 6, 'Air Asia': 7, 'Vistara Premium economy': 8, 'Jet Airways Business': 9, 'Multiple carriers Premium economy': 10, 'Trujet': 11}
sou_rep={'Banglore': 0, 'Kolkata': 1, 'Delhi': 2, 'Chennai': 3, 'Mumbai': 4}
des_rep={'New Delhi': 0, 'Banglore': 1, 'Cochin': 2, 'Kolkata': 3, 'Delhi': 4, 'Hyderabad': 5}
add_rep={'No info': 0, 'In-flight meal not included': 1, 'No check-in baggage included': 2, '1 Short layover': 3, 'No Info': 4, '1 Long layover': 5, 'Change airports': 6, 'Business class': 7, 'Red-eye flight': 8, '2 Long layover': 9}

user_data["Airline"]=air_rep[user_data["Airline"]]
user_data["Source"]=sou_rep[user_data["Source"]]
user_data["Destination"]=des_rep[user_data["Destination"]]
user_data["Additional_Info"]=add_rep[user_data["Additional_Info"]]

# Creating a DataFrame for Doing Prediction
df_user=pd.DataFrame()
for key,value in user_data.items():
  df_user[key]=pd.Series(value)

# Predicting
col1,col2=st.columns(2)
with col1:
  st.markdown("""
                    <br>
                """,unsafe_allow_html=True)
  if st.button("Predict",icon="🛩️"):
    with col2:
      with st.spinner("Ready to Fly✈️"):
        time.sleep(2)
      predict=best_model.predict(df_user)[0]
      
      # Business or Economy
      
      if type=="Business":
        flight_fare=(Total_pass[0]*(predict+(predict*0.25)))+(Total_pass[1]*(predict+(predict*0.25)))
      elif type=="Economy":
        flight_fare=(Total_pass[0]*predict)+(Total_pass[1]*predict)
      else:
        flight_fare=0

      # No. of Days b/w Booking and Travel
      
      today=date.today()
      book_date=date(int(df_user["Year"].iloc[0]), int(df_user["Month"].iloc[0]), int(df_user["Date"].iloc[0]))
      diff=(book_date-today).days
      
      if diff<1:
        flight_fare*=2

      st.markdown("""
                      <h4 style="color:#00ADB5;margin-bottom: 0px;padding-bottom: 0px;">Predicted Flight Fare<br></h4>
                  """,unsafe_allow_html=True)
      if flight_fare!=0:
        st.balloons()
        st.success(f"✈✈✈ Rs. {flight_fare:.2f} ✈✈✈")
      else:
        st.error("Please Enter Valid Input 😊")

# Visualising
df=pd.read_csv("train/Data_Train.csv")
st.markdown("""
                      <center><h3 style="color:white;margin-bottom: 0px;padding-bottom: 0px;"><br>You can Compare the Flight Price<br> among Different Airlines</h3></center><br><br>
                  """,unsafe_allow_html=True)
st.bar_chart(df,x="Airline",y="Price",color="#00ADB5",x_label="Airlines",y_label="Price")
