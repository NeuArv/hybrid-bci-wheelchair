# Hybrid BCI Wheelchair — Brain-Computer Interface Control System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**Design and Implementation of Hybrid BCI based Wheelchair**

A brain-computer interface (BCI) system for wheelchair control using Neurosky Mindwave EEG headset with attention-based control, blink detection, and obstacle avoidance.

## Overview

This project implements a hybrid brain-computer interface that allows users to control a wheelchair using:
- **Attention levels** from EEG signals for forward motion
- **Blink detection** for directional control (double blink = right, triple blink = left)
- **Ultrasonic sensors** for obstacle avoidance and safety

## Hardware Requirements

- **Raspberry Pi 3B+** or later
- **Neurosky Mindwave Mobile 2** EEG headset
- **HC-SR04 Ultrasonic Sensor** for obstacle detection
- **L298N Motor Driver** or equivalent
- **DC Motors** (2x for differential drive)
- **Wheelchair chassis** with motor mounts
- **Power supply** (suitable for motors and Raspberry Pi)

## Software Requirements

- Python 3.7+
- Raspberry Pi OS (Raspbian) or compatible Linux
- Bluetooth for EEG headset connectivity

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NeuArv/hybrid-bci-wheelchair.git
cd hybrid-bci-wheelchair
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Bluetooth Connection

Connect the Neurosky Mindwave headset via Bluetooth:

```bash
sudo bluetoothctl
# In bluetoothctl:
scan on
# Find your device MAC address
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
exit

# Create RFCOMM binding
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX
```

## Quick Start

### Test Hardware Components

Before running the full system, test individual components:

```bash
python scripts/test_sensors.py --test all
```

### Run Attention-Based Control (Main Demo)

```bash
python scripts/run_demo.py --port /dev/rfcomm0 --attention-threshold 50
```

### Run Blink-Only Control Demo

```bash
python scripts/blink_control_demo.py --port /dev/rfcomm0
```

## Project Structure

```
hybrid-bci-wheelchair/
├── src/
│   └── hybrid_bci/
│       ├── __init__.py              # Package initialization
│       ├── neuropy/                 # Neurosky Mindwave interface
│       │   ├── __init__.py
│       │   └── neuropy.py           # Serial communication with EEG
│       ├── motor_control.py         # Motor driver interface
│       ├── blink_detection.py       # Eye blink classifier
│       └── obstacle_detection.py    # Ultrasonic sensor interface
├── scripts/
│   ├── run_demo.py                  # Main attention-based control
│   ├── blink_control_demo.py        # Blink-only control demo
│   └── test_sensors.py              # Hardware testing utilities
├── tests/
│   └── (pytest test files)
├── docs/
│   └── (supplementary documentation)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── LICENSE                          # MIT License
└── CITATION.cff                     # Citation metadata
```

## Usage

### Basic Operation

1. **Wear the EEG headset**: Ensure it's firmly touching your forehead and powered on
2. **Start the system**: Run the main demo script
3. **Control via attention**: Focus to move forward (attention > threshold)
4. **Control via blinks**:
   - Double blink: Turn right
   - Triple blink: Turn left
5. **Safety**: System automatically stops when obstacles are detected

### Configuration

Adjust parameters in the scripts:

- `--attention-threshold`: Minimum attention level to trigger forward motion (0-100)
- `--port`: Serial port for the EEG headset (default: `/dev/rfcomm0`)

Modify hardware pins in the module files:
- `motor_control.py`: GPIO pin assignments for motor driver
- `obstacle_detection.py`: GPIO pin assignments for ultrasonic sensor

## API Usage

### Using as a Python Library

```python
from hybrid_bci.neuropy import NeuroPy
from hybrid_bci.motor_control import MotorController
from hybrid_bci.obstacle_detection import ObstacleDetector
from hybrid_bci.blink_detection import BlinkDetector

# Initialize components
neuropy = NeuroPy("/dev/rfcomm0")
motor = MotorController()
obstacle = ObstacleDetector()

# Set up attention callback
def on_attention(value):
    if value > 50:
        motor.forward()
    else:
        motor.stop()

neuropy.setCallBack("attention", on_attention)
neuropy.start()

# Run your control loop
# ...

# Cleanup
neuropy.stop()
motor.cleanup()
```

## Features

### 1. Attention-Based Control
- Uses **eSense Attention** metric from EEG
- Threshold-based activation (configurable)
- Real-time response (<1s latency)

### 2. Blink Detection
- Detects single, double, and triple blinks
- Uses raw EEG signal spike patterns
- Time-windowed multi-blink classification

### 3. Obstacle Avoidance
- Ultrasonic distance measurement
- Automatic safety stop when obstacles detected
- Configurable safety distance

### 4. Hybrid Control
- Combines multiple BCI modalities
- Attention for forward motion
- Blinks for directional control
- Sensors for safety

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black src/ scripts/ tests/
```

### Linting

```bash
flake8 src/ scripts/ tests/
```

## Troubleshooting

### EEG Headset Not Connecting
- Ensure Bluetooth is enabled and headset is paired
- Check that `/dev/rfcomm0` exists: `ls -l /dev/rfcomm*`
- Try re-binding: `sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX`

### Motors Not Working
- Check GPIO pin connections match code configuration
- Verify motor driver power supply
- Test with `scripts/test_sensors.py --test motor`

### Poor Signal Quality
- Ensure EEG sensor is clean and touching forehead firmly
- Reduce electrical interference (keep away from power lines)
- Check battery level of headset

## Citation

If you use this code in your research, please cite:

```bibtex
@misc{mishra2024hybrid,
  title={Design and Implementation of Hybrid BCI based Wheelchair},
  author={Mishra, Arvind Gyandatt and Chawda, Poonam and Dedhia, Heeral and Sridhar, Arvind and Kambli, Mansi and Kadge, Sushma},
  year={2024},
  howpublished={GitHub repository},
  url={https://github.com/NeuArv/hybrid-bci-wheelchair}
}
```

## Authors

- **Arvind Gyandatt Mishra** — [LinkedIn](https://www.linkedin.com/in/arvind-gyandatt-mishra-a6760a16b/)
- **Poonam Chawda**
- **Heeral Dedhia**
- **Arvind Sridhar**
- **Prof. Mansi Kambli**
- **Prof. Sushma Kadge**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NeuroPy library for Neurosky Mindwave interface
- Raspberry Pi Foundation for excellent embedded platform
- Brain-Computer Interface community for research and inspiration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Related Publications

For more details on the methodology and results, see our paper on ResearchGate:
[Design and Implementation of Hybrid BCI based Wheelchair](https://www.researchgate.net/publication/356207033_Design_and_Implementation_of_Hybrid_BCI_based_Wheelchair)

## Contact

For questions or collaboration opportunities, please reach out via GitHub issues or LinkedIn.
