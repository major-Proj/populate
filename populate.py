from faker import Faker

import random
import string
from datetime import datetime, timedelta

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
        delta = proj_end - proj_start
        random_days = random.randint(0, delta.days)
        random_start = proj_start + timedelta(days=random_days)

        allocation = {
            "email":combination[1],
            "PID":combination[0],
            "allocation_start":random_start,
            "allocation_end":proj_end,
            "created_at":datetime.now()
        }

        fake_allocation.append(allocation)
    
    db['projectassignments'].insert_many(fake_allocation)


    


def PopulateFunction():
    db = CreateClient()
    #PopulateUsers(db)
    #PopulateProjects(db)
    PopulateAssignments(db)

PopulateFunction()
