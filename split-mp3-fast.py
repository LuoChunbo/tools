#!/usr/bin/env python
import argparse
import subprocess
import io
import re
import os
import shutil
from glob import glob


def get_audio_duration(filename):

    cmd = 'ffprobe -i "%s" -show_format -v quiet' % filename
    #print("cmd: %s " % cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()

    pattern="[\d]+[\.]?[\d]*"
    line = p.stdout.readline().decode("utf-8")
    while line :
        #print(line)
        regex = r"duration=%s" % pattern
        m = re.match(regex, line)
        if m:
            #print(m)
            #print(m.group(0))
            sub_line = m.group(0)
            regex2 = r"%s" % pattern
            m2 = re.search(regex2, sub_line)
            if m2:
                #print(m2)
                #print(m2.group(0))
                return float(m2.group(0))
        line = p.stdout.readline().decode("utf-8")

    return -1.0


def split_mp3(in_file, out_file, start_time, duration, ):
    cmd = 'ffmpeg -i "%s" -acodec copy -t %s -ss %s "%s" -v quiet' % (in_file, duration, start_time, out_file)
    print ("cmd: %s " % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()

    line = p.stdout.readline().decode("utf-8")
    while line :
        print(line)
        line = p.stdout.readline().decode("utf-8")

def format_time(second):
    hh = second/3600
    mm = (second%3600)/60
    ss = second%60
    return "%02d:%02d:%02d" %(hh, mm, ss)

def handle_audio(in_file, out_dir, file_name, minutes, create_dir):

    music_slice_ms = minutes*60*1000; #15 minutes
    music_slice_time = format_time(music_slice_ms/1000)
    print("music slice tiime : %s" % music_slice_time)

    mp3_duration = get_audio_duration(in_file)
    mp3_duration_ms = int (mp3_duration * 1000);
    print ("mp3 durations: %f , mp3_duration_ms = %d " % (mp3_duration, mp3_duration_ms))

    if (mp3_duration_ms < music_slice_ms):
        out_file = "%s/%s.mp3" % (out_dir, file_name)
        print("audio duration less than slice, copy original file ")
        shutil.copyfile(in_file, out_file)
        return

    #base_name = os.path.basename(in_file)
    #print ("base name %s" % base_name)

    music_name = os.path.splitext(file_name)[0]
    print ("music name %s " % music_name)

    if create_dir == 1:
        new_dir = "%s/%s" %(out_dir, music_name)
        if not os.path.exists(new_dir):
            print("mkdir %s " % new_dir)
            os.mkdir(new_dir)

    count = 0;
    start_time_ms = 0;
    while start_time_ms < mp3_duration_ms:
        count += 1

        if create_dir == 1:
            out_file = "%s/%02d.mp3" %(new_dir, count)
        else:
            out_file = "%s/%s-%02d.mp3" % (out_dir, music_name, count)

        start_time = format_time(start_time_ms/1000)
        print ("start time %s " % start_time)

        split_mp3(in_file, out_file, start_time, music_slice_time)
        start_time_ms += music_slice_ms;


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",help="Audio input direcotry")
    parser.add_argument("-o", "--output_dir", help="Audio output directory")
    parser.add_argument("-t", "--time", type=int, help="split time in minutes",default=15)
    parser.add_argument("-w", "--width", type=int, help="file name max width",default=24)
    parser.add_argument("-c", "--create_dir", type=int, help ="create sub directory for each file", default=0)

    args = parser.parse_args()
    if args.input_dir is None or args.output_dir is None:
        parser.print_help()
        return

    print(" input dir: %s , output dir: %s , split time %d minutes , file name lenth : %d , create sub dir: %d" %
            (args.input_dir, args.output_dir, args.time, args.width, args.create_dir))

    if os.path.exists(args.output_dir):
        print("mkdir %s" % args.output_dir)
        shutil.rmtree(args.output_dir)
    os.mkdir(args.output_dir)

    mp3_pattern= "%s/*.mp3" % args.input_dir
    for file in glob(mp3_pattern):
        print("source file %s" % file)
        file_name=os.path.basename(file)
        if (len(file_name) > args.width):
            file_name = file_name[:args.width]
        print("file name : %s" % file_name)

        handle_audio(file, args.output_dir, file_name, args.time, args.create_dir)

if __name__ == "__main__":
    main()
