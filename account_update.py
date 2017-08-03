#account update
import secrets, time, json, sys

port_config = {}
for i in range(10):
    port = secrets.choice(range(1024, 9999))
    password = secrets.token_urlsafe(16)
    port_config[port] = password

f = open('info.dat', 'w')
json.dump(port_config, f)
f.close()

f = open('time.dat' ,'w')
f.write(time.asctime(time.localtime(time.time())))
f.close()

port_config["416"] = "0000000"

f = open(sys.argv[1] + 'user-config.json', 'r+')
config = json.load(f)
config['port_password'] = port_config

f.seek(0)
f.write(json.dumps(config))
f.close()
