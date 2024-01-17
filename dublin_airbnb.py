import matplotlib
import pandas as pd
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# Load the Airbnb dataset
df = pd.read_csv('airbnb_listings.csv')


def top_rated_airbnbs(df, min_nights, instant_bookable, top_n=10):
    filtered_df = df[(df['minimum_nights'] >= min_nights) &
                     (df['instant_bookable'] == 't')]

    if filtered_df.empty:
        filtered_df = df[df['minimum_nights'] >= min_nights]

    top_listings = filtered_df.sort_values(
        by='review_scores_rating', ascending=False).head(top_n)

    return top_listings[['name', 'review_scores_rating', 'minimum_nights', 'instant_bookable']]  # noqa


def plot_response(df):
    if df['host_response_rate'].dtype != 'O':
        df['host_response_rate'] = df['host_response_rate'].astype(str)

    df['host_response_rate'] = df['host_response_rate'].replace('nan', np.nan)

    df['host_response_rate'] = pd.to_numeric(
        df['host_response_rate'].str.rstrip('%'), errors='coerce')

    plt.figure(figsize=(12, 8))

    sns.scatterplot(
        x='host_response_time',
        y='host_response_rate',
        data=df,
        hue='host_response_time',
        palette='viridis',
        s=100,
    )

    plt.title('Host Response Rate vs. Host Response Time')
    plt.xlabel('Host Response Time')
    plt.ylabel('Host Response Rate (%)')

    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))

    plt.legend().remove()

    # Show the plot
    plt.show(block=False)
    plt.pause(0.1)
    input("Press Enter to close the plot...")
    plt.close()


def airbnbs_in_dublin(df, review_score_threshold):
    dublin_listings = df[(df['neighbourhood'] == 'Dublin') & (
        df['review_scores_cleanliness'] > review_score_threshold)]
    return dublin_listings.shape[0]


def execute_dublin_cleanliness(review_score_threshold):
    high_cleanliness_listings = airbnbs_in_dublin(df, review_score_threshold)

    if high_cleanliness_listings > 0:
        print(
            f'Number of Airbnbs in Dublin with review score > {review_score_threshold}: {high_cleanliness_listings}')
    else:
        print('No listings match the criteria.')


def cleanliness_ratings_for_listings(df, start, end):
    cleanliness_scores = df.loc[start-1:end-1,
                                ['name', 'review_scores_cleanliness']]
    return cleanliness_scores


def execute_top_rated(min_nights, instant_bookable):
    result = top_rated_airbnbs(df, min_nights, instant_bookable)
    print(result)


def execute_plot_response():
    plot_response(df)


def execute_cleanliness_listings(start, end):
    result = cleanliness_ratings_for_listings(df, start, end)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Perform analysis and visualize data for Airbnb listings.')

    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )

    parser_top_rated = subparsers.add_parser(
        'top_rated',
        help='Get top-rated Airbnb\'s'
    )
    parser_top_rated.add_argument(
        '--min_nights',
        type=int,
        required=True,
        help='Minimum nights to stay'
    )
    parser_top_rated.add_argument(
        '--instant_bookable',
        type=str,
        required=True,
        help='Instant bookable (yes or no)'
    )

    parser_plot_response = subparsers.add_parser(
        'plot_response',
        help='Plot host response rate vs. response time'
    )

    parser_dublin_cleanliness = subparsers.add_parser(
        'dublin_cleanliness',
        help='Get count of Airbnb\'s in Dublin with cleanliness rating'
    )
    parser_dublin_cleanliness.add_argument(
        '--cleanliness_rating',
        type=float,
        required=True,
        help='Cleanliness rating threshold'
    )

    parser_cleanliness_listings = subparsers.add_parser(
        'cleanliness_listings',
        help='Get cleanliness ratings for specified listings'
    )
    parser_cleanliness_listings.add_argument(
        '--start',
        type=int,
        required=True,
        help='Starting listing index'
    )
    parser_cleanliness_listings.add_argument(
        '--end',
        type=int,
        required=True,
        help='Ending listing index'
    )

    args = parser.parse_args()

    if args.command == 'top_rated':
        execute_top_rated(args.min_nights, args.instant_bookable)
        plot_response = input(
            'Would you like to see the Plot? [yes/no]: ').lower().strip()

        if plot_response == 'yes':
            execute_plot_response()
        else:
            print('Your choice was not to see the plot.')
            print('=' * 30)


