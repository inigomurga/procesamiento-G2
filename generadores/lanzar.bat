@echo off
setlocal enabledelayedexpansion

for /L %%i in (1,1,10) do (
    start python molino.py %%i
)

echo Molinos iniciados...
