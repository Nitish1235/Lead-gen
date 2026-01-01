@echo off
echo Starting Full Stack Application...
echo.
echo Starting Backend API Server...
start "Backend API" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Development Server...
start "Frontend Dev" cmd /k "cd frontend && npm run dev"
echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Close these windows to stop the servers.
pause

