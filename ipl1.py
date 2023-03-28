import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
model=pickle.load(open('model_.pkl','rb'))
st.title(':red[IPL WIN PREDICTOR] :cricket_bat_and_ball::tada::tada:')

teams=['Mumbai Indians','Chennai Super Kings','Delhi Capitals','Sunrisers Hyderabad','Kolkata Knight Riders','Punjab Kings','Royal Challengers Bangalore','Rajasthan Royals']
venue=['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Bengaluru', 'Indore', 'Dubai', 'Sharjah']
col1,col2=st.columns(2)
with col1:
    batting_team=st.selectbox('Select Batting Team',sorted(teams))
with col2:
    bowling_team=st.selectbox('Select Bowling Team',sorted(teams))
venue=st.selectbox('Select the city the match is being held',venue)
first_score=st.number_input('Select First Innings Score',min_value=0,step=1)
col3,col4=st.columns(2)
with col3:
    runs_scored=st.number_input('Select the runs scored by the batting team',min_value=0,step=1)
with col4:
    wickets_fallen=st.number_input('Select the number of wickets fallen',min_value=0,max_value=10,step=1)
col5,col6=st.columns(2)
with col5:
    over=st.number_input('Select the number of overs bowled',min_value=0,max_value=19,step=1)
with col6:
    balls=st.number_input('Select the number of balls bowled in the over',min_value=0,max_value=6,step=1)
if runs_scored==first_score:
    st.header('Match Drawn')
elif runs_scored>first_score:
    st.header(batting_team+" won by "+str(10-wickets_fallen)+" wickets")
elif over==19 and balls==6 and runs_scored<first_score:
    st.header(bowling_team+" won by "+str(first_score-runs_scored)+" runs")
elif wickets_fallen==10:
    st.header(bowling_team+" won by "+str(first_score-runs_scored)+" runs")
elif batting_team==bowling_team:
    st.write('Batting and bowling team cannot be the same')
elif over==0 and balls==0:
    st.write('Innings has not started yet')
else:
    if first_score>0 and first_score<=300:
        
        if st.button('Predict'):
            balls_bowled=(over*6)+balls
            current_run_rate=(runs_scored*6)/balls_bowled
            target=first_score+1
            required_runs=target-runs_scored
            balls_left=120-balls_bowled
            req_run_rate=(required_runs*6)/balls_left
            arr=np.array([venue,batting_team,bowling_team,current_run_rate,target,required_runs,balls_left,req_run_rate,wickets_fallen])
            result=model.predict_proba([arr])
            bowl_prob=result[0][0]
            bat_prob=result[0][1]

            st.header(batting_team+"-"+str(round(bat_prob*100,1))+"%")
            st.header(bowling_team+"-"+str(round(bowl_prob*100,1))+"%")
        
    else:
        st.write('Please fill all the details according to situations feasible in a T20 match.')
