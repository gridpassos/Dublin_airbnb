from dublin_airbnb import execute_top_rated, execute_plot_response, execute_cleanliness_listings  # noqa

print('=' * 30)
print(f'{" AIRBNB LISTING ":~^30}')
print('=' * 30)

min_nights = input('Type the minimum nights: ').strip()
bookable = input('Bookable? [yes/no]: ').lower().strip()
print('-' * 30)

while True:
    if not min_nights.isnumeric():
        print('Error, type a valid numeric.')
        min_nights = input('Type the minimum nights: ').strip()
        print('-' * 30)
    else:
        break

while True:
    if bookable == 'no':
        print('Booking not avaliable!')
        break

    elif bookable == 'yes':
        break

    else:
        print('Error, type "yes" or "no".')
        bookable = input('Bookable? [Yes/No]: ').lower().strip()
        print('-' * 30)

execute_top_rated(int(min_nights), bookable)

print('-' * 30)
print("The cleanliness rating scores,please insert the range that you would like to see below ")
listings_start = input('Type the start value: ').strip()
listings_end = input('Type the end value: ').strip()
print('-' * 30)

while True:
    if not listings_start.isnumeric():
        print('Error, type a number.')
        listings_start = input('Type the start value: ').strip()
        print('-' * 30)

    else:
        break

while True:
    if not listings_end.isnumeric():
        print('Error, type a number.')
        listings_end = input('Type the end value: ').strip()
        print('-' * 30)
    else:
        break

execute_cleanliness_listings(int(listings_start)+1, int(listings_end))

print('-' * 30)

plot_response = input(
    'Would you like see the Plot? [yes/no]: ').lower().strip()

while True:
    if plot_response == 'yes':
        execute_plot_response()
    else:
        print('Your choise was no see the plot.')
        print('=' * 30)
        break
