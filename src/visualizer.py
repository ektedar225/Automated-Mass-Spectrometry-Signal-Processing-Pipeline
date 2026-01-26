# src/visualizer.py
import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_processing_stages(mz, raw, smooth, baseline_corrected, peaks_df):
        """
        Plots Raw vs Processed data with detected peaks overlay.
        """
        plt.figure(figsize=(12, 8))

        # Subplot 1: Raw vs Smoothed
        plt.subplot(2, 1, 1)
        plt.plot(mz, raw, label='Raw Signal', color='lightgray', alpha=0.8)
        plt.plot(mz, smooth, label='Smoothed (Savitzky-Golay)', color='blue', linewidth=1)
        plt.title("Stage 1: Noise Reduction")
        plt.ylabel("Intensity")
        plt.legend()

        # Subplot 2: Baseline Corrected + Peaks
        plt.subplot(2, 1, 2)
        plt.plot(mz, baseline_corrected, label='Baseline Corrected', color='green', linewidth=1)
        
        # Overlay peaks
        plt.scatter(peaks_df['m/z'], peaks_df['Intensity'], 
                    color='red', marker='x', s=50, label='Identified Peaks')
        
        plt.title(f"Stage 2: Peak Detection (Count: {len(peaks_df)})")
        plt.xlabel("m/z (Mass-to-Charge Ratio)")
        plt.ylabel("Intensity")
        plt.legend()

        plt.tight_layout()
        plt.show()