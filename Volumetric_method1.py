import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Hydrocarbon Volume Calculator")
st.subheader("Calculate OOIP or OGIP with Optional Recovery Estimation")

# Common reservoir inputs using sliders
st.markdown("### Reservoir Properties")
A = st.slider("Reservoir Area (acres)", min_value=10.0, max_value=10000.0, step=10.0)
h = st.slider("Net Pay Thickness (ft)", min_value=5.0, max_value=300.0, step=1.0)
phi = st.slider("Porosity (fraction)", min_value=0.00, max_value=0.6, step=0.01)
Sw = st.slider("Water Saturation (fraction)", min_value=0.0, max_value=1.0, step=0.01)

# Constants
acre_to_barrels = 7758
acre_to_cuft = 43560

# Pore Volume and HCPV
PV_acreft = A * h * phi

# Select fluid type
fluid_type = st.radio("Select the type of hydrocarbon:", ["Oil", "Gas"])

st.markdown("---")

if fluid_type == "Oil":
    st.markdown("### Oil Properties")
    Bo = st.slider("Oil Formation Volume Factor Bₒ (rb/stb)", min_value=1.0, max_value=2.0, step=0.01)

    # Optional Recovery Factor
    show_rf = st.checkbox("I want to estimate recoverable oil reserves")

    if show_rf:
        RF_oil = st.slider("Recovery Factor (fraction)", min_value=0.05, max_value=0.6, step=0.01)

    # OOIP
    PV_bbl = PV_acreft * acre_to_barrels/1000 #Mbbls
    HCPV = PV_bbl * (1 - Sw) #Mbbls
    OOIP = HCPV / Bo #MSTB

    # Display Results
    st.success("**Oil Calculation Results:**")
    st.write(f"**Pore Volume:** {PV_acreft:.2f} acre-ft | {PV_bbl:,.0f} Mbbl")
    st.write(f"**Hydrocarbon Pore Volume:** {HCPV:,.0f} Mbbl")
    st.write(f"**OOIP:** {OOIP:,.0f} MSTB")

    # Conditional recoverable calculation and visualization
    if show_rf:
        recoverable_oil = OOIP * RF_oil
        non_recoverable_oil = OOIP - recoverable_oil
        st.write(f"**Recoverable Oil Reserves:** {recoverable_oil:,.0f} MSTB")
        st.write(f"**Non-recoverable Oil Reserves:** {non_recoverable_oil:,.0f} MSTB")
        
        #Column chart 1
        chart_data_1 = pd.DataFrame({
            'Volume (Mbbl)': [PV_bbl, HCPV]
        }, index=['Pore Volume', 'Hydrocarbon PV'])
        fig, ax = plt.subplots()
        colors = {'Pore Volume': 'orange', 'Hydrocarbon PV': 'brown'}  # Define colors
        for index, value in enumerate(chart_data_1['Volume (Mbbl)']):
          ax.bar(chart_data_1.index[index], value, color=colors[chart_data_1.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels
 
        ax.set_ylabel("Volume (Mbbl)")  # Y-axis label
        st.pyplot(fig)


        #st.bar_chart(chart_data_2)
        # Column Chart 2 (Comparison of hydrocarbons)
        chart_data_2 = pd.DataFrame({
            'Volume (MSTB)': [recoverable_oil, non_recoverable_oil]
        }, index=['Recoverable Oil', 'Non-Recoverable Oil'])
        fig, ax = plt.subplots()
        colors = {'Recoverable Oil': 'green', 'Non-Recoverable Oil': 'red'}  # Define colors
        for index, value in enumerate(chart_data_2['Volume (MSTB)']):
          ax.bar(chart_data_2.index[index], value, color=colors[chart_data_2.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels

        ax.set_ylabel("Volume (Mbbl)")  # Y-axis label
        st.pyplot(fig)

        
        #st.bar_chart(chart_data_1)

        


        # Pie Chart
        labels = ['Recoverable Oil', 'Non-Recoverable Oil']
        sizes = [recoverable_oil, non_recoverable_oil]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff6666'])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

    else:
        chart_data = pd.DataFrame({
            'Volume (Mbbl)': [PV_bbl, HCPV]
        }, index=['Pore Volume', 'Hydrocarbon PV'])
        fig, ax = plt.subplots()
        colors = {'Pore Volume': 'orange', 'Hydrocarbon PV': 'brown'}  # Define colors
        for index, value in enumerate(chart_data['Volume (Mbbl)']):
          ax.bar(chart_data.index[index], value, color=colors[chart_data.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels
        ax.set_ylabel("Volume (Mbbl)")  # Y-axis label
        st.pyplot(fig)

        #st.bar_chart(chart_data)

elif fluid_type == "Gas":
    st.markdown("### Gas Properties")
    Bg = st.number_input("Gas Formation Volume Factor B₉ (rcf/scf)", min_value=0.001, max_value=0.01, step=0.0001)

    # Optional Recovery Factor
    show_rf = st.checkbox("I want to estimate recoverable gas reserves")

    if show_rf:
        RF_gas = st.slider("Recovery Factor (fraction)", min_value=0.3, max_value=0.95, step=0.01)

    # OGIP
    PV_cuft=PV_acreft*acre_to_cuft/1000000
    HCPV_cuft = PV_cuft * (1 - Sw)
    OGIP = HCPV_cuft / Bg

    # Display Results
    st.success("**Gas Calculation Results:**")
    st.write(f"**Pore Volume:** {PV_acreft:.2f} acre-ft")
    st.write(f"**Hydrocarbon Pore Volume:** {HCPV_cuft:,.0f} MMcu ft")
    st.write(f"**OGIP:** {OGIP:,.0f} MMSCF")

    # Conditional recoverable calculation and visualization
    if show_rf:
        recoverable_gas = OGIP * RF_gas
        non_recoverable_gas = OGIP - recoverable_gas
        st.write(f"**Recoverable Gas Reserves:** {recoverable_gas:,.0f} MMSCF")
        st.write(f"**Non-recoverable Gas Reserves:** {non_recoverable_gas:,.0f} MMSCF")
        
        #Column chart 1
        chart_data_1 = pd.DataFrame({
            'Volume (MMCF)': [PV_cuft, HCPV_cuft]
        }, index=['Pore Volume', 'Hydrocarbon PV'])
        fig, ax = plt.subplots()
        colors = {'Pore Volume': 'orange', 'Hydrocarbon PV': 'brown'}  # Define colors
        for index, value in enumerate(chart_data_1['Volume (MMCF)']):
          ax.bar(chart_data_1.index[index], value, color=colors[chart_data_1.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels
        ax.set_ylabel("Volume (MMCF)")  # Y-axis label
        st.pyplot(fig)

        #st.bar_chart(chart_data_1)

        # Column Chart 2
        chart_data_2 = pd.DataFrame({
            'Volume (MMSCF)': [recoverable_gas, non_recoverable_gas]
        }, index=['Recoverable Gas', 'Non-Recoverable Gas'])
        fig, ax = plt.subplots()
        colors = {'Recoverable Gas': 'green', 'Non-Recoverable Gas': 'red'}  # Define colors
        for index, value in enumerate(chart_data_2['Volume (MMSCF)']):
          ax.bar(chart_data_2.index[index], value, color=colors[chart_data_2.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels
        ax.set_ylabel("Volume (MMCF)")  # Y-axis label
        st.pyplot(fig)

        #st.bar_chart(chart_data_2)

        
        # Pie Chart
        labels = ['Recoverable Gas', 'Non-Recoverable Gas']
        sizes = [recoverable_gas, non_recoverable_gas]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff6666'])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

    else:
        chart_data = pd.DataFrame({
            'Volume (MMCF)': [PV_cuft, HCPV_cuft]
        }, index=['Pore Volume', 'Hydrocarbon PV'])
        fig, ax = plt.subplots()
        colors = {'Pore Volume': 'orange', 'Hydrocarbon PV': 'brown'}  # Define colors
        for index, value in enumerate(chart_data['Volume (MMCF)']):
          ax.bar(chart_data.index[index], value, color=colors[chart_data.index[index]])
          ax.text(index, value, str(round(value, 2)), ha='center', va='bottom') # Add data labels
        ax.set_ylabel("Volume (bbl)")  # Y-axis label
        st.pyplot(fig)

        #st.bar_chart(chart_data)
