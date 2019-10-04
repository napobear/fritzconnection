"""
fritzinspection.py

Module to inspect the FritzBox API for available services and actions.

This module is part of the FritzConnection package.
https://github.com/kbr/fritzconnection
License: MIT (https://opensource.org/licenses/MIT)
Author: Klaus Bremer
"""


import argparse
import os

from ..core import (
    FritzConnection,
    FRITZ_IP_ADDRESS,
    FRITZ_TCP_PORT,
    FRITZ_USERNAME,
)
from .. import package_version


class FritzInspection:
    """
    Class for cli use to inspect available services and according
    actions of the given device (the Fritz!Box).
    """
    # pylint: disable=invalid-name  # self.fc is ok.

    def __init__(self,
                 address=FRITZ_IP_ADDRESS,
                 port=FRITZ_TCP_PORT,
                 user=FRITZ_USERNAME,
                 password=''):
        self.fc = FritzConnection(address, port, user, password)

    def view_header(self):
        print(self.fc)

    def view_servicenames(self):
        """Send all known service names to stdout."""
        print('Servicenames:')
        for service_name in self.fc.device_manager.services:
            print('{:20}{}'.format('', name))

    def view_actionnames(self, servicename):
        """Send all action names of the given service to stdout."""
        print('\n{:<20}{}'.format('Servicename:', servicename))
        print('Actionnames:')
        for name in self.get_actionnames(servicename):
            print('{:20}{}'.format('', name))


def get_cli_arguments():
    """
    Returns a NameSpace object from the ArgumentParser parsing the given
    command line arguments.
    """
    print(f'\nFritzConnection v{package_version}')
    parser = argparse.ArgumentParser(description='Fritz!Box API Inspection:')
    parser.add_argument('-i', '--ip-address',
                        nargs='?', default=None, const=None,
                        dest='address',
                        help='Specify ip-address of the FritzBox to connect to.'
                             'Default: %s' % FRITZ_IP_ADDRESS)
    parser.add_argument('--port',
                        nargs='?', default=None, const=None,
                        help='Port of the FritzBox to connect to. '
                             'Default: %s' % FRITZ_TCP_PORT)
    parser.add_argument('-u', '--username',
                        nargs='?', default=os.getenv('FRITZ_USERNAME', None),
                        help='Fritzbox authentication username')
    parser.add_argument('-p', '--password',
                        nargs='?', default=os.getenv('FRITZ_PASSWORD', None),
                        help='Fritzbox authentication password')
    parser.add_argument('-r', '--reconnect',
                        action='store_true',
                        help='Reconnect and get a new ip')
    parser.add_argument('-s', '--services',
                        action='store_true',
                        help='List all available services')
    parser.add_argument('-S', '--serviceactions',
                        nargs=1,
                        help='List actions for the given service: <service>')
    parser.add_argument('-a', '--servicearguments',
                        nargs=1,
                        help='List arguments for the actions of a '
                             'specified service: <service>.')
    parser.add_argument('-A', '--actionarguments',
                        nargs=2,
                        help='List arguments for the given action of a '
                             'specified service: <service> <action>.')
    parser.add_argument('-c', '--complete',
                        action='store_true',
                        help='List all services with actionnames and arguments.'
                        )
    args = parser.parse_args()
    return args


def main():
    """CLI entry point."""
    args = get_cli_arguments()
    inspector = FritzInspection(
        args.address, args.port, args.username, args.password)
    inspector.view_header()
    if args.services:
        inspector.view_servicenames()
    elif args.serviceactions:
        inspector.view_actionnames(args.serviceactions[0])
#     elif args.servicearguments:
#         inspector.view_servicearguments(args.servicearguments[0])
#     elif args.actionarguments:
#         inspector.view_actionarguments(args.actionarguments[0],
#                                        args.actionarguments[1])
#     elif args.complete:
#         inspector.view_complete()
#     elif args.reconnect:
#         inspector.fc.reconnect()
    print()  # print an empty line


if __name__ == '__main__':
    main()
