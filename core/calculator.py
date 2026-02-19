from datetime import datetime, timedelta


def calculate_days_remaining(birthdate_str, lifespan_years):
    """计算剩余天数"""
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    end_date = birthdate + timedelta(days=lifespan_years * 365.25)
    now = datetime.now()
    remaining = (end_date - now).days
    return max(0, remaining)


def calculate_total_days(lifespan_years):
    """计算总天数"""
    return int(lifespan_years * 365.25)
