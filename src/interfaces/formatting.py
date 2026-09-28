def format_amount(amount):
    """Always 2 decimals and the euro symbol. Example: 2.1 -> '2.10 €'"""
    return f"{amount:.2f} €"


def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"
