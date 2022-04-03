#!/usr/bin/env python3
# -------------------------------------------------------------------------
# Post Generation Script
# -------------------------------------------------------------------------

import ipsedixit
import random
import os
import sys

from datetime import date, timedelta


activities = """
Hiking Fishing Shopping Shoplifting Clubbing Dancing Drinking Sightseeing
Hunting Eating Stranded Kidnapped Murdered Mugged Pickpocketing Skiing
Swimming Sunbathing Surfing Flashing Fighting Robbed Engaged Married
Lost Abandoned Pickpocketed Mountaineering Trekking Besmirched
Drunk Alone Studying Reading Enthroned Insulted Astonished Waterboarded
Assaulted Bewildered Happy Triumphant Bicycling Crofting Spying Dreadnoughts
Battleships Camping Driving Desperate Fireships
Fireworks Chaos Hillwalking Interrogated Crackpots Curfew Languishing
Mortified Moustachioed Nonsense Orphaned Petrified Peppercorns
Potholing Periwinkling Driving Mythmaking Mythologised Remembered Confused Condemned
Underwhelmed Vanquished Woebegone Puzzled Perplexed Baffled Stumped Mystified
Befuddled Dumbfounded Discombobulated Dazed Bamboozled Libeled Slandered Maligned Defamed
Spurned Astounded Thunderstruck Awed Wonderstruck Flummoxed Flabbergasted Gobsmacked
Vexed Indignant Irked Galled Outraged Apoplectic Merry Exultant Rapturous Blithe
Renounced Disavowed Axed Forsaken Disavowed Eschewed Mollycoddled Cosseted
Explosions Riots Protests Uproar Anarchy Berserkers Misrule Insurrection Rebellion
Mutiny Pandemonium Mayhem Celebrating Carousing Bingeing Debauchery Shameless Lechery
Indulged Dissolute Louche Regretful Repentant Rueful Shamefaced Desolate
Forlorn Crestfallen Woeful Woebegone Doleful
""".split()


ireland = """
Dublin Dundalk Clonmel Cork Galway Waterford Wexford Belfast Kerry Kilkenny
Limerick Leitrim Roscommon Tipperary Athlone Newry Drogheda Louth Tralee
Portlaoise Derry Tyrone Carrickfergus Donegal Mayo Armagh Slane Lucan Boyle
Tullamore Skibbereen Crookhaven Glengarriff Kenmare Bearhaven Listowel Blarney
Cobh Fermoy Carlow Tramore Enniscorthy Arklow Wicklow Bray Athy Howth Malahide
Lucan Naas Kildare Navan Slane Dunleer Termonfeckin Inniskeen Carrickmacross
Carlingford Newry Castleblayney Lisburn Letterkenny Bundoran Killybegs Westport
""".split()


england = """
London Manchester Liverpool Kent Sheffield Essex Cornwall Hull York Durham
Newcastle Devon Norfolk Birmingham Oxford Cambridge Bognor Brighton Blackpool
Grantham Nottingham Derby Wrexham Chester Swindon Winchester Chelmsford Colchester
Norwich Ipswich Canterbury Brighton Cheltenham Portsmouth Taunton Bristol Glastonbury
Plymouth Falmouth Barnstaple Leeds Scunthorpe Scarborough Hartlepool Carlisle Lancaster

""".split()


scotland = """
Glasgow Edinburgh Aberdeen Dundee Hamilton Inverness Stirling Falkirk
Dumfries Arbroath Elgin Larkhall Montrose Berwick Dunblane Paisley Galloway
Lockerbie Stranraer Dunblane Aberfeldy Dalwhinnie Dunbarton Kilmarnock Freswick
""".split()


wales = """
Cardiff Swansea Cwmbran Llanelli Caerphilly Pontypridd Aberdare Rhyl
Maesteg Aberystwyth Caernarfon Cardigan Hereford Carmarthen Pembroke Anglesey
Bangor Rhyl Pwlheli Llanrwst Harlech Aberporth Caerphilly Pontypool Talgarth
""".split()


tags = """
red green blue orange yellow pink purple violet brown grey lilac crimson
indigo jade
""".split()


authors = [
    "John Doe",
    "Jane Doe",
]


locations = {
    'ireland': ireland,
    'england': england,
    'scotland': scotland,
    'wales': wales,
}


template = """\
---
title: %(title)s
author: %(author)s
date: %(date)s
tags: %(tags)s
image: blog/image-%(image)02d.jpg
---

%(content)s
"""


start_date = date(1798, 1, 1)
generator = ipsedixit.Generator()
titles = []


if len(sys.argv) > 1:
    dstdir = sys.argv[1]
else:
    sys.exit("Error: you must specify a destination directory.")


for i in range(365):

    while True:
        activity = random.choice(activities)
        country = random.choice(list(locations.keys()))
        location = random.choice(locations[country])

        title = "%s in %s" % (activity, location)

        if title not in titles:
            titles.append(title)
            break

    data = {
        'title': title,
        'author': random.choice(authors),
        'date': str(start_date + timedelta(i)),
        'tags': ', '.join(random.sample(tags, random.randint(2, 4))),
        'content': '\n\n'.join(generator.paragraphs(4, max=3)),
        'slug': title.lower().replace(' ', '-'),
        'image': random.randint(1, 30),
    }

    dirpath = os.path.join(dstdir, country)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, '%s.stx' % data['slug'])
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(template % data)
