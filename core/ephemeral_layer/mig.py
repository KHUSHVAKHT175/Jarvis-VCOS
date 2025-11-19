class MIG:
    def flash(self, cmd_dict):
        print('MIG flash executing: ' + str(cmd_dict))
        return {'status':'executed','cmd':cmd_dict}
