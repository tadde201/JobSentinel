# JobSentinel Login - PowerShell Script
# How to register and login to your API

# ============================================================
# STEP 1: REGISTER A NEW USER
# ============================================================
Write-Host "STEP 1: Register new user" -ForegroundColor Green

$email = "user_$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"
$fullName = "Test User"
$password = "short123"  # Keep passwords short to avoid bcrypt 72-byte limit

$registerBody = @{
    email = $email
    full_name = $fullName
    password = $password
} | ConvertTo-Json

Write-Host "Registering: $email"
Write-Host "POST http://localhost:8003/api/v1/auth/register"
Write-Host "Body: $registerBody"

$registerResponse = Invoke-WebRequest -Uri "http://localhost:8003/api/v1/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body $registerBody

$registerData = $registerResponse.Content | ConvertFrom-Json
$token = $registerData.access_token

Write-Host "Response Status: $($registerResponse.StatusCode)" -ForegroundColor Cyan
Write-Host "Access Token: $($token.Substring(0, 50))..." -ForegroundColor Yellow

# ============================================================
# STEP 2: LOGIN WITH CREDENTIALS
# ============================================================
Write-Host "`nSTEP 2: Login with email and password" -ForegroundColor Green

$loginBody = @{
    email = $email
    password = $password
} | ConvertTo-Json

Write-Host "Logging in: $email"
Write-Host "POST http://localhost:8003/api/v1/auth/login"

$loginResponse = Invoke-WebRequest -Uri "http://localhost:8003/api/v1/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody

$loginData = $loginResponse.Content | ConvertFrom-Json
$token = $loginData.access_token

Write-Host "Response Status: $($loginResponse.StatusCode)" -ForegroundColor Cyan
Write-Host "Access Token: $($token.Substring(0, 50))..." -ForegroundColor Yellow
Write-Host "Token Type: $($loginData.token_type)" -ForegroundColor Yellow

# ============================================================
# STEP 3: GET USER PROFILE (Protected Endpoint)
# ============================================================
Write-Host "`nSTEP 3: Get current user profile" -ForegroundColor Green

Write-Host "GET http://localhost:8003/api/v1/me"
Write-Host "Authorization: Bearer $($token.Substring(0, 20))..."

$profileResponse = Invoke-WebRequest -Uri "http://localhost:8003/api/v1/me" `
    -Method GET `
    -Headers @{Authorization = "Bearer $token"}

$profileData = $profileResponse.Content | ConvertFrom-Json

Write-Host "Response Status: $($profileResponse.StatusCode)" -ForegroundColor Cyan
Write-Host "User ID: $($profileData.user_id)" -ForegroundColor Yellow
Write-Host "Email: $($profileData.email)" -ForegroundColor Yellow
Write-Host "Name: $($profileData.full_name)" -ForegroundColor Yellow
Write-Host "Active: $($profileData.is_active)" -ForegroundColor Yellow

# ============================================================
# CREDENTIALS SUMMARY
# ============================================================
Write-Host "`n========== LOGIN CREDENTIALS ==========" -ForegroundColor Magenta
Write-Host "Email: $email" -ForegroundColor White
Write-Host "Password: $password" -ForegroundColor White
Write-Host "JWT Token: $token" -ForegroundColor White
Write-Host "======================================" -ForegroundColor Magenta
