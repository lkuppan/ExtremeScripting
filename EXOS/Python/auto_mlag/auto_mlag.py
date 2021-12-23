# auto_mlag.py
#
#       This script configures MLAG in the CB (vpex enabled standalone device)
#       this script should be downloaded on the standard VPEX MLAG Switches which
#       should not have more than one PEER for each other CB.
#
#       it detects the PEER using lldp and configures LACP on PEER links and
#       creates ISC_VLAN and assigns the IP Address. And associates the ISC_VLAN to
#       the MLAG.
# Note:
#       script does not work, if more than one peer is connected
#       this script should be downloaded on both PEERs
#       do not run this script parallel on both PEERs. You have to run the script on PEER-1.
#       Once it completes on PEER-1, then start to execute on PEER2
#       Below are the PEER IPs and VLAN details used for this script. It can be changed
#       based on the requirement.
#       peer_ip_list = ['169.254.0.1/16', '169.254.0.2']
#       isc_vlan = {'name' : 'isc_mlag', 'tag' : '4094', 'mode' : 'tagged'}
#
# Last updated: Dec 23, 2021
#
# --- Following variables can be updated, if it conflicts in your network
peer_ip_list = ['169.254.0.1/16', '169.254.0.2']
isc_vlan = {'name': 'isc_mlag', 'tag': '4094', 'mode': 'tagged'}

import json
import time
import sys


def exec_cli(cmd):
    try:
        return exsh.clicmd(cmd, True)
    except:
        return False

def print_userlog(msg):
    cmd = 'create log message \"autoMlag:- {0}\"'.format(msg)
    exec_cli(cmd)

def parse_lldp():
    peer_sw = None
    wait_cnt = 0
    while peer_sw is None:
        output = exec_cli('debug cfgmgr show next lldp.lldpPortNbrInfoShort')
        dict_op = json.loads(output)
        nbr_name, nbr_pid, locl_pid, nbr_mac = ([] for i in range(4))

        for each_list in dict_op['data']:
            if each_list['nbrSysDescr'] and 'ExtremeXOS' in each_list['nbrSysDescr']:
                nbr_name.append(str(each_list['nbrSysName']))
                nbr_mac.append(str(each_list['nbrChassisID']))
                nbr_pid.append(str(each_list['nbrPortID']))
                locl_pid.append(str(each_list['port']))
                peer_sw = 'True'
        if peer_sw is None:
            print('[+] waiting for peer switch..')
            time.sleep(5)
            if wait_cnt <= 10:
                wait_cnt = wait_cnt + 1
            else:
                print('[x] No peer found, exited')
                sys.exit()

    return get_lldp_ports(nbr_name, nbr_mac, nbr_pid, locl_pid)

def get_lldp_ports(nbr_name, nbr_mac, nbr_pid, locl_pid):
    cnt = len(nbr_mac) - 1
    i = 0
    port_cnt = 1
    sharing_ports = []
    peer_list = {}
    while cnt >= 0:
        while i <= cnt:
            if i == cnt:
                break
            if nbr_mac[i] == nbr_mac[cnt]:
                sharing_ports.append("{0}, {1}".format(locl_pid[i], locl_pid[cnt]))
                port_cnt = port_cnt + 1
            i = i + 1
        if sharing_ports:
            peer_list[str(nbr_mac[cnt])] = sharing_ports
        else:
            sharing_ports.append(locl_pid[0])
            peer_list[str(nbr_mac[cnt])] = sharing_ports
        i = 0
        cnt = cnt - 1
    if len(peer_list) > 1:
        print('ERROR: more than one peer is available')
        sys.exit()

    for mac in peer_list:
        print('[+] Port(s) connected to the peer : ' + str(peer_list[mac][0]))
        return peer_list[mac][0].split(',')[0], peer_list[mac][0]

def create_lag(m_port, l_port):
    cmd = ('enable sharing {0} grouping {1} lacp'.format(m_port, l_port))
    exec_cli(cmd)
    print('[+] {}'.format(cmd))
    print_userlog(cmd)

def peer_ping(src_ip, dst_ip, cnt=1):
    out = exec_cli('ping count {0} vr VR-Default {1} from {2}'.format(cnt, dst_ip, src_ip))
    if '16 bytes from' in out:
        return True
    else:
        return False

def config_vlan_ip(ip, vlan_name):
    exec_cli('unconfigure vlan {0} ipaddress'.format(vlan_name))
    exec_cli('configure vlan {0} ipaddress {1}'.format(vlan_name, ip))
    time.sleep(1)
    return True

def create_isc_vlan(pid):
    exec_cli('create vlan {0} tag {1}'.format(isc_vlan['name'], isc_vlan['tag']))
    cmd = ('config vlan {0} add port {1} {2}'.format(isc_vlan['name'], pid, isc_vlan['mode']))
    exec_cli(cmd)
    print_userlog(cmd)
    ip1 = peer_ip_list[0].split('/')[0]
    ip2 = peer_ip_list[1].split('/')[0]
    config_vlan_ip(peer_ip_list[0], isc_vlan['name'])
    if peer_ping(ip1, ip2, '1') is False:
        config_vlan_ip(peer_ip_list[1], isc_vlan['name'])
        if peer_ping(ip2, ip1, '10') is False:
            print('[+] Peer IP is not available')
            config_vlan_ip(peer_ip_list[0], isc_vlan['name'])
            print('[+] Local IP {0}'.format(peer_ip_list[0]))
            return 'Mlag_peer2', ip2
        else:
            print('[+] Peer IP available {0}'.format(peer_ip_list[0]))
            print('[+] Local IP {0}'.format(peer_ip_list[1]))
            return 'Mlag_peer1', ip1
    else:
        print('[+] Peer IP is available')
        config_vlan_ip(peer_ip_list[0], isc_vlan['name'])
        print('[+] Local IP {0}'.format(peer_ip_list[0]))
        return 'Mlag_peer2', ip2

def config_mlag(peer_name, ip):
    exec_cli('create mlag peer {0}'.format(peer_name))
    cmd = ('config mlag peer {0} ipaddress {1} vr vr-default'.format(peer_name, ip))
    exec_cli(cmd)
    print_userlog(cmd)
    print('[+] MLAG created')

if __name__ == '__main__':
    print_userlog('script started')
    master_port, lag_ports = parse_lldp()
    create_lag(master_port, lag_ports)
    time.sleep(10)
    peer_name, ip = create_isc_vlan(master_port)
    config_mlag(peer_name, ip)
    print_userlog('script shutdown')
