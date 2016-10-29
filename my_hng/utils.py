# -*- coding: utf-8 -*-
from datetime import datetime

DATE_FORMAT = '%m/%d/%Y'


def convert_date(raw_date):
    """Converting date received from mysql to American datetype."""
    if raw_date is None:
        formatted_date = raw_date
    else:
        formatted_date = datetime.strptime(
            str(raw_date),
            '%Y-%m-%d'
        ).strftime(DATE_FORMAT)
    return formatted_date
