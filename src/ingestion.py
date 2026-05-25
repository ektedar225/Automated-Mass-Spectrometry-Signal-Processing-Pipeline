import os
import streamlit as st
import numpy as np

# Try to import pyopenms, fall back to mock if not available
try:
    from pyopenms import MSExperiment, MzMLFile
except (ImportError, Exception):
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mock_pyopenms import MSExperiment, MzMLFile

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
