import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Repayment Calculator")

st.write("##Input data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
intrest_rate = col2.number_input("Intrest Rate(in %)" , min_value=0.0,value=5.5)
loan_term = col2.number_input("Loan Term(In Years)",min_value=0,value=30)

#calculate the requirments 
loan_amount = home_value - deposit
monthly_intrest_rate = (intrest_rate /100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    *(monthly_intrest_rate *(1+ monthly_intrest_rate)**number_of_payments)
    /((1+ monthly_intrest_rate)**number_of_payments - 1)
)


#display the repayment
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1,col2,col3 =st.columns(3)
col1.metric(label="Monthly Repayment",value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayment",value=f"${total_payments:,.0f}")
col3.metric(label="Total Intrest",value=f"${total_interest:,.0f}")


#create a dataframe with the payment schedule
schedule=[]
Remaining_balance = loan_amount
for i in range(1,number_of_payments + 1):
    intrest_payment = Remaining_balance * monthly_intrest_rate
    principal_paymnet = monthly_payment - intrest_payment
    Remaining_balance -=principal_paymnet
    year = math.ceil(i/12)
    schedule.append(
        [
        i,
        monthly_payment,
        principal_paymnet,
        intrest_payment,
        Remaining_balance,
        year,
        ]
    )
df = pd.DataFrame(
    schedule,
    columns=["month","Payment","Principal","Intrest","Remaining Balance","Year"],
)

#dispaly data from chart
st.write("##Payment Schedule")
payments_df = df[["Year","Remaining Balance"]].groupby("Year").min()
st.bar_chart(payments_df)

