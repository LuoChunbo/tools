#!/usr/bin/env python3

import argparse
import sys
import wave
import struct


def wave_trans(input_file, output_file, output_channels, effect_channel):
    audio_reader = wave.open(input_file, 'rb')
    if not audio_reader:
        print(" open input file %s failed " % input_file)
        return

    audio_writer = wave.open(output_file, 'wb')
    if not audio_writer:
        pirnt( "open output file %s failed " % ouput_file)
        return

    print (" Input wav channel %d" % audio_reader.getnchannels())
    print (" Input sampwidht %d " % audio_reader.getsampwidth())
    print (" Input framerate %d " % audio_reader.getframerate())
    print (" Input frame number %d " % audio_reader.getnframes())

    audio_writer.setnchannels(output_channels);
    audio_writer.setsampwidth(audio_reader.getsampwidth())
    audio_writer.setframerate(audio_reader.getframerate())

    input_frames = audio_reader.getnframes()

    data_zero = struct.pack('h', 0)

    for i in range(input_frames):
        data = audio_reader.readframes(1)
        data_ch0 = data[0:2]

        if effect_channel == 0:
            output_data = data_ch0
        else:
            output_data = data_zero

        for j in range(1, output_channels):
            if j == effect_channel:
                output_data = output_data + data_ch0
            else:
                output_data = output_data + data_zero;
        audio_writer.writeframesraw(output_data)

    audio_reader.close()
    audio_writer.close()


def main():
    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="input .wav file")
    parser.add_argument("-o", "--output_file", help="output wav file", default="out.wav")
    parser.add_argument("-n", "--channel_num", type=int, help="ouput wav channel number", default=2)
    parser.add_argument("-e", "--effect_channel",type=int,  help="effect channel", default=1)

    args = parser.parse_args()

    print("input file %s " % args.input_file);
    print("output file %s " % args.output_file);
    print("output channel number %d " % args.channel_num);
    print("output effect channel %d " % args.effect_channel);

    if args.input_file is None:
        parser.print_help()
        return

    wave_trans(args.input_file, args.output_file, args.channel_num, args.effect_channel-1)

if __name__ == '__main__':
    main()
