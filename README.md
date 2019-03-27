# Tibia Guild Pruner

Since CipSoft's guild web page lacks quite a few functionalities, this program intended to automate the process of kicking a lot of people from the guild you're in, based on their rank and the number of days they have been inactive.

## Prerequisites

To run this program, you will need (the versions below are the ones that were tested, others may very well work too):

* Python 3.7 with the following libraries:
    * [Scrapy](https://scrapy.org/)* 1.5.2
    * [Selenium](https://www.seleniumhq.org/) 3.141.0
* Google Chrome** 73.0
* [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)** 73.0
 
*Scrapy installation could be a little complicated. If you wish to make it way simpler, install [Anaconda](https://www.anaconda.com/distribution/), then install Scrapy (and Selenium) in it and use its prompt.

**You can also use other browsers, as long as you have them installed, download their driver and change the webdriver in ./guildpruner.py accordingly.

## How does it work?
There are two programs to be executed here (instructions below). The first one, guildcheck, will visit your guild's page and then visit the pages of all the characters in it, collecting their name, rank within the guild and last login date. It will also create a text file called `flagged_characters.txt`, which will contain the names, ranks and number of days offline of those characters that haven't logged in over the last D days and are not in the R ranks, where D and R are defined by the user at runtime.

The second program, guildpruner, will effectively kick those people out of the guild. It runs an automated instance of Chrome, where it will log in on tibia.com, navigate to your guild's page and then kick every character listed in `flagged_characters.txt`.



## Usage
1. Navigate to the ./guildchecker folder and run the following command: `scrapy crawl guildcheck [-o characters.json]`. The part inside the brackets is optional, if used it will create a file named `characters.json` in the current folder, containing the names, ranks, last login date and number of days offline for every character in the guild.
2. The program will then ask for your guild's name. You must enter the guild's name exactly as it is, letter cases are important! For example, if your guild is called 'Redd **A**lliance' and you write 'Redd **a**lliance', the program won't find it.
3. Now the program will ask the number of days a character can be offline before being flagged for removal. You must enter an integer number here.
4. Lastly, it will ask which ranks you want to ignore. In other words, people in the rank(s) listed here won't be flagged. This is useful when you're the leader of a guild and don't want to kick the vice leaders who haven't logged in for more than the number of days you chose, for example. Type in the names of the ranks exactly as they are (like the guild's name, this is also case sensitive) and then type 'FINISH' when you're done. You can also type 'FINISH' without inserting any ranks, in case you want to kick people regardless of their ranks.
5. The program will now run (it will take a while if your guild is big) and create the `flagged_characters.txt` file in the ./guildchecker folder. Leave it there.
6. Now navigate to the ./guildpruner folder and run `python guildpruner.py`. It will fail to start if the text file is not present in the other folder.
7. The program will ask for your guild's name again. And it is, surprise surprise, case sensitive.
8. After entering the guild's name, the program will now start an automated instance of Google Chrome. **DO NOT TOUCH THIS BROWSER!** It will firstly visit tibia.com login page, where you must enter your account number and password, as requested by the program. Again, keep entering the information in the program window, and NOT the browser's window.
9. (optional) If you have an authenticator bound to your account, it will then ask for an access token.
10. The program now will visit your guild's "Edit Members" page and start kicking those characters present in the text file created in step 5. Enjoy the process of kicking lots of people without touching your mouse and keyboard!

Note: This program isn't (yet?) protected against bad input. You can enter whatever you want when it asks you for information, so it is up to you to enter the correct information to get correct results. It's your guild, your account and your connection you're using when you run it, so there's no point in entering bad information on purpose.