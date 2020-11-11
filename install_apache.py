import ansible_runner
import datetime


def run_blocks():
    '''Example of running blocks'''
    PRIVATE_DATA_DIR = '/home/marcelo/ansible'
    PLAYBOOK='/home/marcelo/Ansible/project/install_apache.yaml'
    INVENTORY_PATH='/home/marcelo/Ansible/inventory'
    r = ansible_runner.run(private_data_dir=PRIVATE_DATA_DIR,
                           ident=datetime.datetime.now(),
                           playbook=PLAYBOOK,
                           quiet=False,
                           inventory=INVENTORY_PATH,
                           extravars={"ansible_sudo_pass": 'secret'},
                           event_handler=event_handler_funct())

    stats = r.stats
    status = r.status
    # events = r.event_handler(r.events)
    print(stats)
    print(status)
    for event in r.events:
        if event['event'] != 'verbose':

            print('evento-------------->', event['event'])
            print(event)


def event_handler_funct():

    print("desde el event_handler_funct")


run_blocks()