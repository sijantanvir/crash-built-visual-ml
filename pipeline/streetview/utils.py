from datetime import datetime


def parse_date(date_str: str):
    """
    Parse date string safely.
    Expected format: YYYY-MM
    """
    try:
        return datetime.strptime(date_str, "%Y-%m")
    except Exception:
        return None


def closest_date(target_date, candidate_dates):
    """
    Find closest date from list.
    """
    valid_dates = [d for d in candidate_dates if d is not None]

    if not valid_dates:
        return None

    return min(valid_dates, key=lambda d: abs(d - target_date))