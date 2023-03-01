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
import datetime
global TIME
TIME = datetime.datetime.now()
import argparse
import csv
import glob
import os
from cardDB import *
import logging as log
import coloredlogs
from typing import Text
import colored_traceback.auto
import colored_traceback.always



def run(args):

    #Create mox folder at the path given, make files easier to find
    filtoutputfolder =args.path + '/../results/filt'
    cleanoutputfolder =args.path + '/../results/db'
    os.makedirs(filtoutputfolder, exist_ok=True)
    os.makedirs(cleanoutputfolder, exist_ok=True)

    fils = glob.glob(args.path+'/*.csv', recursive=True)
    if not fils:
        log.warning('No files found in ./'+args.path+'/*')
    for fil in fils:
        log.info('Cleaning '+fil)
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
            outstr = ['Count,Name,Edition,Condition,Language,Foil']
            db = CardDB()

            # Folder Name(0), Quantity(1), Trade Quantity(2), Card Name(3), Set Code(4), Set Name(5), Card Number(6), Condition(7), Printing(8), Language(9), Price Bought(10), Date Bought(11), LOW(12), MID(13), MARKET(14)
            # --1--,--3--,  --5-- ,   --7--  ,   --9-- , --8--
            # Count, Name, Edition, Condition, Language, Foil, <Tag>

            with open('./tmp.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    # wrap card name in double quotes b/c some names have commmas included, this breaks import in Moxfield
                    log.debug('Treating card: '+str(row[3]))
                    tmp_card = Card(
                            name=row[3],
                            edition=row[4],
                            editionstr=row[5],
                            card_number=row[6],
                            condition=row[7],
                            language=row[9],
                            # date format yyyy-mm-dd
                            bdate=row[11],
                            promo=('s' in row[6] or 'p' in row[6]),
                            etched=(row[8] == 'Etched'),
                            foil=(row[8] == 'Foil'),
                            count=int(row[1]),
                            price=(float(row[14]) if row[14] else None)
                        )
                    if not row[14] :
                        log.debug('Updating the price of as none has been found: '+str(tmp_card))
                        tmp_card.update_price()
                    if not db.find(tmp_card):
                        # If card was added after the
                        db.add(tmp_card)
                        log.debug('Adding new card to DB: '+str(tmp_card))
                    else :
                        db.find(tmp_card).count += int(row[1])
                        log.debug('Card already in DB, adding count to existing card: '+str(tmp_card)+ ' -> '+str(db.find(tmp_card).count))


            '''
            Dump db into json file
            '''
            f = open(cleanoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_db.json', 'w')
            f.write(db.dump())
            f.close()
            '''
            If filtering has been requested, filter the files
            '''
            if args.min_instances > 1 or args.min_price > 0.0 or args.max_price != 'inf':
                filt_db = CardDB()
                na_db = CardDB()
                # First update prices if requested currency is not USD
                if args.currency != 'usd':
                    db.update_prices()

                for c in db.cards:
                    if len(db.get_cards_by_name(c.name)) >= args.min_instances :
                        for fcard in db.get_cards_by_name(c.name):
                            log.debug('Filtering card: '+str(fcard))
                            if fcard.price:
                                # if fcard.price >= args.min_price:
                                #     filt_db.add(fcard)
                                filt_db.add(fcard)
                            else :
                                na_db.add(fcard)
                                log.warning('Card has no price, skipping: '+str(fcard))

                # dump filtered db into json file
                f = open(filtoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_filt_db.json', 'w')

                # keep only 2 decimals for total value
                value = int(filt_db.get_value()*100)/100

                f.write(
                        json.dumps({
                            'Header' : {
                                            'nb cards' : len(na_db.cards),
                                            'max value' : value,
                                            '60% resell vallue' : value*0.6,
                                            'currency' : args.currency.upper(),
                                        },
                            'content' : filt_db.__dict__()
                        }, indent=4))
                f.close()
                # print filter summary (nb of filtered cards, max value, 60% resell value)
                log.critical('Filtered cards: '+str(len(filt_db.cards)))
                log.critical('  -- Max value: '+str(value)+ ' ('+args.currency.upper()+')')
                log.critical('  -- 60% resell value: '+str(value*0.6) + ' ('+args.currency.upper()+')')


                if na_db.cards:
                    # dump non applicable db into json file
                    f = open(filtoutputfolder + "/" + (os.path.splitext(os.path.basename(fil))[0])+'_na_db.json', 'w')
                    f.write(
                        json.dumps({
                            'Header' : {
                                            'nb cards' : len(na_db.cards),
                                        },
                            'content' : na_db.__dict__()
                        }, indent=4))
                    f.close()
                    # print non applicable summary (nb of non applicable cards)
                    log.critical('Non applicable cards: '+str(len(na_db.cards)))
                    log.critical('  -- Estimated number of token entries: '+str(len(na_db.get_entries_by_type('token'))))

        elif 'Card Type' in lines[1]:
            '''
            Deck Export case
            '''
            log.warning('No cleaning available for decks yet. (skipping '+fil+')')
        else :
            raise Exception('Unrecognized csv format (allowed are Folder export and Deck export')

        #Remove tmp file
        os.remove('./tmp.csv')

    log.info('Done cleaning files')


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
    parser.add_argument(
        '--min_instances',
        type=int,
        default=1,
        help='Minimum instances of cards to be included in output'
    )
    parser.add_argument(
        '--min_price',
        type=float,
        default=0.0,
        help='Minimum price of cards to be included in output'
    )
    parser.add_argument(
        '--max_price',
        type=float,
        default='inf',
        help='Maximum price of cards to be included in output'
    )
    parser.add_argument(
        '--currency',
        type=str,
        default='usd',
        choices=['usd', 'eur', 'tix'],
        help='Currency to use for price filtering and/or updating'
    )
    parser.add_argument(
        '--loglvl',
        type=str,
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )
    loglvl = getattr(log, parser.parse_args().loglvl.upper())
    args = parser.parse_args()
    # configure logging with colored output
    # Create a logger object.
    logger = log.getLogger(__name__)

    # By default the install() function installs a handler on the root logger,
    # this means that log messages from your code and log messages from the
    # libraries that you use will all show up on the terminal.
    coloredlogs.install(level=args.loglvl)

    # If you don't want to see log messages from libraries, you can pass a
    # specific logger object to the install() function. In this case only log
    # messages originating from that logger will show up on the terminal.
    coloredlogs.install(level=args.loglvl, logger=logger)

    print(banner)
    run(args)


if __name__ == '__main__':
	main()
