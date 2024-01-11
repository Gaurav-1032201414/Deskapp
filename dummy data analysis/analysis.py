import numpy as np
import pandas as pd
from datetime import datetime

def filter(num, df, column=None):
    
    if column is not None:
        filtered_df  = df[df[column] > num]
        return filtered_df
    else:
        pass
    
    
import pandas as pd
from datetime import datetime

def filter_by_date(start_date, end_date, df):
    try:
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

        date_in_range = lambda x: isinstance(x, datetime) and start_date <= x.date() <= end_date

        filtered_df = df[df['UploadDate'].apply(date_in_range)]
        return filtered_df
    
    except ValueError:
        print("Error: Invalid date format. Please use the format dd-mm-yyyy.")
        return None
        


def filter_by_price(price, df, operand):
    try:
        filter_price = float(price)
        operand_mapping = {
            1: '<=',  # less than
            2: '>=',  # greater than
            3: '=='   # equal to
        }

        filtered_df = df[df['Price'].apply(lambda x: eval(f"x {operand_mapping[operand]} {filter_price}"))]

        return filtered_df

    except ValueError:
        print("Error: Invalid price format. Please enter a valid numeric value.")
        return None

       
df = pd.read_csv("dummy data analysis/dummy_data.csv")

print(df)

print('''
      Filter Formats:
      
      1. Filter By Books
      2. Filter By Price
      3. Filter By Date
      4. Custom Filter
      
      ''')
filter_format = int(input("Enter filter format (number): "))

# col = input("Enter column name: ")
# num = int(input("Enter number: "))

if filter_format == 3:
    start_date = input("Enter Start Date: ")
    end_date = input("Enter end date: ")
    print(f"\nFiltered DataFrame based on {filter_format}: {filter_by_date(start_date, end_date, df)}")
elif filter_format == 2:
    price = input("Enter the Price amount: ")
    function = int(input("1. Less Than\n2. Greater Than\n3.Equal to (number): "))
    print(f"\nFiltered DataFrame based on {filter_format}: {filter_by_price(price, df, function)}")
    
  
    


# print(f"\nFiltered DataFrame based on {filter_format}:")
# print(filter(num, df, col))





# import random
# import string

# def generate_username(length=8):
#     # Generate a random username of the specified length
#     letters_and_digits = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters_and_digits) for _ in range(length))

# # Generate 20 random usernames
# random_usernames = [generate_username() for _ in range(20)]

# # Print the generated usernames
# for i, username in enumerate(random_usernames, 1):
#     print(f"{username}")
    
    
# import random
# import string

# def generate_username():
#     # List of common words for usernames
#     words = ["happy", "sunny", "chocolate", "bird", "moon", "purple",
#              "penguin", "guitar", "ocean", "tiger", "star", "coffee"]

#     # Generate a random username by combining two words and a random number
#     username = random.choice(words) + random.choice(words) + str(random.randint(10, 99))
    
#     return username

# # Generate 20 random usernames
# usernames = [generate_username() for _ in range(20)]

# # Print the generated usernames
# for i in usernames:
#     print(i)

# from datetime import datetime, timedelta
# import random

# def generate_random_dates(start_date, end_date, num_dates):
#     date_list = []
#     for _ in range(num_dates):
#         random_days = random.randint(0, (end_date - start_date).days)
#         random_date = start_date + timedelta(days=random_days)
#         date_list.append(random_date)
#     return date_list

# # Specify the date range
# start_date = datetime(2022, 1, 1)
# end_date = datetime(2023, 12, 31)

# # Generate 20 random dates
# random_dates = generate_random_dates(start_date, end_date, 20)

# # Print the generated dates
# for date in random_dates:
#     print(date.strftime("%d-%m-%Y"))
