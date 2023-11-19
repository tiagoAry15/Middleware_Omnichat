import subprocess
import os
import re


def execute_command(command):
    """Execute a command and return its output as a list of lines"""
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    return result.stdout.splitlines()


def get_service_details(pid):
    """Get the service name and details using the process ID"""
    cmd_task_list = f'tasklist /FI "PID eq {pid}" /NH /FO CSV'
    task_list_output = execute_command(cmd_task_list)
    details = None

    if task_list_output and "," in task_list_output[0]:
        executable_name = task_list_output[0].split(",")[0].strip('"').lower()

        # Check the command line arguments to deduce the service and get details
        cmd_wmic = f'wmic process where "ProcessID={pid}" get Commandline'
        wmic_output = execute_command(cmd_wmic)
        if wmic_output and len(wmic_output) > 1:
            for line in wmic_output[1:]:
                if line.strip():
                    details = line.strip()  # Update to take the correct line for commandline details
                    break

        if 'python' in executable_name and 'locust' in (details or ''):
            return 'Locust', details

        # Mapping executable names to service names
        service_map = {
            'locust.exe': 'Locust',
            # Add more mappings if needed
        }
        service_name = service_map.get(executable_name, executable_name)
        return service_name, details

    return 'Unknown', None


def get_ip_address_from_request(request) -> str:
    # Verificar se o cabeçalho 'CustomIp' está presente
    custom_ip = request.headers.get('CustomIp')
    if custom_ip:
        return custom_ip
    if request.sessions:
        return request.sessions.get('ip')
    # Lógica existente para obter o endereço IP
    if request.transport:
        return request.transport.get_extra_info('peername')[0]
    else:
        return 'Unknown'



def __main__():
    username = os.getlogin()  # Get the current logged-in username

    # Get a list of process IDs for processes run by your user
    cmd_task_list = f'tasklist /FI "USERNAME eq {username}" /NH /FO CSV'
    task_list_output = execute_command(cmd_task_list)

    # Extract the PIDs
    p_ids = {line.split(",")[1].strip('"'): line.split(",")[0].strip('"') for line in task_list_output if "," in line}

    # Check if these processes are listening on any port
    netstat_output = execute_command('netstat -ano')
    port_regex = re.compile(r':(\d+)\s+')

    # Using a dictionary to store port-service pairs and their details
    port_service_details = {}

    for line in netstat_output:
        if 'LISTENING' in line and any(pid in line for pid in p_ids.keys()):
            match = port_regex.search(line)
            if match:
                port = int(match.group(1))
                pid = line.rsplit()[-1]
                service_name, details = get_service_details(pid)
                port_service_details[port] = (service_name, details)

    # Printing as a table
    print("{:<25} {:<20} {}".format("Localhost", "Service Name", "Details"))
    print("-" * 80)
    for port in sorted(port_service_details.keys()):
        service, details = port_service_details[port]
        print("{:<25} {:<20} {}".format(f"http://localhost:{port}/", service, details if details else ""))


if __name__ == "__main__":
    __main__()
