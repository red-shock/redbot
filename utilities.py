def format_time_delta(time: datetime.timedelta) -> str:
    seconds = time.total_seconds()
    years = int(seconds // 31536000)
    seconds -= years * 31536000
    months = int(seconds // 2592000)
    seconds -= months * 2592000
    weeks = int(seconds // 604800)
    seconds -= weeks * 604800
    days = int(seconds // 86400)
    seconds -= days * 86400
    time_list = [
        i
        for i in [
            f"{years} years",
            f"{months} months",
            f"{weeks} weeks",
            f"{days} days",
        ]
        if int(i[0]) != 0
    ]
    return (
        ", ".join(time_list[:-1]) + " and " + time_list[-1]
        if len(time_list) > 1
        else time_list[0]
    )
