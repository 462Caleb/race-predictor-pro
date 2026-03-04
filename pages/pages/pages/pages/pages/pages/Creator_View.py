import streamlit as st
from lib.auth import get_my_role

st.title("Creator View")

if get_my_role() != "creator":
    st.error("Creator only page")
else:
    st.write("Creator dashboard")
