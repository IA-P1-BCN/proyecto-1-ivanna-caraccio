def format_amount(amount):
    return f"{amount:.2f}€"


def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def format_history_table(records):
    lines = [f"{'#':<4}{'Inicio':<10}{'Fin':<10}{'Duración':<10}Cantidad"]
    for number, record in enumerate(records, start=1):
        start = record.start_time.strftime("%H:%M:%S")
        end = record.end_time.strftime("%H:%M:%S")
        duration = format_duration(record.duration_seconds)
        amount = format_amount(record.total_amount)
        lines.append(
            f"{number:<4}{start:<10}{end:<10}{duration:<10}{amount}"
        )
    return lines
