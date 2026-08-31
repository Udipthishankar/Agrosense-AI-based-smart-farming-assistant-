#!/usr/bin/env python3
"""
AgroSense Deployment Assistant
Quick setup for Heroku, Railway, or Render deployment
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Success: {description}")
    return True

def check_requirements():
    """Check if all requirements are met"""
    print("\n" + "="*60)
    print("🔍 CHECKING DEPLOYMENT REQUIREMENTS")
    print("="*60)
    
    checks = {
        "git": "Git installed",
        "python": "Python 3.8+ installed",
        "pip": "pip installed"
    }
    
    for cmd, desc in checks.items():
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            print(f"✅ {desc}")
        except:
            print(f"❌ {desc} - MISSING")
            return False
    
    return True

def setup_git():
    """Setup Git repository"""
    if not os.path.exists('.git'):
        print("\n🔄 Initializing Git repository...")
        run_command("git init", "Initialize Git")
        run_command("git add .", "Stage all files")
        run_command("git commit -m 'Initial commit - AgroSense deployment'", "Commit files")
        return True
    else:
        print("\n✅ Git repository already initialized")
        return True

def setup_heroku():
    """Setup Heroku deployment"""
    print("\n" + "="*60)
    print("🟣 HEROKU DEPLOYMENT SETUP")
    print("="*60)
    
    # Check Heroku CLI
    try:
        subprocess.run(["heroku", "--version"], capture_output=True, check=True)
        print("✅ Heroku CLI installed")
    except:
        print("❌ Heroku CLI not found")
        print("   Install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Login to Heroku
    print("\nLogging into Heroku...")
    run_command("heroku login", "Heroku login")
    
    # Get app name
    app_name = input("\n📝 Enter your Heroku app name (or press Enter to skip): ").strip()
    
    if app_name:
        # Create app
        run_command(f"heroku create {app_name}", f"Create Heroku app '{app_name}'")
        
        # Deploy
        if setup_git():
            run_command("git push heroku main", "Deploy to Heroku")
            print(f"\n🎉 Deployed! Your app is at: https://{app_name}.herokuapp.com")
            return True
    
    return False

def setup_railway():
    """Setup Railway deployment"""
    print("\n" + "="*60)
    print("🚂 RAILWAY DEPLOYMENT SETUP")
    print("="*60)
    print("""
Railway makes deployment super easy:

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Authorize GitHub and select your repository
4. Railway auto-detects Python and deploys!

No need to install CLI tools - fully web-based deployment.
    """)
    
    input("Press Enter when done with Railway setup...")

def setup_render():
    """Setup Render deployment"""
    print("\n" + "="*60)
    print("🎨 RENDER DEPLOYMENT SETUP")
    print("="*60)
    print("""
Render offers easy deployment with auto-deploys from GitHub:

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure build command: pip install -r backend/requirements.txt
6. Configure start command: gunicorn backend.app:app
7. Deploy!

Your app will auto-deploy on every git push.
    """)
    
    input("Press Enter when done with Render setup...")

def main():
    """Main deployment assistant"""
    print("\n" + "="*60)
    print("🚀 AGROSENSE DEPLOYMENT ASSISTANT")
    print("="*60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install missing requirements and try again")
        sys.exit(1)
    
    # Setup Git
    if not setup_git():
        print("\n❌ Git setup failed")
        sys.exit(1)
    
    # Choose deployment platform
    print("\n" + "="*60)
    print("📱 CHOOSE DEPLOYMENT PLATFORM")
    print("="*60)
    print("""
1. Heroku (Cloud, Easy, Free tier available)
2. Railway (Cloud, Simple, Free tier)
3. Render (Cloud, Auto-deploy, Free tier)
4. Exit
    """)
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        setup_heroku()
    elif choice == "2":
        setup_railway()
    elif choice == "3":
        setup_render()
    elif choice == "4":
        print("\nExiting deployment assistant...")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("📖 FOR MORE INFORMATION")
    print("="*60)
    print("✓ Read: DEPLOYMENT.md")
    print("✓ Read: HEROKU_QUICK_START.md")
    print("✓ Check: backend/README.md")

if __name__ == "__main__":
    main()
