#!/usr/bin/env python3
''' Importa pontos de montagem cifs para o monit
    Exemplo de log em srvexa02vm01
    sudo monit summary | awk '{if(NR>2)print}' | grep -v 'OK'
'''

import re
from string import Template


MONIT_TEMPLATE = '''
check filesystem $rootfs path $fs_file
        start program = "/bin/mount $fs_spec" timeout 5 seconds
        stop program = "/bin/umount $fs_spec" with timeout 5 seconds
        if does not exist for 3 cycles then restart
        if does not exist for 3 cycles then exec /usr/local/bin/log_monit_event
'''

# fs_spec       //rj2k12dfs01.globosat.net.br/acervo_DEV/
# fs_file       /var/cifs/acervo
# fs_vfstype    cifs
# fs_mntops     _netdev...
# fs_freq       0
# fs_passno     0
FSTAB_LINE = re.compile(r'(?P<fs_spec>.*) '
                        '(?P<fs_file>.*) '
                        '(?P<fs_vfstype>.*) '
                        '(?P<fs_mntops>.*) '
                        '(?P<fs_freq>.*) '
                        '(?P<fs_passno>.*)')


def fs_spec_fs_file_from_fstab(fstab_file):
    ''' Retorna um mapa fs_spec/fs_file
        para cada linha do arquivo fstab
        cujo campo fs_vfstype seja do tipo cifs
    '''
    with open(fstab_file, 'r') as fstab:
        for line in fstab:
            result = re.match(FSTAB_LINE, line)
            if result and (result.group('fs_vfstype') == "cifs"):
                fs_spec = result.group('fs_spec')
                fs_file = result.group('fs_file')
                yield {fs_spec: fs_file}


def fs_file_to_monit_rootfs(fs_file):
    ''' No monit o rootfs é um nome único
        que não deve conter uma ou mais barras "/"
    '''
    return (fs_file[1:]).replace('/', '-')


def build_template(fs_spec_fs_file_map):
    '''Imprime em tela o template'''
    check = Template(MONIT_TEMPLATE)
    for fs_spec, fs_file in fs_spec_fs_file_map.items():
        rootfs = fs_file_to_monit_rootfs(fs_file)
        monit = check.substitute(fs_spec=fs_spec, fs_file=fs_file,
                                 rootfs=rootfs)
        print(monit)


def main():
    '''Resultados'''
    # fs_spec_fs_file_map = fs_spec_fs_file_from_fstab('./srvexa01vm01-fstab')
    for sp in fs_spec_fs_file_from_fstab('./srvexa01vm01-fstab'):
        print(sp)

    # build_template(fs_spec_fs_file_map)


if __name__ in "__main__":
    main()
