#!/usr/bin/python

import MySQLdb
import os
import sys
import json
import socket
import trans

def finish_update_db(vname, format):
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		value = [vname, format]
		conn.select_db("test")
		sql = "update t_seg_video set status = 5 where vname = %s and format = %s"
		cur.execute(sql, value)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])


def get_merge_task():
	merge_task = []
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		conn.select_db("test")
		sql = "select vname, format from t_seg_video where status = 2 group by format"
		cur.execute(sql)
		conn.commit()
		results = cur.fetchall()
		for row in results:
			vname = row[0]
			format = row[1]
			condition = " vname = \"" + vname + "\" and format = \"" + format + "\" "
			get_task_sql = "select segid,vname,format,convsIp from t_seg_video where (select count(*) from t_seg_video where " +condition + ") = totalCount and " + condition
			#print "get data from db, get_task_sql=%s" % (get_task_sql)
			cur.execute(get_task_sql)
			db_tasks = cur.fetchall()
			for one_db_task in db_tasks:
				segid = one_db_task[0]
				vname = one_db_task[1]
				format = one_db_task[2]
				convsip = one_db_task[3]
				print "get data from db, segid=%s, vname=%s, format=%s, convsip=%s" % (segid, vname, format, convsip)
				merge_task.append({"segid":segid, "vname":vname, "format":format, "convsIp":convsip});
			if(len(merge_task) != 0):
				merging_status = 4;
				value = [merging_status]
				update_sql = "update t_seg_video set status = %s where " + condition;
				cur.execute(update_sql, value)
				conn.commit()
				break

				
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])
	return merge_task;
	

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 53))
	ip = s.getsockname()[0]
	s.close()
	return ip

def download_file(ip, name):
	dstfile = "/home/ubuntu/hackathon/videos/" + name;
	download_cmd = "/usr/bin/wget -T 7200 -t 3 --user-agent=\"tmpfs_cache\" \"http://" + ip + "/" + name + "\" -O " + dstfile;
	print download_cmd

	#os.system(download_cmd);
	return dstfile
	
ip = get_local_ip()

merge_tasks = get_merge_task()
lenth = len(merge_tasks)
if(lenth == 0):
	print "no task"
	sys.exit()
my_vname = ""
my_format = ""
cat_cmd = "cat "
for one_task in merge_tasks:
	ip = one_task["convsIp"]
	name = one_task["vname"] + "." + one_task["format"] + "." + str(one_task["segid"]) + ".ts"
	my_vname = one_task["vname"]
	my_format = one_task["format"]
	one_file = download_file(ip, name)
	cat_cmd = cat_cmd + name + " ";
ts_file = "/home/ubuntu/hackathon/result/" + my_vname + "." + my_format + ".ts"
final_file = "/home/ubuntu/hackathon/result/" + my_vname + "." + my_format + ".mp4"
cat_cmd = cat_cmd + final_file
print cat_cmd
#os.system(cat_cmd)
print final_file

finish_update_db(my_vname, my_format)

sys.exit()
