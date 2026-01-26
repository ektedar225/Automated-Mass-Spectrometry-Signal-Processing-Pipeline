import streamlit as st
import plotly.graph_objects as go
import os
import glob
import pandas as pd

# Import our backend modules
from src.ingestion import MzMLLoader
from src.processing import SignalProcessor
from src.analysis import PeakPicker

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Mass Spectrometry Informatics",
    page_icon="🔬",
    layout="wide"
)

# --- SIDEBAR: CONTROLS ---
st.sidebar.title("🎛️ Method Parameters")
st.sidebar.markdown("**Measurement Informatics Control**")

# --- ROBUST PATH FIX ---
# Get the folder where app.py is currently sitting
current_dir = os.path.dirname(os.path.abspath(__file__))
# Build the full path to the data folder
data_dir = os.path.join(current_dir, "data", "mzML")

# Debugging: Print this to the terminal so you can see where it's looking
print(f"Looking for data in: {data_dir}")

files = glob.glob(os.path.join(data_dir, "*.mzML"))
filenames = [os.path.basename(f) for f in files]

selected_file = st.sidebar.selectbox("Select Sample File", filenames)
scan_idx = st.sidebar.number_input("Scan Index", min_value=0, max_value=100, value=0)

st.sidebar.markdown("---")

# 2. Signal Processing Parameters
st.sidebar.subheader("1. Noise Reduction")
sg_window = st.sidebar.slider("Savitzky-Golay Window", 3, 51, 11, step=2, help="Larger = Smoother, but wider peaks")

st.sidebar.subheader("2. Baseline Correction")
baseline_win = st.sidebar.slider("Baseline Window", 10, 200, 50, step=10, help="Estimates chemical noise floor")

st.sidebar.subheader("3. Peak Detection")
peak_height = st.sidebar.slider("Min Intensity Threshold", 100, 10000, 1000, step=100)
peak_dist = st.sidebar.slider("Min Peak Distance", 1, 20, 5)

# --- MAIN DASHBOARD ---
st.title("🔬 Automated Mass Spec Signal Pipeline")
st.markdown("""
**Objective:** Extract true chemical signals from noisy instrument data using digital signal processing.
""")

if selected_file:
    # 1. LOAD DATA
    file_path = os.path.join(data_dir, selected_file)
    mz, raw_int = MzMLLoader.load_spectrum(file_path, scan_idx)

    if len(mz) > 0:
        # 2. PROCESS SIGNAL
        smooth_int, baseline, clean_int = SignalProcessor.apply_filters(
            raw_int, sg_window, 3, baseline_win
        )

        # 3. IDENTIFY PEAKS
        peaks_df = PeakPicker.identify_peaks(mz, clean_int, peak_height, peak_dist)

        # --- VISUALIZATION (PLOTLY) ---
        # Tab 1: Processing View, Tab 2: Results Table
        tab1, tab2, tab3 = st.tabs(["📊 Signal Analysis", "📋 Peak List", "📘 Theory"])

        with tab1:
            # Create interactive plot
            fig = go.Figure()
            
            # Raw Data (Grey, background)
            fig.add_trace(go.Scatter(x=mz, y=raw_int, mode='lines', name='Raw Signal', 
                                     line=dict(color='#d3d3d3', width=1)))
            
            # Smoothed (Blue)
            fig.add_trace(go.Scatter(x=mz, y=smooth_int, mode='lines', name='Smoothed (SG Filter)', 
                                     line=dict(color='#004e98', width=1.5)))
            
            # Baseline (Orange dashed)
            fig.add_trace(go.Scatter(x=mz, y=baseline, mode='lines', name='Estimated Baseline', 
                                     line=dict(color='orange', width=1, dash='dash')))
            
            # Detected Peaks (Red X)
            fig.add_trace(go.Scatter(
                x=peaks_df['m/z'], 
                y=peaks_df['Intensity'], 
                mode='markers', 
                name=f'Detected Ions ({len(peaks_df)})',
                marker=dict(color='red', symbol='x', size=8)
            ))

            fig.update_layout(
                title=f"Spectral Analysis: {selected_file} (Scan {scan_idx})",
                xaxis_title="m/z (Mass-to-Charge Ratio)",
                yaxis_title="Intensity",
                template="plotly_white",
                height=600,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Peaks Found", len(peaks_df))
            col2.metric("Max Intensity", f"{clean_int.max():.0f}")
            col3.metric("Noise Floor Est.", f"{baseline.mean():.0f}")

        with tab2:
            st.dataframe(peaks_df.sort_values(by="Intensity", ascending=False), use_container_width=True)
            
            # Export Button
            csv = peaks_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Peak List as CSV",
                data=csv,
                file_name=f"peaks_{selected_file}.csv",
                mime='text/csv',
            )
            
        with tab3:
            st.markdown("""
            ### Signal Processing Methodology
            
            **1. The Inverse Problem:**
            We observe $y = x + \eta + \beta$, where:
            * $x$ is the true chemical signal (Peaks)
            * $\eta$ is high-frequency electronic noise
            * $\beta$ is low-frequency baseline drift (chemical matrix)
            
            **2. Solution Strategy:**
            * **Noise Reduction:** Applied a **Savitzky-Golay filter** (polynomial least squares) to smooth $\eta$ without destroying the narrow peak width of $x$.
            * **Baseline Removal:** Used **Morphological Minimum Filtering** to estimate the lower envelope $\beta$ of the signal.
            """)

    else:
        st.error("No data found in this scan index.")
else:
    st.info("Please select a file from the sidebar.")