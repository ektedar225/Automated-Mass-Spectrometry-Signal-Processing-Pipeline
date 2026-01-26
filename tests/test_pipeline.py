import unittest
import numpy as np
import pandas as pd
from src.processing import SignalProcessor
from src.analysis import PeakPicker
from src.config import Config

class TestMassSpecPipeline(unittest.TestCase):

    def setUp(self):
        """Runs before every test. Sets up a standard config."""
        self.config = Config()
        # Override config for testing small arrays
        self.config.SG_WINDOW_LENGTH = 5
        self.config.PEAK_HEIGHT_THRESHOLD = 10

    def test_smoothing_reduces_variance(self):
        """
        Physics Check: Smoothing should reduce the standard deviation 
        of a noisy flat signal.
        """
        # 1. Create a fake "noisy" signal (random jitter)
        np.random.seed(42) # Fixed seed for reproducibility
        noisy_signal = np.random.rand(100) * 10 
        
        # 2. Apply smoothing
        processor = SignalProcessor(self.config)
        smoothed_signal = processor.apply_smoothing(noisy_signal)
        
        # 3. Calculate variance (how "jagged" it is)
        variance_raw = np.std(noisy_signal)
        variance_smooth = np.std(smoothed_signal)
        
        print(f"\nRaw StdDev: {variance_raw:.2f} -> Smooth StdDev: {variance_smooth:.2f}")
        
        # 4. Assert that smoothing actually smoothed it
        self.assertLess(variance_smooth, variance_raw, "Smoothing did not reduce signal variance!")

    def test_peak_identification(self):
        """
        Logic Check: Can we find a single clear peak in synthetic data?
        """
        # Create a flat line with ONE spike at index 50
        mz_axis = np.arange(100)
        intensity = np.zeros(100)
        intensity[50] = 100  # The spike
        
        picker = PeakPicker(self.config)
        peaks = picker.find_peaks(mz_axis, intensity)
        
        # We expect exactly 1 peak found
        self.assertEqual(len(peaks), 1, "Expected exactly 1 peak.")
        
        # We expect the peak to be at m/z 50
        found_mz = peaks.iloc[0]['m/z']
        self.assertEqual(found_mz, 50, f"Expected peak at 50, found {found_mz}")

    def test_baseline_correction_floor(self):
        """
        Math Check: Baseline correction should not result in negative intensity.
        """
        intensity = np.array([10, 10, 10, 50, 10, 10]) # Signal on a baseline of 10
        processor = SignalProcessor(self.config)
        
        corrected, baseline = processor.remove_baseline(intensity)
        
        # The lowest value should be near 0, not negative
        self.assertTrue(np.all(corrected >= 0), "Baseline correction created negative values!")

if __name__ == '__main__':
    unittest.main()