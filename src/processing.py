import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import minimum_filter

class SignalProcessor:
    @staticmethod
    def apply_filters(intensity, sg_window, sg_poly, baseline_window):
        """
        1. De-noising (Savitzky-Golay)
        2. Baseline Drift Correction (Morphological)
        """
        # 1. Noise Reduction
        # Constraint: Window length must be odd and > polyorder
        if sg_window <= sg_poly:
            sg_window = sg_poly + 2
        if sg_window % 2 == 0:
            sg_window += 1
            
        smooth_int = savgol_filter(intensity, window_length=int(sg_window), polyorder=int(sg_poly))
        smooth_int = np.maximum(0, smooth_int) # Physics constraint: No negative light
        
        # 2. Baseline Estimation
        baseline = minimum_filter(smooth_int, size=int(baseline_window))
        
        # 3. Correction
        corrected_int = smooth_int - baseline
        
        return smooth_int, baseline, corrected_int