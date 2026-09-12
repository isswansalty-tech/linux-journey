#!/usr/bin/env python3
"""
zombie_lifecycle.py - Demonstrates zombie process creation, /proc persistence,
SIGKILL immunity, and clean parent reaping.
"""
import os
import sys
import time
import signal
import subprocess

def main():
    print("==================================================")
    print("   LAB 2: ZOMBIE PROCESS LIFECYCLE & REAPING      ")
    print("==================================================")
    
    parent_pid = os.getpid()
    print(f"[*] Parent Process PID: {parent_pid}")
    sys.stdout.flush()
    
    # Fork child process
    child_pid = os.fork()
    
    if child_pid == 0:
        # Child process execution
        my_pid = os.getpid()
        print(f"[+] [Child:  {my_pid}] Spawned with PPID {os.getppid()}. Exiting immediately with status 42...")
        sys.stdout.flush()
        sys.exit(42)
    
    # Parent process execution
    print(f"[*] [Parent: {parent_pid}] Forked Child PID: {child_pid}")
    print(f"[*] [Parent: {parent_pid}] Intentionally sleeping for 2 seconds without calling wait()...")
    sys.stdout.flush()
    time.sleep(1) # Allow child to exit and kernel to mark as zombie
    
    # Check child status in /proc
    proc_status_path = f"/proc/{child_pid}/status"
    if os.path.exists(proc_status_path):
        print(f"\n--- Reading {proc_status_path} while child is un-reaped ---")
        with open(proc_status_path, "r") as f:
            for line in f:
                if any(line.startswith(prefix) for prefix in ("Name:", "State:", "Pid:", "PPid:", "VmSize:", "VmRSS:")):
                    print(line.strip())
        sys.stdout.flush()
    
    # Check ps output
    print(f"\n--- Process table view (ps) ---")
    sys.stdout.flush()
    subprocess.run(["ps", "-o", "pid,ppid,stat,cmd", "-p", str(child_pid)])
    
    # Attempting to kill the zombie with SIGKILL
    print(f"\n[*] [Parent: {parent_pid}] Attempting to kill Zombie ({child_pid}) using SIGKILL (kill -9)...")
    try:
        os.kill(child_pid, signal.SIGKILL)
        print(f"[-] [Parent: {parent_pid}] Signal delivered, but checking process state:")
    except ProcessLookupError:
        print(f"[-] [Parent: {parent_pid}] Process already gone.")
    sys.stdout.flush()
        
    subprocess.run(["ps", "-o", "pid,ppid,stat,cmd", "-p", str(child_pid)])
    print("[!] Notice: State is still 'Z'. A dead process cannot be killed.")
    
    # Parent reaps the child
    print(f"\n[*] [Parent: {parent_pid}] Reaping child via os.waitpid({child_pid}, 0)...")
    reaped_pid, exit_status_raw = os.waitpid(child_pid, 0)
    exit_code = os.WEXITSTATUS(exit_status_raw)
    print(f"[+] [Parent: {parent_pid}] Successfully reaped PID {reaped_pid} with Exit Code: {exit_code}")
    
    # Confirm removal from /proc
    time.sleep(0.5)
    still_exists = os.path.exists(proc_status_path)
    print(f"[*] [Parent: {parent_pid}] Does /proc/{child_pid} exist? {still_exists}")
    print("==================================================")

if __name__ == "__main__":
    main()
