import pandas as pd
from tqdm import tqdm
import peewee
from peewee import *
import sqlCredentials

#performing database population using peewee orm mapping

#database connection string
db = MySQLDatabase(sqlCredentials.name, user=sqlCredentials.user, passwd=sqlCredentials.password, port=sqlCredentials.port)

#BaseModel is a subclass of Model class. Model class comes from the PeeWee library. Class is intended to serve as a base class for all other models defined later.
class BaseModel(Model):
    class Meta:
        database = db    #all model classes derived from the BaseModel subclass will use the same database connection as specified in line 10. Ensures all models share the same database connection to operate on the same database.

#Publications class is a subclass of the BaseModel Class. Represents a database for storing publication info.
class Publications(BaseModel):
    #each variable is a column in the database
    authid = IntegerField(db_column='authid', null=False) #authid is a class attribute, so it belongs to the Publications class and is shared amoungst all instances in the class and can be accessed by using the same class name.
    authname, title, authors = TextField(db_column='authname', null=False), TextField(db_column='title', null=False, primary_key=True), TextField(db_column='authors', null=False)
    year, journal, source, raw = IntegerField(db_column='year', null=False), TextField(db_column='journal', null=False), TextField(db_column='source', null=False), TextField(db_column='raw', null=False)

#Citations class is a subclass of the BaseModel Class
class Citations(BaseModel):
    title, year, journal, citation_count = TextField(db_column='title', null=False), IntegerField(db_column='year', null=False), TextField(db_column='journal', null=False), IntegerField(db_column='citation_count', null=False)

class CVPersonalWebsites(BaseModel):
    class Meta:
        db_table = 'CV_personal_websites'

    authname = TextField(db_column='authname', null=False)
    website1_url, website2_url, website3_url, website4_url, website5_url = TextField(db_column='website1_url', null=False), TextField(db_column='website2_url', null=False), TextField(db_column='website3_url', null=False), TextField(db_column='website4_url', null=False), website5_url = TextField(db_column='website5_url', null=False)
    website1_raw, website2_raw, website3_raw = TextField(db_column='website1_raw', null=False), TextField(db_column='website2_raw', null=False), TextField(db_column='website3_raw', null=False)
    website4_raw, website5_raw = TextField(db_column='website4_raw', null=False), TextField(db_column='website5_raw', null=False)
    full_name, publication = TextField(db_column="full_name", null=False), TextField(db_column="publication", null=False)


def populate_publications(file_name):
    data, data = pd.read_csv(file_name), data.fillna(-1)

    for index, row in tqdm(data.iterrows()):
        authid, authname, title, authors, year,journal = row['UID'], row["NameFirst"] + " " + row["NameLast"], row["article_title"], row["authors"], row["year"], row["journal"]
        source, raw = "Google Scholar", row["reference"]

        try:
            Publications.create(authid=authid, authname=authname, title=title, authors=authors, year=year, journal=journal, source=source, raw=raw)
        except Exception as e:
            print(e)
            print("Interrupted at index: " + str(index))


def populate_citations(file_name):
    data, data = pd.read_csv(file_name), data.fillna(-1)
    for index, row in tqdm(data.iterrows()):
        title, year, journal, citation_count = row['article_title'], row['year'], row['journal'], row['citations']
        try:
            Citations.create(title=title, year=year, journal=journal, citation_count=citation_count)
        except Exception as e:
            print(e)
            print("Interrupted at index: " + str(index))


def populate_CVs(file_name):
    data, data = pd.read_csv(file_name), data.fillna(-1)
    for index, row in tqdm(data.iterrows()):
        authname = row['Input.name']
        website1_url, website2_url, website3_url, website4_url, website5_url = row['top_1_url'], row['top_2_url'], row['top_3_url'], row['top_4_url'], row['top_5_url']
        website1_raw, website2_raw, website3_raw, website4_raw, website5_raw = row['top_1_raw'], row['top_2_raw'], row['top_3_raw'], row['top_4_raw'], row['top_5_raw']
        publication, name, name_split = row['unconfirmed_publications'], row["Input.name"], name.split('-')
        # Handle cases like "Donald-Mac Lump"
        if len(name_split) == 2:
            full_name = " ".join(name_split)
        else:
            initials = row["Google Scholar Middle Initial"]
            if isinstance(initials, int):
                full_name = name
            else:
                middle, first, last, full_name = initials[1], name_split[0].split()[0], name_split[0].split()[1], first + " " + middle + " " + last
        try:
            CVPersonalWebsites.create(authname=authname,
                                      website1_url=website1_url,
                                      website2_url=website2_url,
                                      website3_url=website3_url,
                                      website4_url=website4_url,
                                      website5_url=website5_url,
                                      website1_raw=website1_raw,
                                      website2_raw=website2_raw,
                                      website3_raw=website3_raw,
                                      website4_raw=website4_raw,
                                      website5_raw=website5_raw,
                                      publication=publication,
                                      full_name=full_name)
        except Exception as e:
            print(e)
            print("Interrupted at index: " + str(index))

#script entrypoint that connects to the database, calls data population functions to populate the tables, and closes the database connection with db.close()
def main():
    db.connect()
    # populate_publications('NESCent_publications/nescent_ID.csv')
    # populate_citations('Stage_1/NESCent_ID_citations.csv')
    # populate_CVs("Stage_2/turk_grouped.csv")

    db.close()

if __name__ == "__main__":
    main()

