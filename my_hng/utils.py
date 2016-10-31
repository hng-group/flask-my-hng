# -*- coding: utf-8 -*-
from datetime import datetime

DATE_FORMAT = '%m/%d/%Y'


def sql_to_us_date(original):
    """Converts SQL date to U.S date."""
    if original is None:
        return
    return datetime.strptime(
            str(original),
            '%Y-%m-%d'
        ).strftime(DATE_FORMAT)


def us_to_sql_date(original):
    """Converts U.S date to SQL date."""
    return datetime.strptime(
        str(original),
        '%m/%d/%Y'
    ).strftime('%Y-%m-%d')
