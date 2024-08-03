import pandas as pd

df = pd.read_csv('SIMPLII.csv')

print(df.head())
print("Column Names:", df.columns.tolist())
df['Date'] = pd.to_datetime(df['Date'])
filtered_df = df[df['Date'] > '2024-01-01']

# Calculate the sums of the 'FUNDS IN' and 'FUNDS OUT' columns
funds_in_sum = filtered_df[' Funds In '].sum()
funds_out_sum = filtered_df[' Funds Out'].sum()

# Print the sums
print(f"Sum of FUNDS IN: {funds_in_sum}")
print(f"Sum of FUNDS OUT: {funds_out_sum}")
