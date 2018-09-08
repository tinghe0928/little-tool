import logging
import os
import sys
import json
import user360log
import pexpect


from user360log import *


def load_config():
    argv = sys.argv[1:]
    default_file = os.path.abspath('.') +'/'+'config_v_061.json'
    cmd_file = os.path.abspath('.') +'/'+'config_cmd.json'
    if argv != []:
        print "**using customized configure file**"
        if "-" in argv[0]:
            conf_file =  os.path.abspath('.') +'/'+ str(sys.argv[2])
        else:
            conf_file = default_file
    else:
        print "**using default configure file**"
        conf_file = default_file  
    try:
        simulator_ip = get_sim_ip()
    except Exception:
        simulator_ip = '89.0.0.7'
    #conf_file= ''.join([os.path.abspath('.'),'/config_v_052.json'])
    with open(conf_file) as f:
        data = json.load(f)
    clusterip = data['clusterip']
    upg_oam_ip = data['upg_oam_ip']
    #print clusterip
    if clusterip:
        logger.debug( 'Loading configuration SC-2 ip %s', clusterip )
    else:
        logger.debug( 'Configuration clusterip is not defined' )
    user = data['user']
    psd = data['psd']
    user360user = data['user360user']
    user360psd = data['user360psd']
    upg_sc = data['upg_sc']
    upg_pl = data['upg_pl']
    cudb_system = data['cudb_system']
    if not cudb_system:
        logger.warn('Configuration cudb_system is not defined')
    else:
        cudb_oam_vip_list = []
        cudb_psd_list = []
        for cudb_node in cudb_system:
            cudb_oam_vip_list.append(cudb_node['cudb_oam_vip'])
            cudb_psd_list.append(cudb_node['cudb_psd'])
        for ip in cudb_oam_vip_list:
            if not validate_ip(ip):
                logger.debug('Invalid IP %s defined', ip)
                sys.exit('Exit! Invalid configuration - invalid IP address defined')
    dsgs = data['dsgs']
    dsg_port = data['dsg_port']
    dsg_host = data['dsg_host']
    initial_load_estimated_time = data['initial_load_estimated_time']
    
    """get command line list from json file config_cmd.json"""
    with open(cmd_file) as f_cmd:
        list_cmd = json.load(f_cmd)
    user360cmd = list_cmd['user360cmd']
    
    result = {
        'clusterip': clusterip,
        'simulator_ip': simulator_ip,
        'upg_oam_ip': upg_oam_ip,
        'user': user,
        'psd': psd,
        'user360user': user360user,
        'user360psd': user360psd,
        'upg_sc': upg_sc,
        'upg_pl' : upg_pl,
        'initial_load_estimated_time' : initial_load_estimated_time,
        'cudb_system': cudb_system,
        'dsgs' : dsgs,
        'dsg_port':dsg_port,
        'dsg_host':dsg_host,
        'user360cmd' : user360cmd
        }
    return result
def validate_ip(string):
    s = string.split('.')
    if len(s) != 4:
        return False
    else:
        for x in s:
            if not x.isdigit():
                return False
            else:
                i = int(x)
                if i < 0 or i > 255:
                    return False
    return True
def get_sim_ip():
    sim_ip = os.popen("sudo /sbin/ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -2").read().split()[-1]
    return sim_ip