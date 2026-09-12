# OverTheWire Bandit — Level Writeups

Personal log of each level solved, the command used, and the reasoning behind it — kept as proof-of-work for my cloud engineering roadmap, not just a password list. Updated as I clear levels; replayed blind every 10 levels to confirm retention.

---

## Level 0 → 1
**Task:** Log into the game for the first time via SSH.
**Command:**
```
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
**What I learned:** SSH's destination is written as one glued piece — `user@host` — not two separate arguments. Also learned `-p` is the flag for a non-default port; without it SSH silently tries port 22.

---

## Level 1 → 2
**Task:** Password stored in a file literally named `-` (a single dash) in the home directory.
**Command:**
```
cat ./-
```
**What I learned:** A leading `-` gets read as a command option, not a filename, so plain `cat -` just hangs waiting on stdin instead of erroring. Prefixing with `./` tells the shell "this is a path, read it literally."

---

## Level 2 → 3
**Task:** Password stored in a file named `--spaces in this filename--` (dashes and spaces).
**Command:**
```
cat -- "--spaces in this filename--"
```
(`cat "./--spaces in this filename--"` also works — same fix, different route.)
**What I learned:** `--` tells a command "stop parsing flags, everything after this is a literal argument." Quotes handle the spaces separately. First attempt failed because I put both the `--` and the filename inside one set of quotes, making it a single argument instead of two.

---

## Level 3 → 4
**Task:** Password stored in a hidden file (name starts with a dot) inside the `inhere` directory.
**Command:**
```
ls -la
cat ...Hiding-From-You
```
**What I learned:** `ls -la` is required to even see dotfiles — plain `ls` hides them. Also mixed up `cd` vs `cat` here — `cd` only works on directories, not files, which threw a "Not a directory" error until I corrected it.

---

## Level 4 → 5
**Task:** Ten files (`-file00` to `-file09`) in `inhere`; only one is human-readable.
**Command:**
```
file ./-file*
```
**What I learned:** `*` is a wildcard — the shell expands it into every matching filename *before* the command runs, so `file` checks all ten in one call. `file` reports content type (`ASCII text` vs `data`), which is different from `du` (size) or `ls` (metadata) — picking the right tool for "what's inside this" mattered here.

---

## Level 5 → 6
**Task:** Password file somewhere under 20 nested `maybehere` directories, with three properties: human-readable, exactly 1033 bytes, not executable.
**Command:**
```
find . -type f -size 1033c ! -executable
```
**What I learned:** `find` searches recursively through every subfolder automatically — the right tool once a manual folder-by-folder check isn't realistic. `-size 1033c` needs the `c` suffix for bytes (default unit is 512-byte blocks). `!` negates a filter (here, "not executable").

---

## Level 6 → 7
**Task:** Password file somewhere on the entire server, owned by user `bandit7`, group `bandit6`, 33 bytes.
**Command:**
```
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```
**What I learned:** Searching from `/` means `find` hits hundreds of folders with no permission to enter, each printing a "Permission denied" line on stderr. `2>/dev/null` redirects stream 2 (errors) specifically into a discard location, leaving stream 1 (the real result) visible. First tried `1>/dev/null` by mistake — that redirected the *correct* result into the void and left all the noise on screen, which is the exact opposite of what I wanted.

---

## Level 7 → 8
**Task:** Password is the value on the line containing the word "millionth" in `data.txt`.
**Command:**
```
grep millionth data.txt
```
**What I learned:** `grep`'s argument order is pattern-first, file-second. Had it backwards on the first try (`grep data.txt millionth`), which searched for the literal word "data.txt" inside a nonexistent file called "millionth."

---

## Level 8 → 9
**Task:** `data.txt` has every line duplicated except one, which appears exactly once.
**Command:**
```
sort data.txt | uniq -u
```
**What I learned:** `uniq` only catches duplicates sitting immediately next to each other — it doesn't scan the whole file. `sort` groups matching lines together first so `uniq` can actually compare them. `uniq -u` prints only lines with zero duplicates (plain `uniq` just collapses consecutive dupes to one copy, which isn't the same thing). The pipe (`|`) hands `sort`'s output straight into `uniq`'s input with nothing touching disk or screen in between.

---

## Level 9 → 10
**Task:** `data.txt` is mostly binary junk with a few human-readable strings, preceded by several `=` characters.
**Command:**
```
strings data.txt | grep '='
```
**What I learned:** `strings` pulls out only printable text from a file, dropping binary noise — different job from `grep`, which searches text but can't filter binary garbage cleanly on its own. Piped together: `strings` cleans the file down to readable lines, `grep '='` narrows further to the ones matching the goal's hint.

---

## Level 10 → 11 *(in progress)*
**Task:** `data.txt` contains a base64-encoded string.
**Command:**
```
base64 -d data.txt
```
**What I'm learning:** Base64 isn't encryption — it's a text-safe encoding using only letters, numbers, `+`, `/`, and `=` padding (the trailing `==` is the visual tell). `strings` just echoed the base64 text back unchanged here, since it was already printable ASCII — nothing to filter out. `-d` decodes it back to the original text.

---

## Tools used so far
`ssh` · `ls` · `cat` · `cd` · `pwd` · `file` · `du` · `find` · `grep` · `sort` · `uniq` · `strings` · `base64` · pipes (`|`) · redirects (`>`, `2>`)

## Recurring mistake pattern (from my own blind-replay quiz)
Forgetting the leading `-` on dash-prefixed filenames (`./-file*`, not `./file*`) — came up three separate times. Second pattern: initially described stdout/stderr as "succeeded vs failed" instead of two streams that are always both open, regardless of success.
