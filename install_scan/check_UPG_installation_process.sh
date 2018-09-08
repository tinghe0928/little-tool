#!/bin/sh
date
if [ "$1" ]; then
  if [ "$1" == "-h" -o "$1" == "--help" ]; then
    echo "$0 <name_of_your_process>"
    exit 1
  fi
  pro_name="$1"
else
  pro_name="UPG_Management"
fi

pid_1stpro_name=`ps -ef |grep $pro_name |grep "/bin/bash"|grep "\-p"|grep "\-o" |sed -n '1p'|awk '{print $2}'`
if_pro_num=`ps -ef |grep $pro_name |grep "/bin/bash"|grep "\-p"|grep "\-o"|wc -l`
#echo "the system now has $if_pro_num $pro_name processes "
"""When no process running, keep scanning"""
if [ "$if_pro_num" == 0 ]; then
  echo "the system now has $if_pro_num $pro_name processes "
  while [ "$if_pro_num" == 0 ]; do
          if_pro_num=`ps -ef |grep $pro_name |grep "/bin/bash"|grep "\-p"|grep "\-o"|wc -l`
          pid_1stpro_name=`ps -ef |grep $pro_name |grep "/bin/bash"|grep "\-p"|grep "\-o"|sed -n '1p'|awk '{print $2}'`
  sleep 3
  done
fi

if [ "$if_pro_num" == 1 ]; then
  echo "the system now has $if_pro_num $pro_name processes "
  echo "the pid of the $pro_name is : $pid_1stpro_name"
  while [ $if_pro_num ]; do
        #if_UPG_Management=`ps -ef |grep $pro_name |grep bash`
        if_pro_num=`ps -ef |grep $pro_name.sh |grep "/bin/bash"|grep "\-p"|grep "\-o"|wc -l`
        #echo $if_pro_num
        #pid_1stpro_name=`ps -f |grep $pro_name|grep bash|sed -n '1p'`
        i=1
        while [ "$i" -le "$if_pro_num" ]; do
                pid_pro[$i]=`ps -ef |grep $pro_name |grep "/bin/bash"|grep "\-p"|grep "\-o"|sed -n "${i}"p |awk '{print $2}'`
                #echo ${pid_pro[$i]}
                if [[ "$if_pro_num" -gt 1 && "${pid_pro[$i]}" != "$pid_1stpro_name" ]]; then
                        echo "**********************************"
                        #pid_UPG_Management_4rd=`ps -ef |grep $pro_name |grep bash |sed -n '4p' |awk '{print $2}'`
                        kill -9 ${pid_pro[$i]}
                        date
                        echo "the starting id of the process is ${pid_pro[$i]}"
                        echo "your procrss ${pid_pro[$i]} is stopped,if you want to setup agagin, plese exexute: stop_UPG_Management_process.sh"
                        #if_pro_num=`expr $if_pro_num - 1`
                        echo $if_pro_num
                        echo "**********************************"
                #else
                        #echo "no  process"
                fi
                i=`expr $i + 1`
        done
  done
else
  echo "the system now has $if_pro_num $pro_name processes "
  date
  echo "pls check the process first!!!"
fi