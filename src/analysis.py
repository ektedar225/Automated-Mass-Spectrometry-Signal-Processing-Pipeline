import pandas as pd
from scipy.signal import find_peaks

class PeakPicker:
    @staticmethod
    def identify_peaks(mz, intensity, height, distance):
        """
        Finds peaks and returns a clean DataFrame.
        """
        indices, _ = find_peaks(
            intensity,
            height=height,
            distance=distance
        )
        
        return pd.DataFrame({
            "m/z": mz[indices],
            "Intensity": intensity[indices],
            "Index": indices
        })