import streamlit as st

# 1. Initialize session state at the very top of your app
if "high_priority_room" not in st.session_state:
    st.session_state["high_priority_room"] = {}
if "normal_room" not in st.session_state:
    st.session_state["normal_room"] = {}

# 2. The Triage Logic Button
if st.button("Run Patient Triage Audit"):
    patients = ["Alice", "Bob", "Charlie", "David", "Eve"]
    dosages = [600.0, 120.0, 750.0, 400.0, 95.0]
    safety = 500.0
    highPriorMax = 2
    
    # Reset rooms on click
    st.session_state["high_priority_room"] = {}
    st.session_state["normal_room"] = {}
    
    for i in range(len(patients)):
        # FIX 1: Generate real patient IDs starting at 101 (101, 102, 103...)
        patient_id = 101 + i 
        
        if dosages[i] > safety:
            if len(st.session_state["high_priority_room"]) >= highPriorMax:
                continue
            st.session_state["high_priority_room"][patient_id] = [patients[i], dosages[i]]
        else:
            st.session_state["normal_room"][patient_id] = [patients[i], dosages[i]]
            
    st.rerun()

# 3. FIX 2: Convert dictionaries to clean row lists so Streamlit displays them correctly
st.subheader("🏥 Active Room Status")
col1, col2 = st.columns(2)

with col1:
    st.write("🔴 **High Priority Room**")
    if st.session_state["high_priority_room"]:
        # Re-map the dictionary into standard rows
        hp_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                   for k, v in st.session_state["high_priority_room"].items()]
        st.dataframe(hp_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

with col2:
    st.write("🟢 **Normal Room**")
    if st.session_state["normal_room"]:
        norm_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                     for k, v in st.session_state["normal_room"].items()]
        st.dataframe(norm_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

# 4. Chart Review Section (Matches IDs perfectly now)
st.divider()
st.header("📋 Patient Chart Review & Overrides")

search_id = st.number_input("Enter Patient ID", min_value=101, max_value=105, step=1)
new_dosage_input = st.number_input("New Target Dosage (mg)", min_value=0.0, step=10.0)

if st.button("Update Patient Record"):
    if search_id in st.session_state["high_priority_room"]:
        st.session_state["high_priority_room"][search_id][1] = new_dosage_input
        patient_name = st.session_state["high_priority_room"][search_id][0]
        st.success(f"✅ High Priority Updated: {patient_name} (ID: {search_id}) changed to {new_dosage_input}mg.")
        st.rerun()
        
    elif search_id in st.session_state["normal_room"]:
        st.session_state["normal_room"][search_id][1] = new_dosage_input
        patient_name = st.session_state["normal_room"][search_id][0]
        st.success(f"✅ Normal Room Updated: {patient_name} (ID: {search_id}) changed to {new_dosage_input}mg.")
        st.rerun()
        
    else:
        st.error(f"❌ Error: Patient ID {search_id} cannot be found.")