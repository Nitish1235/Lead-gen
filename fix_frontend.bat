@echo off
echo Stopping any running Next.js processes...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *Next*" 2>nul

echo.
echo Clearing Next.js cache...
cd frontend
if exist .next (
    rmdir /s /q .next
    echo [OK] Cache cleared
) else (
    echo [INFO] No cache folder found
)

echo.
echo Starting frontend server...
call npm run dev


