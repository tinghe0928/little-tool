import user360cli
import user360status

from user360cli import *
from user360status import *
    
class StatusTestCase(User360Status):
    
    
    def test_user360_status_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_status() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_status_config_print_cudb_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_status_config_print("cudb") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_status_config_print_upg_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_status_config_print("upg") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)   
        
    
    def test_user360_replication_status_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_status("all") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
  
    def test_user360_replication_status_dsg_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            for i in range(len(self.config_data['dsgs'])):
                if self.user360_replication_status(self.config_data['dsgs'][i]) == True:
                    pass
                else:
                    self.assertTrue(0)
            self.assertTrue(1)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e) 