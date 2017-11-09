def to_int_safe(rev_id):
    try:
        return int(rev_id)
    except ValueError:
        return 0
