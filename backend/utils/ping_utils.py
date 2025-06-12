import subprocess
import platform

def ping_ip(ip_address: str) -> bool:
    """
    Pings the given IP address once to check reachability.
    Returns True if reachable, False otherwise.
    """
    if not ip_address:
        return False

    # Use Windows-style or Unix-style ping based on OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", ip_address],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False
