from django.core.exceptions import ValidationError
import datetime as dt

tz = dt.timezone(-dt.timedelta(hours=4), name='CCS/Venezuela')


def is_auction_active(date):
    current_date = dt.datetime.now(tz=tz)
    time_lapse = date - current_date
    if (time_lapse.total_seconds() < 3600):
        raise ValidationError(
            'Your auction should be at least active for one (1) hour')


def check_bid(bid_offer):
    print(f'The offer is: {bid_offer}')
