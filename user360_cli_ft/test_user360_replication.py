import time
import user360cli
import user360status

from user360cli import *
from user360status import *

class ReplicationTestCase(User360Status):
    
    
    def user360_replication_startsync(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline(self.config_data['user360cmd']['replication_startsync'] + " " + option)
            child.expect('>')
            out = child.before
            if option == "all":
                for i in range(len(self.config_data['dsgs'])):
                    self.assertIn('Replication for ' + self.config_data['dsgs'][i]+" on blade: pl-",out )
                    self.assertIn("is started!",out)
                return True
            else:
                option = option.upper()
                self.assertIn('Replication for ' + option + " on blade: pl-",out )
                self.assertIn("is started!",out)
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    
    def user360_replication_stopsync(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline(self.config_data['user360cmd']['replication_stopsync'] + " "+ option)
            child.expect('>')
            out = child.before
            if option == "all":
                for i in range(len(self.config_data['dsgs'])):
                    self.assertIn('Replication for ' + self.config_data['dsgs'][i]+" on blade: pl-",out )
                    self.assertIn("is stopped!",out)
                return True
            else:
                option = option.upper()
                self.assertIn('Replication for ' + option + " on blade: pl-",out )
                self.assertIn("is stopped!",out)
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
            
    
    def user360_replication_switchsync(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            option = option.upper()
            child.sendline(self.config_data['user360cmd']['replication_switchsync'] + " " + option)
            child.expect('>')
            out = child.before
            if (option + " succeed") in out:
                return True
            elif "Failed" not in out:
                return True
            elif 'not get master position info' in out:
                logger.debug("Could not get master position info to switch replication for DSG")
                print "Could not get master position info to switch replication for DSG"
                return False
            else:
                logger.debug("switchsync failed in printout")
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_replication_i(self,option,node_id,f_option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_status_config_print("cudb") == True and self.cudb_counters() == len(self.config_data['cudb_system']):
                if self.user360_status_config_print("upg") == True and self.dsg_counters() == len(self.config_data['dsgs']):
                    child.sendline( self.config_data['user360cmd']['replication_i'] + " " + option + " "+ node_id + " "+ f_option )
                    i = child.expect(['Are you sure that you want to do initial load once again (Yes/No)?', "User.360@"+self.config_data['user360user']+":~>"],timeout=self.config_data['initial_load_estimated_time'])
                    if i ==0:
                        child.sendline("Yes")
                    elif i == 1:
                        if self.user360_replication_status(option) == True:
                            return True
                        else:
                            print "user360 replication status is not right"
                            return False
                    else:
                        return False
                else:
                    print WARNING + "DSGs are not allocated to UPG, please check" + ENDC
                    return False
            else:
                print WARNING + "Something wrong with cudb confuguration , please check" + ENDC
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    
    def test_user360_replication_i_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_i("all", "", "") == True:
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="user360 replication status is not right")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
    
    
    def test_user360_replication_i_all_n_f_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_i("all", "-N "+self.config_data['cudb_system'][0]['node_id'], "-F") == True:
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="user360 replication status is not right")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_replication_i_dsg_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            pass_dsg_counter = 0
            for i in range(len(self.config_data['dsgs'])):
                if self.user360_replication_i(self.config_data['dsgs'][i], "", "") == True:
                    pass_dsg_counter += 1
                else:
                    pass
            if pass_dsg_counter == len(self.config_data['dsgs']):
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="replication of some dsgs are failed")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_replication_stopsync_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_stopsync("all")  == True:
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="fail to stopsync")  
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_replication_startsync_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_replication_startsync("all")  == True:
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="fail to startsync")  
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    def insert_data_on_cudb(self):
        try:
            child = self.child
            self.user360_logout()
            child.sendline("ssh root@"+self.config_data['cudb_system'][0]['cudb_oam_vip'])
            i= child.expect(["Are you sure you want to continue connecting (yes/no)?", 'Password:'])
            if i == 0:
                child.sendline("yes")
                child.expect("Password:")
            else:
                pass
            child.sendline(self.config_data['cudb_system'][0]['cudb_psd'])
            child.expect("#")
            
            column_name = "(RDN_1,RDN_2,RDN_3,RDN_4,RDN_5,RDN_6,RDN_7,RDN_8,RDN_9,RDN_10,RDN_11,RDN_12,OBJECTS,ENTRY_KEY,O_DN)"
            
            column_value = "('dc=com','dc=o','ou=multiscs','mscId=b38bc529ab2b4e8c8844b15201920322','serv=aaa','','','','','','','',0x000007FF,1115201920322,'serv=AAA,mscId=b38bc529ab2b4e8c8844b15201920322,ou=multiSCs,dc=o,dc=com')"
            insert_sql = "INSERT INTO CUDB_DN "+ column_name+ " VALUES "+ column_value
            select_sql = "select * from CUDB_DN where O_DN='serv=AAA,mscId=b38bc529ab2b4e8c8844b15201920322,ou=multiSCs,dc=o,dc=com'"
            for i in range(len(self.config_data['dsg_port'])): 
                insert_sql_to_dsg = "mysql  -P"+self.config_data['dsg_port'][i]+" -uroot -proot -h"+self.config_data['dsg_host'][i]+" cudb_user_data -e " + "\""+ insert_sql+ "\""
                select_sql_dsg = "mysql  -P"+self.config_data['dsg_port'][i]+" -uroot -proot -h"+self.config_data['dsg_host'][i]+" cudb_user_data -e " + "\""+ select_sql + "\""
                child.sendline(insert_sql_to_dsg)
                child.expect("#")
                child.sendline(select_sql_dsg)
                child.expect("#")
                out = child.before
                if "1115201920322" in out:
                    print "data insert succeed"
                else:
                    print "data insert fail"
            child.sendline("exit")
            child.expect("#")
            self.user360_login()
        except Exception as self.e:
            print "generate traffic on cudb Exception"
    def delete_data_on_cudb(self):
        try:
            child = self.child
            self.user360_logout()
            child.sendline("ssh root@"+self.config_data['cudb_system'][0]['cudb_oam_vip'])
            i= child.expect(["Are you sure you want to continue connecting (yes/no)?", 'Password:'])
            if i == 0:
                child.sendline("yes")
                child.expect("Password:")
            else:
                pass
            child.sendline(self.config_data['cudb_system'][0]['cudb_psd'])
            child.expect("#")
            O_ND_value = "\'"+'serv=AAA,mscId=b38bc529ab2b4e8c8844b15201920322,ou=multiSCs,dc=o,dc=com'+"\'"
            delete_sql = "DELETE from CUDB_DN where O_DN="+ O_ND_value
            select_sql = "select * from CUDB_DN where O_DN='serv=AAA,mscId=b38bc529ab2b4e8c8844b15201920322,ou=multiSCs,dc=o,dc=com'"

            for i in range(len(self.config_data['dsg_port'])): 
                delete_sql_to_dsg = "mysql  -P"+self.config_data['dsg_port'][i]+" -uroot -proot -h"+self.config_data['dsg_host'][i]+" cudb_user_data -e " + "\""+delete_sql+ "\""
                select_sql_dsg = "mysql  -P"+self.config_data['dsg_port'][i]+" -uroot -proot -h"+self.config_data['dsg_host'][i]+" cudb_user_data -e " + "\""+ select_sql + "\""

                child.sendline(delete_sql_to_dsg)
                child.expect("#")
                child.sendline(select_sql_dsg)
                child.expect("#")
                out = child.before
                if "1115201920322" in out:
                    print "data delete fail"
                else:
                    print "data delete succeed"
            child.sendline("exit")
            child.expect("#")
            self.user360_login()
        except Exception as self.e:
            print "delete data on cudb Exception"
                
    
    def test_user360_replication_switchsync_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            sync_dsg_couter = 0
            self.insert_data_on_cudb()
            for i in range(len(self.config_data['dsgs'])):
                if self.user360_replication_switchsync(self.config_data['dsgs'][i])  == True:
                    sync_dsg_couter += 1
                else:
                    pass
            self.delete_data_on_cudb()
            if sync_dsg_couter == len(self.config_data['dsgs']):
                print sys._getframe().f_code.co_name+" succeed !!!!!"
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="Some dsg switchsync failed")  
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)