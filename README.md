# gas-module

##Python Gas Module with Raspberry Pi

###Clone the repository to /home/pi direcotry

###Run the gas module manually with /usr/bin/env python3 /home/pi/gas-module/gas.py

###Create a daemon for the gas module by copying the gas-module-pi.service to /etc/systemd/system
`<sudo cp gas-module/gas-module-pi.service /etc/systemd/system>`
`<sudo systemctl start gas-module-pi.service>`
`<sudo systemctl enable gas-module-pi.service>`

###To stop the gas module for troubleshooting and maintenance
`<sudo systemctl stop gas-module-pi.service>`

##Wiring Diagram

![Wiring Diagram](https://github.com/ericlu5988/gas-module-pi/blob/master/Pi-Gas-Module.png)
