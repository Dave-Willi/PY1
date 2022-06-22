@Echo Off
Echo Mapping LPT Ports

net use lpt1: /delete
net use lpt2: /delete
net use lpt3: /delete
net use lpt4: /delete
net use lpt6: /delete
net use lpt7: /delete
net use lpt1 \\10.151.53.22\rug-cfg-zebra-01 /persistent:yes /USER:config\config.engineer homebuild
net use lpt2 \\10.151.53.22\rug-cfg-zebra-02 /persistent:yes /USER:config\config.engineer homebuild
net use lpt3 \\10.151.53.22\rug-cfg-zebra-03 /persistent:yes /USER:config\config.engineer homebuild
net use lpt4 \\10.151.53.22\rug-cfg-zebra-04 /persistent:yes /USER:config\config.engineer homebuild
net use lpt6 \\10.151.53.22\rug-cfg-zebra-06 /persistent:yes /USER:config\config.engineer homebuild
net use lpt7 \\10.151.53.22\rug-cfg-zebra-07 /persistent:yes /USER:config\config.engineer homebuild