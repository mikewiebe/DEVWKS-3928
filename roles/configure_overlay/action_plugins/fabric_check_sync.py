from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.utils.display import Display
from ansible.plugins.action import ActionBase


display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        results = super(ActionModule, self).run(tmp, task_vars)
        results['changed'] = False
        results['failed'] = False

        fabric = self._task.args["fabric"]

        ndfc_response = self._execute_module(
            module_name="cisco.dcnm.dcnm_rest",
            module_args={
                "method": "GET",
                "path": f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric}/inventory/switchesByFabric",
            },
            task_vars=task_vars,
            tmp=tmp
        )

        if ndfc_response['response'].get('DATA'):
            for switch in ndfc_response['response']['DATA']:
                if switch['ccStatus'] == 'Out-of-Sync':
                    results['changed'] = True
                    break

        return results
