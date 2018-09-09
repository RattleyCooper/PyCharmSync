import os
from time import sleep
import subprocess
from configparser import ConfigParser


name = 'PyCharmSync'


class ProjectSync(object):
    ignore = ['.DS_Store', '.git', '__pycache__', '.idea']
    database = {}
    config = None
    enabled = True

    @classmethod
    def sync_file(cls, filepath):
        """
        Sync's a file to the remote machine using SCP.

        :param filepath:
        :return:
        """

        if not cls.config:
            cls._bootstrap_config(os.getcwd())

        # print('Syncing', filepath)
        remote_location = '{}@{}:{}'.format(
            cls.config['SSH']['USER'],
            cls.config['SSH']['HOST'],
            cls.config['SSH']['PROJECT_ROOT']
        )
        subprocess.run(
            [
                'sshpass',
                '-p',
                '"{}"'.format(cls.config['SSH']['PASS']),
                'scp',
                '"{}"'.format(filepath),
                remote_location
            ]
        )
        return cls

    @classmethod
    def _gettime(cls, filepath):
        """
        Get file's last modified time without throwing an error.  Return False if it fails.

        :param filepath:
        :return:
        """

        try:
            return os.path.getmtime(filepath)
        except FileNotFoundError:
            return False

    @classmethod
    def _check_file(cls, wd, file):
        """
        Uses the file's last modified time to see if the file needs to sync up.

        :param wd:
        :param file:
        :return:
        """

        filepath = wd + '/' + file

        try:
            last_modified_time = cls.database[filepath]
        except KeyError:
            last_modified_time = False

        # Get last modified time of file safely.
        current_modified_time = False
        while not current_modified_time:
            current_modified_time = cls._gettime(filepath)

        if last_modified_time:
            if current_modified_time != last_modified_time:
                cls.sync_file(filepath)

        cls.database[filepath] = current_modified_time
        return cls

    @classmethod
    def _walk(cls, walk):
        """
        Walks through a directory and handles files.

        :param walk:
        :return:
        """

        root_dir = walk[0][0]
        blacklist_paths = ['{}/{}'.format(root_dir, ign) for ign in cls.ignore]

        # Remove any unwanted filepaths from walk.
        walk = [w for w in walk if not any(p in w[0] for p in blacklist_paths)]

        for wd, dirs, files in walk:
            files = [f for f in files if f not in cls.ignore]
            for file in files:
                cls._check_file(wd, file)
        return cls

    @classmethod
    def _bootstrap_config(cls, cwd):
        config = ConfigParser()
        config.read('{}/{}'.format(cwd, '.env'))
        cls.config = config

    @classmethod
    def main(cls, cwd=''):
        """
        Main loop that is fired off to start sending file updates.

        :param cwd:
        :return:
        """

        cwd = os.getcwd() if not cwd else cwd

        # Reformat the cwd if it was given manually.
        if cwd[-1] == '/':
            cwd = cwd[:-1]

        # Create a config parser and try to read the .env file in the cwd if there is none.
        if not cls.config:
            cls._bootstrap_config(cwd)

        # Thread control.  Change cls.enabled to False to shut down the main loop.
        # Launching ProjectSync.main in a new thread is the smoothest way to
        # handle this.
        while cls.enabled:
            walk = [d for d in os.walk(cwd)]
            cls._walk(walk)
            sleep(0.1)

        return cls


if __name__ == '__main__':
    ProjectSync.main()
