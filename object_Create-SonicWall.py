import paramiko
from argparse import ArgumentParser
from paramiko_expect import SSHClientInteraction

class SSH:
    def __init__(self, ip, username, password):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=ip, username=username, password=password)

        except Exception as err:
            print('Error connection', err)

    def exec_cmd(self, prompt, arq, name, zone):
        try:
            n = 0
            with open(arq) as f:
                txt = f.readlines()
                f.close()

            with SSHClientInteraction(self.ssh, timeout=10, display=True) as interact:
                interact.send('configure')
                for data in txt:
                    n += 1
                    data = data.replace('\n', '')
                    var = 'address-object ipv4 \"{}\" host {} zone {}'.format(
                        name + str(n), data, zone)
                    interact.send(var)

                interact.send('commit')

                interact.send('exit')
                interact.send('exit')
                interact.expect(prompt, timeout=10)

        except Exception as err:
            print(err)


def menu():
    parser = ArgumentParser(description='Change options for execute the Script',
                            prefix_chars='--')
    parser.add_argument('-t', action='store', type=str, required=True,
                        help='Use for set host SonicWall - REQUIRED')

    parser.add_argument('-u', action='store', type=str, default='admin',
                        help='Use for set Username to access SonicWall')

    parser.add_argument('-p', action='store', type=str, default='password',
                        help='Use for set Password to access SonicWall')

    parser.add_argument('-a', action='store', type=str, required=True,
                        help='Use for set data list IP - REQUIRED')

    parser.add_argument('-name', action='store', type=str, default='host',
                        help='Use for set name base to Variable in SonicWall')

    parser.add_argument('-zone', action='store', type=str, default='WAN',
                        help='Use for set ZONE to host in SonicWall')
    result = parser.parse_args()
    return result


option = menu()
print('Host: {}\nUsername: {}\nPassword: {}\nData: {}\nVariable Name base: {}\nZone: {}'.format(
        option.t, option.u, option.p, option.a, option.name, option.zone))

ssh = SSH(option.t, option.u, option.p)
prompt = '{}@paramiko-expect-dev:~\$\s+'.format(option.u)

ssh.exec_cmd(prompt, option.a, option.name, option.zone)
