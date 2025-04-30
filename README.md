# Daniel Gaskills Windows Registry Explorer Path Finder

## Description
I created this program to be a helpful tool when conducting a forensic analysis using Eric Zimmermans Windows Registry Explorer. My tool is a fast way to look up the path to a registry key without having to use the internet. Currently it is only applicable for Windows 10. The tool uses SQLite to store data. You have the option to use my default .db file, which comes with about 20 paths. You can also give it your own .db file if you have one already, or you can use my script "db_creator.py" which will take a json file and create a .db file for you. Just make sure you follow the correct format that it accepts. Here is an example line:
```
{ "key_name": "recentdocs", "hive": "NTUSER.DAT", "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs", "description": "Recently accessed folders, executables, documents, pluggable devices, etc." },
```
## Directions
You will need to have python installed on your windows 10 machine which can be a little tricky so I will include a link to a [youtube video](https://www.youtube.com/watch?v=IPOr0ran2Oo)

Once you have python installed you can just download the zipfile, extract it and double click on path_finder.py and your GUI will open up. Also if you want to create your own .db file just double click db_creator.py and you will be prompted with directions. Just remember you need a json file on hand.
