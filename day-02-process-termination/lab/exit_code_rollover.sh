#!/bin/bash
# exit_code_rollover.sh - Testing 8-bit exit code truncation and signal exit codes

echo "=================================================="
echo "   LAB 1: EXIT STATUS CODES & 8-BIT ROLLOVER      "
echo "=================================================="

run_test() {
    local input_code="$1"
    local desc="$2"
    
    # Run in a subshell so our script does not terminate
    (exit "$input_code")
    local actual_code=$?
    
    printf "Input: %-6s | Description: %-30s | Stored in \$?: %s\n" "$input_code" "$desc" "$actual_code"
}

test_signal() {
    local sig_name="$1"
    local sig_num="$2"
    
    bash -c "kill -$sig_name \$\$" 2>/dev/null
    local actual_exit=$?
    printf "Signal: %-8s (Signal %-2s) | Expected: 128 + %-2s = %-3s | Actual \$?: %s\n" \
        "$sig_name" "$sig_num" "$sig_num" "$((128 + sig_num))" "$actual_exit"
}

echo "[1] Testing Standard and Boundary Exit Codes:"
run_test 0 "Success / Clean termination"
run_test 1 "Standard error / Catch-all"
run_test 42 "Arbitrary user error"
run_test 255 "Maximum 8-bit value"

echo -e "\n[2] Testing 8-Bit Overflow / Rollover:"
run_test 256 "Overflow (256 mod 256 = 0)"
run_test 257 "Overflow (257 mod 256 = 1)"
run_test 300 "Overflow (300 mod 256 = 44)"
run_test -1  "Negative integer (-1 mod 256 = 255)"

echo -e "\n[3] Testing Signal-Induced Termination Exit Codes (128 + N convention):"
test_signal SIGHUP 1
test_signal SIGINT 2
test_signal SIGKILL 9
test_signal SIGTERM 15
