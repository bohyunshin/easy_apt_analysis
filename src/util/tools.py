from datetime import datetime

def make_one_step(yrm):
    yrm = str(int(yrm))
    assert len(yrm) == 6
    year, month = yrm[:4], yrm[4:]
    # at the end of year
    if month == '12':
        year = str(int(year)+1)
        month = '01'
        next_yrm = year + month
    # at the middle of year
    else:
        next_yrm = str(int(yrm)+1)
    return next_yrm

def make_datetime(yrm):
    yrm = str(yrm)
    assert len(yrm) == 6
    year, month = yrm[:4], yrm[4:]
    return datetime(int(year), int(month), 1)

if __name__ == '__main__':
    make_one_step('201114')