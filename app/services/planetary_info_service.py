from app.core.planetary_info import compute_planetary_info_telugu

def get_planetary_info_table(params):
    info = compute_planetary_info_telugu(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset,
        params.varga_num
    )
    return {"info": info}
