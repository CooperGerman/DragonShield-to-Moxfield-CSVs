#!/bin/python3

import argparse
import csv
import glob
import os


def run(args):

    #Create mox folder at the path given, make files easier to find
    moxoutputfolder =args.path + '/../mox'
    os.makedirs(moxoutputfolder, exist_ok=True)

    fils = glob.glob(args.path+'/*.csv', recursive=True)
    if not fils:
        print('No files found in ./'+args.path+'/*')
    for fil in fils:
        print('Converting '+fil)
        #utf-8 appears to allow decknames/filenames with special characters to process and not error
        f = open(fil, encoding='utf-8')
        lines = f.readlines()
        f.close()
        if 'Folder Name' in lines[1]:
            '''
            Folder Export case
            '''
            lines.pop(0)
            lines.pop(0)
            f = open('./tmp.csv', 'w')
            f.write(''.join(lines) )
            f.close()
            res = ['Count,Name,Edition,Condition,Language,Foil']

            cond_lut = {
                        'Mint'         : "M",
                        'NearMint'     : "NM",
                        'Excellent'    : "NM",
                        'Good'         : 'LP',
                        'Played'       : 'MP',
                        'LightPlayed'  : 'LP'
                        }

            # Folder Name(0), Quantity(1), Trade Quantity(2), Card Name(3), Set Code(4), Set Name(5), Card Number(6), Condition(7), Printing(8), Language(9), Price Bought(10), Date Bought(11), LOW(12), MID(13), MARKET(14)
            # --1--,--3--,  --5-- ,   --7--  ,   --9-- , --8--
            # Count, Name, Edition, Condition, Language, Foil, <Tag>

            with open('./tmp.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    # wrap card name in double quotes b/c some names have commmas included, this breaks import in Moxfield
                    res.append(row[1]+',"'+ row[3].replace('"','""') +'",'+row[5]+',' + cond_lut[row[7]]+','+row[9]+','+(row[8] if row[8] == 'Foil,' else '').lower()+',')
            f = open(moxoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_mox.csv', 'w')

        elif 'Card Type' in lines[1]:
            '''
            Deck Export case
            '''
            lines.pop(0)
            lines.pop(0)
            f = open('./tmp.csv', 'w')
            f.write(''.join(lines) )
            f.close()
            res = []

            # Card Type(0),Quantity(1),Card Name(2),Mana Cost(3),Min Price (MARKET) (4)
            # --1--,--2--
            # Qty Name

            with open('./tmp.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    if not 'Token' in row[2]:
                        res.append(row[1]+' '+row[2])
            f = open(moxoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0]) + '_mox.txt', 'w')
        else :
            raise Exception('Unrecognized csv format (allowed are Folder export and Deck export')
        f.write('\n'.join(res) )
        f.close()
        os.remove('tmp.csv')



def main():
    banner = '''This program is responsible for converting Dragonshield like csv files to readable Moxfield ones.'''
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog='DS2MOX_convert',
        description=banner,
        epilog='Convert Dragon shield to Moxfield.'
    )
    parser.add_argument(
        'path',
        type=str,
        default='',
        help='Path to input csv files '
    )
    args = parser.parse_args()

    print(banner)
    run(args)


if __name__ == '__main__':
	main()
