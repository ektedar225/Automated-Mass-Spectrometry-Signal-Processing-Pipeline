class Config:
    # ... (Keep paths the same)

    # Signal Processing Parameters
    # REDUCE the window length to preserve sharp peaks
    SG_WINDOW_LENGTH = 5   # Was 11. (Must be odd). Smaller = less smoothing.
    SG_POLY_ORDER = 3      # Keep as 3.

    # Baseline Correction
    BASELINE_WINDOW = 50   # Reduce slightly to follow local trends better

    # Peak Picking
    # LOWER the threshold to catch the smaller peaks visible in the noise
    PEAK_HEIGHT_THRESHOLD = 200  # Was 500. This will find more ions.
    PEAK_DISTANCE = 2            # Allow peaks to be closer together
    PEAK_PROMINENCE = 50         # Lower prominence to catch subtle peaks