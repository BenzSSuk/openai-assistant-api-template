import datetime

def add_hour_timestamp(timestamp_str, format_timestamp="%Y%m%d_%H%M%S", hours=7):
    timestamp_date = datetime.datetime.fromisoformat(timestamp_str)
    timestamp_date = timestamp_date + datetime.timedelta(hours=hours)
    timestamp_str = datetime.datetime.strftime(timestamp_date, format_timestamp)

    return timestamp_date, timestamp_str

def changeTimestampFormatFromISO(timestamp_iso_str, format_timestamp="%Y%m%d_%H%M%S", offset_hours=0):
    timestamp_date = datetime.datetime.fromisoformat(timestamp_iso_str)
    if offset_hours != 0:
        timestamp_date = timestamp_date + datetime.timedelta(hours=offset_hours)
    timestamp_str = datetime.datetime.strftime(timestamp_date, format_timestamp)

    return timestamp_str, timestamp_date

def changeTimestampToDatetime(df, header_time, format_time='iso'):
    timestamp_str = df[header_time].values
    timestamp_str = timestamp_str.astype(datetime64)
    if format_time == 'iso':
        timestamp_date = datetime.datetime.fromisoformat(timestamp_str)

    df[header_time] = timestamp_date

    return df

def getListYMD_fromDate(datetime_in):
    listYMD = []
    listYMD.append(datetime_in.__str__()[0:4])
    listYMD.append(datetime_in.__str__()[5:7])
    listYMD.append(datetime_in.__str__()[8:10])

    return listYMD

def get_timestamp():
    timestamp_now = datetime.datetime.now()
    timestamp_str = datetime.datetime.strftime(timestamp_now, "%Y%m%d_%H%M%S")

    return timestamp_str
