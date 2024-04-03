import csv
from datetime import datetime
import os

data_sources_dir = 'data-sources'
table_history_file = os.path.join(data_sources_dir, 'table-history.csv')
status_changes_file = os.path.join(data_sources_dir, 'status-changes.csv')
membership_start_end_file = os.path.join(data_sources_dir, 'membership_start_end.csv')

# First read in the data
table_history = []
status_changes = []
with open(table_history_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        table_history.append(row)
with open(status_changes_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        status_changes.append(row)

# Then parse table_history data to get the membership data
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
    except ValueError:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return None
memberships = {}
for row in table_history:
    customer_id = row[1]
    changes = row[3].split('@#@#@#')
    for change in changes:
        if change:
            attr, old_value, new_value = change.split('-^!^!^-')
            if attr == 'customer_type':
                if new_value == 'MEMBER':
                    memberships.setdefault(customer_id, []).append({'start_date': None, 'end_date': None, 'end_reason': None})
            elif attr == 'membership_start_date':
                new_value = new_value.strip()  # Remove trailing whitespace
                if new_value:
                    memberships[customer_id][-1]['start_date'] = parse_date(new_value)
            elif attr == 'membership_exp_date':
                new_value = new_value.strip()  # Remove trailing whitespace
                if new_value:
                    memberships[customer_id][-1]['end_date'] = parse_date(new_value)
                    memberships[customer_id][-1]['end_reason'] = 'expire'

# Update membership end dates and reasons based on status_changes
for row in status_changes:
    customer_id = row[1]
    status = row[3]
    start_date = row[4].strip()  # Remove trailing whitespace
    if start_date:
        start_date = parse_date(start_date)
        if customer_id in memberships:
            for membership in memberships[customer_id]:
                if not membership['end_date'] or membership['end_date'] > start_date:
                    membership['end_date'] = start_date
                    if status == 'FREEZE':
                        membership['end_reason'] = 'freeze'
                    elif status == 'TERMINATE':
                        membership['end_reason'] = 'cancel'

# Write output to a new CSV file
with open('membership_start_end.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['customer_id', 'start_date', 'end_date', 'end_reason'])
    for customer_id, memberships_list in memberships.items():
        for membership in memberships_list:
            csv_writer.writerow([customer_id, membership['start_date'], membership['end_date'], membership['end_reason']])