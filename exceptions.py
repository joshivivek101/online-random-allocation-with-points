class DabboException(Exception):
    default_message = 'Something went wrong'
    def __init__(self, message=None):
        super().__init__(self)
        self.message = message if message else self.default_message