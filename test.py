import random
from datetime import datetime, timedelta
car_models = ["KWID", "Triber", "Kiger", "Elevate", "C40", "EVA", "Thar", "Palisade", "M3", "X-Trail" ]
details = {}
# access carId



# print(details)
def add_details(num):
    random_days = random.randint(1, 365)
    random_date = datetime.now() - timedelta(days=random_days)
    details[len(details)] = {
        "carID": str(num),
        'model':random.choice(car_models),
        'dateOfRegistration': random_date.strftime("%Y-%m-%d"),
        'phoneNumber': random.randint(1111111111,9999999999)
    }


def check_details(num):
    for i in details:
        if details[i]['carID'] == num:
            return True
    return False

def print_details(num):
    for i in details:
        if details[i]['carID'] == num:
            return (details[i])

def main(num):
    if not check_details(num):
        add_details(num)
        return print_details(num)
    else:
        return print_details(num)

# if __name__ == '__main__':
#     print(main('TR03K0325'))
#     # print(details)

