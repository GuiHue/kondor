# ATC Notes

## Macros
- M10: move best direction (Determine direction) --> not needed/ implemented as done by carousel.comp
- M11: ccw movement (with #p steps or p emtpy == 1 step) --> not needed/ implemented as done by carousel.comp
- M12: cw movement (with #p steps or p emtpy == 1 step) --> not needed/ implemented as done by carousel.comp
- M13: Homing/ Referencing

- M21 Clamp Tool and Check --> use as macro, not as custom gcode in hal
- M22 UnClamp Tool and Check --> use as macro, not as custom gcode in hal
- M23 Open Doors and CHeck --> not implemented
- M24 Close  Doors and Check --> not implemented

## Custom M Codes to make
- Enable --> M114
- Disable --> M115
- Write Pocket number --> M120 P#
- Force home --> M113
- Forward one pocket  --> M111 --> triggered from probe_basic UI
- Reverse one pocket --> M112 --> triggered from probe_basic UI
- Drawbar -->       M130 open, m131 close       
- Spindle Cone Clean Air Blast -->     m132 activate, m133 deactivate

## Pins to read
- homed --> DIN 00
- ready --> DIN 01
- current pocket atc AIN 00
- current pocket spindle AIN 01
- tool presence --> DIN 02
- sensor   drawbar --> DIN 04
- sensor tool in spindle --> DIN 03 (high when tool present)


## New Macro Structure

## Numbered Parameters of Probe_Basic
- #5191 ongoing --> typically used for tool to pocket relation
- #5170 --> current tool pocket persiste2nt
- #5171 --> homed
- #5231 --> tool in spindle, persistent
- #5399 result of m66

## Python Widget Functions
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.atc_message{}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.atc_message{"REFERENCING"}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.store_tool{#1, #2}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.rotate{#<Steps_to_move>, "cw"}])

## Check me

## Bugs

#### Notes
- https://forum.linuxcnc.org/qtpyvcp/46629-qtpyvcp-probe-basic-changing-tool-table-entries-from-macro-or-script
- https://forum.linuxcnc.org/38-general-linuxcnc-questions/45564-atc-project-debug-phase?start=190
