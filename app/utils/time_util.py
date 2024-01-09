def convert_seconds(seconds):
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60

  return hours, minutes, seconds


def convert_seconds_to_str(seconds):
  if seconds == None:
    return '未知'
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60

  return f'{hours}小时{minutes}分钟{seconds}秒'
