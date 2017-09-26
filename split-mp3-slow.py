b #!/usr/bin/env python

import argparse
import os
import shutil
from glob import glob
from pydub import AudioSegment

def save_audio(audio, name):
    output = open(name, "wb")
    audio.export(output, format='mp3', bitrate='64k')
    output.close()


def handle_audio(audio, out_dir, name, minutes, create_dir):
    print ("audio seconds: %s " % audio.duration_seconds);
    hour = audio.duration_seconds/3600
    minute = (audio.duration_seconds%3600)/60
    second = audio.duration_seconds%60

    print ("audio duration: %d hour %d minute %d second" % (hour, minute, second))


    split_ms = minutes*60*1000;
    max_ms = len(audio)

    if (max_ms < split_ms):
        print("file %s name duration less than %d minute, copy only" % (name, minutes))
        save_name="%s/%s"%(out_dir, name)
        save_audio(audio, save_name)
        return

    start = 0
    end = 0
    count = 0;

    true_name=os.path.splitext(name)[0]

    if create_dir == 1:
        new_dir ="%s/%s" %(out_dir, true_name)
        if not os.path.exists(new_dir):
            print("mkdir %s " % new_dir)
            os.mkdir(new_dir)

    while start < max_ms:
        if ((start + split_ms) < max_ms):
            end = start + split_ms
        else:
            end = max_ms
        count += 1;

        new_audio = audio[start:end]

        if create_dir == 1:
            new_audio_name = "%s/%02d.mp3" %(new_dir, count)
        else:
            new_audio_name = "%s/%s-%02d.mp3" % (out_dir,true_name,count)
        print( "split audio : %s " % new_audio_name )

        save_audio(new_audio, new_audio_name);

        start = end +1;

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
        #os.rmdir(args.output_dir)
        shutil.rmtree(args.output_dir)
    os.mkdir(args.output_dir)

    mp3_pattern= "%s/*.mp3" % args.input_dir
    for file in glob(mp3_pattern):
        print("source file %s" % file)
        file_name=os.path.basename(file)
        if (len(file_name) > args.width):
            file_name = file_name[:args.width]
        print("file name : %s" % file_name)
        source = AudioSegment.from_mp3(file)
        handle_audio(source, args.output_dir, file_name, args.time, args.create_dir)


if __name__=="__main__":
    main()
