def find_top_attendee(meetings):
   
    if not meetings:
        return None
 
    # Build deduplicated year sets per attendee
    attendee_years = {}
    for name, year in meetings:
        attendee_years.setdefault(name, set()).add(year)
 
    best_streak = 0
    streaks = {}
 
    for name, year_set in attendee_years.items():
        max_streak = 1
 
        for year in year_set:
            # Only start counting from the beginning of a streak
            if (year - 2) in year_set:
                continue
 
            # Walk forward by 2 until the chain breaks
            current = year
            length = 1
            while (current + 2) in year_set:
                current += 2
                length += 1
 
            if length > max_streak:
                max_streak = length
 
        streaks[name] = max_streak
        if max_streak > best_streak:
            best_streak = max_streak
 
    winners = sorted(name for name, s in streaks.items() if s == best_streak)
 
    return winners[0] if len(winners) == 1 else winners


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


    # -- Basic tests --
    print()
    print("  [Basic Cases]")

    meetings1 = [
        ("Alice", 2000), ("Alice", 2002), ("Alice", 2004),
        ("Bob", 2000), ("Bob", 2002),
        ("Charlie", 2000), ("Charlie", 2002), ("Charlie", 2004), ("Charlie", 2006),
    ]
    check("Charlie has longest streak (4)", find_top_attendee(meetings1), "Charlie")

    meetings2 = [
        ("Alice", 2000), ("Alice", 2002),
        ("Bob", 2000), ("Bob", 2002),
    ]
    check("Tie returns sorted list", find_top_attendee(meetings2), ["Alice", "Bob"])

    # -- Edge cases --
    print()
    print("  [Edge Cases]")

    check("Empty meetings returns None", find_top_attendee([]), None)

    check("Single entry returns that person", find_top_attendee([("Zara", 2020)]), "Zara")

    meetings3 = [
        ("Dan", 2000), ("Dan", 2002), ("Dan", 2006), ("Dan", 2008),
    ]
    check("Gap resets streak (Dan max=2)", find_top_attendee(meetings3), "Dan")

    meetings4 = [
        ("Eve", 2000), ("Eve", 2000), ("Eve", 2002), ("Eve", 2004),
    ]
    check("Duplicates handled (Eve streak=3)", find_top_attendee(meetings4), "Eve")

    meetings5 = [
        ("Frank", 2006), ("Frank", 2000), ("Frank", 2004), ("Frank", 2002),
    ]
    check("Unsorted input (Frank streak=4)", find_top_attendee(meetings5), "Frank")

    meetings6 = [
        ("A", 2000), ("B", 2000), ("C", 2000),
    ]
    check("Three-way tie at streak=1", find_top_attendee(meetings6), ["A", "B", "C"])

    meetings7 = [
        ("Grace", 2000), ("Grace", 2002), ("Grace", 2004),
        ("Hank", 2000), ("Hank", 2004), ("Hank", 2006),
        ("Ivy", 2010), ("Ivy", 2012), ("Ivy", 2014),
    ]
    check("Grace and Ivy tie at streak=3", find_top_attendee(meetings7), ["Grace", "Ivy"])

    meetings8 = [
        ("Jake", 2000), ("Jake", 2005), ("Jake", 2011),
    ]
    check("No consecutive years gives streak=1", find_top_attendee(meetings8), "Jake")

    meetings9 = [
        ("Kim", 2000), ("Kim", 2002),
        ("Kim", 2010), ("Kim", 2012),
        ("Leo", 2000), ("Leo", 2002), ("Leo", 2004),
    ]
    check("Long streak beats multiple short ones", find_top_attendee(meetings9), "Leo")

    # -- Summary --
    print()
    
    print(f"  {passed} passed, {failed} failed")
  

if __name__ == "__main__":
    run_tests()