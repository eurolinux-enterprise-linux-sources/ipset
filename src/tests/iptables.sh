#!/bin/sh

# set -x
set -e

# We play with the following networks:
# inet: 10.255.255.0/24
# 	10.255.255.0-31 in ip1
# 	10.255.255.32-63 in ip2
# 	rest in ipport
# inet6: 1002:1002:1002:1002::/64
#	1002:1002:1002:1002::1 in ip1
#	1002:1002:1002:1002::32 in ip2
#	rest in ipport

case "$1" in
inet)
	cmd=iptables
	family=
	NET=10.255.255.0/24
	IP1=10.255.255.1
	IP2=10.255.255.32
	;;
inet6)
	cmd=ip6tables
	family="family inet6"
	NET=1002:1002:1002:1002::/64
	IP1=1002:1002:1002:1002::1
	IP2=1002:1002:1002:1002::32
	;;
*)
	echo "Usage: $0 inet|inet6 start|stop"
	exit 1
	;;
esac


case "$2" in
start)
	../src/ipset n ip1 hash:ip $family 2>/dev/null
	../src/ipset a ip1 $IP1 2>/dev/null
	../src/ipset n ip2 hash:ip $family 2>/dev/null
	../src/ipset a ip2 $IP2 2>/dev/null
	../src/ipset n ipport hash:ip,port $family 2>/dev/null
	../src/ipset n list list:set 2>/dev/null
	../src/ipset a list ipport 2>/dev/null
	../src/ipset a list ip1 2>/dev/null
	$cmd -A INPUT ! -s $NET -j ACCEPT
	$cmd -A INPUT -m set ! --match-set ip1 src \
		      -m set ! --match-set ip2 src \
		      -j SET --add-set ipport src,src
	$cmd -A INPUT -m set --match-set ip1 src \
		      -j LOG --log-prefix "in set ip1: "
	$cmd -A INPUT -m set --match-set ip2 src \
		      -j LOG --log-prefix "in set ip2: "
	$cmd -A INPUT -m set --match-set ipport src,src \
		      -j LOG --log-prefix "in set ipport: "
	$cmd -A INPUT -m set --match-set list src,src \
		      -j LOG --log-prefix "in set list: "
	$cmd -A OUTPUT -d $NET -j DROP
	cat /dev/null > .foo.err
	;;
del)
	$cmd -F INPUT
	$cmd -A INPUT -j SET --del-set ipport src,src
	;;
timeout)
	../src/ipset n test hash:ip,port timeout 2
	$cmd -A INPUT -j SET --add-set test src,src --timeout 10 --exist
	;;
stop)
	$cmd -F
	$cmd -X
	../src/ipset -F 2>/dev/null
	../src/ipset -X 2>/dev/null
	;;
*)
	echo "Usage: $0 start|stop"
	exit 1
	;;
esac
