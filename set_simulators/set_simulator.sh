#! /bin/sh
##################echo the message################
if [ "$2" == "" ]; then
    echo "Usage: ./script.sh cluster cluster_num"
    echo "For example: ./script.sh script 08 1"
    exit 1
fi


cluster=$1
cluster_num=$2

#####get the IP of simulator####
line_num=`/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' |cut -d : -f 2 | awk '{ print $1}' | wc -l`
if [ "$line_num" == 1 ]; then
    sim_ip=`/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' |cut -d : -f 2 | awk '{ print $1}'`
    echo "the simulator ip is $sim_ip"
elif [ "$line_num" == 2 ]; then
    sim_ip=`/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' |cut -d : -f 2 | awk '{ print $1}' |sed -n '2p'`
    echo "the simulator ip is $sim_ip"
else
    echo "Fail to get the IP of simulator!"
    exit 1
fi



#######ADMS#######
echo "***************set simulator for adms***************"
if_adms=`netstat -an |grep 16702`
if [ "$if_adms" == "" ]; then
    /opt/HTTPSimulator/HTTP/ADMS/run-http-server_16702.sh 0
    sleep 1
    if_adms=`ps -ef |grep 16702 |grep HTTPServer`
    if [ "$if_adms" != "" ]; then
        echo "***************Finished to set simulator for adms**************** "
    else
        echo "Fail to set simulator for adms"
    fi
else
    echo "simulator for adms has already been set"
fi

#######CUDB#######
echo "***************set simulator for CUDB***************"
cudb_port=1${cluster}4${cluster_num}
echo "CUDB port is $cudb_port"
if_cudb=`ps -ef | grep $cudb_port |grep slapd`
if [ "$if_cudb" == "" ]; then
    sudo -E /lsv/simulators/CUDB/RAM_UPG/empty_db.sh $cluster $cluster_num
    if_cudb=`netstat -an | grep $cudb_port`
    if [ "$if_cudb" != "" ]; then
         echo "Finished to set simulator for CUDB "
    else
        echo "Fail to set simulator for CUDB"
    fi
else
    echo "simulator for CUDB has already been set"
fi

#######FNR#######
echo "***************set simulator for fnr***************"
if_fnr=`netstat -an |grep 8002`
if [ "$if_fnr" == "" ];then
    cd /lsv/simulators/HLR_ssh
    nohup java -jar HLR_Simulator_ssh.jar --port 8002 --responsefile /lsv/simulators/HLR_ssh/hlr.resp --prompt "<" &
    sleep 1
    if_fnr=`ps -ef |grep 8002 |grep java`
    if [ "$if_fnr"  != "" ]; then
        echo "Finished to set simulator for fnr "
    else
        echo "Fail to set simulator for fnr"
    fi
else
    echo "simulator for fnr has already been set"
fi

#######FT_JDBC#######
echo "***************set simulator for JDBC***************"
if_FT_JDBC=`ps -ef |grep mysql |grep mysqld`
if [ "$if_FT_JDBC" == "" ]; then
    echo "please setup database"
else
    echo "simulator for FT_JDBC has already been set"
fi

#######FTP#######
echo "***************set simulator for FTP***************"
if_FTP=`ps -ef |grep -i ftpd |grep SERVER`
if [ "$if_FTP" == "" ]; then
    /lsv/simulators/FTP/start_ftp.sh 1337 & > /lsv/simulators/FTP/ftp_start.log
    sleep 3
    ftp_up=`cat /lsv/simulators/FTP/ftp_start.log | grep /usr/local/sbin/pure-ftpd`
    if [ "ftp_up" != "" ]; then
        echo "start to setup again"
        /usr/sbin/pure-ftpd -A -c2000 -B -C200 -z -fnone -H -I15 -lpam -lunix -L2000:8 -m100 -s -S0.0.0.0,1337 -u0 -x -r -i -k99 -G -Z
        sleep 1
        ftp_pid=`ps -ef |grep pure | grep SERVER | awk '{ print $2 }'`
        echo "started with pid $ftp_pid"
    else
        sleep 1
    fi
    if_FTP=`ps -ef |grep -i ftpd |grep SERVER`
    if [ "$if_FTP" != "" ]; then
        echo "Finished to set simulator for FTP"
    else
        echo "Fail to set simulator for FTP"
    fi
else
    echo "simulator for FTP has already been set"
fi

#######hlr_telnet#######
echo "***************set simulator for hlr_telnet***************"
if_hlr_telnet=`ps -ef |grep 5002 |grep telnet`
if [ "$if_hlr_telnet" == "" ]; then
    cd /lsv/simulators/TELNET/
    nohup ./run-telnet-server.sh -p 5002 -f ./upg_dp89_lsv.resp >> /dev/null 2>&1 &
    sleep 1
    if_hlr_telnet=`ps -ef |grep 5002 |grep telnet`
    if [ "$if_hlr_telnet" != "" ]; then
        echo "Finished to set simulator for DR hlr telnet"
    else
        echo "Fail to set simulator for hlr_telnet"
    fi
else
    echo "simulator for hlr_telnet has already been set"
fi

#######hlrssh#######
echo "***************set simulator for hlrssh***************"
if_hlrssh=`netstat -an |grep 8002`
if [ "$if_hlrssh" == "" ]; then
    cd /lsv/simulators/HLR_ssh
    nohup java -jar HLR_Simulator_ssh.jar --port 8002 --responsefile /lsv/simulators/HLR_ssh/hlr.resp --prompt "<" &
    sleep 1
    if_hlrssh=`ps -ef |grep 8002 |grep java`
    if [ "$if_hlrssh"  != "" ]; then
        echo "Finished to set simulator for hlrssh "
    else
        echo "Fail to set simulator for hlrssh"
    fi
else
    echo "simulator for hlrssh has already been set"
fi

#######hss#######
echo "***************set simulator for hss***************"
hss_port=1${cluster}6${cluster_num}
echo "hss_port is: $hss_port"
if_hss=`ps -ef |grep $hss_port |grep ShDiameterServer`
if [ "$if_hss" == "" ]; then
    cd /opt/SH-Simulator/15A/
    #echo "./startServer.sh ${sim_ip} ${hss_port} hss${hss_port}.simulator upg.cbc.ericsson.com &"
    ./startServer.sh ${sim_ip} ${hss_port} hss${hss_port}.simulator upg.cbc.ericsson.com &
    sleep 3
    if_hss=`ps -ef |grep $hss_port |grep ShDiameterServer`
    if [ "$if_hss" != "" ]; then
        echo "Finished to set simulator for hss"
    else
        echo "Fail to set simulator for hss"
    fi
else
    echo "simulator for hss has already been set"
fi

#######hss_pnr#######
#######pgm#######
echo "***************set simulator fo pgm***************"
if_pgm=`ps -ef |grep 16602 |grep PGM`
if [ "$if_pgm" == "" ]; then
    sudo /opt/HTTPSimulator/HTTP/PGM/run-http-server_16602.sh 0
    sleep 1
    if_pgm=`ps -ef |grep 16602 |grep PGM`
    if [ "$if_pgm" != "" ]; then
        echo "Finished to set simulator for pgm "
    else
        echo "Fail to set simulator for pgm"
    fi
else
    echo "simulator for pgm has already been set"
fi

########mtas and pg#######
echo "***************set simulator fo pg and mtas***************"
if_cai3g=`ps -ef |grep tomcat |grep CAI3G`
if [ "$if_cai3g" == "" ]; then
    cd /lsv/simulators/CAI3G_SIM/agentsim/jakarta-tomcat-5.5.17/bin/
    ./start-cai3g.sh > /lsv/simulators/CAI3G_SIM/agentsim/jakarta-tomcat-5.5.17/bin/tmp.log &
    sleep 5
    if_cai3g=`ps -ef |grep tomcat |grep CAI3G`
    if [ "$if_cai3g" != "" ]; then
        echo "Finished to set simulator for pg and mtas "
    else
        echo "Fail to set simulator for pg and mtas"
    fi
else
    echo "simulator for pg and mtas has already been set"
fi

############################
exit 0
