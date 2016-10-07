#!/usr/bin/env python
import argparse

def extractEvent(data):
    return [int(x,16) for x in data.split('======')[-1].strip(' ').split(' ')]

def extractTBMHeader(eventData):
    return ((eventData[0] & 0xff) << 8) + (eventData[1] & 0xff)

def extractTBMTrailer(eventData):
    return ((eventData[-2] & 0xff) << 8) + (eventData[-1] & 0xff)


parser = argparse.ArgumentParser(description='combine pxar root files')
parser.add_argument('-i','--input',dest='input',metavar='PATH',
                     help='inputfile',
                     default='')
parser.add_argument('-t', '--token-chain-length', dest = 'tokenchainlength', default = 4,
                    help='tokenchainlength')

parser.add_argument('-e', '--event-dump', dest = 'eventdump', default = '',
                    help='event dump output from pxar')

args = parser.parse_args()
lines = []

if len(args.eventdump.strip()) > 1:
    lines = args.eventdump.split('\n')
else:
    with open(args.input) as inputFile:
        lines = inputFile.readlines()

tokenChainLength = int(args.tokenchainlength)

for data in lines:
    data = data.strip()
    if '======' in data:
        print " "

        eventData = extractEvent(data)

        tbmHTOk = True
        if eventData[0] & 0xe000 != 0xa000:
            print " -> no marker! alpha"
            tbmHTOk = False

        if eventData[1] & 0xe000 != 0x8000:
            print " -> no marker! beta"
            tbmHTOk = False
        tbmHeader = extractTBMHeader(eventData)

        rawHeader = '{0:016b}'.format(eventData[0]) + '{0:016b}'.format(eventData[1])
        formattedRH = "\x1b[32m%s\x1b[37m%s\x1b[36m%s\x1b[32m%s\x1b[37m%s\x1b[36m%s\x1b[0m"%(rawHeader[:-29],rawHeader[-29:-24],rawHeader[-24:-16],rawHeader[-16:-13], rawHeader[-13:-8],rawHeader[-8:])
        print "%04x %04x TBM HEADER 0x%04x ID: %03d      %s"%(eventData[0], eventData[1], tbmHeader, ((tbmHeader>>8) & 0xff), formattedRH)


        tbmTrailer = extractTBMTrailer(eventData)
        tbmTrailer0 = eventData[-2]
        tbmTrailer1 = eventData[-1]

        if tbmHTOk:
            eventData = eventData[2:-2]

        i=0
        nRoc = -1
        errors = [0] * len(eventData)
        lastColumn = -1
        while i < len(eventData):
            nibble = eventData[i]

            if nibble & 0xe000 == 0x4000:
                lastRow = -1
                lastColumn = -1
                nRoc += 1
                badRocHeader = False

                if nibble & 0x0ff0 == 0x0ff0:
                    errors[i] = errors[i] | 1
                    badRocHeader = True

                formattedRH = '{0:016b}'.format(nibble)
                formattedRH = "\x1b[33m%s\x1b[36m%s\x1b[32m%s\x1b[36m%s\x1b[35m%s\x1b[0m"%(formattedRH[:-13],formattedRH[-13:-12],formattedRH[-12:-4], formattedRH[-4:-2],formattedRH[-2:])

                xorSumFormatted = ("%d"%((nibble & 0x0ff0) >> 4)).ljust(3)

                rbFormatted = '  '
                if (nibble & 0x0002) > 0:
                    rbFormatted = 'RB'

                if nRoc >= tokenChainLength:
                    badRocHeader = True

                if badRocHeader:
                    print "\x1b[31m     %04x ROC%d HEADER\x1b[0m                                    %s"%(nibble, nRoc, formattedRH)
                else:
                    print "     %04x ROC%d HEADER  XOR-SUM: %s %s                   %s"%(nibble, nRoc, xorSumFormatted, rbFormatted, formattedRH)


            elif nibble & 0xe000 <= 0x2000:

                pixelHitErrors = []

                if nibble & 0x8000:
                    pixelHitErrors.append('MARKER')

                i += 1
                nibble2 = eventData[i]
                raw = ((nibble & 0x0fff) << 12) + (nibble2 & 0x0fff)

                ph = (raw & 0x0f) + ((raw >> 1) & 0xf0)

                if (raw & 0x10) > 0:
                    pixelHitErrors.append('PHFILLBIT')

                r2 = (raw >> 15) & 7
                r1 = (raw >> 12) & 7
                r0 = (raw >> 9) & 7
                r = r2 * 36 + r1 * 6 + r0
                row = 80 - int(r / 2)
                column = 2 * (((raw >> 21) & 7) * 6 + ((raw >> 18) & 7)) + (r & 1)

                if column < lastColumn:
                    pixelHitErrors.append('PIXELORDER')

                lastRow = row
                lastColumn = column

                if not ((row >= 0 and row < 80) and (column >= 0 and column < 52)):
                    pixelHitErrors.append('ADDRESS')

                formattedRaw = '{0:024b}'.format(raw)
                formattedRaw = "\x1b[37m%s\x1b[33m%s\x1b[34m%s\x1b[35m%s\x1b[36m%s\x1b[35m%s\x1b[0m"%(formattedRaw[:-24],formattedRaw[-24:-18],formattedRaw[-18:-9], formattedRaw[-9:-5],formattedRaw[-5],formattedRaw[-4:])

                if len(pixelHitErrors) < 1:
                    print "%04x %04x PIXEL: ROC%02d COL: %+3d ROW: %+3d         %s %s" % (nibble, nibble2, nRoc, column, row, formattedRaw, ", ".join(pixelHitErrors))
                else:
                    print "\x1b[31m%04x %04x PIXEL: ROC%02d COL: %+3d ROW: %+3d\x1b[0m         %s %s" % (nibble, nibble2, nRoc, column, row, formattedRaw, ", ".join(pixelHitErrors))

            i += 1

        rawHeader = '{0:016b}'.format(tbmTrailer0) + '{0:016b}'.format(tbmTrailer1)
        formattedRH = "\x1b[32m%s\x1b[31m%s\x1b[36m%s\x1b[32m%s\x1b[31m%s\x1b[36m%s\x1b[0m"%(rawHeader[:-29],rawHeader[-29:-24],rawHeader[-24:-16],rawHeader[-16:-13], rawHeader[-13:-8],rawHeader[-8:])
        print "%04x %04x TBM TRAILER 0x%04x             %s"%(eventData[0], eventData[1], tbmHeader, formattedRH)
        print " "
