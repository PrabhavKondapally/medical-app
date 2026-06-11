import streamlit as st

col1, col2 = st.columns([1, 4])
with col1:
    st.image("cliniforge_logo.png", width=90)
with col2:
    st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=350)

st.divider()

st.title("🔍 Clinical Chart Review")
st.write("---")
st.info("Medical chart summaries and EHR data validation tools will display here.")