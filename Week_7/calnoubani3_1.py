import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Analyze influenza hospitalization rates.')
parser.add_argument('--file', required=True, help='Path to the input CSV file')
args = parser.parse_args()

# Load and clean the dataset
file_path = args.file
flu_data = pd.read_csv(file_path, skiprows=2, delimiter=',')
flu_data = flu_data.dropna(subset=['YEAR'])
flu_data['YEAR'] = flu_data['YEAR'].str[:4].astype(int)

def plot_pre_post_pandemic(data):
    # Filter overall rates
    overall_data = data[
        (data['SEX CATEGORY'] == 'Overall') & 
        (data['AGE CATEGORY'] == 'Overall') & 
        (data['RACE CATEGORY'] == 'Overall')
    ]

    # Aggregate the cumulative rates by year
    yearly_data = overall_data.groupby('YEAR')['CUMULATIVE RATE'].mean().reset_index()

    # Split data into before and after 2020
    pre_2020_data = yearly_data[yearly_data['YEAR'] < 2020]
    post_2020_data = yearly_data[yearly_data['YEAR'] >= 2020]

    # Plot the hospitalization trends
    plt.figure(figsize=(10, 6))
    plt.plot(pre_2020_data['YEAR'], pre_2020_data['CUMULATIVE RATE'], marker='o', label='2009-2019')
    plt.plot(post_2020_data['YEAR'], post_2020_data['CUMULATIVE RATE'], marker='o', label='2020-2024', linestyle='--')
    plt.title('Influenza Hospitalization Rates Before and After 2020')
    plt.xlabel('Year')
    plt.ylabel('Average Cumulative Hospitalization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def plot_age_group_comparison(data):
    # Updated age groups for filtering
    age_groups_under_20 = ['0-4 yr', '5-17 yr', '1-4 yr', '5-11  yr', '12-17 yr', '< 18']
    age_groups_over_40 = ['40-49 yr', '50-64 yr', '65-74 yr', '75-84 yr', '>= 65 yr', '>= 85', '>= 75']

    # Filter the data for these age groups
    under_20_data = data[
        data['AGE CATEGORY'].isin(age_groups_under_20) & 
        (data['SEX CATEGORY'] == 'Overall') & 
        (data['RACE CATEGORY'] == 'Overall')
    ]

    over_40_data = data[
        data['AGE CATEGORY'].isin(age_groups_over_40) & 
        (data['SEX CATEGORY'] == 'Overall') & 
        (data['RACE CATEGORY'] == 'Overall')
    ]

    # Aggregate cumulative rates by year for each group
    under_20_yearly = under_20_data.groupby('YEAR')['CUMULATIVE RATE'].mean().reset_index()
    over_40_yearly = over_40_data.groupby('YEAR')['CUMULATIVE RATE'].mean().reset_index()

    # Plot the comparison between the two groups
    plt.figure(figsize=(10, 6))
    plt.plot(under_20_yearly['YEAR'], under_20_yearly['CUMULATIVE RATE'], marker='o', label='Under 20 Years')
    plt.plot(over_40_yearly['YEAR'], over_40_yearly['CUMULATIVE RATE'], marker='o', label='Over 40 Years', linestyle='--')
    plt.title('Influenza Hospitalization Rates: Under 20 vs Over 40')
    plt.xlabel('Year')
    plt.ylabel('Average Cumulative Hospitalization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

# Call the functions
plot_pre_post_pandemic(flu_data)
plot_age_group_comparison(flu_data)
