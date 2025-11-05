# API Documentation

Comprehensive API reference for the Hybrid BCI Wheelchair control system.

## Table of Contents

1. [NeuroPy Module](#neuropy-module)
2. [Motor Control Module](#motor-control-module)
3. [Blink Detection Module](#blink-detection-module)
4. [Obstacle Detection Module](#obstacle-detection-module)

---

## NeuroPy Module

Interface for Neurosky Mindwave EEG headset.

### Class: `NeuroPy`

```python
from hybrid_bci.neuropy import NeuroPy
```

#### Constructor

```python
NeuroPy(port=None, baudRate=57600, devid=None)
```

**Parameters:**
- `port` (str, optional): Serial port path. Auto-detects based on OS if None.
- `baudRate` (int, optional): Serial baud rate. Default: 57600.
- `devid` (str, optional): Device ID for RF dongles.

**Example:**
```python
neuropy = NeuroPy("/dev/rfcomm0")
```

#### Methods

##### `start()`

Start data acquisition thread.

```python
neuropy.start()
```

##### `stop()`

Stop data acquisition and close connection.

```python
neuropy.stop()
```

##### `setCallBack(variable_name, callback_function)`

Register a callback for EEG data updates.

**Parameters:**
- `variable_name` (str): Name of EEG variable (see properties below)
- `callback_function` (callable): Function to call on update

**Example:**
```python
def on_attention(value):
    print(f"Attention: {value}")

neuropy.setCallBack("attention", on_attention)
```

#### Properties

All properties are read-only and updated automatically:

| Property | Type | Range | Description |
|----------|------|-------|-------------|
| `attention` | int | 0-100 | eSense attention level |
| `meditation` | int | 0-100 | eSense meditation level |
| `rawValue` | int | -32768 to 32767 | Raw EEG signal |
| `delta` | int | 0+ | Delta wave power (0.5-2.75 Hz) |
| `theta` | int | 0+ | Theta wave power (3.5-6.75 Hz) |
| `lowAlpha` | int | 0+ | Low alpha power (7.5-9.25 Hz) |
| `highAlpha` | int | 0+ | High alpha power (10-11.75 Hz) |
| `lowBeta` | int | 0+ | Low beta power (13-16.75 Hz) |
| `highBeta` | int | 0+ | High beta power (18-29.75 Hz) |
| `lowGamma` | int | 0+ | Low gamma power (31-39.75 Hz) |
| `midGamma` | int | 0+ | Mid gamma power (41-49.75 Hz) |
| `poorSignal` | int | 0-200 | Signal quality (0=good, 200=off head) |
| `blinkStrength` | int | 0-255 | Eye blink strength |
| `packetsReceived` | int | 0+ | Total packets received |

---

## Motor Control Module

GPIO-based control for DC motors via H-bridge driver.

### Class: `MotorController`

```python
from hybrid_bci.motor_control import MotorController
```

#### Constructor

```python
MotorController(right_pins=(3, 5, 7), 
                left_pins=(13, 15, 19),
                pwm_frequency=1000,
                default_speed=85)
```

**Parameters:**
- `right_pins` (tuple): (IN1, IN2, EN) GPIO pins for right motor (BOARD mode)
- `left_pins` (tuple): (IN1, IN2, EN) GPIO pins for left motor (BOARD mode)
- `pwm_frequency` (int): PWM frequency in Hz
- `default_speed` (int): Default PWM duty cycle (0-100)

**Example:**
```python
motor = MotorController(
    right_pins=(3, 5, 7),
    left_pins=(13, 15, 19),
    default_speed=85
)
```

#### Methods

##### `forward()`

Move both motors forward (wheelchair moves forward).

```python
motor.forward()
```

##### `backward()`

Move both motors backward (wheelchair moves backward).

```python
motor.backward()
```

##### `turn_left()`

Turn left (right motor on, left motor off).

```python
motor.turn_left()
```

##### `turn_right()`

Turn right (left motor on, right motor off).

```python
motor.turn_right()
```

##### `stop()`

Stop all motors.

```python
motor.stop()
```

##### `set_speed(speed)`

Set motor speed via PWM.

**Parameters:**
- `speed` (int): PWM duty cycle (0-100)

```python
motor.set_speed(50)  # 50% speed
```

##### Convenience speed methods

```python
motor.speed_low()     # 15% duty cycle
motor.speed_medium()  # 40% duty cycle
motor.speed_high()    # 80% duty cycle
```

##### `cleanup()`

Release GPIO resources.

```python
motor.cleanup()
```

### Legacy Function API

Backward compatible functions:

```python
from hybrid_bci import motor_control

motor_control.forward()
motor_control.backward()
motor_control.forward_left()   # turn_left
motor_control.forward_right()  # turn_right
motor_control.stop()
motor_control.speed_low()
motor_control.speed_medium()
motor_control.speed_high()
```

---

## Blink Detection Module

Detects eye blinks from raw EEG signals for control commands.

### Class: `BlinkDetector`

```python
from hybrid_bci.blink_detection import BlinkDetector
```

#### Constructor

```python
BlinkDetector(neuropy_instance,
              motor_controller=None,
              spike_threshold_high=100,
              spike_threshold_low=-100,
              blink_duration_min=0.01,
              blink_duration_max=0.050,
              multi_blink_window=0.6)
```

**Parameters:**
- `neuropy_instance` (NeuroPy): Connected NeuroPy instance
- `motor_controller` (MotorController, optional): Motor controller for actions
- `spike_threshold_high` (int): Threshold for spike start detection
- `spike_threshold_low` (int): Threshold for spike end detection
- `blink_duration_min` (float): Minimum valid blink duration (seconds)
- `blink_duration_max` (float): Maximum valid blink duration (seconds)
- `multi_blink_window` (float): Time window for multi-blink detection (seconds)

**Example:**
```python
neuropy = NeuroPy("/dev/rfcomm0")
neuropy.start()

motor = MotorController()
detector = BlinkDetector(neuropy, motor)
```

#### Methods

##### `detect_blinks(max_iterations=20000, timeout=60)`

Run blink detection loop.

**Parameters:**
- `max_iterations` (int): Maximum samples to process
- `timeout` (float): Maximum time to run (seconds)

**Returns:**
- `str` or `None`: Blink type detected ('single', 'double', 'triple', or None)

**Example:**
```python
result = detector.detect_blinks(timeout=30)
if result == 'double':
    print("Double blink detected - turned right")
```

##### `reset_state()`

Reset detection state.

```python
detector.reset_state()
```

### Convenience Function

```python
from hybrid_bci.blink_detection import run_blink_detection

result = run_blink_detection(port="/dev/rfcomm0", duration=60)
```

---

## Obstacle Detection Module

Ultrasonic sensor-based obstacle detection.

### Class: `ObstacleDetector`

```python
from hybrid_bci.obstacle_detection import ObstacleDetector
```

#### Constructor

```python
ObstacleDetector(trig_pin=8,
                 echo_pin=10,
                 safety_distance_cm=20,
                 speed_of_sound=343)
```

**Parameters:**
- `trig_pin` (int): GPIO pin for trigger (BOARD mode)
- `echo_pin` (int): GPIO pin for echo (BOARD mode)
- `safety_distance_cm` (float): Minimum safe distance in cm
- `speed_of_sound` (float): Speed of sound in m/s

**Example:**
```python
detector = ObstacleDetector(
    trig_pin=8,
    echo_pin=10,
    safety_distance_cm=20
)
```

#### Methods

##### `measure_distance()`

Measure distance to nearest obstacle.

**Returns:**
- `float`: Distance in centimeters, or -1 on error

```python
distance = detector.measure_distance()
print(f"Obstacle at {distance:.1f} cm")
```

##### `is_obstacle_near()`

Check if obstacle is within safety distance.

**Returns:**
- `tuple`: (is_near: bool, distance: float)

```python
is_near, distance = detector.is_obstacle_near()
if is_near:
    print("Obstacle too close!")
```

##### `monitor_and_stop(motor_controller, blink_callback=None)`

Monitor for obstacles and stop motor if needed.

**Parameters:**
- `motor_controller` (MotorController): Motor controller to stop
- `blink_callback` (callable, optional): Function to call when path is clear

**Returns:**
- `bool`: True if obstacle detected and stopped, False if safe

```python
motor = MotorController()
detector = ObstacleDetector()

is_blocked = detector.monitor_and_stop(motor)
if is_blocked:
    print("Path blocked!")
```

##### `cleanup()`

Release GPIO resources.

```python
detector.cleanup()
```

### Legacy Function API

```python
from hybrid_bci import obstacle_detection

distance = obstacle_detection.measure_distance()
obstacle_detection.check_obstacle(motor, blink_callback)
```

---

## Complete Example

```python
from hybrid_bci.neuropy import NeuroPy
from hybrid_bci.motor_control import MotorController
from hybrid_bci.obstacle_detection import ObstacleDetector
from hybrid_bci.blink_detection import BlinkDetector
import time

# Initialize components
neuropy = NeuroPy("/dev/rfcomm0")
motor = MotorController()
obstacle = ObstacleDetector()
blink = BlinkDetector(neuropy, motor)

# Define callback for attention
def on_attention(value):
    print(f"Attention: {value}")
    if value > 50:
        motor.forward()
        time.sleep(1)
        
        # Check for obstacles
        is_blocked = obstacle.monitor_and_stop(
            motor, 
            blink_callback=lambda: blink.detect_blinks(timeout=2)
        )
    else:
        motor.stop()

# Register callback and start
neuropy.setCallBack("attention", on_attention)
neuropy.start()

try:
    # Run for 60 seconds
    time.sleep(60)
finally:
    # Cleanup
    neuropy.stop()
    motor.cleanup()
    obstacle.cleanup()
```

---

## Error Handling

All modules handle GPIO unavailability gracefully:

```python
# Code runs in simulation mode if RPi.GPIO not available
motor = MotorController()  # Works on non-Pi systems
motor.forward()  # Prints command but doesn't control hardware
```

This allows development and testing on non-Raspberry Pi systems.

