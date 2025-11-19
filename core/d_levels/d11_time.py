class Field11D:
    def review_action(self, cmd, context=None):
        print('11D reviewing: ' + cmd)
        return {'ok': True}

    def learn(self, cmd, result):
        pass
