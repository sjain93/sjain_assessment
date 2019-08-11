##Installs

To run the dependencies in this program, you may use the pipfile provided. Using pip:

pip install pipenv
pipenv shell 
(To activate the environment)

Alternatively, you may pip install the requirements.txt file

## Running the program
Given that the input.txt file and a blank output.txt file are provided in the same directory

python sjain_assess.py 

Will populate the output file with the required JSON ouput to test whether the load was successful or not.

##Structure and Logic explanation
I use a dictionary to track each customer based on their ID,  broke the loading attempt into several checks.
attempt_tracking[customer_id] = {
                'transaction': transaction_id,
                'weekly_amount': load_amount,
                'daily_amount': load_amount,
                'daily_count': 1,
                'weekly_attempt_log': [iso_time]
            }
If this key-value pair does not exist for that load attempt, it is updated into the 