#!/bin/python3
'''
██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗██╗███████╗██╗     ██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║███████╗███████║██║█████╗  ██║     ██║  ██║
██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║███████║██║  ██║██║███████╗███████╗██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝

██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
 ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝
'''
import argparse
import csv
import glob
import os
from cardDB import Card, CardDB

def run(args):

    #Create mox folder at the path given, make files easier to find
    moxoutputfolder =args.path + '/../results/mox'
    manaboxoutputfolder =args.path + '/../results/manabox'
    os.makedirs(moxoutputfolder, exist_ok=True)
    os.makedirs(manaboxoutputfolder, exist_ok=True)

    fils = glob.glob(args.path+'/*.csv', recursive=True)
    if not fils:
        print('No files found in ./'+args.path+'/*')
    for fil in fils:
        print('Converting '+fil)
        db = CardDB()
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

            # Folder Name(0), Quantity(1), Trade Quantity(2), Card Name(3), Set Code(4), Set Name(5), Card Number(6), Condition(7), Printing(8), Language(9), Price Bought(10), Date Bought(11), LOW(12), MID(13), MARKET(14)
            # --1--,--3--,  --5-- ,   --7--  ,   --9-- , --8--
            # Count, Name, Edition, Condition, Language, Foil, <Tag>

            with open('./tmp.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    # Split all elements in the row into local variables
                    folder = row[0]
                    quantity = row[1]
                    trade_quantity = row[2]
                    card_name = row[3]
                    set_code = row[4]
                    set_name = row[5]
                    card_number = row[6]
                    condition = row[7]
                    printing = row[8]
                    language = row[9]
                    price_bought = row[10]
                    date_bought = row[11]
                    low = row[12]
                    mid = row[13]
                    market = row[14]
                    # create an instance of the card as a Card object
                    tmp_card = Card(
                            name=card_name,
                            edition=set_code,
                            editionstr=set_name,
                            card_number=card_number,
                            condition=condition,
                            language=language,
                            # date format yyyy-mm-dd
                            bdate=date_bought,
                            bprice=price_bought,
                            promo=('s' in card_number or 'p' in card_number),
                            etched=(printing == 'Etched'),
                            foil=(printing == 'Foil'),
                            count=int(quantity),
                            price=(float(market) if market else None)
                        )
                    db.add(tmp_card)
            fmox = open(moxoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_mox.csv', 'w')
            fmanabox = open(manaboxoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_manabox.csv', 'w')
            fmox.write(db.to_mox())
            fmanabox.write(db.to_manabox())
            fmox.close()
            fmanabox.close()

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
            f.write(('\n'.join(res)))
            f.close()
        else :
            raise Exception('Unrecognized csv format (allowed are Folder export and Deck export')

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
