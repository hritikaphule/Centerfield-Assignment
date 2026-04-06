# Python Technical Assignments

Solutions for two data processing tasks: managing live event streams and analyzing meeting attendance patterns.

---

## 1. Event Stream Processor (`event_stream.py`)

Collects user-activity events into batches of a given size, then computes per-batch stats (average value, max value, unique users).

### What I focused on beyond the basic requirements

- Validation before buffering — Invalid records (wrong type, missing keys, no user_id in metadata) are filtered out before they ever enter the buffer, preventing corruption of batch calculations.

- Debug mode — When debug=True, events are printed to stdout and the buffer is cleared without computing metrics, allowing inspection of raw data flow.

- Clear batching behavior — The implementation processes only full batches. Any leftover events that do not fill the buffer are ignored. In a production system, this could be extended to flush remaining events to avoid data loss.

### Edge cases covered

- Empty event list or buffer_size <= 0 → returns []
- Buffer larger than event count → no batch is processed, returns []
- All records invalid → returns [] without crashing
- Mix of valid and invalid records → only valid ones are buffered
- All events from the same user → unique_users = 1

### Complexity

- **Time:** O(n) — single pass, each flush is O(batch size)
- **Space:** O(buffer_size) — only the current batch is in memory

---

## 2. Meeting Streak Analyzer (`meeting_scheduler.py`)

Finds the attendee(s) with the longest consecutive biennial conference streak (sessions exactly 2 years apart).

### What I focused on beyond the basic requirements

- **Deduplication with `set()`** — Duplicate `(name, year)` entries are collapsed at collection time so streak math is always accurate without needing a separate cleaning step.
- **Input order doesn't matter** — The solution uses a set for O(1) year lookup, so streak detection works without needing to sort the data.
- **Deterministic tie-breaking** — When multiple people share the longest streak, names are returned in alphabetical order so the output is predictable and easy to test.

### Edge cases covered

- Empty list → returns `None`
- Single attendee with one entry → returns that name (streak = 1)
- Gap in attendance (e.g., 2002 → 2006) resets the streak
- Duplicate `(name, year)` pairs → handled by `set()`
- Unsorted input years → sorted before scanning
- Multiple disjoint streaks for one person → only the longest counts (two streaks of 2 ≠ streak of 4)
- Multi-way ties → returns sorted list of names

### Complexity

- **Time:** O(n) — each year is visited at most once using the "longest consecutive sequence" set-lookup technique
- **Space:** O(n) — stores all (name, year) pairs

---

## Running the Tests

```bash
python event_stream.py       # 19 tests
python meeting_scheduler.py  # 11 tests
```

Both scripts use a simple inline test harness — no external dependencies needed.

---

## Project Structure

```
├── event_stream.py        # Q1 – buffered event processing
├── meeting_scheduler.py   # Q2 – biennial streak analysis
└── README.md
```
