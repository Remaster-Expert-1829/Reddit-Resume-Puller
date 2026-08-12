import subprocess
import sys

def install_requirements():
    print("Installing required Python packages...")
    packages = [
        "playwright"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
            sys.exit(1)
            
    print("\nAll requirements installed successfully!")
    print("You can now run the backend servers or the main script.")

if __name__ == "__main__":
    install_requirements()
