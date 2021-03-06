#!/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
	with open('Resultado.json','w+') as file:
		file.write(json.dumps({"Resultados en v2runner":result._result}, indent=4))
        print(json.dumps({host.name: result._result}, indent=4))

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
# initialize needed objects
loader = DataLoader()
p_to_modules = '/usr/lib/python2.7/dist-packages/ansible'
options = Options(connection='local', module_path=p_to_modules, forks=10,
                  become=None, become_method=None, become_user=None, check=False,
                  diff=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = InventoryManager(loader=loader, sources=['/home/marizaga/ansible/hosts'])
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create play with tasks
play_source =  dict(
        name = "Ansible Play",
        hosts = 'ubuntu_server',
        gather_facts = 'yes',
	#tasks = [
         #   dict(action=dict(module='shell', args='ls'), register='shell_out'),
          #  dict(action=dict(module='command', args='/bin/date'),register='date_out'),
          #  dict(action=dict(module='command', args='apt remove tree'), register='apt_install_out'),
          #  dict(action=dict(module='debug', args=dict(msg='{{/shell_out.stdout}}')))
        # ]
	tasks =[
	   dict(action=dict(module='command', args='ls'), register='command_output')]

       # tasks = [
        #    dict(action=dict(module='sros_command', args=dict(commands='show version')), register='sros_out'),
	 #   dict(action=dict(module='debug', args=dict(msg='{{sros_out.stdout}}')))
         #]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# actually run it
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play)
    #with open('Resultado.json','w+') as file:
     #    file.write(json.dumps({"Resultados":result}, indent=4))

finally:
    if tqm is not None:
        tqm.cleanup()
