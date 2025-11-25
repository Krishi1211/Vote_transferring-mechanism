@echo off
echo Starting Secure Vote-Transfer System...

start "Voting Node (Backend)" cmd /k "python app.py"
timeout /t 2 >nul
start "Observer Node (Dashboard)" cmd /k "python display_server.py"

echo.
echo System is running!
echo.
echo [1] Voter Booth:    http://localhost:5000
echo [2] Admin Dashboard: http://localhost:5001
echo.
echo Opening browsers...
start http://localhost:5000
start http://localhost:5001
