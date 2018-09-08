import user360cli
import user360status
import datetime
import re

from user360cli import *
from user360status import *

schedule_Time=[]

class ReportTestCase(User360Status):
    
    
    def schedule_time(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            schedule_time=[]
            now = datetime.datetime.now()
            now.strftime('%Y-%m-%d %H:%M:%S')
            test_seconds = 65
            time_delta=datetime.timedelta(days=0, seconds = test_seconds, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
            time1 = now + time_delta
            dutation = test_seconds
            time_list = re.split(':|-| |',time1.strftime('%Y-%m-%d %H:%M:%S'))
            print time_list
            #['2017', '11', '14', '16', '30', '00']
            timestamp = ' '.join([time_list[-2],time_list[-3],time_list[-4],time_list[-5],"*"])
            timestamp1 ='-'.join([time_list[0],time_list[1],time_list[2]])
            timestamp2 ='-'.join([time_list[3],time_list[4]])
            timestamp3 ='_'.join([timestamp1,timestamp2])
            print timestamp3
            schedule_time.append(timestamp)
            schedule_time.append(timestamp3)
            schedule_time.append(dutation)
            return schedule_time
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    

    def user360_report_execute(self,filename):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['report_execute'] + " " +filename)
            child.expect('>',timeout=7200)
            out = child.before
            if "SUCC:" in out:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_report_add_schedule(self,filename,timestamp):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            child.sendline( self.config_data['user360cmd']['report_add_schedule']+" "+ filename + " " +"\""+timestamp+"\"")
            child.expect('>',timeout=7200)
            if self.user360_report_show_schedule(filename, timestamp) == True:
                return True
            else:
                return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
        
    
    def user360_report_remove_schedule(self,filename,timestamp):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_report_show_schedule(filename, timestamp) == False:
                return True
            else:
                child.sendline( self.config_data['user360cmd']['report_remove_schedule']+" "+ filename + " " +"\""+timestamp+"\"")
                child.expect('>',timeout=7200)
                if self.user360_report_show_schedule(filename, timestamp) == False:
                    return True
                else:
                    return False
        except Exception as self.e:
            self.excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            return False
    
    
    def test_user360_report_case1_execute_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            if self.user360_report_execute("steer.xml") == True:
                self.assertTrue(1)
            else:
                self.assertTrue(0)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
   
    def test_user360_report_case2_add_schedule_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            schedule_Time = self.schedule_time()
            flag = False
            if self.user360_report_add_schedule("steer.xml",schedule_Time[0]) == True:
                self.user360_logout()
                child.sendline("ssh " + self.config_data['upg_pl'][0])
                child.expect("#")
                filename = "steer_"+ schedule_Time[1]
                logger.debug("filename for schedule report is: " + filename)
                time.sleep(schedule_Time[2]+300)
                logger.debug("start to check the report file in output folder")
                child.sendline("cd /var/data_analytic/report/output")
                child.expect("/var/data_analytic/report/output #")
                for i in range(7):
                    child.sendline("ls -l | grep '" + filename + "' | grep 'tar.gz'")
                    child.expect("/var/data_analytic/report/output #")
                    out = child.before
                    logger.debug("########## This is " + str(i+1) + " time to check report: ")
		    logger.debug(str(out))
		    logger.debug("##############")
                    if len(re.findall(filename,out)) > 1:
                        flag  = True
                        break
                    elif i < 6:
                        time.sleep(180)
                if flag == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0,msg="report not found in output")
            else:
                self.assertTrue(0,msg="fail to found report in output")
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
            
    def test_user360_report_case3_remove_schedule_succeed(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            schedule_Time = self.schedule_time()
            if self.user360_report_add_schedule("steer.xml",schedule_Time[0]) == True:
                if self.user360_report_remove_schedule("steer.xml",schedule_Time[0]) == True:
                    self.assertTrue(1)
                else:
                    self.assertTrue(0)
            else:
                pass
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            self.assertTrue(0,msg=self.e)
