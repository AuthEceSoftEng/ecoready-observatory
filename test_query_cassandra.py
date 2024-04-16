from cassandra.cluster import Cluster
from datetime import datetime, timedelta

# Connect to Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect('eeris')

# Calculate the range of days for the last month
current_date = datetime.today()
first_day_of_current_month = current_date.replace(day=1)
first_day_of_next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
last_day_of_current_month = first_day_of_next_month - timedelta(days=1)
# Iterate over each day of the last month and sum the counts
total_count = 0
current_day = first_day_of_current_month
while current_day <= last_day_of_current_month:
    formatted_day = current_day.strftime('%Y-%m-%d')
    query = f"SELECT count(*) FROM eeris.eeris_table WHERE id = '373' AND day = '{formatted_day}'"
    print(query)
    result = session.execute(query)
    total_count += result[0].count
    current_day += timedelta(days=1)

print(f"Total count for id '374' for the last month: {total_count}")

# Close the connection
cluster.shutdown()

