import os

class ProcessUtils(object):

    @staticmethod
    def run_cmd(strCmd):
        os.system(strCmd)