#!/usr/bin/env python3
"""
signal_matrix.py - Demonstrates signal handling modes (Catch, Ignore, Default),
uncatchable signals (SIGKILL, SIGSTOP), and non-destructive probing via kill -0.
"""
import os
import sys
import time
import signal

def custom_handler(signum, frame):
    sig_name = signal.Signals(signum).name
    print(f"[!] [Caught] Received {sig_name} ({signum}). Executing cleanup before shutdown...")
    print("[!] [Cleanup] Flushing buffers, closing connections, saving state.")
    sys.exit(0)

def probe_process(pid):
    """Uses kill -0 to probe PID existence and access permissions without sending a signal."""
    try:
        os.kill(pid, 0)
        return True, "Process exists and signaling is permitted"
    except ProcessLookupError:
        return False, "Process does not exist (ESRCH)"
    except PermissionError:
        return True, "Process exists, but permission is denied (EPERM)"

def main():
    my_pid = os.getpid()
    print("==================================================")
    print(f"   LAB 3: SIGNAL HANDLING MATRIX (PID: {my_pid})   ")
    print("==================================================")

    # 1. Catching signals
    print("\n[1] Testing Signal Catching (SIGINT / SIGTERM):")
    signal.signal(signal.SIGTERM, custom_handler)
    print("Registered custom_handler for SIGTERM (15).")

    # 2. Ignoring signals
    print("\n[2] Testing Signal Ignoring (SIGUSR1):")
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    print("Configured SIGUSR1 (10) to SIG_IGN (Ignore).")
    print(f"Sending SIGUSR1 to self ({my_pid})...")
    os.kill(my_pid, signal.SIGUSR1)
    print("Process survived SIGUSR1 without interruption.")

    # 3. Uncatchable / Unignorable signals (SIGKILL & SIGSTOP)
    print("\n[3] Testing Uncatchable Signals (SIGKILL & SIGSTOP):")
    for sig in [signal.SIGKILL, signal.SIGSTOP]:
        try:
            signal.signal(sig, custom_handler)
        except (OSError, ValueError) as e:
            print(f"Caught expected error attempting to trap {sig.name} ({sig.value}): {e}")

    # 4. Probing with kill -0
    print("\n[4] Testing Process Probing via kill -0 (Signal 0):")
    exists, reason = probe_process(my_pid)
    print(f"Probe self (PID: {my_pid}): Exists = {exists} -> {reason}")

    fake_pid = 999999
    exists, reason = probe_process(fake_pid)
    print(f"Probe non-existent (PID: {fake_pid}): Exists = {exists} -> {reason}")

    # 5. Triggering the caught signal
    print("\n[5] Triggering graceful exit via SIGTERM to self:")
    os.kill(my_pid, signal.SIGTERM)

if __name__ == "__main__":
    main()
