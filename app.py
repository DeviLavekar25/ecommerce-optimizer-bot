import streamlit as st
from optimizer import run_optimizer


st.set_page_config(page_title="E-Commerce Store Optimizer", page_icon="🛍️",layout="centered")
st.title("🛍️ E-Commerce Store Optimizer")
st.markdown("Enter the URL of your e-commerce website to audit product listings, optimize pricing, and improve SEO.")
site_url=st.text_input("Enter the URL of your e-commerce store:")


if st.button("🚀 Optimize Site") and site_url:
    with st.spinner("Running optimization... Please wait ⏳"):
      try:
        result = run_optimizer(site_url)
        st.subheader("Optimization Output")
        st.markdown(result, unsafe_allow_html=True)
      except Exception as e:
         st.error(f"❌ Something went wrong: {e}")
         


