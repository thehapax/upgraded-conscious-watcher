import csv
from telethon import Button

state_list = {
         'Alabama','Alaska','Arizona','Arkansas','California','Colorado',
         'Connecticut','Delaware', 'District of Columbia','Florida','Georgia',
         'Hawaii','Idaho', 'Illinois','Indiana','Iowa','Kansas','Kentucky',
         'Louisiana', 'Maine' 'Maryland','Massachusetts','Michigan','Minnesota',
         'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
         'New Hampshire','New Jersey','New Mexico','New York',
         'North Carolina','North Dakota','Northern Mariana Islands', 'Ohio',    
         'Oklahoma','Oregon','Pennsylvania', 'Puerto Rico', 'Rhode Island',
         'South  Carolina','South Dakota','Tennessee','Texas','Utah',
         'Vermont','Virginia','Washington','West Virginia',
         'Wisconsin','Wyoming', 'Virgin Islands'
    }


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

regions = ['South', 'Pacific', 'South East', 'Midwest', 
           'Great Lakes', 'Mid-Atlantic', 'Mountain', 'New England']

south = ['Tennessee', 'Texas', 'Louisiana', 'Oklahoma', 'Mississippi', 'Kentucky', 'Arkansas']
pacific = ['California', 'Oregon', 'Washington', 'Hawaii', 'Alaska']
south_east = ['Georgia', 'Florida', 'North Carolina', 'Alabama', 'South Carolina']
midwest = ['Missouri', 'South Dakota','Kansas', 'Iowa', 'North Dakota', 'Nebraska']
great_lakes = ['Michigan', 'Ohio', 'Indiana','Illinois', 'Wisconsin', 'Minnesota']
mid_atlantic = ['Virgina', 'West Virginia', 'Pennsylvania', 'Maryland', 'New York',
                 'New Jersey', 'Delaware', 'District of Colombia']
mountain = ['Idaho', 'Colorado', 'Montana', 'Arizona', 'Nevada', 'Utah', 'Wyoming', 'New Mexico']
new_england = ['Massachusetts', 'Maine', 'New Hampshire', 'Vermont', 'Connecticut', 'Rhode Island']


def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

def get_buttons(my_list):
    buttons = []
    for item in my_list:
        buttons.append(Button.inline(item, item))
    return buttons


def get_state_buttons(query_name):
    button_list = None
    if query_name == 'South':
        button_list = get_buttons(south)
    elif query_name == 'Pacific':
        button_list = get_buttons(pacific)
    elif query_name == 'South East':
        button_list = get_buttons(south_east)
    elif query_name == 'Midwest':
        button_list = get_buttons(midwest)
    elif query_name == 'Great Lakes':
        button_list = get_buttons(great_lakes)
    elif query_name == 'Mid-Atlantic':
        button_list = get_buttons(mid_atlantic)
    elif query_name == 'Mountain':
        button_list = get_buttons(mountain)
    elif query_name == 'New England':
        button_list = get_buttons(new_england)
    
    if button_list is not None:
        all_buttons = split(button_list, 2)
        return all_buttons
    else:
        return None


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
        #print(f'state to Upper {st}')
        if states[st]:
             #print("state is hit")
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
    
    test = 'Tennessee'
    if test in state_list:
        print("Tennessee is in the state_list")