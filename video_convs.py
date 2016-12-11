#!/usr/bin/python

import MySQLdb
import os
import sys
import json
import socket
import trans

def update_db(id, status, ip):
	convsip = ""
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		value = [status, ip, id]
		conn.select_db("test")
		sql = "update t_seg_video set status = %s, convsIp = %s where id = %s"
		cur.execute(sql, value)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])


def get_one_convs_task():
	id = 0
	vname = "no"
	format = ""
	segId = 0
	accessIp = ""
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		conn.select_db("test")
		sql = "select id, vname, format, segId, accessIp from t_seg_video where status = 0 limit 1"
		cur.execute(sql)
		results = cur.fetchall()
		print "test";
		for row in results:
			id = row[0]
			vname = row[1]
			format = row[2]
			segId = row[3]
			accessIp = row[4]
			print "get data from db, id=%s, vname=%s, format=%s, segId=%s, accessIp=%s" % (id, vname, format, segId, accessIp)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])
	return (id, vname, format, segId, accessIp)
	

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 53))
	ip = s.getsockname()[0]
	s.close()
	return ip

def download_file(ip, name):
	dstfile = "/home/ubuntu/hackathon/videos/" + name
	download_cmd = "/usr/bin/wget -T 7200 -t 3 --user-agent=\"tmpfs_cache\" \"http://" + ip + "/" + name + "\" -O " + dstfile
	print download_cmd

	#os.system(download_cmd);
	return dstfile
		

local_ip = get_local_ip()

(id, vname, format, segid, ip) = get_one_convs_task()
print "id=%s, vname=%s, format=%s, segId=%s, accessIp=%s" % (id, vname, format, segid, ip)

name = vname + "." + format + ".src_Video_" + str(segid) + ".mp4";
srcfile = download_file(ip, name)
dstfile = "/var/www/html/" + vname + "." + format + "." + segid + ".dst"

code = trans.trans(srcfile, dstfile, format)

update_db(id, 2, local_ip)

