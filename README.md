# MQTT Button App

A cross-platform application for creating buttons that send MQTT messages when pressed. The app supports Windows and Linux.

## Features

- Create customizable buttons with MQTT settings
- Configure server, port, username, password, topic, and message
- Support for QoS levels and retained messages
- No persistent connection - connects only when sending messages
- Save and load button configurations
- Custom button colors

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

## Usage

1. Click "Add Button" to create a new button
2. Configure the MQTT settings:
   - Server: MQTT broker address (e.g., test.mosquitto.org)
   - Port: MQTT broker port (default: 1883)
   - Username/Password: Optional authentication
   - Topic: MQTT topic to publish to
   - Message: The message to send
   - QoS: Quality of Service level (0, 1, or 2)
   - Retain: Whether to retain the message
   - Label: Button display text
   - Button Color: Button appearance color
3. Click the button to send the MQTT message

## Configuration

Button configurations are saved in `config/buttons.json` by default. You can:
- Save configurations manually by clicking "Save"
- Load configurations by clicking "Load"
- Edit the JSON file directly

## Packaging

To create standalone executables:

### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Linux

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Dependencies

- PyQt6 >= 6.4.0 - GUI framework
- paho-mqtt >= 1.6.1 - MQTT client library

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
