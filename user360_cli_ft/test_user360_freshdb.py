import ConfigParser

import user360cli
import user360status
import paramiko as paramiko

from user360cli import *
from user360status import *

class FreshDBTestCase(User360Status):
    
    
    def user360_freshdb_clean(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_clean'] + " " + option)
            child.expect('>',timeout=600)
            out = child.before
            if ("Failed" or "Invalid") in out:
                return False
            else:
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False       
        
    
    def user360_freshdb_start(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_start'] )
            child.expect('>',timeout=60)
            if self.user360_freshdb_status() == True:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_freshdb_stop(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_stop'] )
            child.expect('>',timeout=60)
            out = child.before
            self.assertIn("FreshDB stopped",out)
            if self.user360_freshdb_status() == False:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
   
    def user360_freshdb_update_schema(self,sql_file_path):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_update_schema'] + " " + sql_file_path)
            child.expect("Are you sure to update FreshDB schema")
            child.sendline('Yes')
            child.expect('>',timeout=60)
            out = child.before
            if ("ailed" or "ERROR") in out:
                return False
            else:
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    
    def test_user360_freshdb_case1_update_schema_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_freshdb_update_schema("/var/data_analytic/config/CA/user360/updateSchema.sql") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_freshdb_case2_clean_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_freshdb_clean("all") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_freshdb_case3_stop_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_freshdb_stop() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
   
    def test_user360_freshdb_case4_start_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_freshdb_start() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)

    def test_user360_freshdb_case5_bind_address(self):
        my_cnf = "/var/data_analytic/my.cnf"
        upg_cfg = "/home/upg/user360/common/config/upg.cfg"
        ori_my_cnf = "/tmp/ori_my_cnf"
        tested_my_cnf = "/tmp/test_my_cnf"
        tested_upg_cfg = "/tmp/test_upg_cfg"
        mock_address = "127.0.0.1"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.config_data["clusterip"], username=self.config_data["user"], password=self.config_data["psd"])
        sftp = ssh.open_sftp()

        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            my_cnf_before = ConfigParser.ConfigParser(allow_no_value=True)
            sftp.get(my_cnf, ori_my_cnf)
            my_cnf_before.read(ori_my_cnf)
            ori_address = my_cnf_before.get("mysqld3306", "bind-address")

            self.child.sendline(self.config_data['user360cmd']['freshdb_bind_address'] + " " + mock_address)
            time.sleep(3)
            sftp.get(my_cnf, tested_my_cnf)
            my_cnf_after = ConfigParser.ConfigParser(allow_no_value=True)
            my_cnf_after.read(tested_my_cnf)
            my_cnf_result = my_cnf_after.get("mysqld3306", "bind-address")
            self.assertEqual(mock_address, my_cnf_result)
            sftp.get(upg_cfg, tested_upg_cfg)
            upg_cfg_after = ConfigParser.ConfigParser(allow_no_value=True)
            upg_cfg_after.read(tested_upg_cfg)
            upg_cfg_result = upg_cfg_after.get("FRESHDBINFOMATION", "bind_address")
            self.assertEqual(mock_address, upg_cfg_result)
        except Exception as e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name, e)
            self.assertTrue(0, msg=e)
        finally:
            self.child.sendline(self.config_data['user360cmd']['freshdb_bind_address'] + " " + ori_address)
            try:
                os.remove(ori_my_cnf)
                os.remove(tested_my_cnf)
                os.remove(tested_upg_cfg)
            except Exception as e:
                self.result_excep_msg_handling(sys._getframe().f_code.co_name, e)


