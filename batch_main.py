# batch_main.py
import os
import glob
import pandas as pd
from src.config import Config
from src.ingestion import MzMLLoader
from src.processing import SignalProcessor
from src.analysis import PeakPicker

def process_single_file(filepath, config):
    print(f"Processing: {os.path.basename(filepath)}...")
    
    # 1. Load
    loader = MzMLLoader(filepath)
    loader.load_data()
    if loader.experiment.getSize() == 0:
        return []

    # 2. Setup Processors
    processor = SignalProcessor(config)
    picker = PeakPicker(config)
    
    all_peaks = []

    # 3. Iterate through FIRST 10 scans (For speed demo)
    # Real app would loop through ALL scans: range(loader.experiment.getSize())
    for i in range(min(10, loader.experiment.getSize())):
        mz, intensity = loader.get_spectrum(i)
        
        # Smooth & Baseline
        smooth = processor.apply_smoothing(intensity)
        corrected, _ = processor.remove_baseline(smooth)
        
        # Pick Peaks
        peaks_df = picker.find_peaks(mz, corrected)
        
        # Add metadata (Scan ID and Filename)
        if not peaks_df.empty:
            peaks_df['Scan_ID'] = i
            peaks_df['Source_File'] = os.path.basename(filepath)
            all_peaks.append(peaks_df)

    return pd.concat(all_peaks) if all_peaks else pd.DataFrame()

def main():
    config = Config()
    
    # Find all .mzML files in the data folder
    mzml_files = glob.glob(os.path.join("data", "**/*.mzML"), recursive=True)
    print(f"Found {len(mzml_files)} files.")

    master_results = []

    for file in mzml_files:
        file_peaks = process_single_file(file, config)
        if not file_peaks.empty:
            master_results.append(file_peaks)

    # Combine and Save
    if master_results:
        final_df = pd.concat(master_results)
        output_file = "batch_results.csv"
        final_df.to_csv(output_file, index=False)
        print(f"\n✅ Batch Processing Complete!")
        print(f"Total Peaks Found: {len(final_df)}")
        print(f"Results saved to: {output_file}")
    else:
        print("No peaks found in any files.")

if __name__ == "__main__":
    main()