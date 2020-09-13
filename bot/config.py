class Config:

    def __init__(self, token):
        self._env = {}
        self._env['token'] = token
        self.env = self._env

    def features(self):
        pass