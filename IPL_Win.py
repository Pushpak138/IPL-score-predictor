import streamlit as st
import pandas as pd
import pickle

# load model
model = pickle.load(open('model .pkl','rb'))

# teams list
teams = [
    'Mumbai Indians','Chennai Super Kings','Royal Challengers Bangalore',
    'Kolkata Knight Riders','Delhi Capitals','Punjab Kings',
    'Rajasthan Royals','Sunrisers Hyderabad'
]

venues = [
    'Wankhede Stadium','M Chinnaswamy Stadium','Eden Gardens',
    'Feroz Shah Kotla','MA Chidambaram Stadium',
    'Rajiv Gandhi International Stadium','Sawai Mansingh Stadium',
    'Punjab Cricket Association Stadium'
]

st.title("🏏 IPL Score Predictor")

# inputs
batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)
venue = st.selectbox("Venue", venues)

current_score = st.number_input("Current Score", min_value=0)
overs = st.number_input("Overs", min_value=0.0, max_value=20.0, step=0.1)
wickets = st.number_input("Wickets", min_value=0, max_value=10)

# prediction
if st.button("Predict Score"):

    # validation check
    if batting_team == bowling_team:
        st.error("❌ You cannot select the same team for batting and bowling!")
    
    else:
        balls_bowled = int(overs * 6)

        input_df = pd.DataFrame({
            'batting_team':[batting_team],
            'bowling_team':[bowling_team],
            'venue':[venue],
            'current_score':[current_score],
            'balls_bowled':[balls_bowled],
            'wickets':[wickets]
        })

        input_df = pd.get_dummies(input_df)

        model_columns = model.feature_names_in_
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        prediction = model.predict(input_df)

        st.success(f"🏆 Predicted Final Score: {int(prediction[0])}")
