@echo off
setlocal

REM Optional commit message argument
set MSG=%*
if "%MSG%"=="" set MSG=.

echo Adding files...
git add .

echo Committing...
git commit -m "%MSG%"

echo Pushing to main...
git push origin main

echo Done.
pause