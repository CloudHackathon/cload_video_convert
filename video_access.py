#!/usr/bin/python

import MySQLdb
import os
import sys
import json
import socket
import trans

def insert_db(vname, format, segid, count, local_ip):
	convsip = ""
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		value = [vname, format, segid, count, local_ip, convsip]
		conn.select_db("test")
		sql = "insert into t_seg_video (vname, format, segId, totalCount, accessIp, convsIp) values \
		(%s, %s, %s, %s, %s, %s)"
		cur.execute(sql, value)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])

def get_one_convs_task():
	try:
		conn = MySQLdb.connect(host="10.66.129.25",user="root",passwd="leozhiqin!",port=3306)
		cur = conn.cursor()
		sql = "select vname, format, segId, accessIp from t_seg_video where status = 0 limit 1"
		cur.execute(sql)
		results = cur.fetchall()
		for row in results:
			student_id = row[0]
			book_info = row[1]
			print "get data from db, student_id=%s, book_info=%s" % (student_id, book_info)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql error %d: %s" % (e.args[0], e.args[1])
	

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 53))
	ip = s.getsockname()[0]
	s.close()
	return ip
		

vname = "test2"
format = sys.argv[1]
file = sys.argv[2]
print file

ip = get_local_ip()

dstfile = "/var/www/html/" + vname + "." + format + ".src"
seg_info = trans.split(file, dstfile)
num = seg_info["count"]
print num
for i in range (1, num + 1):
	file = seg_info[str(i)]
	insert_db(vname, format, i, num, ip)
	print file

sys.exit()
