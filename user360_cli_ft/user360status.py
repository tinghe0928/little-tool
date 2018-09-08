import time
import user360cli
from user360cli import *

class User360Status(User360Cli):
    def dsg_counters(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            dsg_counter = 0
            child.sendline( self.config_data['user360cmd']['config_print_upg_cmd'] )
            child.expect('>',timeout=60)
            out = child.before
            for i in range( len( self.config_data['dsgs'] ) ):
                if self.config_data['dsgs'][i] in out:
                    #print str(self.config_data['dsgs'][i])
                    dsg_counter = dsg_counter + 1
                    print "dsg_counter value is : " + str(dsg_counter)
                else:
                    logger.debug(self.config_data['dsgs'][i] + " not found in out")
                    print self.config_data['dsgs'][i] + " not found in out"
            print "the system has " + str(dsg_counter) +" dsgs allocated"
            return dsg_counter
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return dsg_counter
          
    def cudb_counters(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            cudb_counter = 0
            dsg_counter = 0
            child.sendline( self.config_data['user360cmd']['config_print_cudb_cmd'] )
            child.expect('>',timeout=60)
            out = child.before
            for i in range( len( self.config_data['dsgs'] ) ):
                if self.config_data['dsgs'][i] in out:
                    #for j in range( len( self.config_data['cudb_system'] ) ):
                        #if self.config_data['cudb_system'][j]['node_id'] in out:
                            #dsg_counter += 1
                        #else:
                            #pass   
                    dsg_counter += 1
                else:
                    logger.debug( self.config_data['dsgs'][i] + " not found in out" )
                    print self.config_data['dsgs'][i] + " not found in out"
            if dsg_counter == len(self.config_data['dsgs']):
                for i in range( len( self.config_data['cudb_system'] ) ):
                    if self.config_data['cudb_system'][i]['node_id'] in out:
                        if self.config_data['cudb_system'][i]['cudb_oam_vip'] in out:
                            cudb_counter = cudb_counter + 1
                        else:
                            pass
                    else:
                        pass
            else:
                pass
            print "the system has " + str( cudb_counter ) +" cudb nodes granted" 
            return cudb_counter
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return cudb_counter
    
    """to define whether the cluster is configured or not """

    def user360_config_status_check(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['status'] )
            child.expect('>',timeout=60)
            out = child.before
            if 'System has not been configured yet' in out:
                return False
            else:
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
#################################################################################################################################
    
    def user360_status(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['status'] )
            child.expect('>',timeout=60)
            out = child.before
            if self.user360_config_status_check() == False:
                self.assertIn( 'No active alarms for user360', out)              
                self.assertIn( 'DSG has not been configured yet',out)
                self.assertIn( 'System is not healthy',out)
                return True
            else:
                self.assertIn( 'No active alarms for user360', out)
                self.assertIn( 'Replication ok for all DSGs', out)
                self.assertIn( 'System is healthy', out)
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
#################################################config_status_check##############################################################
    
    def user360_config_cudb_check_access(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            cudb_counter = 0
            for i in range(len(self.config_data['cudb_system'])):
                child.sendline( self.config_data['user360cmd']['config_cudb_check_access'] + " " +  self.config_data['cudb_system'][i]['cudb_oam_vip'])
                child.expect('>',timeout=60)
                out = child.before
                if 'Successful to check if CUDB is accessible for UPG' in out:
                    cudb_counter = cudb_counter + 1
                else:
                    pass
            if cudb_counter == len(self.config_data['cudb_system']):
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    def user360_status_config_print(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if option == "upg":
                if self.user360_config_status_check() == False:
                    if self.dsg_counters() == 0:
                        return True
                    else:
                        return False      
                else:
                    if self.dsg_counters() == len(self.config_data['dsgs']):
                        return True
                    else:
                        return False
            elif option == "cudb":
                if self.user360_config_status_check() == False:
                    if self.cudb_counters() == 0:
                        return True
                    else:
                        return False
                else:
                    if self.cudb_counters() == len( self.config_data['cudb_system'] ):
                        return True
                    else:
                        return False
            else:
                pass
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False

#################################################drill_status_check##############################################################    
    
    def user360_drill_status(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if option == "all":
                child.sendline( self.config_data['user360cmd']['drill_status'] + " " + option )
                child.expect('>',timeout=60)
                out = child.before
                self.assertIn(self.config_data['upg_sc'][1] + ': Drill is running',out)
                for i in range(len(self.config_data['upg_pl'])):
                    self.assertIn( self.config_data['upg_pl'][i] + ": Drill is running", out)
                return True
            else:
                option = str(option)
                child.sendline( self.config_data['user360cmd']['drill_status'] + " -N " + option )
                child.expect('>',timeout=60)
                out = child.before
                self.assertIn( option +": Drill is running",out)
                return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
            
    
#################################################freshdb_status_check##############################################################   
   
    def user360_freshdb_status(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['freshdb_status'] )
            child.expect('>',timeout=60)
            out = child.before
            if "FreshDB is running" in out:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False    

#################################################replication_status_check##############################################################     
   
    def user360_replication_status(self,option):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            time.sleep(120)
            child.sendline( self.config_data['user360cmd']['replication_status'] +" "+ option )
            child.expect('>',timeout=60)
            out = child.before
            replication_nodelay_counter = 0
            if self.user360_config_status_check() == False:
                self.assertIn( 'No DSG has been allocated to UPG', out)
                print "System not configured yet"
                logger.debug( "System not configured yet" )
                return False
            else:
                delay = []
                #print option
                if option == "all":
                    replication_dsg_counter = len(self.config_data['dsgs'])
                    for i in range(len(self.config_data['dsgs'])):
                        self.assertIn( self.config_data['dsgs'][i], out)
                    #print i
                else:
                    replication_dsg_counter = 1
                    self.assertIn( option, out)
                self.assertNotIn( 'NOK', out )
                self.assertNotIn( 'Not', out )
                self.assertIn( 'Running', out )
                self.assertIn( 'OK', out )
                self.assertIn( 'STARTED', out )
                for i in range(len(out.split())):
                    if out.split()[i] == "STARTED": 
                        delay.append( {'dsg_name' : out.split()[i-7],
                                       'delay_time' : out.split()[i-1]
                                       } )
                    else:
                        pass
                for i in range(len(delay)):
                    if int(delay[i]['delay_time']) <= 300:
                        replication_nodelay_counter += 1
                        print delay[i]['dsg_name'] + " Replication delay time is " + delay[i]['delay_time'] + "s"
                    else:
                        print WARNING + delay[i]['dsg_name'] + " Replication delay time is bigger than 0, which is " + delay[i]['delay_time'] + "s" + ENDC
                        logger.debug( WARNING + delay[i]['dsg_name'] + " Replication delay time is bigger than 0, which is " + delay[i]['delay_time'] + "s"+ ENDC )
                print "replication_nodelay_counter is : "
                print replication_nodelay_counter
                print "replication_nodelay_counter is:"
                print replication_dsg_counter
                #print delay
                if replication_nodelay_counter == replication_dsg_counter:
                    print sys._getframe().f_code.co_name+" succeed !!!!!"
                    return True
                else:
                    return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
#################################################report_status_check##############################################################  

  
    def user360_report_show_schedule(self,filename,timestamp):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['report_show_schedule'] )
            child.expect('>',timeout=60)
            out = child.before
            if "python /home/upg/user360/deploy/user360report.py report --execute" in out:
                self.assertIn(filename, out)
                self.assertIn(timestamp, out)
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
#################################################snapshot_status_check##############################################################  

    def user360_snapshot_status(self,timestamp):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['snapshot_status'])
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=60)
            out = child.before
            if 'Snapshot had been scheduled at' in out:  
                if timestamp in out:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
            
                
        