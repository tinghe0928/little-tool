import user360cli
import user360status

from user360cli import *
from user360status import *

class HelpTestCase(User360Status):
    
    def user360_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            self.assertIn('user360 config -i', out)
            self.assertIn('user360 config --print', out)
            self.assertIn('user360 drill --start', out)
            self.assertIn('user360 drill --stop', out)
            self.assertIn('user360 drill --status', out)
            self.assertIn('user360 freshdb --clean', out)
            self.assertIn('user360 freshdb --start', out)
            self.assertIn('user360 freshdb --stop', out)
            self.assertIn('user360 freshdb --status', out)
            self.assertIn('user360 freshdb --update-schema', out)
            self.assertIn('user360 replication -i', out)
            self.assertIn('user360 replication --status', out)
            self.assertIn('user360 report --execute', out)
            self.assertIn('user360 report --add-schedule', out)
            self.assertIn('user360 report --remove-schedule', out)
            self.assertIn('user360 report --show-schedule', out)
            self.assertIn('user360 snapshot --start', out)
            self.assertIn('user360 snapshot --cancel', out)
            self.assertIn('user360 snapshot --status', out)
            self.assertIn('user360 status', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    def user360_helpexpert(self,psd):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['helpexpert'] )
            child.expect('assword:')
            child.sendline(psd)
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 config -i', out)
            self.assertIn('user360 config --print', out)
            self.assertIn('user360 config --cudb-add-user', out)
            self.assertIn('user360 config --cudb-remove-user', out)
            self.assertIn('user360 config --cudb-check-access', out)
            self.assertIn('user360 config --cudb-ssh-grant-only', out)
            self.assertIn('user360 config --cudb-ssh-revoke-only', out)
            self.assertIn('user360 config --fetch', out)
            self.assertIn('user360 config --add', out)
            self.assertIn('user360 config --remove', out)
            self.assertIn('user360 drill --start', out)
            self.assertIn('user360 drill --stop', out)
            self.assertIn('user360 drill --status', out)
            self.assertIn('user360 freshdb --clean', out)
            self.assertIn('user360 freshdb --start', out)
            self.assertIn('user360 freshdb --stop', out)
            self.assertIn('user360 freshdb --status', out)
            self.assertIn('user360 freshdb --update-schema', out)
            self.assertIn('user360 replication -i', out)
            self.assertIn('user360 replication --status', out)
            self.assertIn('user360 replication --startSync', out)
            self.assertIn('user360 replication --stopSync', out)
            self.assertIn('user360 report --execute', out)
            self.assertIn('user360 report --add-schedule', out)
            self.assertIn('user360 report --remove-schedule', out)
            self.assertIn('user360 report --show-schedule', out)
            self.assertIn('user360 snapshot --start', out)
            self.assertIn('user360 snapshot --cancel', out)
            self.assertIn('user360 snapshot --status', out)
            self.assertIn('user360 status', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_config_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['config_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 config -i', out)
            self.assertIn('user360 config --print', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
   
    def user360_replication_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['replication_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 replication -i', out)
            self.assertIn('user360 replication --status', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_freshdb_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 freshdb --clean', out)
            self.assertIn('user360 freshdb --start', out)
            self.assertIn('user360 freshdb --stop', out)
            self.assertIn('user360 freshdb --status', out)
            self.assertIn('user360 freshdb --update-schema', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_snapshot_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['snapshot_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 snapshot --start', out)
            self.assertIn('user360 snapshot --cancel', out)
            self.assertIn('user360 snapshot --status', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_drill_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['drill_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 drill --start', out)
            self.assertIn('user360 drill --stop', out)
            self.assertIn('user360 drill --status', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_report_help(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['report_help'] )
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=120)
            out = child.before
            #out = out.getvalue().strip()
            self.assertIn('user360 report --execute', out)
            self.assertIn('user360 report --add-schedule', out)
            self.assertIn('user360 report --remove-schedule', out)
            self.assertIn('user360 report --show-schedule', out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
   
    def test_user360_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
    
    
    def test_user360_helpexpert_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_helpexpert("expert") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
  
    def test_user360_config_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_config_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
   
    def test_user360_drill_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_drill_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_freshdb_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_freshdb_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_replication_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_report_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_snapshot_help_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_snapshot_help() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
            
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)

            
