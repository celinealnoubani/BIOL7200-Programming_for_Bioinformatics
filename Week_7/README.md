# Week 7: Data Visualization with Pandas & Matplotlib

## Topics Covered
- Data analysis with pandas
- Data visualization with matplotlib
- Argument parsing with argparse
- Analyzing public health datasets

## Main Script: calnoubani3_1.py

Analyzes influenza hospitalization rates from CDC FluSurv-NET data.

```python
import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Analyze influenza hospitalization rates.')
parser.add_argument('--file', required=True, help='Path to the input CSV file')
args = parser.parse_args()

# Load and clean dataset
flu_data = pd.read_csv(args.file, skiprows=2, delimiter=',')
flu_data['YEAR'] = flu_data['YEAR'].str[:4].astype(int)
```

## Visualizations Generated

### 1. Pre/Post-Pandemic Comparison
`pre_post_pandemic_comparison.png`

Compares influenza hospitalization rates before (2009-2019) and after (2020-2024) the COVID-19 pandemic.

```python
def plot_pre_post_pandemic(data):
    pre_2020 = yearly_data[yearly_data['YEAR'] < 2020]
    post_2020 = yearly_data[yearly_data['YEAR'] >= 2020]

    plt.plot(pre_2020['YEAR'], pre_2020['CUMULATIVE RATE'], label='2009-2019')
    plt.plot(post_2020['YEAR'], post_2020['CUMULATIVE RATE'], label='2020-2024')
```

### 2. Age Group Comparison
`influenza_age_comparison.png`

Compares hospitalization rates between age groups (Under 20 vs Over 40).

```python
def plot_age_group_comparison(data):
    age_groups_under_20 = ['0-4 yr', '5-17 yr', '< 18']
    age_groups_over_40 = ['40-49 yr', '50-64 yr', '>= 65 yr']

    # Filter and aggregate by age group
    under_20_yearly = under_20_data.groupby('YEAR')['CUMULATIVE RATE'].mean()
    over_40_yearly = over_40_data.groupby('YEAR')['CUMULATIVE RATE'].mean()
```

## Data Analysis

| Dataset | Source |
|---------|--------|
| Influenza hospitalizations | CDC FluSurv-NET |
| Time period | 2009-2024 |
| Categories | Age, Sex, Race |

## Key Pandas Operations

```python
# Read CSV with skip rows
df = pd.read_csv(file, skiprows=2)

# Filter data
filtered = df[df['COLUMN'] == 'value']

# Group and aggregate
df.groupby('YEAR')['RATE'].mean()

# Multiple conditions
data[(data['SEX'] == 'Overall') & (data['AGE'] == 'Overall')]
```

## Key Matplotlib Operations

```python
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', label='Label')
plt.title('Title')
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.legend()
plt.grid(True)
plt.savefig('output.png')
```

## Output Files

| File | Description |
|------|-------------|
| `calnoubani3_1a.png` | Pre/post pandemic visualization |
| `calnoubani3_1b.png` | Age group comparison |
| `pre_post_pandemic_comparison.png` | Trend analysis |
| `influenza_age_comparison.png` | Age stratified analysis |

## Key Findings
- COVID-19 pandemic significantly impacted influenza patterns
- Older age groups (>40) show higher hospitalization rates
- Hospitalization trends shifted post-2020

## Learning Outcomes
- Load and clean real-world datasets with pandas
- Create publication-quality visualizations with matplotlib
- Use argparse for command-line interfaces
- Analyze epidemiological data
- Filter and aggregate data by categories
