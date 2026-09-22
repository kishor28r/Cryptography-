import streamlit as st
a=st.number_input("Enter your number")
b=st.number_input("Enter your another number")
if st.button("Add"):
        st.success(a+b)
elif st.button("subtraction"):
        st.success(a-b)
elif st.button("multiply"):
        st.success(a8b)