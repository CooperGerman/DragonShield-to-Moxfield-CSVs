# What am I ?

This repo contains some scripts the can be used in order to automate a Dragonshield collection export and upload the converted collection to Archidekt.
- `convert.py` aims at reformatting DragonSHield exported CSV files into Moxfield acceptable ones.
- `advanced_filtering.py` is a more advanced script that can filter the cards based on a list of cards you want to sell. This script uses minimum and maximum prices as well as the minimum number of instances for each card to determine if it should be included in the output.

# How to me ?
## convert.py
To use this tool simply put all your extracted csv files into a directory  and call the python file like follows.

```bash
python3 ./DS2MOX_convert.py <path to csv files folder>
```
This will generate folders for each output format (moxfield, manabox) and will put the converted files in them.

## advanced_filtering.py

This script is to be used alongside a moxfield exported csv file. It will filter the cards based on the minimum and maximum prices you set as well as the minimum number of instances you want to keep.

```bash
python3 ./DS2MOX_advanced_filtering.py <path to csv files folder>
    --min_price <minimum price for a card to be included> (default: 0.0)
        // choices : float
    --max_price <maximum price for a card to be included> (default: 'inf')
        // choices : float
    --min_instances <minimum number of instances for a card to be included> (default: 1)
        // choices : int
    --loglvl <log level> (default: INFO)
        // choices : DEBUG, INFO, WARNING, ERROR, CRITICAL, debug, info, warning, error, critical

```

Example :

```bash
python3 ./DS2MOX_advanced_filtering.py ./csv_files --min_price 0.5 --max_price 1.0 --min_instances 2
```
OUTPUT:


# Future improvements :
- [ ] Store a local database of cards to avoid having to interrogate scryfall each time
- [ ] Add a GUI
- [ ] Add a way to export the filtered cards to a moxfield database
- [ ] Add a way to export the filtered cards to a deckbox database
- [ ] Add a way to export the filtered cards to a manabox database