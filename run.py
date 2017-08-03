path = '/home/frcskoh/app'
project = 'shadowsocksr_share'
git_URL = ''
main_file = 'index.py'
main_route = 'index'

host = '127.0.0.1'
port = '5555'
safe_command = ('apt-get', 'pip', 'git')

import os
from linux_oper import *

def uwsgi_config(main_file, main_route, port):
    os.chdir(path)
    os.chdir(project)

    f = open('config.ini', 'w')

    f.write('[uwsgi]\n')
    f.write('master = true\n')
    f.write('home = ENV\n')
    f.write('wsgi-file = ' + main_file + '\n')
    f.write('callable = ' + main_route + '\n')
    f.write('socket = :' + port + '\n')
    f.write('processes = 1\n')
    f.write('threads = 4\n')
    f.write('buffer-size = 32768\n')

    f.close()
    return 
    
def nginx_config(project, ip, port, path, localhost, main_file, main_route):
    os.chdir('/etc/nginx/sites-enabled/')
    if os.path.exists('default'):
        os.remove('default')

    f = open(project + '_config', 'w')
    
    f.write('server {\n')
    f.write('listen ' + port + ';\n')
    f.write('server_name ' + ip + ';\n')
    f.write('access_log ' + path + '/logs/access.log\n')
    f.write('error_log ' + path + '/logs/error.log\n')
    f.write('location / {\n')
    f.write('include ' + 'uwsgi_params\n')
    f.write('uwsgi_pass ' + localhost + '\n')
    f.write('uwsgi_param UWSGI_PYHOME ' + path + '/ENV\n')
    f.write('uwsgi_param UWSGI_CHDIR ' + path + '\n')
    f.write('uwsgi_param UWSGI_SCRIPT ' + main_file + ':' + main_route + '\n')
    f.write('}\n')
    f.write('}\n')

    f.close()
    
    create_soft_link(project + '_config', '/etc/nginx/sites-enabled/', '/etc/nginx/sites-available/')
    return 

    
#init
task_kill(safe_command)
apt_install(('build-essential -y', 'python3-dev -y', 'virtualenv -y', 'nginx -y', 'git -y'))

#create
if not os.path.exists('app'):
    os.mkdir('app')
os.chdir(path)

#os.system('git clone -b manyuser ' + git_URL)

os.chdir(project)
os.system('virtualenv -p /usr/bin/python3 ENV')

#install
os.chdir(path)
os.chdir(project)
pip_install(('-r requirements.txt', 'uwsgi'), 'ENV/bin/')
uwsgi_config(main_file, main_route, '8888')

#Nginx config
nginx_config(project, host, port, path, '127.0.0.1', main_file, main_route)
