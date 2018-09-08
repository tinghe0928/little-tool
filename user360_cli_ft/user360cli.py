import logging
import pexpect
import sys
import time
import os
import cmd
import unittest
import subprocess
import traceback
import user360log
import datetime
import re

import upgcfg
from user360log import *
from upgcfg import *


PASS = '\033[30;42;1m'
FAIL = '\033[37;41;1m'
WARNING = '\033[33;1m'
ERROR = '\033[37;45;1m'
INCONC = '\033[37;47;1m'
INFO = '\033[37;44;1m'
#PRE = '\033[33;1m'
PRE = '\033[30;42;1m'
ENDC = '\033[0m'

def print_msg(text):
    def decorator(func):
        def func_wrapper(*args, **kw):
            print "*** {}".format( text + func.__name__ ).rjust(100,'*')
            return func(*args, **kw)
        return func_wrapper
    return decorator

def print_step_msg(text):
    def decorator(func):
        def func_wrapper(*args, **kw):
            print ""
            print "----- {}".format( text + func.__name__ ).rjust(60,'-')
            logger.debug( "----- {}".format( text + func.__name__ ).rjust(60,'-') )
            return func(*args, **kw)
        return func_wrapper
    return decorator

class User360Cli(unittest.TestCase):
    def setUp(self):
        try:
            print ""
            print PRE + "-------> {} ".format('case start').rjust(100,'-') + ENDC
            self.cur_dir = os.path.abspath('.')
            self.config_data = config_data = load_config()
            self.psd = self.config_data['psd']
            self.exception_list = []
            self.time_sync()
            retry_ssh_time = 3
            while retry_ssh_time > 0:
                try:
                    self.sc_2_login()
                    break
                except Exception as e:
                    retry_ssh_time -= 1
                    print "Fail to ssh this time, try again"
                    time.sleep(10)
            self.user360_login()
        except Exception as e:
            print ERROR,Exception,"::::",e,ENDC
            traceback.print_exc( file = child.logfile )
            child.logfile.flush()
    
    def sc_2_login(self):
        try:
            host_key_file = '/root/.ssh/known_hosts'
            if os.path.exists(host_key_file):
                os.remove(host_key_file)
            #ssh to sc-2 
            self.child = child = pexpect.spawn ('ssh '+self.config_data['user']+'@'+self.config_data['clusterip'])
            self.testlog = file(log_file,'aw')
            #self.childlog = file(log_file,'aw')
            #define child log
            child.logfile = self.testlog
            #print type(child.logfile)
            ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
            i = child.expect([pexpect.TIMEOUT, pexpect.EOF, ssh_newkey, 'Password:'])
            #print i
            if i == 0: # Timeout
                logger.debug('ERROR!')
                logger.debug('SSH could not login. Here is what SSH said:TIMEOUT')
                logger.debug(child.before)
                sys.exit()
            if i == 1:
                logger.debug('ERROR!')
                logger.debug('EOF')
                logger.debug(child.before)
                sys.exit()
            if i == 2: # SSH does not have the public key. Just accept it.
                child.sendline ('yes')
                #child.expect ('Password:')
                j = child.expect([pexpect.TIMEOUT, pexpect.EOF, 'Password:'])
                if j == 0|1: # Timeout
                    logger.debug('ERROR!')
                    logger.debug('SSH could not login. Here is what SSH said:')
                    logger.debug(child.before)
                    sys.exit()
                if j == 1: # E0F
                    logger.debug('ERROR!')
                    logger.debug('EOF')
                    logger.debug(child.before)
                    sys.exit()
            if i == 3:
                pass
            child.sendline (self.psd)
            child.expect('#')
            child.sendline('pam_tally2 --file /home/dveadm/faillog --user root --reset')
            child.expect('#',timeout=60)
            logger.debug( "ssh login succeed".rjust(100,'*') )
            time.sleep(5)
        except Exception as e:
            print ERROR,Exception,"::::",e,ENDC
            traceback.print_exc( file = child.logfile )
            child.logfile.flush()
            raise e
        
    def user360_login(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            logger.debug( "start to login user360".rjust(100,'*') )
            child.sendline ('user360 login')
            i = child.expect([pexpect.TIMEOUT, '#','Enter User name:'])
            #assert i == 2
            if i == 0:
                logger.debug('ERROR!')
                logger.debug('TIMEOUT')
                logger.debug(child.before)
                sys.exit()
            if i == 1:
                logger.debug( "Fail to login user360,please check the ip is right or user360 is installed".rjust(100,'*') )
                sys.exit()
            if i == 2:
                child.sendline('admin')
                child.expect('password:')
                child.sendline('admin')
                child.expect("User.360@admin:~>")
                logger.debug( 'user360 login succeed'.rjust(100,'*') )
            pass
        except Exception as e:
            print ERROR,Exception,"::::",e,ENDC
            traceback.print_exc( file = child.logfile )
            child.logfile.flush()
    def user360_logout(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            logger.debug( "start to logout user360".rjust(100,'*') )
            child.sendline ("exit")
            child.expect("#")
            logger.debug( 'user360 logout succeed'.rjust(100,'*') )
        except Exception as e:
            print ERROR,Exception,"::::",e,ENDC
            traceback.print_exc( file = child.logfile )
            child.logfile.flush()

    def tearDown(self):
        child = self.child
        child.sendline('exit')
        i = child.expect(['#',pexpect.EOF])
        if i == 0:
            child.sendline('exit')
            child.expect(pexpect.EOF)
        elif i == 1:
            pass
        else:
            pass
        print "-------> {} ".format('case end').rjust(100,'-')
        print ""
    
    def func_start_msg(self,funcname):
        print ( 'function '+ funcname + ' start').rjust(55,'*')
        logger.debug( (funcname + ' start').rjust(100,'*') )
        
    def pass_msg_handling(self,casename):
        child = self.child
        print ( PASS + (casename + ' succeed').rjust(100,'*') + ENDC ) 
        logger.debug( PASS + (casename + ' succeed').rjust(100,'*') + ENDC )
        
    def excep_msg_handling(self,casename,e):
        child = self.child
        self.exception_list.append(e)
        child.logfile.flush()
        
    def result_excep_msg_handling(self,casename,e):
        child = self.child
        self.exception_list.append(e)
        logger.error(FAIL + str(self.exception_list) + ENDC)
#         print ERROR,Exception,":::::::::::::::::::",self.exception_list,ENDC
        logger.debug( FAIL + (casename + ' failed').rjust(100,'*') + ENDC )
        traceback.print_exc( file = child.logfile )
        child.logfile.flush()      
    def time_sync(self):
        try:
            logger.debug("sync time start")
            child_sync = pexpect.spawn("sudo /usr/sbin/sntp -P no -r 10.175.170.102")
            child_sync.logfile = file(log_file,'aw')
            child_sync.expect(pexpect.EOF)
            logger.debug("sync time succeed")
        except Exception as e:
            pass
          
     
if __name__ == '__main__':
    unittest.main()
