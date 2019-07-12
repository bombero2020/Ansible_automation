import ansible_runner
import datetime


def run_blocks():
    '''Example of running blocks'''
    PRIVATE_DATA_DIR = '/home/marcelo/ansible'
    PLAYBOOK='install_apache.yaml'
    r = ansible_runner.run(private_data_dir=PRIVATE_DATA_DIR,
                           ident=datetime.datetime.now(),
                           playbook=PLAYBOOK,
                           quiet=False,
                           extravars={"ansible_sudo_pass": 'linux_mint'},
                           event_handler=event_handler_funct())

    stats = r.stats
    status = r.status
    # events = r.event_handler(r.events)
    print(stats)
    print(status)
    for event in r.events:
        if event['event'] != 'verbose':

            print('evento', event['event'])


def event_handler_funct():

    print("desde el event_handler_funct")


run_blocks()