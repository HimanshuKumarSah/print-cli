import subprocess
import sys
import os
import platform

def install():
    print("Installing Print CLI...")
    try:
        # Install the current directory in editable mode
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("\nSUCCESS: Print CLI has been installed.")
        
        # Path Check Logic
        os_type = platform.system()
        if os_type == "Windows":
            # Typical location for user-installed scripts on Windows
            scripts_dir = os.path.join(os.environ.get("APPDATA", ""), "Python", f"Python{sys.version_info.major}{sys.version_info.minor}", "Scripts")
            path_env = os.environ.get("PATH", "").split(os.pathsep)
            
            if scripts_dir not in path_env:
                print(f"\n[!] WARNING: Your Python Scripts directory is not in your PATH.")
                print(f"    Location: {scripts_dir}")
                print("    To fix this, you should add this directory to your environment variables.")
                
                try:
                    import ctypes
                    if ctypes.windll.shell32.IsUserAnAdmin():
                        print("    Attempting to add to PATH automatically...")
                        # Simple logic to add to user PATH if admin
                        subprocess.run(["powershell", "-Command", f"[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';{scripts_dir}', 'User')"], check=True)
                        print("    PATH updated! Please restart your terminal.")
                    else:
                        print("    (Run this script as Administrator to attempt automatic PATH fixing.)")
                except Exception:
                    pass
        
        print("\nTest the command by typing: print-cli --help")
        
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Installation failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    install()
