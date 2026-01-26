# Automated Mass Spectrometry Signal Processing Pipeline

An end-to-end Python pipeline for processing, analyzing, and visualizing mass spectrometry data with advanced signal processing techniques.

## Overview

This project provides a comprehensive solution for analyzing mass spectrometry (MS) data files. It handles data ingestion from mzML files, applies sophisticated signal processing algorithms, performs peak detection and analysis, and presents results through an interactive web interface powered by Streamlit.

**Key Features:**
-  **mzML File Support**: Native parsing of mass spectrometry data files
-  **Advanced Signal Processing**: Savitzky-Golay filtering, baseline correction, and noise reduction
-  **Automated Peak Detection**: Identifies significant peaks with configurable thresholds
-  **Interactive Visualization**: Real-time plots and analysis dashboards
-  **Batch Processing**: Process multiple files in one run
-  **Professional UI**: Streamlit-based web interface with responsive design

## Project Structure

```
mass_spec_pipeline/
├── app.py                           # Streamlit web application
├── batch_main.py                    # Batch processing script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── data/
│   └── mzML/                        # Mass spectrometry data files
│       ├── Col_1.mzML
│       ├── Cytochrome_C.mzML
│       └── T9_A1.mzML
│
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── config.py                   # Configuration parameters
│   ├── ingestion.py                # mzML file loading
│   ├── processing.py               # Signal processing algorithms
│   ├── analysis.py                 # Peak detection and analysis
│   └── visualizer.py               # Plotting and visualization
│
└── tests/
    ├── __init__.py
    └── test_pipeline.py            # Unit tests
```

## Dependencies

- **numpy**: Numerical computing
- **scipy**: Scientific algorithms (signal processing)
- **pandas**: Data manipulation
- **matplotlib**: Static plotting
- **pyopenms**: Mass spectrometry data format support
- **streamlit**: Web application framework
- **plotly**: Interactive visualization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ektedar225/Automated-Mass-Spectrometry-Signal-Processing-Pipeline.git
   cd Automated-Mass-Spectrometry-Signal-Processing-Pipeline
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Web Application

Launch the Streamlit app to explore and process mass spectrometry data interactively:

```bash
streamlit run app.py
```

Access the application at `http://localhost:8501`

**Features:**
- Select sample files from the data directory
- Adjust signal processing parameters in real-time
- View processed spectra with detected peaks
- Download analysis results

### Batch Processing

Process multiple files automatically:

```bash
python batch_main.py
```

Results are saved to `batch_results.csv` with peak detection data for all files.

### Programmatic Usage

```python
from src.ingestion import MzMLLoader
from src.processing import SignalProcessor
from src.analysis import PeakPicker

# Load MS data
loader = MzMLLoader("data/mzML/sample.mzML")
spectra = loader.load_spectra()

# Process signal
processor = SignalProcessor()
processed = processor.process(spectra, scan_idx=0)

# Detect peaks
picker = PeakPicker()
peaks = picker.pick_peaks(processed)
```

## Configuration

Edit `src/config.py` to customize processing parameters:

- **SG_WINDOW_LENGTH**: Savitzky-Golay filter window (must be odd)
- **SG_POLY_ORDER**: Polynomial order for filtering
- **BASELINE_WINDOW**: Window size for baseline correction
- **PEAK_HEIGHT_THRESHOLD**: Minimum intensity for peak detection
- **PEAK_DISTANCE**: Minimum spacing between peaks
- **PEAK_PROMINENCE**: Minimum prominence threshold

## Processing Pipeline

```
mzML File Input
      ↓
Data Ingestion (mzML Parsing)
      ↓
Signal Denoising (Savitzky-Golay Filter)
      ↓
Baseline Correction
      ↓
Peak Detection (SciPy find_peaks)
      ↓
Peak Analysis & Validation
      ↓
Visualization & Results Export
```

## Example Workflow

1. **Load Data**: Select a sample mzML file
2. **Adjust Parameters**: Fine-tune noise reduction, baseline, and detection thresholds
3. **View Results**: Inspect processed spectra with highlighted peaks
4. **Export Data**: Download peak lists and processed spectra

## Testing

Run the test suite to verify functionality:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Your Name** - Initial work and development

## Acknowledgments

- PyOpenMS for mass spectrometry data parsing
- SciPy for signal processing algorithms
- Streamlit for the web framework

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

## Roadmap

- [ ] Advanced peak annotation
- [ ] Multi-sample comparison tools
- [ ] Machine learning-based peak classification
- [ ] Export to various formats (mzXML, netCDF)
- [ ] Docker containerization
- [ ] Cloud deployment option

---

**Last Updated**: January 26, 2026
