# gas-module-pi

## Raspberry Pi Gas Detection Module

### Installation

#### 1. Clone the repository to /home/pi direcotry

#### 2. Create a daemon for the gas module by copying the gas-module-pi.service to /etc/systemd/system

`sudo cp gas-module/gas-module-pi.service /etc/systemd/system`

`sudo systemctl start gas-module-pi.service`

`sudo systemctl enable gas-module-pi.service`

## Running Manually

Run the gas module manually with `/usr/bin/env python3 /home/pi/gas-module/gas.py`

## Troubleshooting and Maintenance
`sudo systemctl stop gas-module-pi.service`

## Wiring Diagram

![Wiring Diagram](https://github.com/ericlu5988/gas-module-pi/blob/master/Pi-Gas-Module.png)
