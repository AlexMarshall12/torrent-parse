import datetime
import requests
import sys


version_check = sys.version_info[0]
if version_check == 2:
    print("This program was made for python3 only, sorry :-(")
    sys.exit()

minimum_seeds = 50
formats = []
qualities =[]
acceptable = {}

# thepiratebay.se: sorting by most seeds
# extratorrents.cc: sorting by movies category
# 1337x: sorting by most seeds

#torrent_sites = ["https://1337x.to/sort-search/{0}/seeders/desc/1/",
#                 "http://extratorrent.cc/search/?new=1&search={0}&s_cat=4",
#                 "https://isohunt.to/torrents/?ihq={0}&Torrent_sort=-seeders",
#                 "https://kat.cr/usearch/?q={0}",
#                 "https://thepiratebay.se/search/{0}/0/7/0",
#                 "https://torrentz.eu/search?q={0}"
#                ]

torrent_sites = ["https://1337x.to/sort-search/{0}/seeders/desc/1/",
                 "http://extratorrent.cc/search/?new=1&search={0}&s_cat=4",
                ]

searching = input("What do you want to search for?: ")
release_year = input("What year was it released? (or leave blank): ")

raw_torrent = []

first_torrent_links = []
second_torrent_links = []
third_torrent_links = []
fourth_torrent_links = []
fifth_torrent_links = []
sixth_torrent_links = []
acceptable_links = []

parsing_started = datetime.datetime.now().strftime('%H:%M:%S')
print("Loading, please wait... ( Started at {0} )".format(parsing_started))

try:
    for each in torrent_sites:
        replaced = each.replace("{0}", searching)
        raw = requests.get(replaced)
        raw_torrent.append(raw.text)
except Exception as e:
    print(e)

#
# 1337x
#

one_first_split = raw_torrent[0].split('<strong><a href=\"')

for each in one_first_split:
    if "</a></strong>" in each:
        # Links and titles
        one_second_split = each.split("</a></strong>")[0].replace(
                                         '<b>', '').replace('</b>', '').replace('/">', ' TITLE: ')

        one_seed_split = each.split("<div class=\"coll-2\"><span class=\"green\">")[1]
        one_seed_split2 = one_seed_split.split('</span></div>')[0]

        one_leech_split = each.split("<div class=\"coll-3\"><span class=\"red\">")[1]
        one_leech_split2 = one_leech_split.split('</span></div>')[0]

        one_size_split = each.split("<div class=\"coll-4\"><span>")[1]
        one_size_split2 = one_size_split.split('</span></div>')[0]

        first_torrent_links.append("{0} SEEDS: {1} LEECHES: {2} SIZE: {3}".format(
            one_second_split, one_seed_split2, one_leech_split2, one_size_split2))

for each in first_torrent_links:
    one_check_counter = 0
    if formats:
        for each_format in formats:
            if each_format.lower() in each.lower():
                one_check_counter += 1
    else:
        one_check_counter += 1

    if qualities:
        for each_qualities in qualities:
            if each_qualities.lower() in each.lower():
                one_check_counter += 1
    else:
        one_check_counter += 1

    if release_year in each.split(' TITLE: ')[1].split(' SEEDS: ')[0]:
        one_check_counter += 1
    elif release_year == '':
        one_check_counter += 1

    if minimum_seeds != 0:
        if minimum_seeds <= int(each.split(' TITLE: ')[1].split(' SEEDS: ')[1].split(' LEECHES: ')[0]):
            one_check_counter += 1

    if one_check_counter == 4:
        acceptable_links.append(each)

acceptable_counter = 0
for each in acceptable_links:

    # Link
    one_link = each.split(' TITLE: ')[0] + '/'

    one_url_split = torrent_sites[0].split('/')
    # Full Link
    one_full_url =  one_url_split[0] + '//' + one_url_split[2] + one_link

    one_magnet_list = []
    one_magnet_list2 = []
    try:
        raw_magnet = requests.get(one_full_url)
        one_magnet_list.append(raw_magnet.text)
    except Exception as e:
        print(e)

    for all_these in one_magnet_list:
        if "<a id=\"magnetdl\" href=\"" in all_these:
            one_magnet_split = all_these.split("<a id=\"magnetdl\" href=\"")
            one_magnet_split2 = one_magnet_split[1].split("\" onclick=\"javascript:return count(this);")
            one_magnet_list2.append(one_magnet_split2[0])

    # Title
    one_title = each.split(' TITLE: ')[1].split(' SEEDS: ')[0]
    # Seeds
    one_seed = each.split(' TITLE: ')[1].split(' SEEDS: ')[1].split(' LEECHES: ')[0]
    # Leeches
    one_leech = each.split(' SEEDS: ')[1].split(' LEECHES: ')[1].split(' SIZE: ')[0]
    # Size
    one_size = each.split(' LEECHES: ')[1].split(' SIZE: ')[1]

    acceptable[acceptable_counter] =  {"Title": one_title,
                                       "Link": one_full_url,
                                       "Seeds": one_seed,
                                       "Leeches": one_leech,
                                       "Size": one_size,
                                       "Magnet": one_magnet_list2
                                      }
    acceptable_counter += 1

#
# extratorrent.cc
#

print('')
if len(acceptable) != 1:
    for each in range(0, len(acceptable)-1):
        print('Title: {0}\nLink: {1}\nSeeds: {2}\nLeeches: {3}\nSize: {4}\nMagnet: {5}\n'.format(
               acceptable[each]['Title'], acceptable[each]['Link'],
               acceptable[each]['Seeds'], acceptable[each]['Leeches'],
               acceptable[each]['Size'], acceptable[each]['Magnet'][0]
             ))
else:
    for each in range(0, len(acceptable)):
        print('Title: {0}\nLink: {1}\nSeeds: {2}\nLeeches: {3}\nSize: {4}\nMagnet: {5}\n'.format(
               acceptable[each]['Title'], acceptable[each]['Link'],
               acceptable[each]['Seeds'], acceptable[each]['Leeches'],
               acceptable[each]['Size'], acceptable[each]['Magnet'][0]
             ))
