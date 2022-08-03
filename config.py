from zoneinfo import ZoneInfo

config = {
    'sqlite_file_name': "database.db",
    'tz': ZoneInfo("Australia/Melbourne")
}

config['sqlite_url'] = f"sqlite:///{config['sqlite_file_name']}"