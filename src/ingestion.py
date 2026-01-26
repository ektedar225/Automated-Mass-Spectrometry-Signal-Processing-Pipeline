import os
import streamlit as st
from pyopenms import MSExperiment, MzMLFile
import numpy as np

class MzMLLoader:
    @staticmethod
    @st.cache_data(show_spinner=False) # <--- The Magic: Caches the result
    def load_spectrum(filepath, scan_index=0):
        """
        Loads a specific scan from an mzML file.
        Cached by Streamlit so it's instant on reload.
        """
        try:
            exp = MSExperiment()
            MzMLFile().load(filepath, exp)
            
            if exp.getSize() <= scan_index:
                return None, None
                
            spectrum = exp.getSpectrum(scan_index)
            mz, intensity = spectrum.get_peaks()
            return np.array(mz), np.array(intensity)
            
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return np.array([]), np.array([])