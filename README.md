# Library
download, convert and send books from LibGen so you can read and listen to them right away!

Search through terminal Library Genesis, have any book converted to mobi and epub to then be directly sent to your google drive and your kindle. 
This will allow you to read the book immediately and have it read to you.
using an ereader with inbuilt text-to-spech you can uplaod files from google drive directly to your text to speech reader.
I use VoiceDream which comes with the Australian voice Lisa.
see here: https://www.acapela-group.com/demos/
select English AU and Lisa

Voice Dream does cost but IMO very worth it. it enables any book I get to be read to me at a rate I choose with a voice I can bear. I am in no way affiliated with these companies, I just havent come across anything free that does what I'm after. Let me know if there is something better.

This code will need to be personalised to your OS as well as a new google account set up. I have created a step by step instructions that will take you through everything.

To use once set up, simply go to the file location in terminal
$ cd /users/yourname/library/
and run the lib.py file
$python lib.py

you will need to install and update a few packages. this can be done through pip

$pip install json
$pip install requests
$pip install oauth2client
$pip install bs4
$pip install re

Happy reading! or even, happy listening!
