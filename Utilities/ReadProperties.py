import configparser
import os

class ReadConfig:
    """Utility class to read configuration values from config.ini"""

    # Build absolute path to config.ini (so it works from any directory)
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "Configurations", "config.ini")

    config = configparser.RawConfigParser()
    config.read(CONFIG_PATH)

    @staticmethod
    def getURL(region: str) -> str:
        """Get URL for the given region (AP, ME, US, EU)"""
        return ReadConfig.config.get(region, "baseURL")

    @staticmethod
    def getClientID(region: str) -> str:
        """Get client ID for the given region"""
        return ReadConfig.config.get(region, "clientID")

    @staticmethod
    def getUsername(region: str) -> str:
        """Get username for the given region"""
        return ReadConfig.config.get(region, "username")

    @staticmethod
    def getPassword(region: str) -> str:
        """Get password for the given region"""
        return ReadConfig.config.get(region, "password")
