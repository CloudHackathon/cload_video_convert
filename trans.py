#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import sys

split_delta_time = 10
ffmpeg_tool = "/home/ubuntu/hackathon/ffmpeg"
ffprobe_tool = "/home/ubuntu/hackathon/ffprobe"
mp4slice_tool = "/home/ubuntu/hackathon/mp4Slice"

def getMediaInfo(file):
	info = {}
	cmd = "%s -i %s -show_format 2>/dev/null" % (ffprobe_tool, file) 
	res = os.popen(cmd).read().split('\n')
	for i in range(len(res)):
		k_v = res[i].split('=')
		if len(k_v) == 2:
			info[k_v[0]] = k_v[1]
	return info

def split(srcfile, dstfile):
	print "split"
	dstDict = {}
	mediainfo = getMediaInfo(srcfile)
	pieces = int(float(mediainfo["duration"])/split_delta_time)
	for i in range(pieces):
		starttime = i*split_delta_time
		durtime = split_delta_time
		if i == pieces-1:
			durtime = 0
		vfile = "%s_Video_%i.mp4" % (dstfile,i)
		cmd = "%s -i %s -o %s -s %d -t %d >/dev/null 2>&1" % (mp4slice_tool, srcfile, vfile, starttime, durtime)
		print cmd
		os.system(cmd)
		dstDict[str(i+1)] = vfile
	dstDict["count"] = pieces
	return dstDict

def trans(srcfile, dstfile, fmtid):
	vf = "-filter_complex \"scale=480:270[main];[main]overlay=x=10:y=10:enable='between(t,0,5)'\""
	vf = "-filter_complex \"scale=480:270[main];movie=/home/ubuntu/hackathon/logo270.jpg [logo0]; [main] [logo0] overlay=main_w-overlay_w-10:10\""
	vf2 = "-pix_fmt yuv420p  -vcodec libx264 -x264opts threads=auto:bitrate=250"
	vf3 = "-itsoffset 0 -i /home/ubuntu/hackathon/yunpaomadeng270.mp4"
	if fmtid == "HD":
		vf = "-filter_complex \"scale=640:360[main];[main]overlay=x=10:y=10:enable='between(t,0,10)'\""
		vf = "-filter_complex \"scale=640:360[main];movie=/home/ubuntu/hackathon/logo360.jpg [logo0]; [main] [logo0] overlay=main_w-overlay_w-10:10\""
		vf2 = "-pix_fmt yuv420p  -vcodec libx264 -x264opts threads=auto:bitrate=400"
		vf3 = "-itsoffset 0 -i /home/ubuntu/hackathon/yunpaomadeng480.mp4"
	if fmtid == "SHD":
		vf = "-filter_complex \"scale=1280:720[main];[main]overlay=x=10:y=10:enable='between(t,0,10)'\""
		vf = "-filter_complex \"scale=1280:720[main];movie=/home/ubuntu/hackathon/logo720.jpg [logo0]; [main] [logo0] overlay=main_w-overlay_w-10:10\""
		vf2 = "-pix_fmt yuv420p  -vcodec libx264 -x264opts threads=auto:bitrate=950"
		vf3 = "-itsoffset 0 -i /home/ubuntu/hackathon/yunpaomadeng720.mp4"
	vf3 = ""
	af  = "-acodec libfdk_aac -profile:a aac_he  -ab 32k -ar 48000 -ac 2"
	exp = "export LD_LIBRARY_PATH=/home/ubuntu/hackathon/so/"
	cmd = "%s;%s -i %s %s %s %s %s -bsf:v h264_mp4toannexb -f mpegts  -y %s -loglevel error" % (exp, ffmpeg_tool,srcfile,vf3,vf,vf2,af,dstfile)
	print cmd
	return os.system(cmd)

def tomp4(tsfile, mp4file):
	exp = "export LD_LIBRARY_PATH=/home/ubuntu/hackathon/so/"
	cmd = "%s;%s -i %s -codec copy -bsf:a aac_adtstoasc -f mp4 -movflags faststart -y %s -loglevel error" % (exp, ffmpeg_tool,tsfile,mp4file)
	print cmd
        return os.system(cmd)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "./trans.py type srcfile dstfile"
		print "type 1: split"
		print "type 2: trans"
		print "type 3: merge"
		exit()
	if sys.argv[1] == '1':
		print split(sys.argv[2],sys.argv[3])
	if sys.argv[1] == '2':
		print trans(sys.argv[2],sys.argv[3],sys.argv[4])
	if sys.argv[1] == '3':
		print tomp4(sys.argv[2],sys.argv[3])

