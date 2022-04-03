#!/usr/bin/env python3
# -------------------------------------------------------------------------
# Custom Type Generation Script
# -------------------------------------------------------------------------

import ipsedixit
import random
import os
import sys

from datetime import date, timedelta


actions = """
Bitten Stung Befouled Tickled Tormented Tortured Bewitched Attacked
Assaulted Approached Prodded Pecked Nuzzled Burgled Hugged Injured
Eviscerated Licked Chased Oogled Robbed Pummeled Ambushed
Besmirched Nibbled Gnawed Idolized Worshipped Revered Befriended
Cuddled Demented Harried Investigated Judged Murdered Ravished Shamed
Tantalized Vanquished Devoured Swallowed Ravaged Overwhelmed Thrashed
Pummelled Assailed Ambushed Lambasted Pilloried Admonished Berated
Rebuked Impugned Harangued Vilified Roasted Rollicked Excoriated Applauded
Celebrated Acclaimed Honoured Adored Venerated Flatttered Blessed
""".split()


animals = """
Lionfish Spider Tarantula Scorpion Bulldog Rabbit Aardvark Sloth Horse
Pony Ant Beetle Centipede Bee Wasp Fly Ladybird Aphid Poodle Beagle
Dachshund Terrier Spaniel Collie Sheepdog Chihuahua Monkey Ape Gibbon
Shark Dolphin Goldfish Piranha Python Viper Rattlesnake Badger Deer
Moose Bear Fox Wolf Lion Tiger Elephant Crab Lobster Oyster Bison
Zebra Antelope Goat Bull Horse Sheep Chicken Duck Ostrich Emu Boar
Buck Jay Eagle Vulture Blackbird Thrush Starling Sparrow Baboon Chimp
Cobra Whale Monkfish Shark Alpaca Aardwolf Albatross Baboon Badger Bat Blackbird
Otter Tapir Hyena Lemur Pelican Crocodile Raven Starling Fox Capybara Caribou
Catfish Cheeta Chimpanzee Chipmunk Lizard Raccoon Wombat Partridge Cougar Coyote
Crab Mule Bustard Turtle Tortoise Dingo Dove Dragon Beaver Squirell Stork
Falcon Hawk Frog Anteater Possum Jackal Heron Gorilla Gazelle Owl Flamingo
Roadrunner Griffon Groundhog Hedgehog Lark Sparrow Ibis Peacock Kangaroo
Vulture Pigeon Mouse Llama Loris Macaw Manatee Meerkat Alligator Mongoose Crocodile
Ocelot Ostrich Pelican Penguin Kingfisher Rattlesnake Toucan Cockatoo Warthog
Wildebeest Wombat Woodpecker
""".split()


tags = """
red green blue orange yellow pink purple violet brown grey lilac crimson
indigo jade
""".split()


authors = [
    "John Doe",
    "Jane Doe",
    "Jake Doe",
    "Jill Doe",
]


template = """\
---
title: %(title)s
author: %(author)s
date: %(date)s
tags: %(tags)s
image: animalia/image-%(image)02d.jpg
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
        action = random.choice(actions)
        animal = random.choice(animals)
        article = 'an' if animal[0].lower() in 'aeiou' else 'a'

        title = "%s by %s %s" % (action, article, animal)
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

    dirpath = dstdir
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, '%s.stx' % data['slug'])
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(template % data)
