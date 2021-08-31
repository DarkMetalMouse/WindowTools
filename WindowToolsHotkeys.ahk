#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


F13::
;^!Space::
Run pythonw.exe "D:\programming\WindowTools\SwitchDisplays.pyw"
sleep, 250
return

rotated := 0
F14::
#^r::
if(rotated == 1) {
    Run, %ComSpec% /c "display64 /rotate 0"
    rotated = 0
} else {
    Run, %ComSpec% /c "display64 /rotate 90"
    rotated = 1
}
sleep, 250
return

F16::
#y::  
Winset, Alwaysontop, , A

