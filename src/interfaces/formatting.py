def format_amount(amount):
    return f"{amount:.2f}€"


def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"
