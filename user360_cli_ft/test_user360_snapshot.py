import user360cli
import user360status
import test_user360_config
import time
import datetime
import re
from user360cli import *
from user360status import *
from test_user360_config import *


class ConfigTest(ConfigTestCase):
    
    def revoke(self,child,config_data,option,psd):
        self.child = child
        self.config_data = config_data
        return self.user360_revoke_only(option,psd)
    
class SnapshotTestCase(User360Status):
      
    def snapshot_time(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            snapshot_time = []
            now = datetime.datetime.now()
            now.strftime('%Y-%m-%d %H:%M:%S')
            test_seconds = 65
            test_minutes = 10
            time_delta = datetime.timedelta(days=0, seconds=test_seconds, microseconds=0, milliseconds=0, minutes=test_minutes, hours=0, weeks=0)
            duration = test_minutes * 60 + test_seconds
            time_snapshot = now + time_delta
            time_list = re.split(':|-| |',time_snapshot.strftime('%Y-%m-%d %H:%M:%S'))
#             print time_list
            #['2017', '11', '14', '16', '30', '00']
            timestamp_snapshot ='-'.join([time_list[0],time_list[1],time_list[2]])
#             print timestamp_snapshot
#             print type(timestamp_snapshot)
            snapshot_time.append(time_snapshot.strftime('%Y-%m-%d %H:%M:%S'))
            snapshot_time.append(timestamp_snapshot)
            snapshot_time.append(duration)
            return snapshot_time
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            
    
    def user360_snapshot_start(self,timestamp):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline("exit")
            child.expect("#")
            child.sendline( "ssh "+ self.config_data['upg_pl'][0]+ " sed -i '/user360report.py/d' /var/spool/cron/tabs/root ")
            child.expect('#',timeout=60)
            child.sendline( "sed -i '/snapshot_start.sh/d' /var/spool/cron/tabs/root")
            child.expect('#',timeout=60)
            self.user360_login()
            child.sendline( self.config_data['user360cmd']['snapshot_start'] + " " +"\"" + timestamp +"\"")
            child.expect("User.360@"+self.config_data['user360user']+":~>",timeout=60)
            if self.user360_snapshot_status(timestamp) == True:  
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_snapshot_cancel(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['snapshot_cancel'])
            child.expect('>',timeout=60)
            child.sendline( self.config_data['user360cmd']['snapshot_status'])
            child.expect('>',timeout=60)
            out = child.before
            self.assertIn('No snapshot is scheduled',out)
            return True
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    
    def test_user360_snapshot_case1_start_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            snapshot_Time = self.snapshot_time()
            FLAG = False
            if self.user360_snapshot_start(snapshot_Time[0]) == True:
                flag = False
                child.sendline("exit")
                child.expect("#")
                child.sendline("ssh "+ self.config_data['upg_pl'][0])
                child.expect("#")
                child.sendline("cd /var/data_analytic/report/output")
                child.expect("/var/data_analytic/report/output #")
                time.sleep(snapshot_Time[2]+600)
                filename = "snapshotReport_"+ snapshot_Time[1]
                for i in range(3):
                    child.sendline("ls -l")
                    child.expect("#")
                    out = child.before
                    out_array = out.split()
                    out_array_fit =[]
                    snapshot_Time_int = int(re.sub(r'\D',"",snapshot_Time[0]))
                    #print snapshot_Time_int
                    for i in range(len(out_array)):
                            out_array[i] = re.search('snapshotReport.*.gz',out_array[i])
                            if out_array[i] != None:
                                    out_array[i] =  out_array[i].group()
                                    out_array_fit.append(out_array[i])
                    for i in  range(len(out_array_fit)):
                            out_array_fit[i] = int(re.sub(r'\D',"",out_array_fit[i]))
                            if abs(out_array_fit[i]-snapshot_Time_int) <= 600:
                                    flag =True
                            else:
                                    pass
                    if (filename in out and flag == True):
                        FLAG = True
                        break
                    else:
                        time.sleep(120)
                if FLAG == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0,msg="snapshot not found in output")
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    
    def test_user360_snapshot_case2_cancel_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_snapshot_cancel() == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e) 
    def test_replace_snapshotfiles(self,snapshot_file,snapshot_conflict_file):
        try:
            child = self.child
            self.user360_logout()
            child.sendline("scp -r /var/data_analytic/config/CA/user360/" + snapshot_conflict_file + " " + self.config_data['upg_pl'][0]+ ":/var/data_analytic/report/input/" + snapshot_file)
            child.expect("#")
            self.user360_login()
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e) 
        
        
    def test_user360_snapshot_config_revoke_conflict(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            self.test_replace_snapshotfiles("snapshotReport.xml", "snapshotReport_conflict.xml")
            snapshot_time = self.snapshot_time()
            configtest = ConfigTest()
            user360_snapshot_result = self.user360_snapshot_start(snapshot_time[0])
            logger.debug('waiting for snapshot start')
            time.sleep(snapshot_time[2])
            user360_revoke_result = configtest.revoke(child,self.config_data,self.config_data['cudb_system'][0]['cudb_oam_vip'], self.config_data['cudb_system'][0]['cudb_psd'])
            self.test_replace_snapshotfiles("snapshotReport.xml", "snapshotReport.xml")
            if user360_snapshot_result == True:
                print "**"
                if user360_revoke_result == False:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0,msg="It is not right to revoke when doing snapshot")
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e) 
            
        