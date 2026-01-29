@echo off
echo Starting Coddy AI System...

:: Start Backend API in a new window
start "Coddy API Server" cmd /k "python api.py"

:: Wait a moment for API to initialize
timeout /t 5 /nobreak

:: Start Frontend
cd frontend
echo Starting Frontend...
npm run dev
