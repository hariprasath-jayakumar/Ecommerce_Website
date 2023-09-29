#Importing required Lib

import streamlit as st
import csv
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image

# Sidebar navigation
with st.sidebar:
    choice = option_menu('Menu', ("Home", "Profile", "Store", "Dashboard"), #settingup menu options
                        menu_icon="chat-text-fill",
                        default_index=1)

# File path for user data
user_data = r"E:\Projects\Marlo\user_data.csv"
review_data = r"E:\Projects\Marlo\review_data.csv"

#Function to load existing user
def load_users():
    try:
        with open(user_data, "r", newline="") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

#function to save new registered users
def save_users(users):
    with open(user_data, "w", newline="") as file:
        fieldnames = ["username", "password", "mobile_number"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

#function to authenticate the login user with existing credentials
def authenticate(user_data, username, password):
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return True
    return False

#intitialing session_state for the purpose of authentication
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

#functon to perfom login
def perform_login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if authenticate(load_users(), username, password):
            st.session_state.is_authenticated = True  # Set session state to authenticated
            st.write("Logged in successfully")
        else:
            st.error("Unknown User")


#function to perfom register
def perform_register():
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    mobile = st.text_input("Mobile Number")
    users = load_users()
    if st.button("Register"):
        users.append({"username": username, "password": password, "mobile_number": mobile})
        save_users(users)
        st.success("Registration successful. You can now log in.")

# Initialize stored_data as an empty list
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = []

#function to file upload
def file_upload():
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:        
        try:
            uploaded_data = pd.read_csv(uploaded_file, encoding='latin1')
            st.write("Uploaded CSV data:")
            st.write(uploaded_data)
            st.session_state.stored_data.append(uploaded_data)
        except UnicodeDecodeError:
            st.error("Error: Unable to decode the CSV file. Please ensure it's in the correct encoding.")

#Profile -

if choice == "Profile":
    st.subheader("Access/Register your account here")
    choose = st.selectbox("Login/Register", ("Login", "Register"))

    if choose == "Login":
        perform_login()
    elif choose == "Register":
        perform_register()

#Dashboard - 
if choice == "Dashboard":
    if not st.session_state.is_authenticated:
        st.error("Access denied. Please log in to access the Dashboard.")
    else:
        option = st.selectbox("Option",("Reports","Product"))
        if option == "Product":
            file_upload()

    if option == "Reports":
        st.subheader('Reports')
        user_report = st.button("User Report")
        if user_report:
            users = load_users()
            csv_content = "\n".join([",".join(row.values()) for row in users])
            st.download_button("Download User Report", csv_content, key="user_report", mime="text/csv")


#Store - 
if choice == "Store":
    # Display the stored_data (uploaded data)
    if st.session_state.stored_data:
        view = pd.concat(st.session_state.stored_data, ignore_index=True)
        st.write(view)
        st.subheader("Review Chat")
        product_id = st.text_input("Product ID")
        review = st.text_area("Enter Your Review")
        submit_review = st.button("Submit Review")
    else:
        st.write("No uploaded data available.")


#Home - 
if choice == "Home":
    st.header('Welcome to :blue[Ecom DotCom]')
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Welcome to our online store! Discover a world of shopping convenience with a wide range of products at your fingertips. From electronics to fashion, we offer quality items and unbeatable deals. Enjoy secure and hassle-free shopping, fast delivery, and exceptional customer service. Explore our website today and experience the joy of finding what you need, all in one place. Your satisfaction is our priority, and we look forward to serving you!**")
    with col2:
        image = Image.open(r"E:\Projects\Marlo\logo.jpg")
        st.image(image)