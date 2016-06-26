import datetime
import requests
import sys


version_check = sys.version_info[0]
if version_check == 2:
    print("This program was made for python3 only, sorry :-(")
    sys.exit()

minimum_seeds = 1
minimum_size = '100mb'
formats = [] # 'bluray', 
qualities = [] # '1080p' or '720p' for movies, or FLAC for music
acceptable = {}

# 1337x: sorted by most seeds
# extratorrents.cc: sorted by any category
# isohunt.to: sorted by most seeds
# kat.cr: sorted by most seeds
# thepiratebay.se: sort by most seeds
# torrentz.eu: sorted by peers

print("The more vague your search term is, the longer the program may take.")
print("Be sure to set format and quality within the program.")
searching = input("What do you want to search for?: ")
release_year = input("What year was it released? (or leave blank): ")

torrent_sites = ["https://1337x.to/sort-search/{0}/seeders/desc/1/",
                 "https://kat.cr/usearch/{0}/?field=seeders&sorder=desc",
                ]

raw_torrent_1 = []
raw_torrent = []
first_torrent_links = []
second_torrent_links = []
acceptable_links = []
acceptable_links2 = []

for each in torrent_sites:
    replaced = each.replace("{0}", searching)
    raw_torrent_1.append(replaced)

parsing_started = datetime.datetime.now().strftime('%H:%M:%S')
print("Loading, please wait... ( Started at {0} )".format(parsing_started))


def torrent_lookup(raw_number):
    try:
        raw1 = raw_number
        raw = requests.get(raw1)
        raw_torrent.append(raw.text)
    except Exception as e:
        print(e)


def validity(torrent_links_number, acceptable_type, qualities, release_year, minimum_seeds, minimum_size):
    for each in torrent_links_number:
        check_counter = 0
        if 'MAGNET' in each:
            without_magnet_each = each.split(' MAGNET: ')[0]
        else:
            without_magnet_each = each
        if formats:
            for each_format in formats:
                if each_format.lower() in without_magnet_each.lower():
                    check_counter += 1
        else:
            check_counter += 1

        if qualities:
            for each_qualities in qualities:
                if each_qualities.lower() in without_magnet_each.lower():
                    check_counter += 1
        else:
            check_counter += 1

        title_only = without_magnet_each.split(' LINK: ')[0].split(' SEEDS: ')[0].replace("TITLE: ", '')
        if release_year in title_only:
            check_counter += 1
        elif release_year == '':
            check_counter += 1

        if minimum_seeds:
            seeds_only = int(without_magnet_each.split(' SEEDS: ')[1].split(' LEECHES: ')[0])
            if minimum_seeds <= seeds_only:
                check_counter += 1

        if minimum_size:
            check_counter = size_check(without_magnet_each, minimum_size, check_counter)
        else:
            check_counter += 1

        if check_counter == 5:
            acceptable_type.append(each)


def size_check(each, minimum_size, check_counter):
    size_only = float(each.replace(',', '').split('SIZE: ')[1][:-2].rstrip())
    size_characters = each.split('SIZE: ')[1][-2:].rstrip().lower()
    minimum_characters = minimum_size[-2:].lower()
    minimum_size_only = float(minimum_size[:-2])

    if minimum_characters == 'tb':
        if size_characters == 'tb':
            if minimum_size_only <= size_only:
                check_counter += 1
        elif size_characters == 'gb':
            pass
        elif size_characters == 'mb':
            pass
        elif size_characters == 'kb':
            pass

    elif minimum_characters == 'gb':
        if size_characters == 'tb':
            check_counter += 1
        elif size_characters == 'gb':
            if minimum_size_only <= size_only:
                check_counter += 1
        elif size_characters == 'mb':
            pass
        elif size_characters == 'kb':
            pass

    elif minimum_characters == 'mb':
        if size_characters == 'tb':
            check_counter += 1
        elif size_characters == 'gb':
            check_counter += 1
        elif size_characters == 'mb':
            if minimum_size_only <= size_only:
                check_counter += 1
        elif size_characters == 'kb':
            pass

    elif minimum_characters == 'kb':
        if size_characters == 'tb':
            check_counter += 1
        elif size_characters == 'gb':
            check_counter += 1
        elif size_characters == 'mb':
            check_counter += 1
        elif size_characters == 'kb':
            if minimum_size_only <= size_only:
                check_counter += 1

    return check_counter


#############################
#        Start 1337x        #
#############################
def _1337x(raw_torrent, minimum_size):
    raw_number = raw_torrent_1[0]
    torrent_lookup(raw_number)
    one_first_split = raw_torrent[0].split('<strong><a href=\"')

    for each in one_first_split:
        if "</a></strong>" in each:
            # Links and titles
            one_second_split = each.split("</a></strong>")[0].replace(
                                          '<b>', '').replace(
                                          '</b>', '').replace(
                                          '/">', ' TITLE: ')

            one_seed_split = each.split("<div class=\"coll-2\"><span class=\"green\">")[1]
            one_seed_split2 = one_seed_split.split('</span></div>')[0]

            one_leech_split = each.split("<div class=\"coll-3\"><span class=\"red\">")[1]
            one_leech_split2 = one_leech_split.split('</span></div>')[0]

            one_size_split = each.split("<div class=\"coll-4\"><span>")[1]
            one_size_split2 = one_size_split.split('</span></div>')[0]

            one_link = each.split(' TITLE: ')[0].split("><b>")[0]

            first_torrent_links.append("{0} SEEDS: {1} LEECHES: {2} SIZE: {3}".format(
                one_second_split, one_seed_split2, one_leech_split2, one_size_split2))

    torrent_links_number = first_torrent_links
    acceptable_type = acceptable_links
    validity(torrent_links_number, acceptable_type, qualities, release_year, minimum_seeds, minimum_size)

    acceptable_counter = 0
    one_magnet_list = []
    for each in acceptable_type:
        # Link
        one_link = each.split(' TITLE: ')[0] + '/'
        # Full Link
        one_full_url =  'https://1337x.to' + one_link

        try:
            raw_magnet = requests.get(one_full_url)
            if "<title>Error</title>" not in raw_magnet.text:
                one_magnet_list.append(raw_magnet.text)
        except Exception as e:
            print(e)

        if one_magnet_list != []:
            for all_these in one_magnet_list:                
                if "<a id=\"magnetdl\" href=\"" in all_these:
                    one_magnet_split = all_these.split("<a id=\"magnetdl\" href=\"")[1]
                    one_magnet_split2 = one_magnet_split.split("\" onclick=\"javascript:return")[0]

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
                                                   "Download": one_magnet_split2
                                                  }
            acceptable_counter += 1
        else:
            return 0
    return acceptable_counter
#######################
#      End 1337x      #
#######################


###################################
#      Start kickasstorrents      #
###################################
def kickasstorrents(raw_torrent, minimum_size, counter):
    raw_number = raw_torrent_1[1]
    torrent_lookup(raw_number)
    four_first_split = raw_torrent[1].split('"Torrent magnet link" href="')

    four_magnet_list = []
    four_magnet_counter = 0

    for each in four_first_split:
        if '</td>\n\t\t\t</tr>\n\t\t\t\t\t\t' in each:
            four_link_split = each.split('<a href="')[1]
            four_link_split2 = four_link_split.split('" class="torType filmType"></a>')[0]

            four_title_split = each.split('class="cellMainLink">')[1].replace('<strong class="red">', '').replace('</strong>', '')
            four_title_split2 = four_title_split.split('</a>\n')[0].replace('</strong> <strong class="red">', '').replace('</strong>', '')

            # seeders
            four_seed_split = each.split('<td class="green center">')[1]
            four_seed_split2 = four_seed_split.split('</td>\n')[0]

            # leechers
            four_leech_split = each.split('<td class="red lasttd center">')[1]
            four_leech_split2 = four_leech_split.split('</td>\n\t\t\t</tr>')[0]

            # size
            four_size_split = each.split('<td class="nobr center">')[1].rstrip(' ')
            four_size_split2 = four_size_split.split('</span></td>')[0].replace(' <span>', '')

            four_magnet = each.split('" class="icon16"><i class="ka ka16 ka-magnet">')[0]
            four_magnet_list.append(four_magnet)

            fourth_torrent_links.append("TITLE: {0} LINK: {1} SEEDS: {2} LEECHES: {3} SIZE: {4} MAGNET: {5}".format(
                four_title_split2, four_link_split2, four_seed_split2, four_leech_split2, four_size_split2, four_magnet_list[four_magnet_counter]))

            four_magnet_counter += 1

    torrent_links_number = fourth_torrent_links
    acceptable_type = acceptable_links1
    validity(torrent_links_number, acceptable_type, qualities, release_year, minimum_seeds, minimum_size)

    for each in acceptable_type:
        four_link = each.split(' TITLE: ')[0] + '/'
        four_url_split = torrent_sites[2].split('/')
        # Full Link
        four_full_url = 'https://kat.cr' + each.split(' TITLE: ')[0].split(' LINK: ')[1].split(' SEEDS: ')[0] + '/'

        # Title
        four_title = each.split(' TITLE: ')[0].split(' LINK: ')[0].replace('TITLE: ', '').replace('\n', '')
        # Seeds
        four_seed = each.split(' SEEDS: ')[1].split(' LEECHES: ')[0]
        # Leeches
        four_leech = each.split(' LEECHES: ')[1].split(' SIZE: ')[0]
        # Size
        four_size = each.split(' LEECHES: ')[1].split(' SIZE: ')[1].split(' MAGNET: ')[0]
        # Magnet
        four_magnet = each.split(' MAGNET: ')[1]

        acceptable[counter] = {"Title": four_title,
                               "Link": four_full_url,
                               "Seeds": four_seed,
                               "Leeches": four_leech,
                               "Size": four_size,
                               "Download": four_magnet
                              }
        counter += 1
    return acceptable, counter
#################################
#      End kickasstorrents      #
#################################


counter = 0
if not counter:
    print('Trying 1337x')
    counter = _1337x(raw_torrent, minimum_size)
    if not counter:
        print('Trying KickAssTorrents')
        acceptable, counter = kickasstorrents(raw_torrent, minimum_size, counter)
        if not counter:
            print("Your search term has given no results")
            print("Revise your search and try again?")

print('')
try:
    for each in range(0, counter):
        print('Title: {0}'.format(acceptable[each]['Title']))
        print('Link: {0}'.format(acceptable[each]['Link']))
        print('Seeds: {0}'.format(acceptable[each]['Seeds']))
        print('Leeches: {0}'.format(acceptable[each]['Leeches']))
        print('Size: {0}'.format(acceptable[each]['Size']))
        print('Download: {0}'.format(acceptable[each]['Download']))
        print('')
except KeyError:
    pass
