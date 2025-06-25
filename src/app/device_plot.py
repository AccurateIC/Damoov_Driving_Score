
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('D:/Downloadss/Sample_Table.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s' )

# Plot 1: Bar plot - number of unique device_ids
device_counts = df['device_id'].value_counts()

plt.figure(figsize=(14,6))

plt.subplot(1,2,1)
device_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Records per Device_ID')
plt.xlabel('device_id')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Plot 2: Scatter plot - device usage over time
plt.subplot(1,2,2)
for device in df['device_id'].unique():
    device_data = df[df['device_id'] == device]
    plt.scatter(device_data['timestamp'], [device]*len(device_data), label=device)

plt.title('Device Usage Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Device_ID')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
