# Basic
## Permissions
For setting the correct permissions inside the container and on the host we will use the following commands: `chown` and `chmod`.

### chown
Inside the [Dockerfile](Dockerfile) we give the `rootless-nginx` user permissions to the required nginx files using the chown command.
```
RUN chown -R rootless-nginx:rootless-nginx-group /var/lib/nginx /var/log/nginx /run/nginx
```
When we comment out or remove the line above from the configuration we get the following error when starting the [docker-compose.yml](docker-compose.yml) file.
```bash
Attaching to reverse-proxy-1, webserver-1
webserver-1  | nginx: [alert] could not open error log file: open() "/var/lib/nginx/logs/error.log" failed (13: Permission denied)
webserver-1  | 2026/02/19 00:00:00 [emerg] 1#1: mkdir() "/var/lib/nginx/tmp/client_body" failed (13: Permission denied)
reverse-proxy-1  | nginx: [alert] could not open error log file: open() "/var/lib/nginx/logs/error.log" failed (13: Permission denied)
reverse-proxy-1  | 2026/02/19 00:00:00 [emerg] 1#1: mkdir() "/var/lib/nginx/tmp/client_body" failed (13: Permission denied)
webserver-1 exited with code 1
reverse-proxy-1 exited with code 1
```

### chmod
When using chmod on the reverse proxy [nginx.conf](reverse-proxy/nginx.conf) we can change the permissions. For this example we will be using the following command:
```bash
sudo chmod 000 reverse-proxy/nginx.conf
```

Before the chmod command
```bash
/1-basic/reverse-proxy$ ls -l
total 4
-rw-rw-r-- 1 user user 1139 Feb 19 00:00 nginx.conf
```

After the chmod command
```shell
/1-basic/reverse-proxy$ ls -l
total 4
---------- 1 user user 1139 Feb 19 00:00 nginx.conf
```

To revert back to default we can just use the following command:
```shell
sudo chmod 664 reverse-proxy/nginx.conf
```

## Connectivity
Once we have started our containers using the `docker compose up -d` (do not forget the -d to detach) command we can test our connectivity. To test connectivity of our containers we will use the following commands `curl`, `ip a` and some docker commands.

### curl
We first test if our connectivity to the container on port 80 is working.
```shell
/1-basic$ curl localhost:80
<body>Hello world!</body>
```

Now we test if our connectivity to the container on port 443 is working.
```shell
/1-basic$ curl localhost:443
<body>Hello world!</body>
```

### docker ps -a
This looks good we can see that both our port 80 and 443 show the Hello World! text we defined in our [index.html](webserver/index.html). However this does not confirm if we are actually passing the connection using our reverse proxy or we are connecting directly. We can check that by looking at the bound ports on our machine.
```shell
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                                                          NAMES
000000000001   1-basic-reverse-proxy   "nginx -g 'daemon of…"   3 minutes ago   Up 3 minutes   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp   1-basic-reverse-proxy-1
000000000002   1-basic-webserver       "nginx -g 'daemon of…"   3 minutes ago   Up 3 minutes   80/tcp, 443/tcp                                                                1-basic-webserver-1
```
Here we can see our webserver has two ports exposed `80/tcp, 443/tcp`, but it is not bound to our host as we can see on the ports of our reverse proxy `0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp`.

### ip a
This is cool but the IPs are assigned dynamically to the containers so using the `ip a` command we can actually see what IP they have locally (Your logging will look bigger, but due to this being public I have removed identifying information).
```shell
/1-basic$ ip a

1: lo: <LOOPBACK,UP> mtu 65536
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host

2: docker0: <BROADCAST,MULTICAST,UP> mtu 1500
    inet 172.17.0.1/16 scope global docker0

3: br-XXXX: <BROADCAST,MULTICAST,UP> mtu 1500
    inet 172.18.0.1/16 scope global br-XXXX
```

### docker network / ping
The above is cool and all, but we still do not know what IPs our containers have specifically so to find those we can do the following. First we get the automatically created networks from docker compose (we could also pre create them, but that is out of scope for this example)
```shell
/1-basic$ sudo docker network list
NETWORK ID     NAME                  DRIVER    SCOPE
000000000001   1-basic_edge-router   bridge    local
000000000002   1-basic_internal      bridge    local
000000000003   bridge                bridge    local
000000000004   host                  host      local
000000000005   none                  null      local
```

Now we have the names and IDs we can use that to inspect them.
```shell
/1-basic$ sudo docker network inspect 1-basic_internal
[
    {
        "Name": "1-basic_internal",
        "Id": "000000000002",
        "Created": "2026-02-19T00:00:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": true,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Options": {},
        "Labels": {
            "com.docker.compose.config-hash": "xxxxxxxxxxxxxxxxBBBBBBBBBBBBBBccccccccccccccccccQQQQQQQQQQQQQQQQ",
            "com.docker.compose.network": "internal",
            "com.docker.compose.project": "1-basic",
            "com.docker.compose.version": "5.0.2"
        },
        "Containers": {
            "000000000001": {
                "Name": "1-basic-reverse-proxy-1",
                "EndpointID": "xxxxxxxxxxxxxxxxBBBBBBBBBBBBBBccccccccccccccccccQQQQQQQQQQQQQQQQ",
                "MacAddress": "aa:bb:cc:dd:ee:ff",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            },
            "000000000002": {
                "Name": "1-basic-webserver-1",
                "EndpointID": "xxxxxxxxxxxxxxxxBBBBBBBBBBBBBBccccccccccccccccccQQQQQQQQQQQQQQQQ",
                "MacAddress": "ff:ee:dd:cc:bb:aa",
                "IPv4Address": "172.19.0.3/16",
                "IPv6Address": ""
            }
        },
        "Status": {
            "IPAM": {
                "Subnets": {
                    "172.19.0.0/16": {
                        "IPsInUse": 5,
                        "DynamicIPsAvailable": 65531
                    }
                }
            }
        }
    }
]
```
And voila we have our two dynamically assigned IPs created by Docker! For the reverse proxy it is `172.19.0.2` and for the webserver it is `172.19.0.3`. So now lets try to ping them.

For our reverse proxy (172.19.0.2)
```shell
/1-basic$ ping 172.19.0.2
PING 172.19.0.2 (172.19.0.2) 56(84) bytes of data.
64 bytes from 172.19.0.2: icmp_seq=1 ttl=64 time=0.770 ms
64 bytes from 172.19.0.2: icmp_seq=2 ttl=64 time=0.106 ms
64 bytes from 172.19.0.2: icmp_seq=3 ttl=64 time=0.084 ms
64 bytes from 172.19.0.2: icmp_seq=4 ttl=64 time=0.075 ms
^C
--- 172.19.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3052ms
rtt min/avg/max/mdev = 0.075/0.258/0.770/0.295 ms
```

For our webserver (172.19.0.3)
```shell
/1-basic$ ping 172.19.0.3
PING 172.19.0.3 (172.19.0.3) 56(84) bytes of data.
64 bytes from 172.19.0.3: icmp_seq=1 ttl=64 time=0.269 ms
64 bytes from 172.19.0.3: icmp_seq=2 ttl=64 time=0.084 ms
64 bytes from 172.19.0.3: icmp_seq=3 ttl=64 time=0.092 ms
64 bytes from 172.19.0.3: icmp_seq=4 ttl=64 time=0.054 ms
^C
--- 172.19.0.3 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3106ms
rtt min/avg/max/mdev = 0.054/0.124/0.269/0.084 ms
```

But if we use an IP not connected to a container we get the following:
```shell
/1-basic$ ping 172.19.0.5
PING 172.19.0.5 (172.19.0.5) 56(84) bytes of data.
From 172.19.0.1 icmp_seq=1 Destination Host Unreachable
From 172.19.0.1 icmp_seq=2 Destination Host Unreachable
From 172.19.0.1 icmp_seq=3 Destination Host Unreachable
^C
--- 172.19.0.5 ping statistics ---
5 packets transmitted, 0 received, +3 errors, 100% packet loss, time 4126ms
```

### docker network / attach
To test if the connectivity between our containers is working we can attach to one of the containers and try to ping one another. Luckily Docker automatically assigns DNS names for the containers started in the same docker compose. This allows us to ping based on the service name defined in the docker compose.

```shell
/1-basic$ sudo docker compose exec webserver ping reverse-proxy
PING reverse-proxy (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=42 time=0.076 ms
64 bytes from 172.18.0.3: seq=1 ttl=42 time=0.120 ms
64 bytes from 172.18.0.3: seq=2 ttl=42 time=0.157 ms
64 bytes from 172.18.0.3: seq=3 ttl=42 time=0.164 ms
^C
--- reverse-proxy ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 0.076/0.129/0.164 ms
```

And voila connectivity from our webserver to our reverse-proxy. Since our webserver is in a Docker network with the internal flag enabled. It shouldn't be able to ping for example to Cloudflares dns.
```shell
/1-basic$ sudo docker compose exec webserver ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
ping: sendto: Network unreachable
```
And indeed it does not work. However our reverse proxy should be able to connect to the outside world.
```shell
/1-basic$ sudo docker compose exec reverse-proxy ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=42 time=5.731 ms
64 bytes from 1.1.1.1: seq=1 ttl=42 time=3.518 ms
64 bytes from 1.1.1.1: seq=2 ttl=42 time=3.144 ms
64 bytes from 1.1.1.1: seq=3 ttl=42 time=3.538 ms
^C
--- 1.1.1.1 ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 3.144/3.982/5.731 ms
```

### Confirmation
So after all these tests lets confirm that our reverse proxy headers have come with the request.
```shell
/1-basic$ curl -i localhost
HTTP/1.1 200 OK
Server: nginx/1.28.2
Date: Thu, 19 Feb 2026 00:00:00 GMT
Content-Type: text/html
Content-Length: 26
Connection: keep-alive
Last-Modified: Thu, 19 Feb 2026 00:00:00 GMT
ETag: "69905b15-1a"
Accept-Ranges: bytes
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self';

<body>Hello world!</body>
```
