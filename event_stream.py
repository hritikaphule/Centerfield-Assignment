def process_event_stream(events, buffer_size=3, debug=False):

    if not events or buffer_size <= 0:
        return []

    results = []
    buffer = []

    for event in events:
        # Skip invalid records
        if not isinstance(event, dict):
            continue
        if not {"event_id", "timestamp", "value", "metadata"}.issubset(event):
            continue
        if not isinstance(event.get("metadata"), dict) or "user_id" not in event["metadata"]:
            continue

        buffer.append(event)

        if len(buffer) == buffer_size:
            if debug:
                for e in buffer:
                    print(f"[DEBUG] {e}")
            else:
                values = [e["value"] for e in buffer]
                user_ids = {e["metadata"]["user_id"] for e in buffer}
                results.append({
                    "avg_value": sum(values) / len(values),
                    "max_value": max(values),
                    "unique_users": len(user_ids),
                })
            buffer.clear()

    return results
# Tests
def run_tests():
    passed = 0
    failed = 0

    def check(label, actual, expected):
        nonlocal passed, failed
        if actual == expected:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}")
            print(f"        Expected: {expected}")
            print(f"        Got:      {actual}")

    

    sample_events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]

    # Basic batch of 3
    res = process_event_stream(sample_events, buffer_size=3)
    check("Basic batch (size=3) produces 1 result", len(res), 1)
    check("avg_value = 20.0", res[0]["avg_value"], 20.0)
    check("max_value = 30.0", res[0]["max_value"], 30.0)
    check("unique_users = 2", res[0]["unique_users"], 2)

    # Two full batches (size=2)
    res2 = process_event_stream(sample_events, buffer_size=2)
    check("Two batches (size=2) produces 2 results", len(res2), 2)
    check("Batch 1 avg = 15.0", res2[0]["avg_value"], 15.0)
    check("Batch 2 avg = 35.0", res2[1]["avg_value"], 35.0)

    # buffer_size = 1
    res3 = process_event_stream(sample_events, buffer_size=1)
    check("buffer_size=1 produces 4 results", len(res3), 4)

    # Edge: empty events
    check("Empty events returns []", process_event_stream([]), [])

    # Edge: buffer larger than event count
    check("Buffer larger than events returns []", process_event_stream(sample_events, buffer_size=10), [])

    # Edge: buffer_size = 0 or negative
    check("buffer_size=0 returns []", process_event_stream(sample_events, buffer_size=0), [])
    check("buffer_size=-1 returns []", process_event_stream(sample_events, buffer_size=-1), [])

    # Edge: invalid records skipped
    mixed = [
        {"event_id": "e1", "timestamp": "t", "value": 5.0, "metadata": {"user_id": "u1"}},
        {"bad": "record"},
        {"event_id": "e3", "timestamp": "t", "value": 15.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e4", "timestamp": "t", "value": 25.0, "metadata": {}},
        {"event_id": "e5", "timestamp": "t", "value": 25.0, "metadata": {"user_id": "u1"}},
    ]
    res_mixed = process_event_stream(mixed, buffer_size=3)
    check("Invalid records skipped, 1 batch from 3 valid", len(res_mixed), 1)
    check("avg_value = 15.0", res_mixed[0]["avg_value"], 15.0)

    # Edge: all same user
    same_user = [
        {"event_id": "e1", "timestamp": "t", "value": 2.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "t", "value": 4.0, "metadata": {"user_id": "u1"}},
    ]
    res_same = process_event_stream(same_user, buffer_size=2)
    check("All same user gives unique_users = 1", res_same[0]["unique_users"], 1)

    # Debug mode
    print("\n  Debug mode output:")
    res_debug = process_event_stream(sample_events, buffer_size=3, debug=True)
    check("Debug mode returns []", res_debug, [])

    print(f"\n{passed} passed, {failed} failed\n")


if __name__ == "__main__":
    run_tests()