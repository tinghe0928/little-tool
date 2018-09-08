import user360cli
import time
from user360cli import *

class TestSetUp(User360Cli):
    
      
    def test_scp_files(self):
        try:
            self.func_start_msg(sys._getframe().f_code.co_name)
            child = self.child
            simulator_ip = self.config_data['simulator_ip']
            ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
            dsg_counter = 0
            self.user360_logout()
            child.sendline('pam_tally2 --file /home/dveadm/faillog --user root --reset')
            child.expect('#',timeout=60)
            child.sendline("scp -r lsv@"+simulator_ip+":"+ self.cur_dir + "/resources/* /var/data_analytic/config/CA/user360/")
            i = child.expect([ssh_newkey, 'assword:'])
            if i == 0:
                child.sendline("yes")
                child.expect("assword:")
            elif i==1:
                pass
            child.sendline ("lsv")
            child.expect('#',timeout=60)
            child.sendline("chmod 777 /var/data_analytic/config/CA/user360/*")
            child.expect('#',timeout=60)
            retry_times1 = 3
            while retry_times1 > 0:
                try:
                    child.sendline ('cd /opt/dve/tools/jmxbatchclient/jmxbatchclient-* && sh jbc.sh -Aadmin:admin service:jmx:rmi://127.0.0.1:6868/jndi/rmi://127.0.0.1:6099/connector /var/data_analytic/config/CA/user360/User360FreshDB.xml')
                    child.expect("#")
                    break
                except Exception as e:
                    retry_times1 -= 1
                    print "fail to configure DR"
                    time.sleep(5)
                    
            retry_times2 = 3
            while retry_times2 > 0:
                try:
                    child.sendline("scp -r /var/data_analytic/config/CA/user360/* " + self.config_data['upg_pl'][0]+ ":/var/data_analytic/report/input/")
                    child.expect('#',timeout=60)
                    break
                except Exception as e:
                    retry_times2 -= 1
                    print "fail to copy files to PL nodes"
                    time.sleep(5)
            retry_times3 = 3
            while retry_times3 > 0:   
                try:
                    child.sendline('sed -i "s/log_level = INFO/log_level = DEBUG/g" /home/upg/user360/common/config/logging.ini')
                    child.expect('#',timeout=60)
                    child.sendline( 'sed -i "/snapshot_start.sh/d" /var/spool/cron/tabs/root')
                    child.expect('#',timeout=60)
                    break
                except Exception as e:
                    retry_times3 -= 1
                    print "Fail to set log level to DEBUG"
                    time.sleep(5)
            retry_times4 = 3
            while retry_times4 > 0:     
                try:
                    child.sendline( 'ssh '+ self.config_data['upg_pl'][0]+ ' "rm -rf /var/data_analytic/report/output/snapshotReport_*" ')
                    child.expect('#',timeout=60)
                    child.sendline( 'ssh '+ self.config_data['upg_pl'][0]+ ' sed -i "/user360report.py/d" /var/spool/cron/tabs/root ')
                    child.expect('#',timeout=60)
                    break
                except Exception as e:
                    retry_times4 -= 1
                    print "fail to delete test files"
                    time.sleep(5)
            child.sendline("exit")
            child.expect(pexpect.EOF)
        except Exception as self.e:
            self.result_excep_msg_handling(sys._getframe().f_code.co_name,self.e)
            traceback.print_exc( file = child.logfile )
            child.logfile.flush()