# Auto MLAG on Controlling Bridge platforms
This tool configures MLAG on vpex enabled/disabled switches.

### Description
This script detects peer connected links thru lldp and configures LACP on PEER links and creates ISC_VLAN with IP Address. And associates the ISC_VLAN to the MLAG
This script has to be executed on both PEERs

**Please review the configuration before loading the configuration on a switch**

### Files
* [The Core Python Script - auto_mlag.py](auto_mlag.py)
* [README.md](README.md)

### Requirements
Firmware: ExtremeXOS(TM)
This script was tested on 31.5 and older.

### Features
* This Script can only run on EXOS. 
 

### How to use
* download this script to the switches PEER-1 and PEER-2
* Execute the script on PEER-1 Ex: 'run script auto_mlag.py'
* Wait for the PEER-1 execution to get completed
* Now execute the script on PEER-2
* The above steps completes the MLAG configuration.
* You shall enable "vpex auto-configuration" to attach BPEs to the MLAG switches 

### NOTE :
* script does not work, if more than one peer is connected
* do not run this script parallel on both PEERs. You have to run the script on PEER-1 first.
* Once it completes on PEER-1, then start to execute on PEER2
* **Below are the PEER IPs and VLAN details variable used in the script. It can be changed based on the requirement.**
```
peer_ip_list = ['169.254.0.1/16', '169.254.0.2']
isc_vlan = {'name' : 'isc_mlag', 'tag' : '4094', 'mode' : 'tagged'}
```

## EXOS run example:
Execution on PEER-1 :

```
* (CIT_31.6.0.404) X465-24MU.13 # run script auto_mlag.py
[+] Port(s) connected to the peer : 26, 28
Warning: Any config on the master port is lost (STP, IGMP Filter, IGMP Static Group, MAC-Security, CFM, etc.)

[+] enable sharing 26 grouping 26, 28 lacp
Error: VLAN isc_mlag does not have primary address!
[+] Peer IP is not available
[+] Local IP 169.254.0.1/16
[+] MLAG created
```

Execution on PEER-2:

```
* (CIT_31.6.0.412) X465-24XE.2 # run script auto_mlag.py
[+] Port(s) connected to the peer : 22, 24
Warning: Any config on the master port is lost (STP, IGMP Filter, IGMP Static Group, MAC-Security, CFM, etc.)

[+] enable sharing 22 grouping 22, 24 lacp
Error: VLAN isc_mlag does not have primary address!
[+] Peer IP available 169.254.0.1/16
[+] Local IP 169.254.0.2
[+] MLAG created
* (CIT_31.6.0.412) X465-24XE.3 # show mlag peer
Multi-switch Link Aggregation Peers:

MLAG Peer         : Mlag_peer1
VLAN              : isc_mlag               Virtual Router    : VR-Default
Local IP Address  : 169.254.0.2            Peer IP Address   : 169.254.0.1
MLAG ports        : 0                      Tx-Interval       : 1000 ms
Checkpoint Status : Up                     Peer Tx-Interval  : 1000 ms
Rx-Hellos         : 9                      Tx-Hellos         : 9
Rx-Checkpoint Msgs: 10                     Tx-Checkpoint Msgs: 10
Rx-Hello Errors   : 0                      Tx-Hello Errors   : 0
Hello Timeouts    : 0                      Checkpoint Errors : 0
Up Time           : 0d:0h:0m:7s            Peer Conn.Failures: 0
Local MAC         : 00:04:96:ba:84:50      Peer MAC          : 00:11:88:fe:df:f2
Config'd LACP MAC : None                   Current LACP MAC  : 00:04:96:ba:84:50
Authentication    : None

Alternate path information: None
* (CIT_31.6.0.412) X465-24XE.4 #
* (CIT_31.6.0.412) X465-24XE.4 # show log
12/23/2021 14:07:14.74 <Info:AAA.authPass> Login passed for user admin through serial
12/23/2021 12:39:48.20 <Noti:DM.Notice> Setting hwclock time to system time, and broadcasting time
12/23/2021 11:41:57.59 <Info:AAA.logout> Administrative account (admin) logout from serial
12/23/2021 11:21:48.11 <Noti:VSM.RmtMLAGPeerUp> Peer 2:169.254.0.1:: Peer is active
12/23/2021 11:21:47.75 <Info:System.userComment> autoMlag:- script shutdown
12/23/2021 11:21:47.75 <Info:System.userComment> autoMlag:- config mlag peer Mlag_peer1 ipaddress 169.254.0.1 vr vr-default
12/23/2021 11:21:47.75 <Noti:VSM.RmtMLAGPeerDown> Peer 0::: Peer is down
12/23/2021 11:21:34.89 <Info:System.userComment> autoMlag:- config vlan isc_mlag add port 22 tagged
12/23/2021 11:21:26.82 <Info:LACP.AddPortToAggr> Add port 24 to aggregator
12/23/2021 11:21:26.82 <Info:LACP.AddPortToAggr> Add port 22 to aggregator
12/23/2021 11:21:24.82 <Info:System.userComment> autoMlag:- enable sharing 22 grouping 22, 24 lacp
12/23/2021 11:21:24.71 <Info:System.userComment> autoMlag:- script started

```

## License
Copyright© 2015, Extreme Networks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
The software is provided as is and Extreme Networks has no obligation to provide
maintenance, support, updates, enhancements or modifications.
Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).

>Be Extreme
