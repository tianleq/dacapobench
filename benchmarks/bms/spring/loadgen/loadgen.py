#!/usr/bin/env python3
#
# Generate a load for PetClinic app within spring workload.
#
# Creates two files:
#    requests.txt  (which will be included in downloads/spring-data.zip)
#    data.sql      (which will be used to replace src/main/resources/db/h2/data.sql)
# 
# Each line of requests.txt encodes a get or post request that will be issued by the client.
# data.sql will create the initial state of the petclinic database.   The schema for the 
# database is in src/main/resources/db/h2/schema.sql
#
from random import choice, randrange, random, shuffle
from time import mktime, strptime, strftime, localtime


pet_kinds = ["cat", "dog", "bird", "snake", "hamster", "guinea pig", "lizard", "fish"]
reasons = ["check up", "neutered", "injury", "vaccination"]
pet_names = []
given_names = []
family_names = []
town_names = []

def init():
    global family_names
    with open('family.txt') as f:
        family_names = f.read().splitlines()
    global given_names
    with open('given.txt') as f:
        given_names = f.read().splitlines()
    global town_names
    with open('towns.txt') as f:
        town_names = f.read().splitlines()
    global pet_names
    with open ('petnames.txt') as f:
        pet_names = f.read().splitlines()


def random_street_address():
    st_types = ['St.', 'Rd.', 'Ave.', 'Pl.', 'Blvd']
    return str(randrange(1,1000))+" "+choice(family_names)+" "+choice(st_types)


def random_date(start, end, dash):
    fmt = '%Y-%m-%d' if dash else '%Y/%m/%d'  # '-' for sql, '/' for http
    s = mktime(strptime(start, fmt))
    e = mktime(strptime(end, fmt))
    date = s + random() * (e - s)
    return strftime(fmt, localtime(date))

class Owner:
    def __init__(self):
        self.given = choice(given_names)
        self.family = choice(family_names)
        self.street = random_street_address()
        self.town = choice(town_names)
        self.phone = randrange(400000000,500000000)
        self.pets = []
        self.sessions = choice([[0, 0, 1, 1, 2, 2, 3, 3],[0, 0, 1, 1, 1, 1, 1, 4],[0, 0, 1, 1, 1, 1, 1, 5]])
        shuffle(self.sessions)

    def as_sql(self, id):
        return "INSERT INTO owners VALUES ("+str(id)+", '"+self.given+"', '"+self.family+"', '"+self.street+"', '"+self.town+"', '"+str(self.phone)+"');"

class Pet:
    def __init__(self, owner_id):
        self.name = choice(pet_names)
        self.dob = random_date('2010-01-01', '2022-06-01', True)
        self.kind = 1 + randrange(len(pet_kinds))
        self.owner = owner_id
    def as_sql(self, id):
        return "INSERT INTO pets VALUES ("+str(id)+", '"+self.name+"', '"+self.dob+"', "+str(self.kind)+", "+str(self.owner)+");"

class Visit:
    def __init__(self, pet, petid):
        self.owner = pet.owner
        self.petid = petid
        self.date = random_date(pet.dob, '2022-08-01', True)
        self.desc = choice(reasons)
    def as_sql(self, idx):
        return "INSERT INTO visits VALUES ("+str(idx+1)+", "+str(self.petid)+", '"+self.date+"', '"+str(self.desc)+"');"


def gen_session(owner_id, owners, pet_id, pets, idx):
    dummy_digest = "     0 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX "
    generic = ["G/resources/css/petclinic.css","G/resources/images/favicon.png","G/resources/images/pets.png","G/webjars/jquery/2.2.4/jquery.min.js","G/vets.html","G/owners/find"]
    match idx:
        case 0:
            return dummy_digest+"G/\n" + dummy_digest + choice(generic)
        case 1:
            return dummy_digest + choice(generic) +"\n" + dummy_digest + choice(generic)
        case 2:
            return dummy_digest + "G/owners/"+str(owner_id)+"\n" + dummy_digest + "G/owners/"+str(owner_id)+"/edit"
        case 3:
            return dummy_digest + "G/owners?lastName="+owners[owner_id-1].family+"\n" + dummy_digest + "G/owners/"+str(owner_id)
        case 4:
            ses = dummy_digest + "G/owners/"+str(owner_id)+"/pets/"+str(pet_id)+"/visits/new\n"
            ses = ses + dummy_digest + "P/owners/"+str(owner_id)+"/pets/"+str(pet_id)+"/visits/new/"
            ses = ses + "&date="+random_date('2022-06-01','2022-12-01', False)
            ses = ses + "&description="+choice(reasons)
            return ses
        case 5:
            ses = dummy_digest + "G/owners/"+str(owner_id)+"/edit\n"
            ses = ses + dummy_digest + "P/owners/"+str(owner_id)+"/edit/"
            ses = ses + "&firstName="+choice(given_names)+"&lastName="+owners[owner_id-1].family+"&address="+random_street_address()+"&telephone="+str(owners[owner_id-1].phone)
            return ses
            """
generic:
    home
    css
    favicon
    pets.png
    js
    vets.html
    find owner page

owner-specific:
    view owner
    find owner by last name
    edit owner

    pet-specific:
        2 new visit

"""

def dump_sql(owners, pets, visits):
    with open("data.sql", "w") as f:

        print("INSERT INTO vets VALUES (1, 'James', 'Carter');", file=f)
        print("INSERT INTO vets VALUES (2, 'Helen', 'Leary');", file=f)
        print("INSERT INTO vets VALUES (3, 'Linda', 'Douglas');", file=f)
        print("INSERT INTO vets VALUES (4, 'Rafael', 'Ortega');", file=f)
        print("INSERT INTO vets VALUES (5, 'Henry', 'Stevens');", file=f)
        print("INSERT INTO vets VALUES (6, 'Sharon', 'Jenkins');", file=f)
        print("", file=f)
        print("INSERT INTO specialties VALUES (1, 'radiology');", file=f)
        print("INSERT INTO specialties VALUES (2, 'surgery');", file=f)
        print("INSERT INTO specialties VALUES (3, 'dentistry');", file=f)
        print("", file=f)
        print("INSERT INTO vet_specialties VALUES (2, 1);", file=f)
        print("INSERT INTO vet_specialties VALUES (3, 2);", file=f)
        print("INSERT INTO vet_specialties VALUES (3, 3);", file=f)
        print("INSERT INTO vet_specialties VALUES (4, 2);", file=f)
        print("INSERT INTO vet_specialties VALUES (5, 1);", file=f)
        
        print("", file=f)
        for i in range(len(pet_kinds)):
            print("INSERT INTO types VALUES ("+str(i+1)+",'"+pet_kinds[i]+"');", file=f)

        print("", file=f)
        for i in range(len(owners)):
            print(owners[i].as_sql(i+1), file=f)

        print("", file=f)
        for i in range(len(pets)):
            id = i + 1
            print(pets[i].as_sql(id), file=f)

        print("", file=f)
        for i in range(len(visits)):
            id = i + 1
            print(visits[i].as_sql(id), file=f)

def main():
    print("Hi")
    init()
    print(pet_names[0])
    print(town_names[0])

    owners = []
    for i in range(8192):
        owners.append(Owner())

    pets = []
    for i in range(len(owners)):
        for j in range(1+randrange(2)):
            pets.append(Pet(i+1))
            owners[i].pets.append(len(pets))

    visits = []
    for i in range(len(pets)):
        visits.append(Visit(pets[i], i+1))

    dump_sql(owners, pets, visits)

    with open("requests.txt", "w") as f:
        for i in range(8):
            for j in range(len(owners)):
                print(gen_session(j+1, owners, choice(owners[j].pets), pets, owners[j].sessions[i]), file=f)

if __name__ == "__main__":
    main()