channel channel01 create -dst-addr 127.0.0.1 -protocol tcp
controller controller01 create -channel channel01 -role equal -connection-type main

interface interface01 create -type ethernet-rawsock -device br-eth

port port01 create -interface interface01

bridge bridge01 create -controller controller01 -port port01 1 -dpid 0x1
bridge bridge01 enable

flow bridge01 add in_port=1 apply_actions=output:4294967292
