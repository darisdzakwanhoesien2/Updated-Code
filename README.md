# Project Notes and Fixes

This repository is primarily a collection of Jupyter notebooks plus a few Python scripts under `NTU Drone Programming, 1st October 2019/`.

On **2026-05-31** I audited the Python scripts, fixed clear bugs/broken logic, and cleaned up a few rough edges so the scripts are safer to run and easier to understand.

## 1) Bugs, errors, or broken logic identified

### `NTU Drone Programming, 1st October 2019/MainFlight.py`
- **Invalid local bind address**: `local1_address` was set to `(' ', 9000)` (a single space). This can fail to bind on many systems.
- **Potential infinite hang**: the receive thread called `recvfrom()` in a tight loop without a timeout, so it can block forever if no packets arrive.
- **Resource cleanup risk**: sockets/threads were not coordinated for shutdown.

### `NTU Drone Programming, 1st October 2019/BoxFlight.py`
- **Crash on exit**: script tried to close `sock2`, but `sock2` was never defined (`NameError`).
- **`yaw_direction` not used**: variable was defined but the code always sent `"cw ..."` (logic inconsistency / redundancy).
- **Potential infinite hang**: same “blocking receive forever” issue as above.

### `NTU Drone Programming, 1st October 2019/Swarm Box Flight.py`
- **Potential infinite hang**: receive loop could block forever waiting for 4 responses.
- **Minor typo**: comment marker said `PAS` instead of `PAST`.

### `NTU Drone Programming, 1st October 2019/Network Testing.py`
- **Deprecated API**: uses `networkx.from_pandas_dataframe(...)` which is deprecated in modern `networkx`.

## 2) Fixes applied

### Safer UDP receive loops
For the drone scripts:
- Added `sock.settimeout(1.0)` so `recvfrom()` won’t block forever when the drone(s) are unreachable.
- Added a `threading.Event()` (`stop_event`) to allow the background receive thread to exit cleanly.

### Concrete bug fixes
- `MainFlight.py`: changed `local1_address` to `('', 9000)` (bind all local interfaces).
- `BoxFlight.py`: removed the invalid `sock2.close()` call and used `yaw_direction` consistently.
- `Network Testing.py`: replaced deprecated `nx.from_pandas_dataframe(...)` with `nx.from_pandas_edgelist(...)`.

## 3) Cleanup (redundancy / readability)

- `MainFlight.py`: wrapped the mission logic in a `main()` function and used `if __name__ == "__main__":` for cleaner execution/cleanup.
- `BoxFlight.py`: used `_` as the loop variable when it isn’t used.
- Small readability tweaks (f-strings / consistent messaging) where it didn’t change behavior.

## 4) Inline comments for complex logic

Inline comments were added only where the logic is non-obvious:
- Why command delays exist (Tello can drop/ignore commands when sent too quickly).
- Why socket timeouts + a `stop_event` are used (avoid indefinite hangs; allow graceful shutdown of a background receive thread).

## 5) What changed and why (summary)

- Added `notes.md` as the “old README destination”. No root `README.md` existed at the time, so `notes.md` records that fact.
- Fixed runtime errors (`sock2.close()` in `BoxFlight.py`) so scripts don’t crash at shutdown.
- Fixed potentially broken network binding (`' '` → `''`) and prevented infinite blocking receives by adding socket timeouts and stop events.
- Updated a deprecated `networkx` call to its modern equivalent to reduce warnings/breakage on newer environments.
- Refactored lightly for clarity without changing the intended drone mission logic.

## Quick verification

These scripts were verified to at least parse/compile under Python 3 via:
- `python3 -m py_compile ...`

No end-to-end flight tests were run (that requires actual Tello hardware and network access to the drones).
