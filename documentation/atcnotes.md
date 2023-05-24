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

* On the order im implementation:
    - Enter into atc
    - Remove from atc
    - tool change
    - TouchOffAll
* atc_toolchange.ngc: M6 Master Document
    * Modal Junk handling around the script as before
    * check if current tool is part of wheel
    * check if new tool is in wheel
    * if spindle NOT empty()
        * Empty spindle first
        * If tool is in ATC
            * signale ATC to move to previous pocket
            * signal animation
            * move to Safe front position at z0
            * check if ready and pocket empty
                * if: drop off
                * else: error out after time (ready) or on sensor
        * tool not from atc:
            * move to manual drop off position at G0
            * triggert Tx M6 dialog to engage hal_manualtoolchange
    * if spindle empty(): directly go to next steps
        * if new tool not in atc and old tool from atc:
            * go to manual tool change position and trigger Tx M6 for hal manual tool change
            * after confirm perform tool length check
            * exit
        * if new tool not in atc and old tool not in atc:
            * This won't happen and has been handled above
        * if new tool in atc:
            * check spindle empty directly 
            * call atc pocket
            * signal animation
            * g0 to safe top location
            * check ready and tool pocket empty
            * SpindleGetToolFromATC.ngc
            * M61 Qx
            * load tooloffset
            * end
* tool_touch_off.ngc: Macro to measure the currently loaded tool (and no other) *(DONE)*
* remove_tool_atc.ngc: Macro to fetch and remove a tool
    - Check if tool is in ATC
        - yes:
            -  Check if spindle is empty:
                - yes: continue
                - no: perform drop off of current tool
                    - if old tool from atc: drop off at atc
                    - if old tool from manual: drop off at manual position and TxM6 
            - call atc pocket
            - trigger animation
            - g0 to front safe location
            - wait for ready and check if pocket is not empty
            - Get Tool
            - Set pocketvariable to 0 to delete record of tool being in ATC
            - Move to Manual Handover Position and Trigger dialoge via T0 M6
        - else: abort with message
* enter_tool_atc.ngc: Macro to enter a tool into the ATC
    - Assumes that this is triggered from PB interface with a textfield that provides the tool number to be put to the wheel
    - Assume that whatever the number is, it is going to be put into the wheel
    - if new tool in wheel
        - msg: TOll already in wheel
        - exit
    - elif: newtool = 99
        - msg: Nope, no probes in the wheel dummy
        - exit
    - else: continue
        - determien wheel status: are there empty pockets (lowest empty pocket != 0)
        - if: wheel not empty:
            - msg error
            - abort
        - else:
        - if newtool!= toolinspindle
            - drop off the tool to whereever it goes
        - else
            - trigger wheel
            - move to safe front position
            - wait for ready and check empty
            - SpindlePutTooltoATC
            - M61Q0
            - Write data to pocketvariable
            - exit

* TouchOffAll.ngc: Touch of all tools in the wheel
    * for all non empty pockets:


* SubMacros
    * remove_tool_pocket.ngc: Only relevant spindle movement *(DONE)*       
    * put_tool_pocket.ngc: Only relevant spindle movement *(DONE)*

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

- When does the tool sensor trigger empty (check with fixed holder in pocket) and determien mm ==> safe distance Z (when the forks can do that) --> instant
- m21, m22: What does abort really do?


- add button and macro to fully empty atc (virtually)

- load_tool_atc animation logic is sketchy - check

## Bugs
* jog-fwd / jog-rev: stick to state 20 an do not perform align



#### Notes
- https://forum.linuxcnc.org/qtpyvcp/46629-qtpyvcp-probe-basic-changing-tool-table-entries-from-macro-or-script
- https://forum.linuxcnc.org/38-general-linuxcnc-questions/45564-atc-project-debug-phase?start=190
