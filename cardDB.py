#!/usr/bin/env python3
import json
import logging as log
from typing import Text
import colored_traceback.auto
import colored_traceback.always

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

    def dump(self):
        '''
        Dump DB to JSON
        '''
        return json.dumps(self.cards, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Card(object):
    '''
    Card class to hold card info
    attributes are:
        name
        edition
        condition
        language
        foil
        count
        price
        currency
    '''
    def __init__(self, name, edition, card_number : int, condition, language, promo : bool, etched : bool, foil : bool, count : int, price, currency = 'usd'):
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
        self.name = name
        self.card_number = card_number
        self.edition = edition.lower()
        self.condition = condition
        self.language = lang_lut[language.lower()]

        self.foil = foil
        self.promo = promo
        self.etched = etched
        self.count = count
        self.price = price
        self.currency = currency
        self.alt_prc = False
        # if self.promo:
        #     self.edition = self.edition[1:]

    def update_price(self, currency = 'usd'):
        '''
        Update price of card by using scryfall API
        Search for exact card name, edition, language and foil
        '''
        import requests
        # search using this api /cards/:code/:number(/:lang)
        url = 'https://api.scryfall.com/cards/'+self.edition+'/'+self.card_number+'/'+self.language
        log.debug(url)
        r = requests.get(url)
        if r.status_code == 200:
            # check if we got a match
            if r.json()['object'] == 'error':
                log.warning('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                exit(1)
            price = r.json()['prices'][currency+('_etched' if self.etched else '_foil' if self.foil else '')]
            self.price = float(price) if price else None
            self.currency = currency
        else:
            # search using this api /cards/:code/:number
            log.info('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil) + ' trying without language')
            url = 'https://api.scryfall.com/cards/'+self.edition+'/'+self.card_number
            log.debug(url)
            r = requests.get(url)
            if r.status_code == 200:
                # check if we got a match
                if r.json()['object'] == 'error':
                    log.warning('No card found for: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                    exit(1)
                price = r.json()['prices'][currency+('_etched' if self.etched else '_foil' if self.foil else '')]
                self.price = float(price) if price else None
                self.currency = currency
                self.alt_prc = True
            else :
                log.critical('Error getting price for card: ' + self.name + ' ' + self.edition + ' ' + self.language + ' ' + str(self.foil))
                log.critical('Please check if the card is available on scryfall.com')
                log.critical('Search for '+self.name+' on : https://scryfall.com/')
                log.critical('-- Language might not be available for this card or edition mistake might have been made')
                exit(1)

    def __eq__(self, other):
        '''
        Only matches if all attributes are equal (except count and price)
        '''
        return (self.name == other.name and self.edition == other.edition and self.language == other.language and self.foil == other.foil)

    def __repr__(self):
        return self.name + ' ' + self.edition + ' ' + self.condition + ' ' + self.language + ' ' + str(self.foil) + ' ' + str(self.count) + ' ' + str(self.price)

    def __str__(self):
        return self.name + ' ' + self.edition + ' ' + self.condition + ' ' + self.language + ' ' + str(self.foil) + ' ' + str(self.count) + ' ' + str(self.price)