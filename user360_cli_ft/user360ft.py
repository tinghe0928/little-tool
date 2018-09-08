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
import cases_define
import xmlrunner
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
from cases_define import *

def set_config_file(argv):
    print "argv" 
    print argv
    config_file = ''
    opts,args = getopt.getopt(argv,"hf:",["help","file="])
    print opts
    print args
    for opt,arg in opts:
        if opt in ("-h","--help"):
            logger.info( 'python script_name.py -f config_file_name' )
            sys.exit(1)
        elif opt in ("-f","--file"):
            config_file = arg
        else:
            sys.exit(1)
    return config_file

def run_suite_output_xml_report(suite,**args):
    descriptions = args.get('TEST_OUTPUT_DESCRIPTIONS', True)
    output_dir = os.path.abspath('.')
    single_file = args.get('TEST_OUTPUT_FILE_NAME', 'user360_clift_testreport.xml')
    kwargs = dict(verbosity=1, descriptions=descriptions, failfast=False)
    if single_file is not None:
        file_path = os.path.join(output_dir, single_file)
        with open(file_path, 'wb') as xml:
            return xmlrunner.XMLTestRunner(output=xml,**kwargs).run(suite)
    else :
        return xmlrunner.XMLTestRunner(output=output_dir,**kwargs).run(suite)

def setup():
    setup = unittest.TextTestRunner()
    setup_result = setup.run(user360_setup())
    return len(setup_result.failures)

def main(argv):
    for i in range(1):
        try:
            os.system("chmod 777 *")
            retry = 3
            while retry > 0:
                if setup() == 0:
                    break
                else:
                    retry -= 1
            test_suite = user360_testsuite()
            run_suite_output_xml_report(test_suite)
#             runner = unittest.TextTestRunner()
#             runner.run(test_suite)
        except Exception as e:
            pass
         
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
