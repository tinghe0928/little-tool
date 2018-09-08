import datetime
import logging
import pprint
import time
import sys
import os
import getopt
import unittest
import traceback
import user360cli
import upgcfg
import test_user360_status
import test_user360_login
import test_user360_config
import test_user360_replication
import test_user360_drill
import test_user360_freshdb
import test_user360_report
import test_user360_snapshot
import test_user360_help
import test_setup


from unittest import runner
from upgcfg import *
from user360log import *
from user360cli import *
from test_user360_status import *
from test_user360_login import *
from test_user360_config import *
from test_user360_replication import *
from test_user360_drill import *
from test_user360_freshdb import *
from test_user360_report import *
from test_user360_snapshot import *
from test_user360_help import *
from test_setup import *

case_path = os.getcwd()
report_path = os.getcwd()
suite = unittest.TestSuite()

"""This part must be executed before test, aim to copy test files to cluster and remove previous configuration"""
def user360_setup():
    before_suite = unittest.TestSuite()
    before_suite.addTest(test_setup.TestSetUp("test_scp_files"))
    before_suite.addTest(test_user360_config.ConfigTestCase("test_user360_remove_all_succeed"))
    before_suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_cudb_remove_user_succeed"))
    before_suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_cudb_add_user_succeed"))
    return before_suite
    
"""Initial test cases"""
"""These test cases must be executed first, aim to do user360 configuration and initial load"""
def user360_inital():
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_i_succeed"))
    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_i_all_succeed")) 
    
"""Config test cases"""
def user360_config():
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_auto_dsu_switch"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_grant_only_invalid_ip"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_status_config_print_cudb_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_status_config_print_upg_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_fetch_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_counter_switch"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_counter_interval_change"))
"""replication test cases"""
def user360_replication():
#    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_i_all_succeed")) 
    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_i_all_n_f_succeed"))
    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_i_dsg_succeed"))
    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_stopsync_all_succeed"))
    suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_startsync_all_succeed"))
    #suite.addTest(test_user360_replication.ReplicationTestCase("test_user360_replication_switchsync_succeed"))
    
"""drill test cases"""
def user360_drill():
    suite.addTest(test_user360_drill.DrillTestCase("test_drilltestcase1_user360_drill_stop_all_succeed"))
    suite.addTest(test_user360_drill.DrillTestCase("test_drilltestcase2_user360_drill_start_all_succeed"))
    suite.addTest(test_user360_drill.DrillTestCase("test_drilltestcase3_user360_drill_stop_n_succeed"))
    suite.addTest(test_user360_drill.DrillTestCase("test_drilltestcase4_user360_drill_start_n_succeed"))

"""snapshot test cases"""
def user360_snapshot():
    suite.addTest(test_user360_snapshot.SnapshotTestCase("test_user360_snapshot_case1_start_succeed"))
    suite.addTest(test_user360_snapshot.SnapshotTestCase("test_user360_snapshot_case2_cancel_succeed"))

"""report test cases"""
def user360_report():
    suite.addTest(test_user360_report.ReportTestCase("test_user360_report_case1_execute_succeed"))
    suite.addTest(test_user360_report.ReportTestCase("test_user360_report_case2_add_schedule_succeed"))
    suite.addTest(test_user360_report.ReportTestCase("test_user360_report_case3_remove_schedule_succeed"))
   
"""freshDB test cases"""
def user360_freshDB():
    suite.addTest(test_user360_freshdb.FreshDBTestCase("test_user360_freshdb_case1_update_schema_succeed"))
    suite.addTest(test_user360_freshdb.FreshDBTestCase("test_user360_freshdb_case2_clean_all_succeed"))
    suite.addTest(test_user360_freshdb.FreshDBTestCase("test_user360_freshdb_case3_stop_succeed"))
    suite.addTest(test_user360_freshdb.FreshDBTestCase("test_user360_freshdb_case4_start_succeed"))
    suite.addTest(test_user360_freshdb.FreshDBTestCase("test_user360_freshdb_case5_bind_address"))
    
"""help test cases"""
def user360_help():
    suite.addTest(test_user360_help.HelpTestCase("test_user360_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_helpexpert_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_config_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_drill_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_freshdb_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_replication_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_report_help_succeed"))
    suite.addTest(test_user360_help.HelpTestCase("test_user360_snapshot_help_succeed"))    

"""login test cases"""
def user360_login():
    suite.addTest(test_user360_login.LoginTestCase("test_user360_login_success"))
    suite.addTest(test_user360_login.LoginTestCase("test_user360_login_fail_psd"))
    suite.addTest(test_user360_login.LoginTestCase("test_user360_login_fail_user"))
    suite.addTest(test_user360_login.LoginTestCase("test_user360_login_fail_alr"))
    suite.addTest(test_user360_login.LoginTestCase("test_user360_login_timeout_succeed"))

"""status test cases"""
def user360_status():
    suite.addTest(test_user360_status.StatusTestCase("test_user360_status_succeed"))
    suite.addTest(test_user360_status.StatusTestCase("test_user360_status_config_print_cudb_succeed"))
    suite.addTest(test_user360_status.StatusTestCase("test_user360_status_config_print_upg_succeed"))
    suite.addTest(test_user360_status.StatusTestCase("test_user360_replication_status_all_succeed"))
    suite.addTest(test_user360_status.StatusTestCase("test_user360_replication_status_dsg_succeed"))

"""cleanup test cases"""
def user360_cleanup():
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_remove_all_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_add_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_remove_dsg_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_revoke_only_succeed")) 
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_grant_only_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_cudb_remove_user_succeed"))
    suite.addTest(test_user360_config.ConfigTestCase("test_user360_config_cudb_add_user_succeed"))

def user360_testsuite():
    """mandatory cases"""
    user360_inital()
    """optional cases"""
    user360_config()
    user360_replication()
    user360_drill()
    user360_snapshot()
    user360_report()
    user360_freshDB()
    user360_help()
    user360_login()
    user360_status()
    user360_cleanup()
    return suite

