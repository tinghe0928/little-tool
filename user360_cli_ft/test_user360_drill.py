import user360cli
import user360status

from user360cli import *
from user360status import *

class DrillTestCase(User360Status):
    
    
    def user360_drill_start(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if option == "all":
                child.sendline( self.config_data['user360cmd']['drill_start'] + " " + option )
            else:
                option = str(option)
                child.sendline( self.config_data['user360cmd']['drill_start'] + " -N " + option )
            child.expect('>',timeout=120)
            out = child.before
            if self.user360_drill_status(option) == True:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_drill_stop(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if option == "all":
                child.sendline( self.config_data['user360cmd']['drill_stop'] + " " + option )
            else:
                option = str(option)
                child.sendline( self.config_data['user360cmd']['drill_stop'] + " -N " + option )
            child.expect('>',timeout=120)
            out = child.before
            if self.user360_drill_status(option) == False:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
   
    
    def test_drilltestcase1_user360_drill_stop_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_drill_stop("all") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_drilltestcase2_user360_drill_start_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_drill_start("all") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_drilltestcase3_user360_drill_stop_n_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            for i in range(len(self.config_data['upg_pl'])+1):
                if self.user360_drill_stop(i+2) == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_drilltestcase4_user360_drill_start_n_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            for i in range(len(self.config_data['upg_pl'])+1):
                if self.user360_drill_start(i+2) == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
 