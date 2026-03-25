# Python Technical Assignments

This repository contains solutions to two data processing challenges implemented in Python.

## 1. Event Stream Processing (`event_stream.py`)
A script that processes a stream of user events, validating and aggregating them into configurable batches defined by `buffer_size`. 

**Edge Cases Handled:**
- Handles empty event streams without error.
- Evaluates the final subset of events remaining in the buffer if the total event count isn't a perfect multiple.
- Identifies, drops, and skips invalid malformed records (e.g., missing dictionary keys, unusable data types) via strong schema-based exception handling.
- Implements a functional localized debug mode (`debug=True`) which logs out records locally but still properly evaluates final numeric aggregates.

## 2. Meeting Scheduling Analysis (`meeting_scheduler.py`)
A string analytics query function built to identify the attendee with the longest unbroken streak of visiting a biennial conference exactly every 2 years.

**Edge Cases Handled:**
- Handles entirely empty meeting iterations (safely returns an empty array).
- Identifies single attendees explicitly.
- Distinctly separates matching 2-year gaps from longer/shorter irregular non-consecutive jumps (which break streaks and reset execution cleanly back to 1).
- Uses programmatic set-based operations (`set()`) dynamically ensuring arbitrary redundant duplicate entries for the exact same person-year combinations are correctly ignored.
