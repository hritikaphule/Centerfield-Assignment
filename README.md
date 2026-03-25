# Python Technical Assignments

Solutions for two data processing tasks: managing live event streams and analyzing meeting attendance patterns.

---

## 1. Event Stream Processor (`event_stream.py`)

Collects user-activity events into batches of a given size, then computes per-batch stats (average value, max value, unique users).

### What I focused on beyond the basic requirements

- **Remainder handling** — If the total events don't divide evenly into the batch size (e.g., 4 events with `buffer_size=3`), the leftover events are still processed instead of being silently dropped. In a real analytics pipeline you wouldn't want to lose data just because it didn't fill a buffer.
- **Validation before buffering** — Invalid records (wrong type, missing keys, no `user_id` in metadata) are filtered out before they ever enter the buffer, so they can't corrupt batch calculations.
- **Debug mode** — When `debug=True`, events are printed to stdout and the buffer is cleared without computing metrics, matching the spec's intent of swapping behavior.

### Edge cases covered

- Empty event list or `buffer_size <= 0` → returns `[]`
- Buffer larger than event count → remainder is still flushed (1 result instead of 0)
- All records invalid → returns `[]` without crashing
- Mix of valid and invalid records → only valid ones are buffered
- All events from the same user → `unique_users = 1`

### Complexity

- **Time:** O(n) — single pass, each flush is O(batch size)
- **Space:** O(buffer_size) — only the current batch is in memory

---

## 2. Meeting Streak Analyzer (`meeting_scheduler.py`)

Finds the attendee(s) with the longest consecutive biennial conference streak (sessions exactly 2 years apart).

### What I focused on beyond the basic requirements

- **Deduplication with `set()`** — Duplicate `(name, year)` entries are collapsed at collection time so streak math is always accurate without needing a separate cleaning step.
- **Input order doesn't matter** — Years are sorted per attendee before scanning, so the function works regardless of how the data comes in.
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
