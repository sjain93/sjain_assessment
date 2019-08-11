import json
import dateutil.parser
import sys

attempt_tracking = {}
# Creating a dict to store/update attempts of money transfer.

def in_same_week(iso_time, customer_id):
    # checking to see if we're in the same week by cycles of Monday
    has_attempts = len(attempt_tracking[customer_id]['weekly_attempt_log']) > 0
    if has_attempts:
        first_day_week = attempt_tracking[customer_id]['weekly_attempt_log'][0]
        delta = dateutil.parser.parse(iso_time) - dateutil.parser.parse(first_day_week)
        if delta.days < 7:
            prev_entry = attempt_tracking[customer_id]['weekly_attempt_log'][-1]
            prev_weekday = dateutil.parser.parse(prev_entry).weekday()
            current_weekday = dateutil.parser.parse(iso_time).weekday()
            if current_weekday > prev_weekday:
                return True  # in the same week
            elif (current_weekday == prev_weekday) and delta.days == 0:
                return True
            else:
                #monday has passed, week paramaters to refresh
                return False
        else:
            # week parameters refresh
            return False
    else:#return True if its the first valid transaction in the week
        return True

def daily_count_check(customer_id):
    if attempt_tracking[customer_id]['daily_count'] > 2:
        return False
    else:
        return True


def within_a_day(iso_time, customer_id):
    has_attempts = len(attempt_tracking[customer_id]['weekly_attempt_log']) > 0
    if has_attempts:
        prev_time = attempt_tracking[customer_id]['weekly_attempt_log'][-1]
        delta = dateutil.parser.parse(iso_time) - dateutil.parser.parse(prev_time)
    
        if delta.days == 0:
            return True
        else:
            return False
    else:
        return False
            

def load_limit_checks(iso_time, customer_id, load_amount):
    if within_a_day(iso_time, customer_id):
        if daily_count_check(customer_id):
            if ((attempt_tracking[customer_id]['daily_amount'] + load_amount) < 5000) and ((attempt_tracking[customer_id]['weekly_amount'] + load_amount) <20000):
                attempt_tracking[customer_id]['daily_count'] += 1
                attempt_tracking[customer_id]['weekly_amount'] += load_amount
                attempt_tracking[customer_id]['daily_amount'] += load_amount
                attempt_tracking[customer_id]['weekly_attempt_log'].append(iso_time)
                return True
            else:
                return False
        else:
            return False              
    else:
        if (load_amount < 5000) and (attempt_tracking[customer_id]['weekly_amount'] + load_amount < 20000):
            attempt_tracking[customer_id]['daily_count'] = 1
            attempt_tracking[customer_id]['daily_amount'] = load_amount
            attempt_tracking[customer_id]['weekly_amount'] += load_amount
            attempt_tracking[customer_id]['weekly_attempt_log'].append(iso_time)
            return True
        else:
            return False


def load_funds(attempt):
    ''' 
    Function will check the following parameters:
    - A maximum of $5,000 can be loaded per day
    - A maximum of $20,000 can be loaded per week
    - A maximum of 3 loads can be performed per day, regardless of amount

    If attempt is valid within these conditions, function returns True- else False
    '''
    customer_id = int(attempt['customer_id'])
    transaction_id = int(attempt['id'])
    load_amount = float(attempt['load_amount'].split("$")[1])
    iso_time = attempt['time']

    # initial attempt to load new customer, creating dicitonary structure to track each customer instance
    if attempt_tracking.get(customer_id) == None:
        if load_amount <= 5000:
            attempt_tracking[customer_id] = {
                'transaction': transaction_id,
                'weekly_amount': load_amount,
                'daily_amount': load_amount,
                'daily_count': 1,
                'weekly_attempt_log': [iso_time]
            }
            return True
        else:
            return False
    
    elif attempt_tracking[customer_id]['transaction'] == transaction_id:
        return 'transaction_exists'
    else:
        attempt_tracking[customer_id]['transaction'] = transaction_id
        if in_same_week(iso_time, customer_id):
            return load_limit_checks(iso_time,customer_id,load_amount)
        else:
            attempt_tracking[customer_id]['weekly_attempt_log'] = []
            attempt_tracking[customer_id]['weekly_amount'] = 0
            return load_limit_checks(iso_time, customer_id, load_amount)



input_file = sys.argv[1] if len(sys.argv) >= 2 else 'input.txt'
output_file = sys.argv[2] if len(sys.argv) >= 3 else 'output.txt'

in_file = open(input_file, 'r')
out_file = open(output_file, 'a+')

for line in in_file:
    attempt = json.loads(line)
    x = load_funds(attempt)
    if x == 'transaction_exists':
        continue
    else:
        output = json.dumps({"id":attempt['id'], 'customer_id':attempt['customer_id'], 'accepted':x})
        outFile.write(f'{output}\n')
in_file.close()
out_file.close()


