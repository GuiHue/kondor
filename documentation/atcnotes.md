# ATC Notes

## General Function of Probe_Basic

### List of connected macros from interface

### Python Widget Functions
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


## Numbered Parameters of Probe_Basic

### toolchange.ngc
- holds a list of all pockets

- #5191 ongoing --> typically used for tool to pocket relation

#5170 --> current tol pocket persiste2nt
#5171 --> homed

#5231 --> tool in spindle, persistent


#5399 result of m66

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

