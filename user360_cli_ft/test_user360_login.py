import user360cli
import user360status

from user360cli import *
from user360status import *

#test_user360login.py

def login_alr(self,cmd1,user,psd,cmd2):
        child1 = pexpect.spawn (cmd1)
        child1.expect("word:")
        child1.sendline (psd)
        child1.expect("#")
        child1.sendline(cmd2)
        child1.expect("#")
        out_test = child1.before
        logger.debug(out_test + ENDC)
        print out_test + ENDC
        return out_test

class LoginTestCase(User360Status):

    def test_user360_login_success(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        print 
        try:
            self.user360_logout()
            self.user360_login()
            child.sendline('')
            child.expect('>')
            out = child.before
            self.assertIn('User.360@', out)
            logger.debug( PASS + 'case user360_login_success succeed'.rjust(100,'*') + ENDC )
            self.assertTrue(1)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)    
    
    def test_user360_login_fail_psd(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            self.user360_logout()
            child.sendline('user360 login')
            child.expect('Enter User name: ')
            child.sendline('admin')
            child.expect('password: ')
            child.sendline('wrong_password')           
            child.expect('#')
            out = child.before
            self.assertIn('User.360 login failed', out)
            logger.debug( PASS + 'case user360_login_fail succeed'.rjust(100,'*') + ENDC )
            self.assertTrue(1)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
    
    def test_user360_login_fail_user(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            self.user360_logout()
            child.sendline('user360 login')
            child.expect('Enter User name: ')
            child.sendline('wronguser')
            child.expect('password: ')
            child.sendline('admin')           
            child.expect('#')
            out = child.before
            self.assertIn('User.360 login failed', out)
            logger.debug( PASS + 'case user360_login_fail_user succeed'.rjust(100,'*') + ENDC )
            self.assertTrue(1)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)           
    
    def test_user360_login_timeout_succeed(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            child.sendline('')
            time.sleep(1200)
            child.expect('#')
            out = child.before + child.after
            self.assertIn('Session timeout after idle for', out)
            logger.debug( PASS + 'case test_user360_login_timeout_succeed succeed'.rjust(100,'*') + ENDC )
            self.assertTrue(1)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
    
    def test_user360_login_fail_alr(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        try:
            cmd1 = 'ssh '+self.config_data['user']+'@'+self.config_data['clusterip']
            result = login_alr(self,cmd1,self.config_data['user'],self.config_data['psd'],self.config_data['user360cmd']['login_cmd'])
            if 'command is already running on this blade' in result:
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg='command is already running on this blade not found in printout')
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            