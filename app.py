import streamlit as st

# 1. App Styling & Header
st.title("🏥 Clinical Patient Priority Queue")
st.write("Input patient data below to automatically triage rooms and monitor overflow constraints.")

# 2. UI Inputs: Let the user type names and dosages directly on the webpage
patients_input = st.text_input("Enter Patient Names (separated by commas):", "Alice, Bob, Charlie, David")
dosages_input = st.text_input("Enter Prescribed Dosages in mg (separated by commas):", "600, 120, 700, 900")
safety_input = st.number_input("Set Safety Threshold Limit (mg):", min_value=0, value=500, step=50)

# FIX: Wrapped in int() to ensure capacity is always a whole number, not a decimal
highPriorityMax_input = int(st.number_input("Enter the # of beds in the High Priority Room", min_value=0, step=1, value=2))

# 3. Action Button
if st.button("Run Triage Audit"):
    
    # Process the raw text inputs into clean Python lists
    patients = [p.strip() for p in patients_input.split(",") if p.strip()]
    
    try:
        dosages = [float(d.strip()) for d in dosages_input.split(",") if d.strip()]
    except ValueError:
        st.error("Error: Please ensure all dosages entered are valid numbers.")
        st.stop()

    # --- Your Core Validation Logic ---
    if len(patients) != len(dosages):
        st.error(f"Configuration Error! Mismatched Records. Patients: {len(patients)}, Dosages: {len(dosages)}")
    else:
        # --- Your Core Triage Architecture ---
        highPriority = {}  # Perfect: Now a dictionary
        highPriorMax = highPriorityMax_input
        normal = {}        # Perfect: Now a dictionary
        safety = safety_input
        overflow_triggered = False

        for i in range(len(patients)):
            if dosages[i] > safety:
                # This check now runs perfectly with whole numbers
                if len(highPriority) >= highPriorMax:
                    overflow_triggered = True
                    break
                # Perfect dictionary insertion: Key = Name, Value = Dosage
                highPriority[patients[i]] = dosages[i]
            else:
                normal[patients[i]] = dosages[i]

        # 4. UI Outputs: Display results using visual frontend components
        if overflow_triggered:
            st.error("🚨 CRITICAL OVERFLOW! High Priority Room Capacity Full! Deployment Halted.")
        else:
            st.success("✅ Audit Complete. All patients routed safely.")
            
            # Split screen into two visual columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔴 High Priority Room")
                st.write(f"Total Beds Occupied: {len(highPriority)}/{highPriorMax}")
                st.json(highPriority)  # Will display clean Key-Value pairs!
                
            with col2:
                st.subheader("🟢 Normal Room")
                st.write(f"Total Patients: {len(normal)}")
                st.json(normal)