from faker import Faker

import random
import string
from datetime import datetime, timedelta
from collections import defaultdict
import math
import concurrent
import threading
import queue

from connect import CreateClient


def PopulateUsers(db):

    fake_users = []
    fake = Faker()

    for i in range(50):

        single_user = {}
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        role = random.choice(['engineer','consultant'])
        single_user['first_name'] = first_name
        single_user['last_name'] = last_name
        single_user['email'] = email
        single_user['phone'] = phone
        single_user['role'] = role
        single_user['password'] = 'jman'

        fake_users.append(single_user)

    db['users'].insert_many(fake_users)

def PopulateProjects(db):
    project_names = [
    "Phoenix Rising",
    "Infinite Horizons",
    "TechNova",
    "Alpha Wave",
    "NexGen Solutions",
    "EcoSphere",
    "CodeCrafters",
    "Future Forge",
    "SkyLabs",
    "DataSphere",
    "Quantum Quest",
    "SwiftEdge",
    "InnoVision",
    "OptiTech",
    "FusionWorks"
    ]
    
    fake_projects = []

    for project in project_names:
        single_project = {}

        project_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        delta = datetime(2024, 5, 31) - datetime(2024, 2, 1)
        random_days = random.randint(0, delta.days)
        random_gap = random.randint(7,120)
        random_start = datetime(2024, 2, 1) + timedelta(days=random_days)
        random_end = random_start + timedelta(days=random_gap)

        single_project['name'] = project
        single_project['PID'] = project_id
        single_project['client_name'] = random.choice( [
            "Google",
            "Apple",
            "Microsoft",
            "Amazon",
            "Facebook"
        ])
        single_project['start'] = random_start
        single_project['end'] = random_end

        fake_projects.append(single_project)
    
    db['projects'].insert_many(fake_projects)

def PopulateAssignments(db):
    all_projects = []
    all_users = []

    allocation_projects = []
    allocation_users = []
    project_start_end = {}

    allocation_set = set()

    for doc in db['projects'].find():
        all_projects.append(doc['PID'])
        project_start_end[doc['PID']] = {
            "start":doc['start'],
            "end":doc['end']
        }
    
    print(project_start_end)
    
    for doc in db['users'].find():
        all_users.append(doc['email'])
    
    for projects in all_projects:
        allocation_projects.append(projects)
    
    for users in all_users:
        allocation_users.append(users)

    for projects in range(150-len(allocation_projects)):
        allocation_projects.append(random.choice(all_projects))
    
    for users in range(150 - len(allocation_users)):
        allocation_users.append(random.choice(all_users))
    
    # print(allocation_projects)
    # print(allocation_users)

    for entry in range(len(allocation_projects)):
        project = allocation_projects[entry]
        user = allocation_users[entry]
        combination = (project,user)
        allocation_set.add(combination)
    
    fake_allocation = []
    for combination in list(allocation_set):
        proj_start = project_start_end[combination[0]]['start']
        proj_end = project_start_end[combination[0]]['end']

        allocation = {
            "email":combination[1],
            "PID":combination[0],
            "allocation_start":proj_start,
            "allocation_end":proj_end,
            "created_at":datetime.now()
        }

        fake_allocation.append(allocation)
    
    db['projectassignments'].insert_many(fake_allocation)

# def PopulateTimesheets(db):
#     project_allocations = defaultdict(dict)

#     # Fetch project allocations from the database and store them in a dictionary
#     for doc in db['projectassignments'].find():
#         project_allocations[doc['email']][doc['PID']] = {
#             "start": doc['allocation_start'],
#             "end": doc['allocation_end']
#         }

#     # Initialize start and end dates for the timesheets
#     start_date_timesheet = datetime(2024, 1, 1)
#     end_date_timesheet = datetime(2024, 1, 7)

#     fake_timesheet_entries = []
#     total = 0

#     # Loop through each week
#     for _ in range(22):
#         # Loop through each user and their project allocations
#         for user, allocations in project_allocations.items():
#             isSubmitted = random.choice([True, False])
#             numberOfEntries = random.randint(1, 3)  # Random number of entries per user

#             total_entreis_for_the_week = 0
#             # Loop to generate fake timesheet entries for the user
#             for _ in range(numberOfEntries):
#                 project = random.choice(list(allocations.keys()))  # Randomly select a project
#                 allocation = allocations[project]

#                 # Check if the project falls within the week
#                 if allocation['start'] <= end_date_timesheet and allocation['end'] >= start_date_timesheet:
#                     UID = ''.join(random.choices(string.digits, k=7))
#                     number_of_hours_per_entry = math.floor(20 / numberOfEntries)
#                     activity = random.choice(['client_project', 'sales_activity'])

#                     # Generate a fake timesheet entry
#                     single_entry = {
#                         "UID": UID,
#                         "email": user,
#                         "PID": project,
#                         "activity": activity,
#                         "comments": "Automated Filling!",
#                         "start_period": start_date_timesheet,
#                         "end_period": end_date_timesheet,
#                         "mon": random.randint(4, number_of_hours_per_entry),
#                         "tue": random.randint(4, number_of_hours_per_entry),
#                         "wed": random.randint(4, number_of_hours_per_entry),
#                         "thur": random.randint(4, number_of_hours_per_entry),
#                         "fri": random.randint(4, number_of_hours_per_entry),
#                         "sat": random.randint(0, 4),
#                         "sun": random.randint(0, 4),
#                         "visible": True,
#                         "submitted": isSubmitted
#                     }

#                     fake_timesheet_entries.append(single_entry)
#                     total += 1

#         # Move to the next week
#         start_date_timesheet += timedelta(days=7)
#         end_date_timesheet += timedelta(days=7)

#     print("Total fake timesheet entries generated:", total)

import concurrent.futures

def process_time_frame(start_date_timesheet, end_date_timesheet, project_allocations, fake_timesheet_entries):
    total = 0
    for user, allocations in project_allocations.items():
        isSubmitted = random.choice([True, False])
        numberOfEntries = random.randint(1, 3)  # Random number of entries per user

        total_entries_for_the_week = 0
        for _ in range(numberOfEntries):
            project = random.choice(list(allocations.keys()))  # Randomly select a project
            allocation = allocations[project]

            # Check if the project falls within the week
            if allocation['start'] <= end_date_timesheet and allocation['end'] >= start_date_timesheet:
                UID = ''.join(random.choices(string.digits, k=7))
                number_of_hours_per_entry = math.floor(20 / numberOfEntries)
                activity = random.choice(['client_project', 'sales_activity'])

                # Generate a fake timesheet entry
                single_entry = {
                    "UID": UID,
                    "email": user,
                    "PID": project,
                    "activity": activity,
                    "comments": "Automated Filling!",
                    "start_period": start_date_timesheet,
                    "end_period": end_date_timesheet,
                    "mon": random.randint(4, number_of_hours_per_entry),
                    "tue": random.randint(4, number_of_hours_per_entry),
                    "wed": random.randint(4, number_of_hours_per_entry),
                    "thur": random.randint(4, number_of_hours_per_entry),
                    "fri": random.randint(4, number_of_hours_per_entry),
                    "sat": random.randint(0, 4),
                    "sun": random.randint(0, 4),
                    "visible": True,
                    "submitted": isSubmitted
                }

                fake_timesheet_entries.append(single_entry)
                total_entries_for_the_week += 1
                total += 1

    print("Total fake timesheet entries generated:", total)
    
def PopulateTimesheets(db):
    project_allocations = defaultdict(dict)

    # Fetch project allocations from the database and store them in a dictionary
    for doc in db['projectassignments'].find():
        project_allocations[doc['email']][doc['PID']] = {
            "start": doc['allocation_start'],
            "end": doc['allocation_end']
        }

    fake_timesheet_entries = []

    # Initialize start and end dates for the timesheets
    start_date_timesheet = datetime(2024, 1, 1)
    end_date_timesheet = datetime(2024, 1, 7)

    # Create a thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks for each time frame
        futures = []
        for _ in range(22):
            futures.append(executor.submit(process_time_frame, start_date_timesheet, end_date_timesheet, project_allocations, fake_timesheet_entries))
            start_date_timesheet += timedelta(days=7)
            end_date_timesheet += timedelta(days=7)
        
        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            future.result() 
    
    db['timesheets'].insert_many(fake_timesheet_entries)
    print(len(fake_timesheet_entries))

    
def PopulateFunction():
    db = CreateClient()
    #PopulateUsers(db)
    #PopulateProjects(db)
    #PopulateAssignments(db)
    #PopulateTimesheets(db)

PopulateFunction()
