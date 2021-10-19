import ast, os, sys, subprocess, json, re, collections, math, warnings

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(
        sys.version[:5]))

################################################################################
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
LINTER = False  # set to False if linter should be turned off for project
################################################################################

PASS = "PASS"
TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties.
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered"  # question type when the expected answer is a list of dicts where the order does matter
PNG_FORMAT = "png"  # use when the expected answer is an image

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=2, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=3, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=6, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=9, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=10, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=13, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=14, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=15, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=16, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=17, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": ['10/10/2021',
             '10/11/2021',
             '10/12/2021',
             '10/13/2021',
             '10/14/2021',
             '10/15/2021',
             '10/16/2021'],
    "2": ['Albania',
             'Angola',
             'Anguilla',
             'Antigua and Barbuda',
             'Argentina',
             'Armenia',
             'Aruba',
             'Austria',
             'Azerbaijan',
             'Bahamas',
             'Bahrain',
             'Bangladesh',
             'Barbados',
             'Belarus',
             'Belgium',
             'Benin',
             'Bermuda',
             'Bhutan',
             'Botswana',
             'Brazil',
             'Brunei',
             'Bulgaria',
             'Cambodia',
             'Cameroon',
             'Canada',
             'Cayman Islands',
             'Central African Republic',
             'Chad',
             'Chile',
             'China',
             'Colombia',
             'Congo',
             'Costa Rica',
             "Cote d'Ivoire",
             'Croatia',
             'Cuba',
             'Curacao',
             'Cyprus',
             'Czechia',
             'Denmark',
             'Dominica',
             'Dominican Republic',
             'Ecuador',
             'El Salvador',
             'England',
             'Equatorial Guinea',
             'Estonia',
             'Eswatini',
             'Ethiopia',
             'Faeroe Islands',
             'Fiji',
             'Finland',
             'France',
             'French Polynesia',
             'Gabon',
             'Georgia',
             'Germany',
             'Gibraltar',
             'Greece',
             'Greenland',
             'Guatemala',
             'Guernsey',
             'Guinea',
             'Guinea-Bissau',
             'Guyana',
             'Haiti',
             'Honduras',
             'Hong Kong',
             'Hungary',
             'Iceland',
             'India',
             'Indonesia',
             'Iran',
             'Ireland',
             'Isle of Man',
             'Israel',
             'Italy',
             'Jamaica',
             'Japan',
             'Jersey',
             'Jordan',
             'Kazakhstan',
             'Kenya',
             'Kiribati',
             'Kosovo',
             'Kyrgyzstan',
             'Laos',
             'Latvia',
             'Lebanon',
             'Lesotho',
             'Libya',
             'Liechtenstein',
             'Lithuania',
             'Luxembourg',
             'Macao',
             'Malawi',
             'Malaysia',
             'Maldives',
             'Mali',
             'Malta',
             'Mauritania',
             'Mauritius',
             'Mexico',
             'Moldova',
             'Mongolia',
             'Montenegro',
             'Morocco',
             'Namibia',
             'Nepal',
             'Netherlands',
             'New Caledonia',
             'New Zealand',
             'Niger',
             'Nigeria',
             'North Macedonia',
             'Northern Ireland',
             'Norway',
             'Oman',
             'Pakistan',
             'Palestine',
             'Panama',
             'Paraguay',
             'Peru',
             'Philippines',
             'Poland',
             'Portugal',
             'Qatar',
             'Romania',
             'Russia',
             'Rwanda',
             'Saint Kitts and Nevis',
             'Saint Lucia',
             'Saint Vincent and the Grenadines',
             'San Marino',
             'Sao Tome and Principe',
             'Saudi Arabia',
             'Scotland',
             'Senegal',
             'Serbia',
             'Sierra Leone',
             'Singapore',
             'Slovakia',
             'Slovenia',
             'Solomon Islands',
             'Somalia',
             'South Africa',
             'South Korea',
             'South Sudan',
             'Spain',
             'Sri Lanka',
             'Suriname',
             'Sweden',
             'Switzerland',
             'Syria',
             'Taiwan',
             'Tajikistan',
             'Thailand',
             'Timor',
             'Tokelau',
             'Trinidad and Tobago',
             'Tunisia',
             'Turkey',
             'Uganda',
             'Ukraine',
             'United Arab Emirates',
             'United Kingdom',
             'United States',
             'Uruguay',
             'Uzbekistan',
             'Vanuatu',
             'Vietnam',
             'Wales',
             'Wallis and Futuna',
             'Zambia',
             'Zimbabwe'],
    "3": {'Albania': 2872972,
             'Angola': 33933280,
             'Anguilla': 15125,
             'Antigua and Barbuda': 98731,
             'Argentina': 45604583,
             'Armenia': 2967346,
             'Aruba': 107192,
             'Austria': 9043326,
             'Azerbaijan': 10223013,
             'Bahamas': 396924,
             'Bahrain': 1748320,
             'Bangladesh': 166320063,
             'Barbados': 287705,
             'Belarus': 9442870,
             'Belgium': 11632619,
             'Benin': 12448178,
             'Bermuda': 62091,
             'Bhutan': 779919,
             'Botswana': 2397551,
             'Brazil': 213990906,
             'Brunei': 441526,
             'Bulgaria': 6896057,
             'Cambodia': 16946879,
             'Cameroon': 27245512,
             'Canada': 38068055,
             'Cayman Islands': 66497,
             'Central African Republic': 4919943,
             'Chad': 16976945,
             'Chile': 19212158,
             'China': 1444200065,
             'Colombia': 51268576,
             'Congo': 5655107,
             'Costa Rica': 5138943,
             "Cote d'Ivoire": 27054208,
             'Croatia': 4081642,
             'Cuba': 11317671,
             'Curacao': 164795,
             'Cyprus': 896022,
             'Czechia': 10724425,
             'Denmark': 5813397,
             'Dominica': 72170,
             'Dominican Republic': 10953914,
             'Ecuador': 17888343,
             'El Salvador': 6518621,
             'England': 56549090,
             'Equatorial Guinea': 1449829,
             'Estonia': 1325223,
             'Eswatini': 1172570,
             'Ethiopia': 117915651,
             'Faeroe Islands': 49055,
             'Fiji': 902891,
             'Finland': 5548474,
             'France': 67564291,
             'French Polynesia': 282530,
             'Gabon': 2277848,
             'Georgia': 3979762,
             'Germany': 83899864,
             'Gibraltar': 33691,
             'Greece': 10371097,
             'Greenland': 56870,
             'Guatemala': 18248434,
             'Guernsey': 67052,
             'Guinea': 13492772,
             'Guinea-Bissau': 2014041,
             'Guyana': 790311,
             'Haiti': 11479551,
             'Honduras': 10062163,
             'Hong Kong': 7552858,
             'Hungary': None,
             'Iceland': 343362,
             'India': 1393333537,
             'Indonesia': 276374016,
             'Iran': 85029669,
             'Ireland': 4982949,
             'Isle of Man': 85411,
             'Israel': 8789552,
             'Italy': 60365427,
             'Jamaica': 2973332,
             'Japan': 126046888,
             'Jersey': 101071,
             'Jordan': 10269469,
             'Kazakhstan': 18995456,
             'Kenya': 55014414,
             'Kiribati': 121379,
             'Kosovo': 1775443,
             'Kyrgyzstan': 6628448,
             'Laos': None,
             'Latvia': 1866970,
             'Lebanon': 6768981,
             'Lesotho': 2159668,
             'Libya': 6958968,
             'Liechtenstein': 38255,
             'Lithuania': 2689890,
             'Luxembourg': 634791,
             'Macao': 658402,
             'Malawi': 19646999,
             'Malaysia': 32775477,
             'Maldives': 543606,
             'Mali': 20884750,
             'Malta': 514572,
             'Mauritania': 4775717,
             'Mauritius': 1273439,
             'Mexico': 130261459,
             'Moldova': 4024295,
             'Mongolia': 3329184,
             'Montenegro': 628055,
             'Morocco': 37343907,
             'Namibia': 2587914,
             'Nepal': 29673579,
             'Netherlands': 17173167,
             'New Caledonia': 288226,
             'New Zealand': 4860712,
             'Niger': 25139534,
             'Nigeria': 211248673,
             'North Macedonia': 2082702,
             'Northern Ireland': 1896013,
             'Norway': 5465713,
             'Oman': 5223128,
             'Pakistan': 225207494,
             'Palestine': 5223082,
             'Panama': 4381530,
             'Paraguay': 7219633,
             'Peru': 33360107,
             'Philippines': 111048454,
             'Poland': 37797130,
             'Portugal': 10167757,
             'Qatar': 2930559,
             'Romania': 19127458,
             'Russia': 145901438,
             'Rwanda': 13277078,
             'Saint Kitts and Nevis': 53549,
             'Saint Lucia': 184390,
             'Saint Vincent and the Grenadines': 111275,
             'San Marino': 34011,
             'Sao Tome and Principe': 223362,
             'Saudi Arabia': 35340352,
             'Scotland': 5465917,
             'Senegal': 17191190,
             'Serbia': 6908539,
             'Sierra Leone': 8142654,
             'Singapore': 5896592,
             'Slovakia': 5460559,
             'Slovenia': 2078626,
             'Solomon Islands': 703969,
             'Somalia': 16341009,
             'South Africa': 60048172,
             'South Korea': 51303768,
             'South Sudan': 11338236,
             'Spain': 46744849,
             'Sri Lanka': 21497022,
             'Suriname': 591789,
             'Sweden': 10160175,
             'Switzerland': 8715679,
             'Syria': 18269616,
             'Taiwan': 23855431,
             'Tajikistan': 9749972,
             'Thailand': 69952004,
             'Timor': 1343811,
             'Tokelau': 1369,
             'Trinidad and Tobago': 1403443,
             'Tunisia': 11935130,
             'Turkey': 85041629,
             'Uganda': 47110574,
             'Ukraine': 43462272,
             'United Arab Emirates': 9991298,
             'United Kingdom': 68205745,
             'United States': 336316105,
             'Uruguay': 3485200,
             'Uzbekistan': 33937267,
             'Vanuatu': 314482,
             'Vietnam': 98176530,
             'Wales': 3169966,
             'Wallis and Futuna': 11095,
             'Zambia': 18909126,
             'Zimbabwe': 15091425},
    "4": 78,
    "5": {'Albania': 6147,
             'Angola': None,
             'Anguilla': None,
             'Antigua and Barbuda': None,
             'Argentina': None,
             'Armenia': None,
             'Aruba': 201,
             'Austria': 26429,
             'Azerbaijan': None,
             'Bahamas': None,
             'Bahrain': 7192,
             'Bangladesh': 444078,
             'Barbados': 1230,
             'Belarus': None,
             'Belgium': 9622,
             'Benin': None,
             'Bermuda': None,
             'Bhutan': None,
             'Botswana': None,
             'Brazil': None,
             'Brunei': None,
             'Bulgaria': 5548,
             'Cambodia': 285711,
             'Cameroon': None,
             'Canada': 89992,
             'Cayman Islands': 366,
             'Central African Republic': None,
             'Chad': None,
             'Chile': 221139,
             'China': 1423000,
             'Colombia': 273573,
             'Congo': None,
             'Costa Rica': None,
             "Cote d'Ivoire": None,
             'Croatia': 6144,
             'Cuba': 230815,
             'Curacao': None,
             'Cyprus': None,
             'Czechia': 6425,
             'Denmark': 2766,
             'Dominica': None,
             'Dominican Republic': 61965,
             'Ecuador': 44181,
             'El Salvador': 30384,
             'England': 57143,
             'Equatorial Guinea': None,
             'Estonia': 1697,
             'Eswatini': None,
             'Ethiopia': 12386,
             'Faeroe Islands': None,
             'Fiji': None,
             'Finland': 24337,
             'France': 170917,
             'French Polynesia': None,
             'Gabon': None,
             'Georgia': None,
             'Germany': 200131,
             'Gibraltar': 489,
             'Greece': 15148,
             'Greenland': 65,
             'Guatemala': 71289,
             'Guernsey': None,
             'Guinea': 57128,
             'Guinea-Bissau': None,
             'Guyana': 2626,
             'Haiti': None,
             'Honduras': None,
             'Hong Kong': 217,
             'Hungary': None,
             'Iceland': None,
             'India': 4564718,
             'Indonesia': 2328841,
             'Iran': None,
             'Ireland': 2071,
             'Isle of Man': 15,
             'Israel': 18942,
             'Italy': 197559,
             'Jamaica': 5365,
             'Japan': 740956,
             'Jersey': None,
             'Jordan': 14033,
             'Kazakhstan': 70953,
             'Kenya': None,
             'Kiribati': None,
             'Kosovo': 7952,
             'Kyrgyzstan': 8877,
             'Laos': None,
             'Latvia': 13529,
             'Lebanon': 46720,
             'Lesotho': None,
             'Libya': None,
             'Liechtenstein': 21,
             'Lithuania': 5970,
             'Luxembourg': None,
             'Macao': None,
             'Malawi': None,
             'Malaysia': 209277,
             'Maldives': 854,
             'Mali': None,
             'Malta': 1948,
             'Mauritania': None,
             'Mauritius': None,
             'Mexico': None,
             'Moldova': 4170,
             'Mongolia': 787,
             'Montenegro': None,
             'Morocco': None,
             'Namibia': None,
             'Nepal': 2275,
             'Netherlands': None,
             'New Caledonia': None,
             'New Zealand': None,
             'Niger': None,
             'Nigeria': None,
             'North Macedonia': None,
             'Northern Ireland': 1043,
             'Norway': 7517,
             'Oman': None,
             'Pakistan': None,
             'Palestine': None,
             'Panama': None,
             'Paraguay': None,
             'Peru': 187907,
             'Philippines': 460748,
             'Poland': 8247,
             'Portugal': None,
             'Qatar': 4225,
             'Romania': None,
             'Russia': 365653,
             'Rwanda': None,
             'Saint Kitts and Nevis': None,
             'Saint Lucia': 495,
             'Saint Vincent and the Grenadines': None,
             'San Marino': None,
             'Sao Tome and Principe': None,
             'Saudi Arabia': 167540,
             'Scotland': 7832,
             'Senegal': None,
             'Serbia': None,
             'Sierra Leone': None,
             'Singapore': 25953,
             'Slovakia': 2446,
             'Slovenia': 5352,
             'Solomon Islands': None,
             'Somalia': None,
             'South Africa': None,
             'South Korea': 468685,
             'South Sudan': None,
             'Spain': 60050,
             'Sri Lanka': 87739,
             'Suriname': 2250,
             'Sweden': 37603,
             'Switzerland': 32565,
             'Syria': None,
             'Taiwan': 269374,
             'Tajikistan': None,
             'Thailand': 962558,
             'Timor': None,
             'Tokelau': None,
             'Trinidad and Tobago': 6425,
             'Tunisia': 38526,
             'Turkey': 242206,
             'Uganda': None,
             'Ukraine': 164387,
             'United Arab Emirates': None,
             'United Kingdom': 68207,
             'United States': 794421,
             'Uruguay': 19140,
             'Uzbekistan': None,
             'Vanuatu': None,
             'Vietnam': 1126342,
             'Wales': 2189,
             'Wallis and Futuna': None,
             'Zambia': 8535,
             'Zimbabwe': 20058},
    "6": {'Albania': 12781,
             'Angola': None,
             'Anguilla': None,
             'Antigua and Barbuda': None,
             'Argentina': 1548234,
             'Armenia': None,
             'Aruba': 585,
             'Austria': 124986,
             'Azerbaijan': 105571,
             'Bahamas': None,
             'Bahrain': 48396,
             'Bangladesh': 2838296,
             'Barbados': 5519,
             'Belarus': None,
             'Belgium': 25552,
             'Benin': None,
             'Bermuda': None,
             'Bhutan': None,
             'Botswana': None,
             'Brazil': 6752141,
             'Brunei': None,
             'Bulgaria': 39213,
             'Cambodia': 1767528,
             'Cameroon': None,
             'Canada': 542813,
             'Cayman Islands': 617,
             'Central African Republic': None,
             'Chad': None,
             'Chile': 740426,
             'China': 10439000,
             'Colombia': 1251585,
             'Congo': None,
             'Costa Rica': None,
             "Cote d'Ivoire": None,
             'Croatia': 33831,
             'Cuba': 1286245,
             'Curacao': 53,
             'Cyprus': 6816,
             'Czechia': 38673,
             'Denmark': 9139,
             'Dominica': None,
             'Dominican Republic': 355554,
             'Ecuador': 181736,
             'El Salvador': 149292,
             'England': 351675,
             'Equatorial Guinea': None,
             'Estonia': 12129,
             'Eswatini': 7504,
             'Ethiopia': 111553,
             'Faeroe Islands': 129,
             'Fiji': None,
             'Finland': 101346,
             'France': 614107,
             'French Polynesia': None,
             'Gabon': None,
             'Georgia': 30103,
             'Germany': 840239,
             'Gibraltar': 2039,
             'Greece': 96587,
             'Greenland': 278,
             'Guatemala': 417952,
             'Guernsey': None,
             'Guinea': 84865,
             'Guinea-Bissau': None,
             'Guyana': 2626,
             'Haiti': None,
             'Honduras': None,
             'Hong Kong': 92020,
             'Hungary': None,
             'Iceland': None,
             'India': 29652224,
             'Indonesia': 12554928,
             'Iran': None,
             'Ireland': 19460,
             'Isle of Man': 35,
             'Israel': 134245,
             'Italy': 1238125,
             'Jamaica': 19458,
             'Japan': 3623659,
             'Jersey': None,
             'Jordan': 41367,
             'Kazakhstan': 404833,
             'Kenya': 18000,
             'Kiribati': None,
             'Kosovo': 65273,
             'Kyrgyzstan': 65312,
             'Laos': None,
             'Latvia': 71548,
             'Lebanon': 87761,
             'Lesotho': None,
             'Libya': None,
             'Liechtenstein': 124,
             'Lithuania': 34997,
             'Luxembourg': 6,
             'Macao': None,
             'Malawi': 22478,
             'Malaysia': 1253011,
             'Maldives': 5295,
             'Mali': None,
             'Malta': 12597,
             'Mauritania': None,
             'Mauritius': None,
             'Mexico': 3230114,
             'Moldova': 17820,
             'Mongolia': 3051,
             'Montenegro': 9585,
             'Morocco': None,
             'Namibia': None,
             'Nepal': 283342,
             'Netherlands': None,
             'New Caledonia': None,
             'New Zealand': 184193,
             'Niger': None,
             'Nigeria': None,
             'North Macedonia': 2656,
             'Northern Ireland': 7773,
             'Norway': 19083,
             'Oman': None,
             'Pakistan': 954000,
             'Palestine': None,
             'Panama': 68529,
             'Paraguay': None,
             'Peru': 1216798,
             'Philippines': 1808572,
             'Poland': 37055,
             'Portugal': None,
             'Qatar': 21552,
             'Romania': 236037,
             'Russia': 4296137,
             'Rwanda': 200743,
             'Saint Kitts and Nevis': None,
             'Saint Lucia': 495,
             'Saint Vincent and the Grenadines': None,
             'San Marino': None,
             'Sao Tome and Principe': None,
             'Saudi Arabia': 1186112,
             'Scotland': 48229,
             'Senegal': None,
             'Serbia': None,
             'Sierra Leone': None,
             'Singapore': 212507,
             'Slovakia': 9834,
             'Slovenia': 30336,
             'Solomon Islands': None,
             'Somalia': None,
             'South Africa': None,
             'South Korea': 3196723,
             'South Sudan': None,
             'Spain': 122494,
             'Sri Lanka': 548488,
             'Suriname': 8994,
             'Sweden': 114019,
             'Switzerland': 114903,
             'Syria': None,
             'Taiwan': 1194163,
             'Tajikistan': None,
             'Thailand': 4305580,
             'Timor': None,
             'Tokelau': None,
             'Trinidad and Tobago': 35308,
             'Tunisia': 247222,
             'Turkey': 1636884,
             'Uganda': None,
             'Ukraine': 745515,
             'United Arab Emirates': 133480,
             'United Kingdom': 430518,
             'United States': 3870135,
             'Uruguay': 78359,
             'Uzbekistan': None,
             'Vanuatu': None,
             'Vietnam': 4723675,
             'Wales': 22841,
             'Wallis and Futuna': None,
             'Zambia': 41304,
             'Zimbabwe': 115640},
    "7": 'India',
    "8": {'10/10/2021': 15646236,
             '10/11/2021': 13364434,
             '10/12/2021': 20497398,
             '10/13/2021': 17692532,
             '10/14/2021': 16587172,
             '10/15/2021': 20678860,
             '10/16/2021': 11698636},
    "9": {'Albania': '10/13/2021',
             'Angola': '10/14/2021',
             'Anguilla': '10/15/2021',
             'Antigua and Barbuda': '10/13/2021',
             'Argentina': '10/16/2021',
             'Armenia': '10/11/2021',
             'Aruba': '10/15/2021',
             'Austria': '10/16/2021',
             'Azerbaijan': '10/16/2021',
             'Bahamas': '10/15/2021',
             'Bahrain': '10/16/2021',
             'Bangladesh': '10/16/2021',
             'Barbados': '10/16/2021',
             'Belarus': '10/10/2021',
             'Belgium': '10/14/2021',
             'Benin': '10/12/2021',
             'Bermuda': '10/15/2021',
             'Bhutan': '10/10/2021',
             'Botswana': '10/14/2021',
             'Brazil': '10/16/2021',
             'Brunei': '10/14/2021',
             'Bulgaria': '10/16/2021',
             'Cambodia': '10/16/2021',
             'Cameroon': '10/11/2021',
             'Canada': '10/16/2021',
             'Cayman Islands': '10/14/2021',
             'Central African Republic': '10/14/2021',
             'Chad': '10/11/2021',
             'Chile': '10/15/2021',
             'China': None,
             'Colombia': '10/14/2021',
             'Congo': '10/14/2021',
             'Costa Rica': '10/11/2021',
             "Cote d'Ivoire": '10/11/2021',
             'Croatia': '10/16/2021',
             'Cuba': '10/15/2021',
             'Curacao': '10/16/2021',
             'Cyprus': '10/14/2021',
             'Czechia': '10/16/2021',
             'Denmark': '10/14/2021',
             'Dominica': '10/15/2021',
             'Dominican Republic': '10/16/2021',
             'Ecuador': '10/14/2021',
             'El Salvador': '10/16/2021',
             'England': '10/16/2021',
             'Equatorial Guinea': '10/12/2021',
             'Estonia': '10/16/2021',
             'Eswatini': '10/11/2021',
             'Ethiopia': '10/16/2021',
             'Faeroe Islands': '10/15/2021',
             'Fiji': '10/12/2021',
             'Finland': '10/16/2021',
             'France': '10/14/2021',
             'French Polynesia': '10/12/2021',
             'Gabon': '10/14/2021',
             'Georgia': '10/14/2021',
             'Germany': '10/15/2021',
             'Gibraltar': '10/16/2021',
             'Greece': '10/16/2021',
             'Greenland': '10/15/2021',
             'Guatemala': '10/16/2021',
             'Guernsey': None,
             'Guinea': '10/14/2021',
             'Guinea-Bissau': '10/12/2021',
             'Guyana': '10/13/2021',
             'Haiti': '10/15/2021',
             'Honduras': '10/15/2021',
             'Hong Kong': '10/16/2021',
             'Hungary': '10/14/2021',
             'Iceland': '10/14/2021',
             'India': '10/16/2021',
             'Indonesia': '10/16/2021',
             'Iran': '10/10/2021',
             'Ireland': '10/16/2021',
             'Isle of Man': '10/14/2021',
             'Israel': '10/16/2021',
             'Italy': '10/16/2021',
             'Jamaica': '10/15/2021',
             'Japan': '10/16/2021',
             'Jersey': '10/14/2021',
             'Jordan': '10/16/2021',
             'Kazakhstan': '10/16/2021',
             'Kenya': '10/16/2021',
             'Kiribati': '10/12/2021',
             'Kosovo': '10/16/2021',
             'Kyrgyzstan': '10/16/2021',
             'Laos': '10/10/2021',
             'Latvia': '10/16/2021',
             'Lebanon': '10/16/2021',
             'Lesotho': '10/10/2021',
             'Libya': '10/14/2021',
             'Liechtenstein': '10/14/2021',
             'Lithuania': '10/16/2021',
             'Luxembourg': None,
             'Macao': '10/16/2021',
             'Malawi': '10/16/2021',
             'Malaysia': '10/16/2021',
             'Maldives': '10/16/2021',
             'Mali': '10/15/2021',
             'Malta': '10/16/2021',
             'Mauritania': '10/13/2021',
             'Mauritius': '10/14/2021',
             'Mexico': '10/16/2021',
             'Moldova': '10/16/2021',
             'Mongolia': '10/16/2021',
             'Montenegro': '10/16/2021',
             'Morocco': '10/13/2021',
             'Namibia': '10/14/2021',
             'Nepal': '10/14/2021',
             'Netherlands': None,
             'New Caledonia': '10/12/2021',
             'New Zealand': '10/16/2021',
             'Niger': '10/10/2021',
             'Nigeria': '10/14/2021',
             'North Macedonia': '10/15/2021',
             'Northern Ireland': '10/16/2021',
             'Norway': '10/14/2021',
             'Oman': '10/11/2021',
             'Pakistan': '10/12/2021',
             'Palestine': '10/10/2021',
             'Panama': '10/16/2021',
             'Paraguay': '10/15/2021',
             'Peru': '10/16/2021',
             'Philippines': '10/16/2021',
             'Poland': '10/16/2021',
             'Portugal': '10/11/2021',
             'Qatar': None,
             'Romania': '10/16/2021',
             'Russia': '10/16/2021',
             'Rwanda': '10/15/2021',
             'Saint Kitts and Nevis': '10/15/2021',
             'Saint Lucia': '10/15/2021',
             'Saint Vincent and the Grenadines': '10/16/2021',
             'San Marino': '10/10/2021',
             'Sao Tome and Principe': '10/13/2021',
             'Saudi Arabia': '10/16/2021',
             'Scotland': '10/16/2021',
             'Senegal': '10/14/2021',
             'Serbia': '10/12/2021',
             'Sierra Leone': '10/12/2021',
             'Singapore': '10/16/2021',
             'Slovakia': '10/13/2021',
             'Slovenia': '10/16/2021',
             'Solomon Islands': '10/12/2021',
             'Somalia': '10/14/2021',
             'South Africa': '10/16/2021',
             'South Korea': '10/16/2021',
             'South Sudan': '10/11/2021',
             'Spain': '10/14/2021',
             'Sri Lanka': '10/16/2021',
             'Suriname': '10/15/2021',
             'Sweden': '10/15/2021',
             'Switzerland': '10/14/2021',
             'Syria': '10/12/2021',
             'Taiwan': '10/16/2021',
             'Tajikistan': '10/10/2021',
             'Thailand': '10/15/2021',
             'Timor': '10/12/2021',
             'Tokelau': '10/12/2021',
             'Trinidad and Tobago': '10/16/2021',
             'Tunisia': '10/16/2021',
             'Turkey': '10/16/2021',
             'Uganda': '10/14/2021',
             'Ukraine': '10/16/2021',
             'United Arab Emirates': '10/16/2021',
             'United Kingdom': '10/16/2021',
             'United States': '10/16/2021',
             'Uruguay': '10/16/2021',
             'Uzbekistan': None,
             'Vanuatu': '10/12/2021',
             'Vietnam': '10/16/2021',
             'Wales': '10/16/2021',
             'Wallis and Futuna': '10/12/2021',
             'Zambia': '10/16/2021',
             'Zimbabwe': '10/16/2021'},
    "10": {'Albania': 845877,
             'Angola': 1290152,
             'Anguilla': 9157,
             'Antigua and Barbuda': 45088,
             'Argentina': 24514822,
             'Armenia': 170212,
             'Aruba': 76011,
             'Austria': 5531374,
             'Azerbaijan': 4196348,
             'Bahamas': 110710,
             'Bahrain': 1132855,
             'Bangladesh': 18682901,
             'Barbados': 116514,
             'Belarus': 1749584,
             'Belgium': 8489064,
             'Benin': 186951,
             'Bermuda': 43400,
             'Bhutan': 502274,
             'Botswana': 258260,
             'Brazil': 105171980,
             'Brunei': 224028,
             'Bulgaria': 1383964,
             'Cambodia': 12541420,
             'Cameroon': 140494,
             'Canada': 27681160,
             'Cayman Islands': 55780,
             'Central African Republic': 9901,
             'Chad': 36682,
             'Chile': 14366309,
             'China': None,
             'Colombia': 19370919,
             'Congo': 119594,
             'Costa Rica': 2395829,
             "Cote d'Ivoire": 607739,
             'Croatia': 1754676,
             'Cuba': 6748348,
             'Curacao': 90664,
             'Cyprus': 564181,
             'Czechia': 6026901,
             'Denmark': 4394501,
             'Dominica': 22024,
             'Dominican Republic': 5082077,
             'Ecuador': 10032731,
             'El Salvador': 3588788,
             'England': 38022391,
             'Equatorial Guinea': 178461,
             'Estonia': 727290,
             'Eswatini': 225042,
             'Ethiopia': 945066,
             'Faeroe Islands': 36977,
             'Fiji': 496091,
             'Finland': 3703598,
             'France': 45303504,
             'French Polynesia': 144124,
             'Gabon': 86340,
             'Georgia': 892410,
             'Germany': 54658274,
             'Gibraltar': 39751,
             'Greece': 6301143,
             'Greenland': 36622,
             'Guatemala': 2988941,
             'Guernsey': None,
             'Guinea': 655258,
             'Guinea-Bissau': 9513,
             'Guyana': 226649,
             'Haiti': 28941,
             'Honduras': 2537900,
             'Hong Kong': 4334726,
             'Hungary': 5694336,
             'Iceland': 277837,
             'India': 278694030,
             'Indonesia': 62166916,
             'Iran': 19326200,
             'Ireland': 3727958,
             'Isle of Man': 64021,
             'Israel': 5698663,
             'Italy': 42208004,
             'Jamaica': 337419,
             'Japan': 83656184,
             'Jersey': 74270,
             'Jordan': 3408756,
             'Kazakhstan': 7097611,
             'Kenya': 1208987,
             'Kiribati': 8384,
             'Kosovo': 666265,
             'Kyrgyzstan': 685013,
             'Laos': 2343258,
             'Latvia': 932291,
             'Lebanon': 1411895,
             'Lesotho': 339506,
             'Libya': 296760,
             'Liechtenstein': 23116,
             'Lithuania': 1643920,
             'Luxembourg': None,
             'Macao': 325440,
             'Malawi': 518477,
             'Malaysia': 22651939,
             'Maldives': 351169,
             'Mali': 257460,
             'Malta': 425020,
             'Mauritania': 587570,
             'Mauritius': 831887,
             'Mexico': 51615810,
             'Moldova': 827724,
             'Mongolia': 2135870,
             'Montenegro': 230821,
             'Morocco': 20587049,
             'Namibia': 219342,
             'Nepal': 6469159,
             'Netherlands': None,
             'New Caledonia': 123577,
             'New Zealand': 2494557,
             'Niger': 216615,
             'Nigeria': 2359781,
             'North Macedonia': 758001,
             'Northern Ireland': 1224459,
             'Norway': 3705142,
             'Oman': 2294880,
             'Pakistan': 34809848,
             'Palestine': 1176037,
             'Panama': 2336653,
             'Paraguay': 2058067,
             'Peru': 13877213,
             'Philippines': 23981240,
             'Poland': 19725793,
             'Portugal': 8782671,
             'Qatar': None,
             'Romania': 5654687,
             'Russia': 47272007,
             'Rwanda': 1718424,
             'Saint Kitts and Nevis': 23069,
             'Saint Lucia': 37617,
             'Saint Vincent and the Grenadines': 14566,
             'San Marino': 22218,
             'Sao Tome and Principe': 27755,
             'Saudi Arabia': 20643384,
             'Scotland': 3877849,
             'Senegal': 564998,
             'Serbia': 2933395,
             'Sierra Leone': 66852,
             'Singapore': 4680794,
             'Slovakia': 2276678,
             'Slovenia': 1064678,
             'Solomon Islands': 28497,
             'Somalia': 258631,
             'South Africa': 10539458,
             'South Korea': 33166732,
             'South Sudan': 32761,
             'Spain': 37029165,
             'Sri Lanka': 12720463,
             'Suriname': 184821,
             'Sweden': 6791114,
             'Switzerland': 5295433,
             'Syria': 367744,
             'Taiwan': 5039052,
             'Tajikistan': 2011987,
             'Thailand': 25012380,
             'Timor': 315033,
             'Tokelau': 968,
             'Trinidad and Tobago': 564703,
             'Tunisia': 4189084,
             'Turkey': 47226488,
             'Uganda': 415486,
             'Ukraine': 6467945,
             'United Arab Emirates': 8505838,
             'United Kingdom': 45360146,
             'United States': 188902483,
             'Uruguay': 2604607,
             'Uzbekistan': None,
             'Vanuatu': 28368,
             'Vietnam': 17849651,
             'Wales': 2235447,
             'Wallis and Futuna': 5260,
             'Zambia': 492678,
             'Zimbabwe': 2473780},
    "11": 'Germany',
    "12": {'country': 'United States',
             'date': '10/16/2021',
             'daily_vaccinations': 876086,
             'total_vaccinations': 407446961,
             'people_vaccinated': 218562924,
             'people_fully_vaccinated': 188902483,
             'population': 336316105},
    "13": {'country': 'Argentina',
             'date': '10/12/2021',
             'daily_vaccinations': None,
             'total_vaccinations': 54115894,
             'people_vaccinated': 30265200,
             'people_fully_vaccinated': 23928986,
             'population': 45604583},
    "14": {'country': 'Belgium',
             'date': '10/15/2021',
             'daily_vaccinations': None,
             'total_vaccinations': 16741664,
             'people_vaccinated': 8645665,
             'people_fully_vaccinated': 8489064,
             'population': 11632619},
    "15": {'country': 'China',
             'date': '10/10/2021',
             'daily_vaccinations': 1117000,
             'total_vaccinations': 2221245000,
             'people_vaccinated': None,
             'people_fully_vaccinated': None,
             'population': 1444200065},
    "16": {'country': 'Isle of Man',
             'date': '10/11/2021',
             'daily_vaccinations': None,
             'total_vaccinations': 129494,
             'people_vaccinated': 65485,
             'people_fully_vaccinated': None,
             'population': 85411},
    "17": {'Albania': 0.14756991855789908,
             'Angola': 1.4481619220060893,
             'Anguilla': 0.042699574096319755,
             'Antigua and Barbuda': 0.2144694819020582,
             'Argentina': 0.2717781104019438,
             'Armenia': 1.0211794703076165,
             'Aruba': 0.07950165107681782,
             'Austria': 0.05121801563228232,
             'Azerbaijan': 0.17769141167510416,
             'Bahamas': 0.20667509710053292,
             'Bahrain': 0.03327080694351881,
             'Bangladesh': 1.0045131106780472,
             'Barbados': 0.24432257067820176,
             'Belarus': 0.4109331132429195,
             'Belgium': 0.018447381242502118,
             'Benin': 0.1582018817765083,
             'Bermuda': 0.03725806451612903,
             'Bhutan': 0.165656593811346,
             'Botswana': 1.035696584836986,
             'Brazil': 0.48372489516694467,
             'Brunei': 0.5161810130876497,
             'Bulgaria': None,
             'Cambodia': 0.08323610882978164,
             'Cameroon': 1.815565077512207,
             'Canada': 0.06689856927961112,
             'Cayman Islands': 0.0,
             'Central African Republic': 23.78981921018079,
             'Chad': 2.9983915817021973,
             'Chile': 0.12147831429770861,
             'China': None,
             'Colombia': 0.4678699033329291,
             'Congo': 1.3336538622338914,
             'Costa Rica': 0.4714155309080907,
             "Cote d'Ivoire": 2.2423902365982764,
             'Croatia': 0.06582411795681938,
             'Cuba': 0.43800630909964927,
             'Curacao': 0.09464616606370775,
             'Cyprus': 0.06310031709681822,
             'Czechia': 0.016761516407852062,
             'Denmark': 0.016153142302163546,
             'Dominica': 0.21712677079549583,
             'Dominican Republic': 0.23779470480278045,
             'Ecuador': 0.16699142038194784,
             'El Salvador': 0.17804896806387002,
             'England': 0.08855584594877265,
             'Equatorial Guinea': 0.3226699390903335,
             'Estonia': 0.05983582889906365,
             'Eswatini': 0.033016059224500315,
             'Ethiopia': 2.2172176334774503,
             'Faeroe Islands': 0.051734862211645076,
             'Fiji': 0.19911871007536924,
             'Finland': 0.12899321146625525,
             'France': 0.120893805476945,
             'French Polynesia': 0.06892675751436263,
             'Gabon': 0.39023627519110493,
             'Georgia': 0.12899676157819837,
             'Germany': 0.04707093385349124,
             'Gibraltar': 0.00550929536363865,
             'Greece': 0.03834050425454556,
             'Greenland': 0.09264922724045656,
             'Guatemala': 0.6887817457755104,
             'Guernsey': None,
             'Guinea': 1.0681395725042655,
             'Guinea-Bissau': 10.682014085987596,
             'Guyana': 0.6319374892454853,
             'Haiti': 1.541999239832763,
             'Honduras': 0.3873292879940108,
             'Hong Kong': 0.05168446633074386,
             'Hungary': 0.039617261784341495,
             'Iceland': 0.01620014612884533,
             'India': 1.4901577977827511,
             'Indonesia': 0.7158639492427129,
             'Iran': 1.3323400875495441,
             'Ireland': 0.016969075295376182,
             'Isle of Man': 0.023164274222520737,
             'Israel': 0.08834545927702692,
             'Italy': 0.09432220485953327,
             'Jamaica': 0.6630954392017047,
             'Japan': 0.13081090335174744,
             'Jersey': 0.052389928638750506,
             'Jordan': 0.12001827059490325,
             'Kazakhstan': 0.12767183211365063,
             'Kenya': 1.722272447925412,
             'Kiribati': 4.1340648854961835,
             'Kosovo': 0.24746609832424035,
             'Kyrgyzstan': 0.3227238023219997,
             'Laos': 0.319172280645153,
             'Latvia': 0.09175032259240945,
             'Lebanon': 0.20152065132322164,
             'Lesotho': 0.024535648854512145,
             'Libya': 3.8601091791346542,
             'Liechtenstein': 0.07202803253157986,
             'Lithuania': 0.08250523139812156,
             'Luxembourg': None,
             'Macao': 0.28175700589970504,
             'Malawi': 0.7220513156803484,
             'Malaysia': 0.11212470596887975,
             'Maldives': 0.12105282641691037,
             'Mali': 0.27131593257205,
             'Malta': 0.0015599265916898027,
             'Mauritania': 0.21079190564528483,
             'Mauritius': 0.060128358779497695,
             'Mexico': 0.3298963244013801,
             'Moldova': None,
             'Mongolia': 0.055147551115002316,
             'Montenegro': 0.09595314117866226,
             'Morocco': 0.12398042089470909,
             'Namibia': 0.3355308148918128,
             'Nepal': 0.29667581211097144,
             'Netherlands': None,
             'New Caledonia': 0.32092541492348897,
             'New Zealand': 0.3953243000661039,
             'Niger': 0.9826466311197285,
             'Nigeria': 1.1690241594453044,
             'North Macedonia': 0.05412393915047606,
             'Northern Ireland': 0.07585145766416025,
             'Norway': 0.13102979588906444,
             'Oman': 0.2896473889702294,
             'Pakistan': 0.865785280073616,
             'Palestine': None,
             'Panama': 0.26650298525283816,
             'Paraguay': 0.3938370325164341,
             'Peru': 0.27149104074427627,
             'Philippines': None,
             'Poland': 0.015219464180730275,
             'Portugal': 0.021966210507031403,
             'Qatar': None,
             'Romania': 0.14372555014981378,
             'Russia': 0.08549641228475871,
             'Rwanda': 0.7042086237156837,
             'Saint Kitts and Nevis': 0.13784732758246998,
             'Saint Lucia': 0.30480899593269,
             'Saint Vincent and the Grenadines': 0.5660442125497734,
             'San Marino': 0.12899450895670178,
             'Sao Tome and Principe': 1.703512880562061,
             'Saudi Arabia': 0.15670914226078436,
             'Scotland': 0.10526325290128626,
             'Senegal': 1.2496026534607203,
             'Serbia': 0.04477235421755338,
             'Sierra Leone': 3.371432417878298,
             'Singapore': 0.011904817857824976,
             'Slovakia': 0.08739400125973018,
             'Slovenia': 0.07027382927044609,
             'Solomon Islands': 2.980173351580868,
             'Somalia': 0.3188055569517962,
             'South Africa': 0.32164566716808396,
             'South Korea': 0.21805105790947388,
             'South Sudan': 1.5301120234425079,
             'Spain': 0.02266559345856165,
             'Sri Lanka': 0.1609465787526759,
             'Suriname': 0.30284437374540774,
             'Sweden': 0.0616365739111433,
             'Switzerland': 0.06491386067957049,
             'Syria': 0.8539826618517229,
             'Taiwan': 1.8568800242585313,
             'Tajikistan': 0.24948620443372646,
             'Thailand': 0.46814413502433594,
             'Timor': 0.573873213282418,
             'Tokelau': 0.0,
             'Trinidad and Tobago': 0.07868383911542882,
             'Tunisia': 0.28909637524575776,
             'Turkey': 0.16108102300556418,
             'Uganda': 4.723829443109996,
             'Ukraine': 0.22487327891625547,
             'United Arab Emirates': 0.11627907796974267,
             'United Kingdom': 0.08917012745064798,
             'United States': 0.15701456396420158,
             'Uruguay': 0.0563516876058461,
             'Uzbekistan': None,
             'Vanuatu': 1.0873871968415116,
             'Vietnam': 1.468971858329331,
             'Wales': 0.07899672861848211,
             'Wallis and Futuna': 0.09296577946768061,
             'Zambia': None,
             'Zimbabwe': 0.2992982399404959},
    "18": 'Cayman Islands',
    "19": 'Gibraltar',
    "20": 'Cambodia'
}


# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# find correct python command based on version
def get_python_cmd():
    cmds = ['py', 'python3', 'python']
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd + ' -V', shell=True, universal_newlines=True)
            m = re.match(r'Python\s+(\d+\.\d+)\.*\d*', out)
            if m:
                if float(m.group(1)) >= 3.6:
                    return cmd
        except subprocess.CalledProcessError:
            pass
    else:
        return ''


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-220-test.ipynb'

    # re-execute it from the beginning
    py_cmd = get_python_cmd()
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    if py_cmd:
        # cmd = py_cmd + ' -m ' + cmd
        pass
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook, encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell, format):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get('text/plain', [])
        if lines:
            actual_lines = lines
            break
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines)
    try:
        actual = ast.literal_eval(actual)
    except ValueError:
        pass
    expected = expected_json[str(qnum)]

    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
            return list_compare_special(expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
        elif format == TEXT_FORMAT_LIST_DICTS_ORDERED:
            return list_compare_ordered(expected, actual)
        else:
            if expected != actual:
                return "found %s but expected %s" % (repr(actual), repr(expected))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def simple_compare(expected, actual, complete_msg=True):
    msg = PASS
    if type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (list may not be ordered as required)"
            except:
                pass
    return msg


def list_compare_helper(larger, smaller):
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], False)
                break
            val = simple_compare(larger[i], smaller[j], False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg


def list_compare_unordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in list; expect a list of entries of type %s" % (type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg


def list_compare_special(expected, actual):
    msg = PASS
    expected_list = []
    for expected_item in expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in expected:
            j = len(expected_item)
            actual_item = actual[i: i + j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i + j - 1) + val
                msg = msg + " (list may not be ordered as required)"
                break
            i += j

    return msg


def dict_compare(expected, actual, obj="dict"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
    except:
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (
            type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if expected[key] == None or type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub" + obj)
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg


def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format.split()[0] == TEXT_FORMAT:
        return check_cell_text(question.number, cell, question.format)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score': 0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def linter_severe_check(nb):
    issues = []
    func_names = set()
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        code = "\n".join(cell.get('source', []))
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    if name in func_names:
                        issues.append('name <%s> reused for multiple functions' % name)
                    func_names.add(name)
        except Exception as e:
            print('Linter error: ' + str(e))

    return issues


def main():
    if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    if not os.path.exists(orig_notebook):
        print("File not found: " + orig_notebook)
        print(
            "\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
        print("python test.py <notebook.ipynb>")
        sys.exit(1)

    nb = rerun_notebook(orig_notebook)

    if LINTER:
        # check for sever linter errors
        issues = linter_severe_check(nb)
        if issues:
            print("\nPlease fix the following, then rerun the tests:")
            for issue in issues:
                print(' - ' + issue)
            print("")
            sys.exit(1)

    # extract qnums with png expected answer
    png_expected = [q.number for q in questions if q.format == PNG_FORMAT]

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total
    png_passed = [t['test'] for t in results['tests'] if t['result'] == PASS and t['test'] in png_expected]

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])

    if len(png_passed) > 0:
        print("\nWARNING: ", end="")
        if len(png_passed) == 1:
            print("Q%d is not checked by test.py." % (png_passed[0]))
        else:
            for n in png_passed[:-1]:
                print("Q%d" % n, end=", ")
            print("and Q%d are not checked by test.py." % (png_passed[-1]))
        print(
            "Please refer to the corresponding reference png files and the expected output dictionary given in the documentation.\n")

    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
