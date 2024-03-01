#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from netmiko import ConnectHandler

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            search_string=dict(type='str', required=True),
        )
    )

    host = module.params['host']
    username = module.params['username']
    password = module.params['password']
    search_string = module.params['search_string']

    try:
        # Connect to the MikroTik device using Netmiko
        device = {
            'device_type': 'mikrotik_routeros',
            'ip': host,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**device)

        # Send the command to retrieve the running configuration
        output = net_connect.send_command("/export")

        # Check if the search string is present in the configuration
        result = {"found": search_string in output}

        net_connect.disconnect()

        module.exit_json(changed=False, meta=result)

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
