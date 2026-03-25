# Python Technical Assignments
This repository contains Python solutions for two common data processing tasks: managing live event streams and analyzing meeting patterns.

---

## 1. Event Stream Processor (`event_stream.py`)

This script handles a continuous flow of user data. It collects events into "batches" (groups of a specific size) before processing them, making the data easier to manage.

### Features & Edge Cases
* **Empty Data:** If there are no events to process, the script finishes quietly without crashing.
* **Leftover Events:** If the total number of events doesn't perfectly fit into your batch size (e.g., 12 events with a batch size of 5), it ensures the final 2 events are still processed.
* **Bad Data:** It automatically spots and skips "broken" records like those with missing information or the wrong format so one bad entry doesn't stop the whole script.
* **Debug Mode:** You can turn on a `debug` setting to see exactly what’s happening line-by-line while still getting your final totals.

---

## 2. Meeting Streak Analyzer (`meeting_scheduler.py`)

This tool looks through conference records to find the person with the longest "perfect" attendance streak—specifically, people who attend a biennial conference exactly every two years without missing a beat.

### Features & Edge Cases
* **No Meetings:** Returns a clean, empty result if no data is provided.
* **Single Attendees:** Correctly identifies people who have only attended once.
* **Strict Timing:** It only counts gaps of exactly two years. If someone skips a year or waits four years, the script knows to "reset" their streak and start counting over.
* **Duplicate Records:** If a person's name is accidentally listed twice for the same year, the script uses a `set()` to ignore the extra entry and keep the math accurate.

---

## Getting Started

To run these scripts, ensure you have Python installed:

```bash
python event_stream.py
python meeting_scheduler.py
