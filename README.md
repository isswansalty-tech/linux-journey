# Linux Journey

Personal developer study notes, terminal labs, and practical write-ups covering Linux kernel internals, process lifecycles, signal dispatching, systems engineering edge cases, and hands-on command-line challenges.

---

## Repository Index

### 1. [Day 1: Linux Process Fundamentals & Lifecycle](./day-01-linux-processes/day-01-linux-processes.md)
* **Part 1 (Mental Models):**
  * Programs vs. processes and instance isolation.
  * Kernel process accounting via `task_struct` (PID, PPID, UID/GID, memory maps, file descriptors).
  * CPU scheduling (CFS / EEVDF) and virtual address spaces (MMU page tables).
  * Process creation mechanics: the `fork()` + `execve()` execution loop.
  * `execve()` memory wipe and file descriptor survival (`O_CLOEXEC`).
  * PID 1 responsibilities, orphan adoption, and why running apps as PID 1 in containers causes zombie leaks.
* **Part 2 (Practical Labs):**
  * [`lab/inspect_proc.sh`](./day-01-linux-processes/lab/inspect_proc.sh): Inspecting `/proc/<PID>/cmdline`, `status`, and open file descriptors.
  * [`lab/orphan_demo.py`](./day-01-linux-processes/lab/orphan_demo.py) & [`lab/orphan_demo.sh`](./day-01-linux-processes/lab/orphan_demo.sh): Spawning child processes, parent termination, and orphan reparenting.
  * [`lab/fd_cloexec_demo.py`](./day-01-linux-processes/lab/fd_cloexec_demo.py): Demonstrating file descriptor leakage across `execve()` memory wipes.

---

### 2. [Day 2: Process Termination, Signals & Lifecycle States](./day-02-process-termination/day-02-process-termination.md)
* **Part 1 (Mental Models):**
  * Exit status codes and the strict 8-bit boundary (`status & 0xFF`, `$?`, rollover bug).
  * The waiting and reaping cycle: memory cleanup vs. process table persistence.
  * Zombie process anatomy, PID table starvation, and immunity to `SIGKILL`.
  * Asynchronous signals, keyboard traps (`Ctrl+C`, `Ctrl+Z`), and kernel faults (`SIGSEGV`).
  * Signal reactions: default actions (`SIG_DFL`), ignoring (`SIG_IGN`), userland catching, and uncatchable signals (`SIGKILL`, `SIGSTOP`).
  * Non-destructive process probing via `kill -0`.
  * Niceness, scheduling priorities ($PR = 20 + NI$), and dynamic adjustment via `renice`.
  * Kernel process states (`R`, `S`, `D`, `Z`, `T`) and `/proc/<PID>/wchan` wait channels.
  * State transition Mermaid diagram.
  * Production / SRE gotchas: exit 256 false positives in CI/CD, zombie storms, unkillable `D`-state storage deadlocks.
* **Part 2 (Practical Labs):**
  * [`lab/exit_code_rollover.sh`](./day-02-process-termination/lab/exit_code_rollover.sh): Verifying 8-bit integer truncation and `128 + N` signal exit conventions.
  * [`lab/zombie_lifecycle.py`](./day-02-process-termination/lab/zombie_lifecycle.py): Reproducing `<defunct>` zombie processes, testing `kill -9` resistance, and harvesting exit codes with `os.waitpid()`.
  * [`lab/signal_matrix.py`](./day-02-process-termination/lab/signal_matrix.py): Testing signal catch handlers, ignoring `SIGUSR1`, kernel errors trapping `SIGKILL`, and `kill -0` probing.
  * [`lab/niceness_and_states.sh`](./day-02-process-termination/lab/niceness_and_states.sh): Adjusting nice levels with `renice`, toggling `S` -> `T` -> `S` states via `SIGSTOP`/`SIGCONT`, and reading wait channels.

---

### 3. [OverTheWire Bandit Writeups](./bandit.md)
* Practical command-line and security challenge solutions (Levels 0 through 11+).
* Explanations covering dash-prefixed files, paths with whitespace, hidden dotfiles, file inspection with `file`, recursive directory filtering with `find`, text manipulation with `sort`/`uniq`/`strings`, base64 decoding, stream redirection (`2>/dev/null`), and SSH port routing.

---

## Directory Layout

```text
linux-journey/
├── README.md                          # Repository documentation index
├── bandit.md                          # OverTheWire Bandit level writeups
├── day-01-linux-processes/            # Day 1: Process Fundamentals
│   ├── README.md                      # Day 1 writeup copy
│   ├── day-01-linux-processes.md      # Full Day 1 notes & lab outputs
│   └── lab/                           # Executable lab scripts
│       ├── fd_cloexec_demo.py
│       ├── inspect_proc.sh
│       ├── orphan_demo.py
│       └── orphan_demo.sh
└── day-02-process-termination/        # Day 2: Process Termination & Signals
    ├── README.md                      # Day 2 writeup copy
    ├── day-02-process-termination.md  # Full Day 2 notes & lab outputs
    └── lab/                           # Executable lab scripts
        ├── exit_code_rollover.sh
        ├── niceness_and_states.sh
        ├── signal_matrix.py
        └── zombie_lifecycle.py
```
