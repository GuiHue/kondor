# ATC Notes

## Python Widget Functions
![Annotated Screenshot of ATC Page](Isolated.png "ATC Page with Standard Linked Macros")

(DEBUG, EVAL[vcp.getWidget{"dynatc"}.atc_message{}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.atc_message{"REFERENCING"}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.store_tool{#1, #2}])
(DEBUG, EVAL[vcp.getWidget{"dynatc"}.rotate{#<Steps_to_move>, "cw"}])


## Macros
- m10: move best direction (Determine direction) --> not needed
- m11: ccw movement (with #p steps or p emtpy == 1 step) --> not needed
- m12: cw movement (with #p steps or p emtpy == 1 step)
- m13: Homing/ Referencing

- m21: move carousel to tool change position - OUT (removes tool)
- m22 Move Carousel to the home position - IN
- m23 - m26: unused

https://github.com/kcjengr/probe_basic/blob/main/configs/probe_basic/subroutines/toolchange.ngc
- see for example of abort script with message

- store_tool_in_carousel.ngc ??
- toolsetter_wco.ngc - measure tool currently in spindle and store

## New Macro Structure

* On the order im implementation:
    - Tool Measurement
    - Spindle PUT REMOVE
    - Enter into atc
    - Remove from atc
    - tool change
    - TouchOffAll
* ATCToolchange.ngc: M6 Master Document
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
* ToolLenghtMeasurement.ngc: Macro to measure the currently loaded tool (and no other)
    - from whereever the spindle is with the tool in the spindle 
    - G53 G0 Z0, G53 G0 XY TS
    - Perform Measurement
    - Calculate and store offset
* RemoveToolFromATC.ngc: Macro to fetch and remove a tool
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
* PlaceToolinATC.ngc: Macro to enter a tool into the ATC
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
    * SpindleGetToolFromATC.ngc: Only relevant spindle movement
        * Only the spindle motions, no interaction with ATC (avoids) stupid parameters
        * Check if spindle is empty, otherwise abort 
        * From safe position move to Safe Position above pocket at G0
        * open and blowout spindle (check drawbar)
        * move down G0 and G1
        * air off, final move
        * clamp, check for tool presence and drawbar state
        * move out of pocket safely
        * G53 G0 Z0 once clear
    * SpindlePutTooltoATC.ngc: Only relevant spindle movement
        * Only the spindle motions, no interaction with atc
        * Check if tool in spindle
        * at G53 G0Z0 move to safe location in front of pocket
        * move to Z height for Pocket
        * move Y into pocket
        * unclamp
        * raise Z slightly at G1
        * spindle empty? 
        * blowoff  on
        * move to G53 Z0
        * blowoff off
        * drawbar close + check


## Numbered Parameters of Probe_Basic

- #5191 ongoing --> typically used for tool to pocket relation
- #5170 --> current tol pocket persiste2nt
- #5171 --> homed
- #5231 --> tool in spindle, persistent
- #5399 result of m66

## Custom M Codes to make
- enable --> M114
- Disable --> M115
- pocket number --> M120 P#
- force home --> M113
- forward one  --> M111
- reverse one --> M112
- Drawbar (maybe through M65)       M130 open, m131 close       ==> try to interlock this with spindle! - sort of safe, since spindle cannot be satrted... due to no tool
- spindle air blast     m132 activate, m133 deactivate      ==> CAREFUL: THESE ARE NOT CHECKED

## Pins to read
- homed --> DIN 00
- ready --> DIN 01
- current pocket atc AIN 00
- current pocket spindle AIN 01
- tool presence --> DIN 02
- tool sensor drawbar --> DIN 04
- tool sensor in spindle --> DIN 03


## This is the way / ToDo

* Use probe_basic persistent variables to store what tools are in the carousel
* in M6 Macro: Check if <requested_tool> is in any of the Carousel Pockets (see toolchange.ngc for effective code to do that)
* remove programmable coolant shit
* find a way to trigger homing through custom script --> set #5171 homed (or use pin), furthermore: issue vcp.getWidget("dynatc")... statement to display "home" - "Ready" etc.

trigger MDI commands from HAL using: https://linuxcnc.org/docs/html/man/man1/halui.1.html
halui.mod-command-xx systematics --> could be used to triggert homing

https://forum.linuxcnc.org/qtpyvcp/46629-qtpyvcp-probe-basic-changing-tool-table-entries-from-macro-or-script
https://forum.linuxcnc.org/38-general-linuxcnc-questions/45564-atc-project-debug-phase?start=190

## Bugs

* jog-fwd / jog-rev: stick to state 20 an do not perform align

