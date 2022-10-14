# LinuxCNC Config for groot2.0
_WARNING_: The MAIN BRANCH of this repo has been moved to linuxcnc 2.9 with probe_basic GUI  on October 8, 2022. Branches in this repository are generally outdated and not maintained. 

Repository for all things related to the linuxCNC and MESA based control system of my CNC router groot2.0. You're welcome to fork, however, push requests will not be considered as the main purpose of this repo is VC for myself.

_Status_: This is a work in progress, expect substantial changes over time. In other words: For the love of all that is holy: Don't try this at home. It couldn't possibly be more broken and machine specific.

## About the machine
* CNC router made from aluminum profile and plate based on a design by fraseserbruch.de
* Workspace XYZ approx. 650/1200/230 mm
* Key components
    * ATC spindle Jianken JGL80 (2.2 kW, ISO20) driven by VFD Hitachi WJ20-022SF
    * All drives Delta A2 Series (Driver Delta ASDA-A2 0421L and Motors EMCA0604 series) interface based on step/dir
    * 4th axis (A Axis) using Nema 34 Stepper and Step/Dir Interface
    * Control based on linuxCNC 2.9 and Mesa cards (7i76E + 7i84)
    * ATC Setup using a carousel style tool change based on probe_basic and carousel.comp (to come)
    * tool lenght sensor and 3D wireless touch probe
    * Pendant by talla83 with TSHW housing as designed by surmetal (see thingiverse) (depreceated)
    * xhc-whb04b-6 wireless 4 axis pendant
    * Further features: Status lights, control console for start/stop and feed and spindle override

## About the config
* LinuxCNC 2.9 pre (following master)
* Debian 11 Bookworm with Preempt-rt kernel 
* GUI: QtPyVCP based Probe_basic (python3) with several modifications to the gui file

## Useful Links 
* General LinuxCNC items:
    * Physical override using poti https://forum.linuxcnc.org/24-hal-components/36336-physical-feed-override-knob?start=0
    * Run/Step buttons https://forum.linuxcnc.org/47-hal-examples/13201-run-step-hold-resume-buttons?start=0
    * bin to hex converter https://www.rapidtables.com/convert/number/binary-to-hex.html
    * Install deb11 (bullseye) for linxucnc: https://gnipsel.com/linuxcnc/debian-11.html (i use XFCE as GUI)
    
* Probe_Basic related
    * Offizial documentation to install qtpyvcp: https://www.qtpyvcp.com/install/index.html
    * For BULLSEYE: USE THIS: https://www.qtpyvcp.com/install/bullseye.html
    * Installing lxcnc 2.9 on Bullseye (deb11) install script: https://github.com/joco-nz/lcnc-bullseye-installer (Note: This may miss some dependencies)
    * Good Info on installing PB with dependency infos: https://www.forum.linuxcnc.org/9-installing-linuxcnc/43506-buildbot-debian-11-bullseye-questions?start=0#220493
    * Installing PB (dev): https://kcjengr.github.io/probe_basic/dev_install.html 
    * Migrate working config to PB: https://forum.linuxcnc.org/qtpyvcp/44889-probe-basic-config-conversion-doc
    * qtpyvcp doc: https://www.qtpyvcp.com/
* GMOCCAPY related
    * GMOCCAPY Docu https://linuxcnc.org/docs/devel/html/gui/gmoccapy.html
    * GMOCCAPY tool change: https://xpkiller.de/2016/12/06/automatische-werkzeuglaengenmessung/


## Useful Hints
* Serial communication common fixes: 
    * add cnc user to group dialout (debian) using usermod -a -G dialout username
    * additionally, consider chmod 777 for /dev/ttyUSB0 (or any other device that is used)
* Serial communication using modbus via TCP --> use socat

## Cooking Mesa Bitfiles
* Installing ISE 14_7
   * May require license to be downloaded for ise webpack - follow acquire license link
   * install via VirtualBox current version and import image from 14GB Download  
* Making a firmware
   * make sure that there are exactly 32 lines in the first array
   * Pick configs from others as needed
   * get rid of additional features with empty pins to avoid dealing with the indexes
   * muxed encoders only on supported boards (i.e. 7i85   )
   * make sure the counts for stepgen etc are right
   * index and array errors point to fuck-ups above
   * Mesaflash: https://www.mankier.com/1/mesaflash
* Useful links
   * http://wiki.linuxcnc.org/cgi-bin/wiki.pl?Editing_MESA_Bitfiles
   * https://forum.linuxcnc.org/27-driver-boards/45581-mesa-7i76e-xilinix-bitfile-creation
