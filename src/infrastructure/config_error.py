class ConfigError(Exception):
    def __init__(self, message, user_message):
        super().__init__(message)
        self.user_message = user_message
