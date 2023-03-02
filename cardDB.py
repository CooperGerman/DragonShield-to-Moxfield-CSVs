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
import json
import logging as log
import re
import time
from typing import Text
import colored_traceback.auto
import colored_traceback.always

global TIME
TIME = datetime.datetime.now()
class CardDB(object):
    '''
    CardDB class to hold card info
    attributes are:
        cards
    '''
    def __init__(self):
        '''
        Init DB list of Card objects
        '''
        self.cards = []

    def add(self, card):
        '''
        Add card to DB
        '''
        self.cards.append(card)

    def get_value(self):
        '''
        Get total value of cards in DB
        '''
        return sum([c.get_value() for c in self.cards])

    def find(self, card):
        '''
        Find card in DB
        '''
        for c in self.cards:
            if c == card:
                return c
        return None

    def get_cards_by_name(self, name):
        '''
        Get all cards with given name
        '''
        return [c for c in self.cards if c.name == name]

    def get_entries_by_type(self, type):
        '''
        Get all card entries with given type (card are merged if same name)
        '''
        res = []
        treated = []
        if not type.lower() in ['token', 'land', 'creature', 'artifact', 'enchantment', 'planeswalker', 'instant', 'sorcery']:
            raise ValueError('Type must be one of: token, land, creature, artifact, enchantment, planeswalker, instant, sorcery')
        if type.lower() == 'token':
            for c in self.cards:
                if (not c.name in treated) and ('token' in c.editionstr.lower()):
                    res.append(c)
                    treated.append(c.name)

        else:
            raise NotImplementedError('Other types not implemented yet')

        return res


    def get_cards_by_type(self, type):
        '''
        Get all cards with given type
        '''
        res = []
        if not type.lower() in ['token', 'land', 'creature', 'artifact', 'enchantment', 'planeswalker', 'instant', 'sorcery']:
            raise ValueError('Type must be one of: token, land, creature, artifact, enchantment, planeswalker, instant, sorcery')
        if type.lower() == 'token':
            for c in self.cards:
                if 'token' in c.editionstr.lower():
                    res.append(c)

        else:
            raise NotImplementedError('Other types not implemented yet')

        return res

    def update_prices(self, currency = 'usd'):
        '''
        iterate over all cards in DB and update price
        by getting price from card by using scryfall API
        '''
        for c in self.cards:
            c.update_price(currency = currency)

    def __repr__(self):
        return str(self.cards)

    def __str__(self):
        return str(self.cards)

    def __dict__(self):
        '''
        convert DB to dict with each element being a dict
        '''
        return {'cards' : [c.__dict__ for c in self.cards]}

    def to_mox(self):
        '''
        convert DB to moxfield format
        '''
        res = ['Count,Name,Edition,Condition,Language,Foil,Tag']
        for c in self.cards:
            res.append(c.to_mox())
        return '\n'.join(res)

    def to_archidekt(self):
        '''
        convert DB to archidekt format
        '''
        res = ['Count,Name,Edition,Condition,Language,Foil,Card number']
        for c in self.cards:
            res.append(c.to_archidekt())
        return '\n'.join(res)

    def to_manabox(self):
        '''
        convert DB to manabox format
        '''
        res = ['card name,quantity,set name,set code,foil,card number,language,condition,purchase price,purchase currency']
        for c in self.cards:
            res.append(c.to_manabox())
        return '\n'.join(res)

    def dump(self):
        '''
        Dump DB to JSON
        '''
        return json.dumps(self.cards, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Card(object):
    '''
    Card class to hold card info
    '''
    def __init__(self, name, edition, editionstr, card_number : int, condition, language, bdate : datetime, bprice, promo : bool, etched : bool, foil : bool, count : int, price, currency = 'usd'):
        '''
        en  | en | English             |
        es  | sp | Spanish             |
        fr  | fr | French              |
        de  | de | German              |
        it  | it | Italian             |
        pt  | pt | Portuguese          |
        ja  | jp | Japanese            |
        ko  | kr | Korean              |
        ru  | ru | Russian             |
        zhs | cs | Simplified Chinese  |
        zht | ct | Traditional Chinese |
        he  |    | Hebrew              |
        la  |    | Latin               |
        grc |    | AncientGreek        |
        ar  |    | Arabic              |
        sa  |    | Sanskrit            |
        ph  | ph | Phyrexian           |
        '''
        lang_lut = {
            'english' : 'en',
            'spanish' : 'es',
            'french' : 'fr',
            'german' : 'de',
            'italian' : 'it',
            'portuguese' : 'pt',
            'japanese' : 'ja',
            'korean' : 'ko',
            'russian' : 'ru',
            'simplified Chinese' : 'zhs',
            'traditional Chinese' : 'zht',
            'hebrew' : 'he',
            'latin' : 'la',
            'ancientgreek' : 'grc',
            'arabic' : 'ar',
            'sanskrit' : 'sa',
            'phyrexian' : 'ph',
        }
        '''
        #FIXME: This lookup table should be updated with corner case edition names that are not the same as the scryfall API
        For example, the scryfall API uses 'gk2' for 'gk2_rakdos' but the lookup table below uses 'gk2_rakdos'
        This table has been updated with empirically found corner cases
        '''
        ed_lut_patt = {
            'plgs'  : 'plg20',
            'gk2_*' : 'gk2',
            'gk1_*' : 'gk1',
            'veld'  : 'eld',
        }
        self.name = name
        self.card_number = card_number
        # iterate over lookup table and replace edition if needed by using regex pattern (as key)
        self.edition = edition.lower()
        for k, v in ed_lut_patt.items():
            if re.match(k, edition, re.IGNORECASE):
                self.edition = v.lower()

        self.editionstr = editionstr.lower()
        self.condition = condition
        self.language = lang_lut[language.lower()]
        self.bdate = bdate
        self.bprice = bprice

        self.foil = foil
        self.promo = promo
        self.etched = etched
        self.count = count
        self.price = price
        self.currency = currency
        self.alt_prc = False
        # if self.promo:
        #     self.edition = self.edition[1:]
    def get_value(self):
        '''
        Get value of card
        '''
        return self.price * self.count

    def update_price(self, currency = 'usd'):
        '''
        Update price of card by using scryfall API
        Search for exact card name, edition, language and foil
        '''
        import requests
        # search using this api /cards/:code/:number(/:lang)
        url = 'https://api.scryfall.com/cards/'+self.edition+'/'+self.card_number+'/'+self.language
        log.debug(url)
        # compare last TIME and now and verify at least 100ms have passed
        # if not, sleep for 100ms
        # this is to avoid hitting the rate limit of 10 requests per second
        # https://scryfall.com/docs/api
        global TIME
        if (datetime.datetime.now() - TIME).total_seconds() < 0.1:
            time.sleep(0.1)
        TIME = datetime.datetime.now()
        r = requests.get(url)

        self.currency = currency
        if r.status_code == 200:
            # check if we got a match
            if r.json()['object'] == 'error':
                log.warning('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                exit(1)
            price = r.json()['prices'][self.currency+('_etched' if self.etched else '_foil' if self.foil else '')]
            self.price = float(price) if price else None
        else:
            # search using this api /cards/:code/:number
            log.warning('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil) + ' trying without language')
            url = 'https://api.scryfall.com/cards/'+self.edition+'/'+self.card_number
            log.debug(url)
            # compare last TIME and now and verify at least 100ms have passed
            # if not, sleep for 100ms
            # this is to avoid hitting the rate limit of 10 requests per second
            # https://scryfall.com/docs/api
            if (datetime.datetime.now() - TIME).total_seconds() < 0.1:
                time.sleep(0.1)
            TIME = datetime.datetime.now()
            r = requests.get(url)

            if r.status_code == 200:
                # check if we got a match
                if r.json()['object'] == 'error':
                    log.warning('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                    exit(1)
                prices= r.json()['prices']
                if self.currency+('_etched' if self.etched else '_foil' if self.foil else '') in prices:
                    price = prices[self.currency+('_etched' if self.etched else '_foil' if self.foil else '')]
                else:
                    log.warning('No exact match found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil)+ 'in '+self.currency+('_etched' if self.etched else '_foil' if self.foil else '')+' using '+self.currency+' instead')
                    price = prices[self.currency]
                self.price = float(price) if price else None
                self.alt_prc = True
            else :
                log.critical('Error getting price for card: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                log.critical('Please check if the card is available on scryfall.com')
                log.critical('Search for "'+self.name+'" on : https://scryfall.com/')
                log.critical('-- Language might not be available for this card or edition mistake might have been made')
                log.critical('-- Set code might be wrong (correct convention are to be deducted from scryfall.com. Search your card and look at the resulting URL. Some codes contain ★ DragonSHield might export XXXetc card codes that do not seem supported.)')
                log.critical('-- Edition code might be wrong (correct convention are to be deducted from scryfall.com. Search your card and look at the resulting URL. Some codes from dragon shield like PLGS should be plg20.)')
                exit(1)

    def __eq__(self, other):
        '''
        Only matches if all attributes are equal (except count and price)
        '''
        # return (self.name == other.name and self.edition == other.edition and self.language == other.language and self.bdate == other.bdate and self.foil == other.foil)
        return (self.name == other.name and self.edition == other.edition and self.language == other.language and self.foil == other.foil)

    def __dict__(self):
        return {'name': self.name, 'edition': self.edition, 'condition': self.condition, 'language': self.language, 'foil': self.foil, 'promo': self.promo, 'etched': self.etched, 'count': self.count, 'price': self.price, 'currency': self.currency, 'alt_prc': self.alt_prc}

    def to_mox(self):
        cond_lut = {
                    'Mint'         : "M",
                    'NearMint'     : "NM",
                    'Excellent'    : "NM",
                    'Good'         : 'LP',
                    'Played'       : 'MP',
                    'LightPlayed'  : 'LP'
                    }
        # Count, Name, Edition, Condition, Language, Foil, <Tag>
        return (',').join([str(self.count), '"'+self.name+'"', self.edition.upper(), cond_lut[self.condition], self.language, 'foil' if self.foil else '""', '""'])

    def to_archidekt(self):
        cond_lut = {
                    'Mint'         : "M",
                    'NearMint'     : "NM",
                    'Excellent'    : "NM",
                    'Good'         : 'LP',
                    'Played'       : 'MP',
                    'LightPlayed'  : 'LP'
                    }
        # Count, Name, Edition, Condition, Language, Foil, <Tag>
        return (',').join([str(self.count), '"'+self.name+'"', self.edition.upper(), cond_lut[self.condition], self.language, 'foil' if self.foil else '""', self.card_number])

    def to_manabox(self):
        # card name,quantity,set name,set code,foil,card number,language,condition,purchase price,purchase currency
        return (',').join(['"'+self.name+'"', str(self.count), '"'+self.editionstr+'"', self.edition, 'foil' if self.foil else '', self.card_number, self.language, self.condition, str(self.price if self.price else 0.0), self.currency])
    def __repr__(self):
        return self.name + ' ' + self.edition + ' ' + self.condition + ' ' + self.language + ' ' + str(self.foil) + ' ' + str(self.count) + ' ' + str(self.price)

    def __str__(self):
        return self.name + ' ' + self.edition + ' ' + self.condition + ' ' + self.language + ' ' + str(self.foil) + ' ' + str(self.count) + ' ' + str(self.price)