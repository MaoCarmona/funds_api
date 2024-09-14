import json
from typing import Any

class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.database_name = ""
        self.mongo_uri = ""
        self.twilio_tk = ""
        self.twilio_account_sid =""
        self.host_number= ""
        self._load_config()

    def _load_config(self):
        with open(self.config_file, "r") as file:
            self._config_data = json.load(file)
        self.database_name = self._config_data.get("database_name", "")
        self.mongo_uri = self._config_data.get("mongo_uri", "")
        self.twilio_tk = self._config_data.get("twilio_tk","")
        self.twilio_account_sid = self._config_data.get("twilio_account_sid","")
        self.host_number = self._config_data.get("host_number","")

    def get(self, key: str) -> Any:
        return self._config_data.get(key)

config = Config("config.json")