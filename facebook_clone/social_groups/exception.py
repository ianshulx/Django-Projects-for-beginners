class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket recieve()
    handler and translated into a send back to the client
    """
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code 
        if message:
            self.message = message