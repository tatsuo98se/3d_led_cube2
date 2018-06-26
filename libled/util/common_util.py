from collections import defaultdict

def to_int_safe(rev_id):
    try:
        return int(rev_id)
    except ValueError:
        return 0

def create_nested_dict(n):
    if n == 1:
        return defaultdict(lambda: None)
    else:
        return defaultdict(lambda: create_nested_dict(n-1))
