import csv

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def is_state_value(state_value):
    with open ('states.csv') as csv_file:
        state_abbv = csv.reader(csv_file, delimiter=',')
        for key,value in state_abbv:
            if key.lower() == state_value:
#                print(key + ":" + value)
                return True
    return False

# reformat state names with two words for url ok format. 
def reformat_2W_states(name):
    if " " in name:
        newname = name.replace(" ", "%20")
        return newname
    else:
        return name


def two_letter_statecode(state_value):
    try:
        st = str(state_value).upper()
        print(f'state to Upper {st}')
        if states[st]:
            print("state is hit")
            return states[st]
    except Exception as e:
        return False


if __name__ == "__main__":
    state_value = 'ca'
    result = is_state_value(state_value)
    if result:
        print(f"{state_value} : State value is Matched")
    
    state_value = "california"
    result = is_state_value(state_value)
    if result:
        print(f"{state_value} : State value is Matched")
    
    state_value = "New Hampshire"
    name = reformat_2W_states(state_value)
    print(name)