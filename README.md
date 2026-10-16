# 2.4 GHz RF Activity Monitor

A Raspberry Pi Pico H project using an nRF24L01+ module to detect RF activity across 126 channel centres from 2400 to 2525 MHz.

The project combines **MicroPython hardware control** with **MATLAB visualisation of recorded data**.

## Features

- Scan RF activity using the nRF24L01+ Received Power Detector (RPD)
- Check frequencies corresponding to Wi-Fi channels 1, 6 and 11
- Display detection counts in the serial terminal
- Identify the channel with the highest detection count
- Visualise existing binary recordings in MATLAB as a 3D surface plot

RPD is a threshold detector, not a calibrated signal-strength measurement. Detections may come from different RF sources; the application does not identify Wi-Fi networks or decode their traffic.

## Files

| File | Purpose |
|---|---|
| `rf_scan.py` | MicroPython diagnostic scanner |
| `plot_rf_recording.m` | MATLAB script for visualising an existing recording |

The MicroPython scanner also requires a compatible `nrf24l01.py` driver on the Pico.

## Hardware

- Raspberry Pi Pico H
- nRF24L01+ radio module
- Breadboard and jumper wires
- 100 µF capacitor across the radio supply

### SPI Wiring

| nRF24L01+ | Pico connection |
|---|---|
| VCC | Suitable 3.3 V supply |
| GND | GND |
| CE | GP20 |
| CSN | GP17 |
| SCK | GP18 |
| MOSI | GP19 |
| MISO | GP16 |

## Running the MicroPython Scanner

1. Connect the hardware using the wiring table.
2. Open the Pico in Thonny with MicroPython selected.
3. Save the compatible `nrf24l01.py` driver onto the Pico.
4. Open and run `rf_scan.py`.
5. View the detection counts in the serial shell.

The preliminary frequency checks use **200 samples** each. The full scan uses **100 samples per channel** and runs once.

## MATLAB Recording Analysis

The MATLAB script reads an existing `.bin` recording containing repeated scans.

1. Open `plot_rf_recording.m` in MATLAB.
2. Run the script.
3. Select your recording file.
4. Explore the 3D plot of frequency, time and detection percentage.

### Expected Recording Format

Each record contains **130 bytes**:

| Bytes | Contents |
|---|---|
| First 4 | Little-endian timestamp in milliseconds |
| Next 126 | One detection count for each channel |

The supplied analysis assumes **50 samples per channel** in the recording.

This setting belongs to the firmware that created the recording. It is separate from the 100-sample setting in the diagnostic scanner.

## Project Versions

`rf_scan.py` is a single-scan diagnostic version. It prints results but does not create the binary recording.

The OLED display and continuous-recording firmware are separate project versions and have not yet been added here.

## Skills Demonstrated

- MicroPython programming
- SPI communication
- Microcontroller and radio-module integration
- RF activity detection
- Binary data processing
- MATLAB visualisation
