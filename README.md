# LinuxCNC Config for groot2.0
Repository for all things related to the linuxCNC and MESA based control system of my CNC router groot2.0

_Status_: Experimental, expect substantial changes during setup. In other words: For the love of all that is holy: Don't try this at home. It couldn't possibly be more broken and machine specific.

## About the machine
* CNC router made from aluminium profile and plate based on a design by fraseserbruch.de
* Workspace XYZ approx. 650/1200/230 mm
* Key components
    * AC spindle Jianken JGL80 (2.2 kW, ISO20) driven by VFD Hitachi WJ20-022SF
    * All drives Delta A2 Series (Driver Delta ASDA-A2 0421L and Motors EMCA0604 series)
    * Control based on linuxCNC 2.8 and Mesa cards (7i76E + 7i84)
    * ATC Setup using rack stle toolchange (to come)
    * tool lenght sensor and 3D wireless touch probe
    * Pendant by talla83 with TSHW housing as designed by surmetal (see thingiverse)
    * Further features: Status lights, control consolde for start/stop and feed and spindle override

## About the config
* _Currently_ Manual tool change operated by a toogled push-button on Z axis
* in the process of being converted to probe_basic

## Useful Links 

* Physical override using poti https://forum.linuxcnc.org/24-hal-components/36336-physical-feed-override-knob?start=0
* Run/Step buttons https://forum.linuxcnc.org/47-hal-examples/13201-run-step-hold-resume-buttons?start=0
* GMOCCAPY Docu https://linuxcnc.org/docs/devel/html/gui/gmoccapy.html
* GMOCCAPY tool change: https://xpkiller.de/2016/12/06/automatische-werkzeuglaengenmessung/
* bin to hex converter https://www.rapidtables.com/convert/number/binary-to-hex.html
* 

## Useful Hints
* Serial communication common fixes: 
    * add cnc user to group dialout (debian) using usermod -a -G dialout username
    * additionally, consider chmod 777 for /dev/ttyUSB0 (or any other device tha tis used)
* Serial communication using modbus via TCP --> use socat
