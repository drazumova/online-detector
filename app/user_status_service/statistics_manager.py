from database_factory import *
from enum import Enum
from datetime import datetime

class Status(Enum):
    ONLINE = 1
    AWAY = 2
    OFFLINE = 3
    UNKNOWN = 4

class StatisticsManager:
    minute = 60
    away_time = 15 * minute
    offline_time = 30 * minute

    def __init__(self):
        self._storage = DatabaseFactory.create_default()

    def get_user_status(self, id):
        current_time = datetime.now()
        last_time = self._storage.get_user_time(id)
        if last_time is None:
            return Status.UNKNOWN
        delta = (current_time - last_time).total_seconds()
        if (delta < self.away_time):
            return Status.ONLINE
        elif delta < self.offline_time:
            return Status.AWAY
        return Status.OFFLINE

    def update_time(self, id):
        current_time = datetime.now()
        self._storage.upsert_user_time(id, current_time)
