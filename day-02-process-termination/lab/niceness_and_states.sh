#!/bin/bash
# niceness_and_states.sh - Demonstrates nice values, renice, and process state transitions (S, T, R)

echo "=================================================="
echo "   LAB 4: PROCESS NICENESS & STATE TRANSITIONS    "
echo "=================================================="

# 1. Start a background worker with nice +10
echo "[1] Starting background worker with nice -n 10:"
nice -n 10 sleep 30 &
WORKER_PID=$!
echo "Worker started with PID: $WORKER_PID"

sleep 0.5

# 2. Inspect priority and nice value
echo -e "\n[2] Process priority in ps:"
ps -o pid,ni,pri,stat,comm -p "$WORKER_PID"

echo -e "\n[3] Raw nice value in /proc/$WORKER_PID/stat:"
# In /proc/[pid]/stat, field 18 is priority, field 19 is nice
awk '{print "PID: "$1" | Comm: "$2" | State: "$3" | Priority: "$18" | Nice: "$19}' /proc/"$WORKER_PID"/stat

# 3. Modify nice value using renice
echo -e "\n[4] Lowering priority further with renice -n 15:"
renice -n 15 -p "$WORKER_PID"
ps -o pid,ni,pri,stat,comm -p "$WORKER_PID"

# 4. State transitions: Stop process (State T)
echo -e "\n[5] Sending SIGSTOP to pause process (State T):"
kill -STOP "$WORKER_PID"
sleep 0.2
ps -o pid,ni,pri,stat,wchan:20,comm -p "$WORKER_PID"

# 5. State transitions: Resume process (State S / R)
echo -e "\n[6] Sending SIGCONT to resume process:"
kill -CONT "$WORKER_PID"
sleep 0.2
ps -o pid,ni,pri,stat,wchan:20,comm -p "$WORKER_PID"

# 6. Cleanup
kill -TERM "$WORKER_PID" 2>/dev/null
wait "$WORKER_PID" 2>/dev/null
echo -e "\n[*] Worker process $WORKER_PID reaped and cleaned up."
echo "=================================================="
