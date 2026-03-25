from typing import List, Tuple, Union
from collections import defaultdict

def find_top_attendee(meetings: List[Tuple[str, int]]) -> Union[str, List[str]]:
    
    if not meetings:
        return []
        
    # Group years by attendee and use a set to automatically drop duplicate person-year entries
    attendee_years = defaultdict(set)
    for name, year in meetings:
        attendee_years[name].add(year)
        
    # Dictionary to keep track of max streak lengths for each attendee
    streaks = {}
    
    for name, years in attendee_years.items():
        # Sort the years to easily find consecutive attended events
        sorted_years = sorted(list(years))
        
        longest_streak = 1
        current_streak = 1
        
        # Calculate max streak for this attendee
        for i in range(1, len(sorted_years)):
            # Check if the attendance is exactly 2 years apart
            if sorted_years[i] == sorted_years[i-1] + 2:
                current_streak += 1
            else:
                current_streak = 1
                
            longest_streak = max(longest_streak, current_streak)
            
        streaks[name] = longest_streak
        
    # Find the maximum streak length across all attendees
    max_streak_length = max(streaks.values())
    
    # Collect all attendees who have this maximum streak length
    top_attendees = [name for name, streak in streaks.items() if streak == max_streak_length]
    top_attendees.sort() # Sort alphabetically in case of a tie
    
    # Return string if unique, otherwise the sorted list
    if len(top_attendees) == 1:
        return top_attendees[0]
    return top_attendees

def run_tests():
    meetings1 = [
        ("Alice", 2000), ("Alice", 2002), ("Alice", 2004),
        ("Bob",   2000), ("Bob",   2002),
        ("Charlie", 2000), ("Charlie", 2002), ("Charlie", 2004), ("Charlie", 2006),
    ]
    print("Test 1 (Charlie):", find_top_attendee(meetings1))

    meetings2 = [
        ("Alice", 2000), ("Alice", 2002),
        ("Bob",   2000), ("Bob",   2002),
    ]
    print("Test 2 ['Alice', 'Bob']:", find_top_attendee(meetings2))

    meetings_empty = []
    print("Test 3 (Empty):", find_top_attendee(meetings_empty))

    meetings_single = [("Alice", 2000)]
    print("Test 4 (Single):", find_top_attendee(meetings_single))

    meetings_non_consecutive = [("Alice", 2000), ("Alice", 2004), ("Alice", 2008)]
    print("Test 5 (Non-consecutive, Alice):", find_top_attendee(meetings_non_consecutive))
    
    meetings_duplicates = [("Alice", 2000), ("Alice", 2000), ("Alice", 2002)]
    print("Test 6 (Duplicates, Alice):", find_top_attendee(meetings_duplicates))

if __name__ == "__main__":
    run_tests()
