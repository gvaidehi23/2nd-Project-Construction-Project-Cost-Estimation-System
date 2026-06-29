import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.title("Construction Project Cost Estimation System")

# Load model pipeline
pipe = pickle.load(open("pipe.pkl", "rb"))

# Load dataset
df = pd.read_csv("final_data.csv")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        180deg,
        #081B33,
        #0F4C81,
        #1B75BB
    );
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #04152D,
        #063970
    );
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>

/* Text input, number input */
[data-baseweb="base-input"] {
    background: black !important;
}

[data-baseweb="base-input"] input {
    background: black !important;
    color: white !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: black !important;
    color: white !important;
}

/* Dropdown */
[data-baseweb="popover"] {
    background: black !important;
}

ul[role="listbox"] {
    background: black !important;
}

li[role="option"] {
    background: black !important;
    color: white !important;
}

            .stNumberInput button {
    background-color: black !important;
    color: white !important;
    border: none !important;
}

.stNumberInput button svg {
    fill: white !important;
}
            


</style>
""", unsafe_allow_html=True)
#st.button("Predict Cost")

# button color change
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #87CEEB;
    color: #000080;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)



# Extract unique values for dropdowns
project_ids = sorted(df["project_id"].unique())
item_idS = sorted(df['item_id'].unique())
categories = sorted(df["category"].unique())


# Sidebar Inputs

project_id = st.sidebar.selectbox("Select Project ID",project_ids)
item_id = st.sidebar.selectbox('Select Item ID:', item_idS)
category = st.sidebar.selectbox("Select Category",categories)
sub_categories = sorted(df[df["category"] == category]["sub_category"].unique())
sub_category = st.sidebar.selectbox("Select Sub Category",sub_categories)

items = sorted(df[(df["category"] == category) &(df["sub_category"] == sub_category)]["item_name"].unique())
item_name = st.sidebar.selectbox( "Select Item Name",items)


# Automatically select unit according to item name
unit = df[(df["category"] == category) &(df["sub_category"] == sub_category) &(df["item_name"] == item_name)]["unit"].iloc[0]
# Display unit (user cannot change it)
st.sidebar.write("Unit:", unit)


quantity = st.sidebar.number_input("Enter Quantity",value=100.0,step=1.0)
rate_per_unit = st.sidebar.number_input("Enter Rate per Unit (INR)",value=1000.0,step=100.0)


# Prediction

if st.sidebar.button("Predict Cost"):
    st.write("### Selected Details")
    st.write(f"Project ID: {project_id}")
    st.write(f"Category: {category}")
    st.write(f"Sub Category: {sub_category}")
    st.write(f"Item Name: {item_name}")
    st.write(f"Unit: {unit}")
    st.write(f"Quantity: {quantity}")
    st.write(f"Rate per Unit: ₹{rate_per_unit}")
   


    # Creating input dataframe
    myinput = [[item_id,project_id,category,sub_category,item_name,unit,quantity,rate_per_unit]]           # item_id (if not used in model)                                                                                               
    columns = ['item_id','project_id','category','sub_category','item_name','unit','quantity','rate_per_unit_inr']
    myinput = pd.DataFrame(myinput,columns=columns)
    result = pipe.predict(myinput)

   


    if result[0] < 0:
        st.write("Sorry, predicted cost is negative. Please check inputs.")

    else:
       st.markdown(
       f"""
       <div style="
       background-color: #87CEFA;
       color: #000080;
       padding: 15px;
       border-radius: 10px;
       font-size: 22px;
       font-weight: bold;
       text-align: center;
       ">
       Total Predicted Project Cost: ₹{round(result[0],2):,.2f}
       </div>
       """,
       unsafe_allow_html=True
       )


    st.markdown(
    """
    <br>
    <p style="color: white; font-size: 15px; font-weight: normal;">
        Note: This model considers multiple project factors and associated expenditures while estimating cost.
    </p>
    """,
    unsafe_allow_html=True
    )



























































