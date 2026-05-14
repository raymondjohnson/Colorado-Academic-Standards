#!/usr/bin/python3
import requests, sys, time, random
from bs4 import BeautifulSoup
from markdownify import markdownify as md

content_lookup = sys.argv[1]
content_abbreviation = sys.argv[1][:2]
content_year = sys.argv[1][2:]
filecount = 2

# ====== DOWNLOADER ====== #

## A data dictionary keeps lists of all the URLs for each content area
url_lookup = {
    'CH2018': [
        'https://www.cde.state.co.us/apps/standards/3,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/3,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/3,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/3,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/3,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/3,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/3,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/3,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/3,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/3,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/3,15,0' # High School
    ],
    'CS2018': [
        'https://www.cde.state.co.us/apps/standards/12,15,0' # High School
    ],
    'CS2024': [
        'https://www.cde.state.co.us/apps/standards/60012,60002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/60012,60003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/60012,60004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/60012,60005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/60012,60006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/60012,60007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/60012,60038,0', # Middle School
        'https://www.cde.state.co.us/apps/standards/60012,60015,0' # High School
    ],
    'DA2018': [
        'https://www.cde.state.co.us/apps/standards/1,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/1,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/1,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/1,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/1,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/1,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/1,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/1,8,0', # Novice
        'https://www.cde.state.co.us/apps/standards/1,9,0', # Emerging
        'https://www.cde.state.co.us/apps/standards/1,10,0', # Intermediate
        'https://www.cde.state.co.us/apps/standards/1,17,0', # Proficient
        'https://www.cde.state.co.us/apps/standards/1,16,0' # Exemplary
    ],
    'DA2022': [
        'https://www.cde.state.co.us/apps/standards/30001,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30001,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30001,30003,0', # First grade
        'https://www.cde.state.co.us/apps/standards/30001,30004,0', # Second grade
        'https://www.cde.state.co.us/apps/standards/30001,30005,0', # Third grade
        'https://www.cde.state.co.us/apps/standards/30001,30006,0', # Fourth grade
        'https://www.cde.state.co.us/apps/standards/30001,30007,0', # Fifth grade
        'https://www.cde.state.co.us/apps/standards/30001,30043,0', # Novice
        'https://www.cde.state.co.us/apps/standards/30001,30047,0', # Emerging
        'https://www.cde.state.co.us/apps/standards/30001,30044,0', # Intermediate
        'https://www.cde.state.co.us/apps/standards/30001,30045,0', # Proficient
        'https://www.cde.state.co.us/apps/standards/30001,30048,0' # Exemplary
    ],
    'DT2018': [
        'https://www.cde.state.co.us/apps/standards/2,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/2,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/2,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/2,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/2,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/2,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/2,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/2,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/2,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/2,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/2,17,0', # High School - Fundamental Pathway
        'https://www.cde.state.co.us/apps/standards/2,27,0', # High School - Advanced Pathway
        'https://www.cde.state.co.us/apps/standards/2,39,0' # High School - Professional Pathway
    ],
    'DT2022': [
        'https://www.cde.state.co.us/apps/standards/30002,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30002,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30002,30003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/30002,30004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30002,30005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30002,30006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30002,30007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30002,30008,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/30002,30009,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/30002,30010,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/30002,30017,0', # High School - Fundamental Pathway
        'https://www.cde.state.co.us/apps/standards/30002,30027,0', # High School - Advanced Pathway
        'https://www.cde.state.co.us/apps/standards/30002,30039,0' # High School - Professional Pathway
    ],
    'FL2018': [
        'https://www.cde.state.co.us/apps/standards/8,1,45', # Preschool
        'https://www.cde.state.co.us/apps/standards/8,2,45', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/8,3,45', # First Grade
        'https://www.cde.state.co.us/apps/standards/8,4,45', # Second Grade
        'https://www.cde.state.co.us/apps/standards/8,5,45', # Third Grade
        'https://www.cde.state.co.us/apps/standards/8,6,45', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/8,7,45', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/8,8,45', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/8,9,45', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/8,10,45', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/8,15,45' # High School
    ],
    'FL2022': [
        'https://www.cde.state.co.us/apps/standards/30008,30001,30045', # Preschool
        'https://www.cde.state.co.us/apps/standards/30008,30002,30045', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30008,30003,30045', # First Grade
        'https://www.cde.state.co.us/apps/standards/30008,30004,30045', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30008,30005,30045', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30008,30006,30045', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30007,30045', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30008,30045', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30009,30045', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/30008,30010,30045', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30015,30045' # High School
    ],
    'MA2018': [
        'https://www.cde.state.co.us/apps/standards/4,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/4,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/4,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/4,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/4,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/4,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/4,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/4,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/4,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/4,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/4,15,0' # High School
    ],
    'MU2018': [
        'https://www.cde.state.co.us/apps/standards/5,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/5,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/5,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/5,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/5,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/5,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/5,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/5,31,0', # Sixth Grade/Novice
        'https://www.cde.state.co.us/apps/standards/5,32,0', # Seventh Grade/Intermediate
        'https://www.cde.state.co.us/apps/standards/5,33,0', # Eighth Grade/Proficient
        'https://www.cde.state.co.us/apps/standards/5,34,0', # High School/Accomplished
        'https://www.cde.state.co.us/apps/standards/5,35,0' # High School/Advanced
    ],
    'MU2022': [
        'https://www.cde.state.co.us/apps/standards/30005,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30005,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30005,30003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/30005,30004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30005,30005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30005,30006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30005,30007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30005,30043,0', # Novice
        'https://www.cde.state.co.us/apps/standards/30005,30044,0', # Intermediate
        'https://www.cde.state.co.us/apps/standards/30005,30045,0', # Proficient
        'https://www.cde.state.co.us/apps/standards/30005,30046,0' # Accomplished
    ],
    'PE2018': [
        'https://www.cde.state.co.us/apps/standards/11,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/11,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/11,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/11,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/11,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/11,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/11,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/11,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/11,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/11,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/11,15,0' # High School
    ],
    'PE2024': [
        'https://www.cde.state.co.us/apps/standards/11,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/11,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/11,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/11,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/11,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/11,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/11,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/11,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/11,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/11,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/11,15,0' # High School
    ],
    'RW2018': [
        'https://www.cde.state.co.us/apps/standards/6,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/6,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/6,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/6,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/6,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/6,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/6,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/6,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/6,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/6,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/6,30,0', # Ninth / Tenth Grade Band
        'https://www.cde.state.co.us/apps/standards/6,29,0' # Eleventh / Twelfth Grade Band
    ],
    'RW2026': [
        'https://www.cde.state.co.us/apps/standards/6,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/6,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/6,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/6,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/6,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/6,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/6,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/6,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/6,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/6,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/6,30,0', # Ninth / Tenth Grade Band
        'https://www.cde.state.co.us/apps/standards/6,29,0' # Eleventh / Twelfth Grade Band
    ],
    'SC2026': [
        'https://www.cde.state.co.us/apps/standards/7,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/7,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/7,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/7,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/7,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/7,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/7,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/7,38,0', # Middle School
        'https://www.cde.state.co.us/apps/standards/7,15,0' # High School
    ],
    'SC2018': [
        'https://www.cde.state.co.us/apps/standards/30007,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30007,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30007,30003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/30007,30004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30007,30005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30007,30006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30007,30007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30007,30038,0', # Middle School
        'https://www.cde.state.co.us/apps/standards/30007,30015,0' # High School
    ],
    'SS2018': [
        'https://www.cde.state.co.us/apps/standards/8,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/8,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/8,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/8,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/8,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/8,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/8,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/8,8,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/8,9,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/8,10,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/8,15,0' # High School
    ],
    'SS2022': [
        'https://www.cde.state.co.us/apps/standards/30008,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30008,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30008,30003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/30008,30004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30008,30005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30008,30006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30008,0', # Sixth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30009,0', # Seventh Grade
        'https://www.cde.state.co.us/apps/standards/30008,30010,0', # Eighth Grade
        'https://www.cde.state.co.us/apps/standards/30008,30015,0' # High School
    ],    
    'VA2018': [
        'https://www.cde.state.co.us/apps/standards/9,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/9,2,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/9,3,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/9,4,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/9,5,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/9,6,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/9,7,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/9,8,0', # Middle School 1
        'https://www.cde.state.co.us/apps/standards/9,9,0', # Middle School 2
        'https://www.cde.state.co.us/apps/standards/9,10,0', # Middle School 3
        'https://www.cde.state.co.us/apps/standards/9,15,0' # High School
    ],
    'VA2022': [
        'https://www.cde.state.co.us/apps/standards/30009,30001,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/30009,30002,0', # Kindergarten
        'https://www.cde.state.co.us/apps/standards/30009,30003,0', # First Grade
        'https://www.cde.state.co.us/apps/standards/30009,30004,0', # Second Grade
        'https://www.cde.state.co.us/apps/standards/30009,30005,0', # Third Grade
        'https://www.cde.state.co.us/apps/standards/30009,30006,0', # Fourth Grade
        'https://www.cde.state.co.us/apps/standards/30009,30007,0', # Fifth Grade
        'https://www.cde.state.co.us/apps/standards/30009,30040,0', # Middle School 1
        'https://www.cde.state.co.us/apps/standards/30009,30041,0', # Middle School 2
        'https://www.cde.state.co.us/apps/standards/30009,30042,0', # Middle School 3
        'https://www.cde.state.co.us/apps/standards/30009,30015,0' # High School
    ],
    'WL2018': [
        'https://www.cde.state.co.us/apps/standards/10,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/10,21,0', # Novice-Low
        'https://www.cde.state.co.us/apps/standards/10,22,0', # Novice-Mid
        'https://www.cde.state.co.us/apps/standards/10,20,0', # Novice-High
        'https://www.cde.state.co.us/apps/standards/10,23,0', # Intermediate-Low
        'https://www.cde.state.co.us/apps/standards/10,24,0', # Intermediate-Mid
        'https://www.cde.state.co.us/apps/standards/10,36,0', # Intermediate-High
        'https://www.cde.state.co.us/apps/standards/10,37,0' # Advanced-Low
    ],
    'WL2024': [
        'https://www.cde.state.co.us/apps/standards/10,1,0', # Preschool
        'https://www.cde.state.co.us/apps/standards/10,21,0', # Novice-Low
        'https://www.cde.state.co.us/apps/standards/10,22,0', # Novice-Mid
        'https://www.cde.state.co.us/apps/standards/10,20,0', # Novice-High
        'https://www.cde.state.co.us/apps/standards/10,23,0', # Intermediate-Low
        'https://www.cde.state.co.us/apps/standards/10,24,0', # Intermediate-Mid
        'https://www.cde.state.co.us/apps/standards/10,36,0', # Intermediate-High
        'https://www.cde.state.co.us/apps/standards/10,37,0' # Advanced-Low
    ]
}

## Fetching content from the web page with a custom user agent and a delay to avoid overwhelming the server. ##
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
})

def get_page(url):
    response = session.get(url)
    response.raise_for_status()  # throws an error on 4xx/5xx responses    
    # Random delay between requests — be a polite guest
    time.sleep(random.uniform(2, 5))
    return response.text

for url in url_lookup[content_lookup]:
    print("Reading "+url)
    page_content = get_page(url)
    time.sleep(random.randint(5,15)) ### Be nice to the server and give it time between page requests
    # with open(data_dir+content_abbreviation+'.html', 'ab') as f:  # 'ab' for "append binary"
    #     f.write(page_content.encode('utf-8'))  # Ensure content is written as bytes
    html = page_content

    # url = sys.argv[1]
    # html = get_page(url)


    #### Generating the GLE code. ####
    def GLEcode(content_area, grade, strandnum):
        content_area_dictionary = {
            'Comprehensive Health': 'CH',
            'Computer Science': 'CS',
            'Dance': 'DA',
            'Drama and Theatre Arts': 'DT',
            'Financial Literacy': 'FL',
            'Mathematics': 'MA',
            'Music': 'MU',
            'Physical Education': 'PE',
            'Reading, Writing and Communicating': 'RW',
            'Science': 'SC',
            'Social Studies': 'SS',
            'Visual Arts': 'VA',
            'World Languages': 'WL',
        }

        grade_dictionary = {
            'Preschool': 'P',
            'Kindergarten': 'K',
            'First Grade': '1',
            'Second Grade': '2',
            'Third Grade': '3',
            'Fourth Grade': '4',
            'Fifth Grade': '5',
            'Sixth Grade': '6',
            'Sixth Grade/Novice': '6N', # Used in Music
            'Seventh Grade': '7',
            'Seventh Grade/Intermediate': '7I', # Used in Music
            'Eighth Grade': '8',
            'Eighth Grade/Proficient': '8P', # Used in Music
            'Middle School': 'MS', # Used in Science
            'Middle School 1': 'M1', # Used in Visual Arts
            'Middle School 2': 'M2', # Used in Visual Arts
            'Middle School 3': 'M3', # Used in Visual Arts
            'High School': 'HS',
            'Ninth / Tenth Grade Band': 'H1', # Used in RWC
            'Ninth–Tenth Grade Band': 'H1', # Used in RWC
            'High School - Fundamental Pathway': 'H1', # Used in Dance, Drama and Theatre Arts
            'High School/Accomplished': 'H1', # Used in Music
            'Eleventh / Twelfth Grade Band': 'H2', # Used in RWC
            'Eleventh–Twelfth Grade Band': 'H2', # Used in RWC
            'High School - Advanced Pathway': 'H2', # Used in Drama and Theatre Arts
            'High School/Advanced': 'H2', # Used in Music
            'High School - Extended Pathway': 'H2', # Used in Dance
            'High School - Professional Pathway': 'H3', # Used in Drama and Theatre Arts
            'Novice-Low': 'NL', # Used in World Languages
            'Novice-Mid': 'NM', # Used in World Languages
            'Novice-High': 'NH', # Used in World Languages
            'Intermediate-Low': 'IL', # Used in World Languages
            'Intermediate-Mid': 'IM', # Used in World Languages
            'Intermediate-High': 'IH', # Used in World Languages
            'Advanced-Low': 'AL', # Used in World Languages
            'Novice': 'NO', # Used in Music and Dance
            'Emerging': 'EM', # Used in Dance
            'Intermediate': 'IN', # Used in Music and Dance
            'Proficient': 'PR', # Used in Music and Dance
            'Accomplished': 'AC', # Used in Music
            'Exemplary': 'EX', # Used in Dance
        }

        ### And this is the part of the function that assembles the pieces of the code.
        CODE_content_area = content_area_dictionary[content_area]
        CODE_grade = grade_dictionary[grade]
        # CODEgle = gle.split(' ')[0]
        CODE = CODE_content_area+'.'+CODE_grade+'.'+str(strandnum)+'.'
        if CODE_content_area == "MA": ### Math gets an exception because of its CCSS-familiar coding
            CODE = "MA."+glenum
        if CODE_content_area == "WL": ### World languages gets an exception
            CODE = "WL."+CODE_grade+'.'
        if CODE.endswith('.'):
            CODE = CODE[:-1]
        return(CODE)


    #### HTML to Markdown conversion. ####
    soup = BeautifulSoup(html, "html.parser")

    content_area = soup.find('div', class_="col-3").text.split(' - ')[0] # Split this to cut off the year portion at the end
    grade = soup.find('div', class_="col-9").text.split(', ')[0].strip() # Split to isolate the grade level
    grade_for_filename = grade.replace('/','-').replace(' / ','-').replace(' – ','-').replace('–','-').replace(' - ','-') # Replace the en dashes and slashes with a hyphen for the filename to avoid issues on some operating systems

    markfile = open(f"{filecount:02d} {content_area} ({content_year}) {grade_for_filename}.md", 'w', encoding='utf-8')
    filecount += 1
    markfile.write("# " + grade + " | " + content_area + "\n\n")

    blocks = soup.find_all('div', class_="caBlock") # A "block" is the part(s) of a page encapsulating a topic strand that can hold multiple GLEs
    for block in blocks:

        standard = block.find('div', class_="col-9").text.split(', ')[1].strip() # Split to isolate the strand
        markfile.write("## " + standard + "\n\n")

        gles = block.find_all('div', class_="gle") # A GLE is the part(s) of the page in the expandable/collpsable boxes and includes everything attached to the GLE, not just the statement of the GLE.
        for gle in gles:

            gleheader = gle.find('p', class_="gleDetail").text.split(':')[0].strip()
            gletext = gle.find('p', style="padding-left:40px;").text.replace('.',':', 1).strip()
            standard_number = standard.split('Standard ')[1].split('.')[0]
            glecode = GLEcode(content_area, grade, standard_number)
            markfile.write("### " + gleheader + " " + glecode + "." + gletext + "\n\n")

            prepared_graduates = gle.find('div','p', class_="gleDetail").text.strip().replace('Graduates:', 'Graduates')
            markfile.write("#### " + prepared_graduates + "\n\n")

            # LEFT SIDE OF GLE BOX
            leftcol = gle.find('div', class_="col eocol leftcol") # Left column contains the evidence outcomes

            evidence_outcomes = leftcol.find('p').text.strip().rstrip(':')
            markfile.write("#### " + evidence_outcomes + "\n\n")

            students_can = leftcol.find('em').text.strip()
            markfile.write("##### " + students_can + "\n\n")

            eo_list = leftcol.find('ol')
            enum = 1
            for eo in eo_list.find_all('li', recursive=False):
                
                eo_text = str(eo).removeprefix("<li>").removesuffix("</li>").strip()
                markfile.write(str(enum) + ". " + md(eo_text).replace('* ', '   - ').replace('\n\n   - ','\n   - ').replace(' \*', '\*') + "\n") # These replace functions clean up RW sub-EOs
                enum += 1

            # RIGHT SIDE OF GLE BOX
            rightcol = gle.find('div', class_="col eocol rightcol") # Right column contains the contexts and connections

            academic_contexts_and_connections = rightcol.find('p').text.strip().rstrip(':')
            markfile.write("\n#### "+academic_contexts_and_connections+"\n\n")

            acc_subsections = rightcol.find_all('div', class_="eoinfo")
            for subsection in acc_subsections:
                subheading = subsection.find('p').text.strip()
                markfile.write("##### " + subheading + "\n\n")

                items = subsection.find_all('li')
                i = 1
                for item in items:
                    item = str(item).removeprefix('<li>').removesuffix('</li>').strip()
                    markfile.write(str(i)+". "+item + "\n")
                    i += 1

                markfile.write("\n")

    #        markfile.write("----------" + "\n\n")