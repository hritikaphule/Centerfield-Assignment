import logging
from typing import List, Dict, Any, Iterable

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def process_event_stream(events: Iterable[Dict[str, Any]], buffer_size: int = 3, debug: bool = False) -> List[Dict[str, Any]]:
    """
    Processes a stream of events, aggregating them into batches of `buffer_size`.
    Returns a list of metrics (avg_value, max_value, unique_users) for each batch.
    """
    if buffer_size <= 0:
        raise ValueError("buffer_size must be positive.")
        
    results = []
    buffer = []
    
    def flush_buffer():
        """Calculates metrics for the current buffer and clears it."""
        if not buffer:
            return
            
        # Print debug information if enabled
        if debug:
            for evt in buffer:
                print(f"DEBUG: {evt}")
                
        # Calculate metrics for the buffered events
        total_value = sum(evt['value'] for evt in buffer)
        max_value = max(evt['value'] for evt in buffer)
        unique_users = len(set(evt['metadata']['user_id'] for evt in buffer))
        
        # Save the aggregated results for this batch
        results.append({
            'avg_value': total_value / len(buffer),
            'max_value': max_value,
            'unique_users': unique_users
        })
            
        # Clear the buffer for the next batch
        buffer.clear()
        
    # Process each event in the stream
    for event in events:
        # Skip invalid event types
        if not isinstance(event, dict):
            logging.warning(f"Invalid record type. Expected dict, got {type(event).__name__}. Skipping.")
            continue
            
        # Extract and validate required fields
        try:
            val = float(event['value'])
            user_id = event['metadata']['user_id']
            
            valid_event = {
                'event_id': event.get('event_id'),
                'timestamp': event.get('timestamp'),
                'value': val,
                'metadata': {'user_id': user_id}
            }
        except (KeyError, ValueError, TypeError) as e:
            # Skip events with missing keys or invalid data types
            logging.warning(f"Invalid record data, missing fields or bad types. Skipping. Record: {event}")
            continue
            
        # Add the valid event to our buffer
        buffer.append(valid_event)
        
        # Process the batch once the buffer is full
        if len(buffer) == buffer_size:
            flush_buffer()
            
    # Process any remaining events left in the buffer after the loop finishes
    if buffer:
        flush_buffer()
        
    return results

def run_tests():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]
    res = process_event_stream(events, buffer_size=3)
    print("Normal:", res)
    
    process_event_stream(events, buffer_size=3, debug=True)

if __name__ == "__main__":
    run_tests()
