import ConfigParser

import user360cli
import user360status

from user360cli import *
from user360status import *

boolean2status = {True: 'enable', False: 'disable'}

class ConfigTestCase(User360Status):
    def runTest(self):
        pass
    
    def user360_grant_only(self,cudb_oam_vip,cudb_psd):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            """no need to do pre-check because no matter you grant or not if will not effect """
            child.sendline( self.config_data['user360cmd']['grant_only'] + " " + cudb_oam_vip )
            child.expect('assword:')
            child.sendline(cudb_psd)
            child.expect('>')
            out = child.before
            if 'Successful to prepare CUDB and UPG for cooperation in terms of SSH setup' in out:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    def user360_config_i(self,cudb_oam_vip):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.dsg_counters() == 0:
                child.sendline( self.config_data['user360cmd']['config_i'] + " " + cudb_oam_vip )
                child.expect('>')
                if self.dsg_counters() == len(self.config_data['dsgs']):
                    return True
                else:
                    return False
            else:
                if self.dsg_counters() == len(self.config_data['dsgs']):
                    print WARNING + "Current UPG already configured. Remove all DSGs first." + ENDC
                    print WARNING + "Command Failed!" + ENDC
                    return True
                else:
                    return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False       

    def user360_config_fetch(self,cudb_oam_vip):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            
            child.sendline( self.config_data['user360cmd']['config_fetch'] + " " + cudb_oam_vip )
            child.expect('>',timeout=60)
            out = child.before
            if ("Host key verification failed" or "Command Failed")in out:
                return False
            else:
                if self.cudb_counters() == len(self.config_data['cudb_system']):
                    return True
                else:
                    return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False       
        
    def user360_config_add(self,option,blade):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            option = option.upper()
            blade = blade.upper()
            if self.dsg_counters() == len(self.config_data['dsgs']):
                    print WARNING + "Current UPG already configured. Remove all DSGs first." + ENDC
                    print WARNING + "Command Failed!" + ENDC
                    print 'Current UPG already configured'
                    return False
            else:
                child.sendline( self.config_data['user360cmd']['config_add'] + " " + option + " " + blade)
                child.expect('User.360@admin:~>',timeout=60)
                if option == "ALL":
                    if self.dsg_counters() == len(self.config_data['dsgs']):
                        return True
                    else:
                        print 'NOT all DSGs configured correctly'
                        return False
#                 elif option == "DSG0" and blade != self.config_data['upg_pl'][0]:
#                     print 'DSG0 must be allocated to' + " " + self.config_data['upg_pl'][0]
#                     return False
                else:
                    child.sendline(self.config_data['user360cmd']['config_print_upg_cmd'])
                    child.expect('>')
                    out = child.before
#                     print option
#                     print out
                    if option in out:
                        return True
                    else:
                        print 'did not find '+ option + "in printout"
                        return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    def user360_config_cudb_add_user(self,cudb_oam_vip,cudb_psd):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            """no need to do pre-check because no matter you grant or not if will not effect """
            child.sendline( self.config_data['user360cmd']['config_cudb_add_user'] + " " + cudb_oam_vip )
            child.expect('assword:')
            child.sendline(cudb_psd)
            child.expect('>')
            out = child.before
            if 'Successful to add UPG user to CUDB node' in out:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
 
    def user360_remove(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.dsg_counters() == 0:
                print "NO DSG found configuration"
                return True
            else:
                child.sendline( self.config_data['user360cmd']['config_remove'] + " " + option)
                child.expect('>')
                if option == "all":
                    if self.dsg_counters() == 0:
                        return True
                    else:
                        return False
                else:
                    child.sendline( self.config_data['user360cmd']['config_print_upg_cmd'])
                    child.expect('>')
                    out= child.before
                    if option.upper() not in out:
                        return True
                    else:
                        return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False    
            
   
    def user360_revoke_only(self,option,psd):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.cudb_counters() == 0:
                print "No cudb granted"
                return True
            else:
                try:
                    child.sendline( self.config_data['user360cmd']['config_revoke'] + " " + option )
                    child.expect('assword:')
                    child.sendline( psd )
                    child.expect('>')
                    out = child.before
                    if 'Successful to revoke' in out:
                        return True
                    else:
                        return False
                except Exception as self.e:
                    print "exception when revoke s%" % (option)
                    return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False        
        
    
    def user360_config_cudb_remove_user(self,cudb_oam_vip,cudb_psd):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            """no need to do pre-check because no matter you grant or not if will not effect """
            child.sendline( self.config_data['user360cmd']['config_cudb_remove_user'] + " " + cudb_oam_vip )
            child.expect('assword:')
            child.sendline(cudb_psd)
            child.expect('>')
            out = child.before
            if 'Successful to remove user from CUDB node' in out:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False

    def send_dsu_switch_command(self, para):
        parameter_dict = {'disable': 'disable', 'enable': 'enable', 'status': 'status'}
        self.child.sendline("{} {}".format(self.config_data['user360cmd']['config_dsu_switch'], parameter_dict[para]))
        self.child.expect('>')
        return self.child.before

    def get_dsu_switch_status(self):
        status = self.send_dsu_switch_command('status')
        if 'Disable' in status:
            return False
        elif 'Enable' in status:
            return True
        else:
            raise Exception("Get dsu switch status error: {}".format(status))

    def test_dsu_switch(self, status):
        opposite_status = not status
        self.send_dsu_switch_command(boolean2status[opposite_status])
        current_status = self.get_dsu_switch_status()
        if current_status == opposite_status:
            self.assertTrue(True)
        else:
            self.assertTrue(False, msg='Auto dsu switch failed')

    def restore_switch_status(self, status):
        self.send_dsu_switch_command(boolean2status[status])

    def send_counter_switch_command(self, para):
        parameter_dict = {'disable': 'disable', 'enable': 'enable', 'status': 'status'}
        self.child.sendline("{} {}".format(self.config_data['user360cmd']['config_counter'], parameter_dict[para]))
        self.child.expect('>')
        return self.child.before

    def get_counter_switch_status(self):
        status = self.send_counter_switch_command('status')
        if 'disable' in status:
            return False
        elif 'enable' in status:
            return True
        else:
            raise Exception("Get counter status error: {}".format(status))

    def test_counter_switch(self, status):
        opposite_status = not status
        self.send_counter_switch_command(boolean2status[opposite_status])
        current_status = self.get_counter_switch_status()
        if current_status == opposite_status:
            self.assertTrue(True)
        else:
            self.assertTrue(False, msg='counter status switch failed')

    def restore_counter_switch_status(self, status):
        self.send_counter_switch_command(boolean2status[status])

    def get_counter_interval_value(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        child.sendline(self.config_data['user360cmd']['config_counter_interval'])
        child.expect('>')
        return self.child.before

    def change_counter_interval_value(self):
        self.func_start_msg(sys._getframe().f_code.co_name)
        child = self.child
        origin_value = self.get_counter_interval_value()
        change_value = int(current_value) + 5
        child.sendline(self.config_data['user360cmd']['config_counter_interval'] + " " + str(change_value))
        current_value = self.get_counter_interval_value()
        if current_value == change_value:
            self.assertTrue(True)
        else:
            self.assertTrue(False, msg='change counter interval failed')

    #############################################test###################################
     
     
    def test_user360_config_cudb_add_user_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            cudb_user_counter = 0
            for i in range(len(self.config_data['cudb_system'])):
                if self.user360_config_cudb_add_user(self.config_data['cudb_system'][i]['cudb_oam_vip'],self.config_data['cudb_system'][i]['cudb_psd']) == True:
                    cudb_user_counter += 1
                else:
                    pass
            if cudb_user_counter == len(self.config_data['cudb_system']):
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
     
    
    def test_user360_grant_only_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            granted_cudb_counters = 0
            for i in range(len(self.config_data['cudb_system'])):
                if self.user360_grant_only(self.config_data['cudb_system'][i]['cudb_oam_vip'],self.config_data['cudb_system'][i]['cudb_psd']) == True:
                    granted_cudb_counters += 1
                else:
                    pass
            if granted_cudb_counters == len(self.config_data['cudb_system']):
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
             
   
    def test_user360_grant_only_invalid_ip(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            invalid_ip = ["10.170.11","10.170.11.899","1"]
            granted_cudb_counters = 0
            for i in range(len(invalid_ip)):
                if self.user360_grant_only(invalid_ip[i],"") == False:
                    granted_cudb_counters += 1
                else:
                    pass  
            if granted_cudb_counters == len(invalid_ip):
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
     
   
    def test_user360_config_i_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child =self.child
            if self.user360_config_i(self.config_data['cudb_system'][0]['cudb_oam_vip']) == True:
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
            if self.user360_status_config_print("cudb")  == True:
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
            
    
    def test_user360_config_fetch_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            fetched_cudb_counters = 0
            for i in range(len(self.config_data['cudb_system'])):
                if self.user360_config_fetch(self.config_data['cudb_system'][i]['cudb_oam_vip']) == True:
                    fetched_cudb_counters += 1
                else:
                    pass
            if fetched_cudb_counters == len(self.config_data['cudb_system']):
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="number of fetched cubd nodes is not right")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_config_add_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            config_add_counters = 0
            self.user360_remove("all")
            if self.user360_config_add("all", "") == True:
                config_add_counters += 1
            else:
                print "user 360 config add all failed"
            self.user360_remove("all")
            for i in range(len(self.config_data['dsgs'])):
                if self.user360_config_add(self.config_data['dsgs'][i], "") == True:
                    config_add_counters += 1
                    print config_add_counters
                else:
                    print "user 360 config add " + self.config_data['dsgs'][i] + " failed"
            if config_add_counters == (len(self.config_data['dsgs']) + 1):
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="not all dsgs add in a right way")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_remove_all_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_remove("all") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_remove_dsg_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            for i in range(len(self.config_data['dsgs'])):
                if self.user360_remove(self.config_data['dsgs'][i]) == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
     
    def test_user360_revoke_only_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            print sys._getframe().f_code.co_name
            child = self.child
            print sys._getframe().f_code.co_name
            revoke_counter = 0
            for i in range(len(self.config_data['cudb_system'])):
                if self.user360_revoke_only(self.config_data['cudb_system'][i]['cudb_oam_vip'], self.config_data['cudb_system'][i]['cudb_psd']) == True:
                    revoke_counter += 1
                else:
                    print "fail to revoke for s%" % (self.config_data['cudb_system'][i]['cudb_oam_vip'])
                    logger.debug( "fail to revoke for s%" % (self.config_data['cudb_system'][i]['cudb_oam_vip']) )
            if revoke_counter == len(self.config_data['cudb_system']):
                self.assertTrue(1)
            else:
                self.assertTrue(0,msg="not all cudb nodes are revoked")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_config_cudb_remove_user_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            cudb_user_counter = 0
            for i in range(len(self.config_data['cudb_system'])):
                if self.user360_config_cudb_remove_user(self.config_data['cudb_system'][i]['cudb_oam_vip'],self.config_data['cudb_system'][i]['cudb_psd']) == True:
                    cudb_user_counter += 1
                else:
                    pass
            if cudb_user_counter == len(self.config_data['cudb_system']):
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)

    def test_user360_config_auto_dsu_switch(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            ori_status = self.get_dsu_switch_status()
            self.test_dsu_switch(ori_status)
            self.restore_switch_status(ori_status)
        except Exception as e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,e)
            self.assertTrue(False, msg=e)

    def test_user360_config_counter_switch(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            ori_status = self.get_counter_switch_status()
            self.test_counter_switch(ori_status)
            self.restore_counter_switch_status(ori_status)
        except Exception as e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name, e)
            self.assertTrue(False, msg=e)

    def test_user360_config_counter_interval_change(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            self.change_counter_interval_value()
        except Exception as e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name, e)
            self.assertTrue(False, msg=e)