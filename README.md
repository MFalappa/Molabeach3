# Phenopy Source Code

Source code for the **phenopy** software, originally published in [1].

> **⚠️ Important Notice:** This code has been refactored from Python 2 to Python 3 but is **not actively maintained** and **not tested**. Use at your own discretion.

## System Requirements

- Python 3.6+ (tested with Python 3.7+)
- Operating System: Windows, macOS, or Linux

## Installation

### Method 1: Using requirements.txt (Recommended)

1. Create and activate a clean virtual environment:
   ```sh
   python -m venv phenopy-env
   source phenopy-env/bin/activate  # On Windows: phenopy-env\Scripts\activate
   ```

2. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Method 2: Manual Installation

Alternatively, you can install packages manually:
```sh
pip install numpy pyserial subprocess32 xbee PyQt5 matplotlib scipy passlib pandas h5py pyedflib scikit-learn
```

## Usage

1. Activate your virtual environment (if using one)
2. Navigate to the main scripts directory:
   ```sh
   cd phenopy3/mainScripts
   ```
3. Run the main application:
   ```sh
   python Phenop3.py
   ```

## Hardware Requirements

This software was designed to work with specific CAN bus hardware (LAWICEL CANUSB). Please refer to the original publication [1] for detailed hardware setup requirements.

## Known Issues

- **Legacy code**: This is research software that may contain outdated patterns
- **No testing**: The Python 3 conversion has not been thoroughly tested
- **Hardware dependencies**: May require specific hardware drivers that are no longer actively maintained

## Support

**No active support is provided.** This code is shared for reproducibility purposes only. For questions about the methodology, please refer to the original publication [1].

## License

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA

## Citation

If you use this software, please cite the original publication:

```bibtex
@article{balzani2018approach,
  title={An approach to monitoring home-cage behavior in mice that facilitates data sharing},
  author={Balzani, Edoardo and Falappa, Marco and Balci, Fuat and Tucci, Valter},
  journal={Nature Protocols},
  volume={13},
  number={6},
  pages={1331--1347},
  year={2018},
  publisher={Nature Publishing Group},
  doi={10.1038/nprot.2018.031}
}
```

## References

[1] Balzani E, Falappa M, Balci F, Tucci V. An approach to monitoring home-cage behavior in mice that facilitates data sharing. Nat Protoc. 2018 Jun;13(6):1331-1347. doi: 10.1038/nprot.2018.031. Epub 2018 May 17. PMID: 29773907.
