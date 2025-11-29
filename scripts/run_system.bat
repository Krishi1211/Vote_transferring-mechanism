@echo off
echo ================================================
echo   Secure Vote-Transfer System - Startup
echo ================================================
echo.

cd /d "%~dp0.."

echo [1/3] Starting Voting Node (Backend)...
start "Voting Node (Backend)" cmd /k "cd server\voting_node && python app.py"

timeout /t 2 >nul

echo [2/3] Starting Observer Node (Dashboard)...
start "Observer Node (Dashboard)" cmd /k "cd server\observer_node && python display_server.py"

timeout /t 2 >nul

echo [3/3] Opening web interfaces...
echo.
echo ================================================
echo   System is running!
echo ================================================
echo.
echo   [1] Voter Booth:    http://localhost:5000
echo   [2] Admin Dashboard: http://localhost:5001
echo.
echo   Press Ctrl+C in server windows to stop
echo ================================================
echo.

start http://localhost:5000
timeout /t 1 >nul
start http://localhost:5001
