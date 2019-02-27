Simulating network problems on OSX
==================================

Recently I had to simulate unreliable connections to a remote server,
for testing purposes. I needed two cases: a fully unreachable host, and
a host with considerable packet loss and delay. The first is easy to
achieve: just pull the cable. For the second, I had to google up, as my
network-fu is a bit rusty on the latest developments, especially on OSX.
I am more of a Linux guy when it comes to networking.

A quick search produced [this
blog](http://www.joemiller.me/2010/08/31/simulate-network-latency-packet-loss-and-bandwidth-on-mac-osx/),
with great details on how to achieve my needs. I copy the details here
for future reference.

Here I add a 1 second delay and a 0.4 packet loss in both directions

``` {.console}
bash-3.2# ipfw add pipe 1 ip from any to 10.0.0.1
00100 pipe 1 ip from any to 10.0.0.1

bash-3.2# ipfw add pipe 1 ip from 10.0.0.1 to any
00200 pipe 1 ip from any to any src-ip 10.0.0.1

bash-3.2# ipfw pipe 1 config delay 1000ms plr 0.4
bash-3.2# ipfw pipe 2 config delay 1000ms plr 0.4

bash-3.2# ping 10.0.0.1
PING 10.0.0.1 (10.0.0.1): 56 data bytes
Request timeout for icmp_seq 0
64 bytes from 10.0.0.1: icmp_seq=0 ttl=64 time=2000.386 ms
```

This is really harsh, but it is what I need.

The `ipfw` utility is the traditional FreeBSD packet filter. The amount
of power behind this little command is impressive and reminds me of
Linux `iptables`. `ipfw` has been deprecated in OSX 10.9 in favor of
`pfctl`. Similarly, `iptables` is going to be deprecated on Linux in
favor of `nftables`.
