import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class Ontodoc():

    log = logging.getLogger(__name__)

    def __init__(self):
        super(Ontodoc, self).__init__(
            description='ontodoc - Generate static documentation from OWL files',
            version='0.1',
            command_manager=CommandManager('ontodoc'),
            )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)

def main(argv=sys.argv[1:]):
    myapp = Ontodoc()
    return myapp.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))