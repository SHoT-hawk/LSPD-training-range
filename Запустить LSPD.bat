@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "LSPD Training Range" http://localhost:8080/
python -m http.server 8080 --bind 127.0.0.1
