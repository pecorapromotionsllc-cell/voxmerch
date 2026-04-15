# VoxMerch Git setup script
# Run this from PowerShell on your Windows machine:
#   cd C:\Users\marya\Projects\VoxMerch
#   .\setup-git.ps1
#
# Prerequisites:
#   1. Git for Windows installed (https://git-scm.com/download/win)
#   2. A new PRIVATE GitHub repo named 'voxmerch' created at:
#      https://github.com/new   (leave it empty -- no README, no .gitignore, no license)
#   3. Your GitHub username handy

$ErrorActionPreference = "Stop"

Write-Host "==> Checking Git is installed..."
$gitVersion = git --version
Write-Host $gitVersion

Write-Host ""
Write-Host "==> Moving to project directory..."
Set-Location "C:\Users\marya\Projects\VoxMerch"

if (Test-Path ".git") {
    Write-Host "WARNING: .git already exists. Aborting so nothing is overwritten."
    Write-Host "If you want a fresh init, delete the .git folder first, then rerun."
    exit 1
}

Write-Host ""
Write-Host "==> git init (main branch)..."
git init -b main

Write-Host ""
Write-Host "==> Setting repo-local identity..."
git config user.name "Mary Anne Keane"
git config user.email "maryannekeane@gmail.com"
git config core.autocrlf input

Write-Host ""
Write-Host "==> Staging all files (respecting .gitignore)..."
git add -A

Write-Host ""
Write-Host "==> Files about to be committed:"
git status --short

Write-Host ""
Write-Host "==> Creating initial commit..."
git commit -m "Initial VoxMerch consolidation"

Write-Host ""
$username = Read-Host "Enter your GitHub username (the account that owns the new 'voxmerch' repo)"

Write-Host ""
Write-Host "==> Adding GitHub remote..."
git remote add origin "https://github.com/$username/voxmerch.git"

Write-Host ""
Write-Host "==> Pushing to GitHub (you may be prompted to authenticate)..."
git push -u origin main

Write-Host ""
Write-Host "Done. Repo is live at https://github.com/$username/voxmerch"
