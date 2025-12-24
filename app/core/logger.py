import logging
from typing import Optional


class LoggerSingleton:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = logging.getLogger("coffee-email")
            cls._instance.setLevel(logging.INFO)

            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
            handler.setFormatter(formatter)
            cls._instance.addHandler(handler)
        return cls._instance


logger = LoggerSingleton.get_logger()
