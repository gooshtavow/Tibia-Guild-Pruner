# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from guildchecker.items import GuildcheckerItem

class GuildcheckSpider(scrapy.Spider):
    name = 'guildcheck'
    allowed_domains = ['tibia.com']
    time_now = datetime.today()

    guild_name = input('Enter the guild name (case sensitive): ')
    guild_name = guild_name.replace(' ', '+')

    days_inactive = int(input('Enter the maximum number of days a character can be inactive: '))

    ranks = []
    rank = ""

    print('Enter the ranks that won\'t be taken into consideration. Type FINISH when done. Also case sensitive.')
    while 'FINISH' not in ranks:
        rank = str(input('> '))
        if rank not in ranks:
            ranks.append(rank)
        else:
            print('Rank already inserted.')

    start_urls = ['https://www.tibia.com/community/?subtopic=guilds&page=view&GuildName=' + guild_name]

    characters_flagged = []

    # clear output json file
    file = open("characters.json", "w")
    file.close()

    # First function called by scrapy, goes to self.start_urls
    def parse(self, response):
        # Find the character page link for all of the characters in the guild.
        characterpage_links = response.xpath('//*[@class="TableContent"]/tr/td[2]/a/@href').extract()

        # Calls self.parse_characters to visit all those links and parse their content
        for item in characterpage_links:
            yield scrapy.Request(url=item, callback=self.parse_characters)

    def parse_characters(self, response):
        # Creates an instance of the class defined in ../items.py
        character = GuildcheckerItem()

        # Extract all of the character's information and builds a list with it
        char_info = response.xpath('//*[@class="BoxContent"]/table[1]/tr/td[2]/text()').extract()

        # Parse the list and extract what we want
        character['name'] = char_info[0][:-1]
        has_lastlogin = False
        has_rank = False
        for field in char_info:
            if (('CET' in field) or ('CEST' in field)) and not has_lastlogin:
                last_login = datetime.strptime(field[0:11], "%b %d %Y")
                character['last_login'] = last_login
                delta = self.time_now - last_login
                if delta.days < 0:
                    character['days_offline'] = 0
                else:
                    character['days_offline'] = delta.days
                has_lastlogin = True
            elif ' of the ' in field and not has_rank:
                character['rank'] = field.rsplit(' of the ')[0]
                has_rank = True

        # Checks if the character has logged in in the past X days, where X has been defined by the user at runtime.
        # If not, flags it to be written in the output .txt file
        if int(character['days_offline']) >= self.days_inactive and character['rank'] not in self.ranks:
            self.characters_flagged.append(character['name'] + ", " + character['rank'] + ", " + str(character['days_offline']) + " days.")

        # "Returns" the character info
        yield character

    # Executed after the crawler is done visiting all the links (or found any error).
    # Creates the 'flagged_characters.txt' file, which contains the names, ranks and days of inactivity of every
    # character to be kicked
    def closed(self, reason):
        flaggedcharacters = open("flagged_characters.txt", "w")
        for item in self.characters_flagged:
            flaggedcharacters.write(item + "\n")
        flaggedcharacters.close()