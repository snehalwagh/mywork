import pymongo
import sys
import csv

from pymongo import MongoClient
client = MongoClient('localhost', 10080)

db = client.oilbird
new_coll = db.OilBird3_all_interventions_master_db_v1
#coll = sys.argv[1]


def clean_data(input_l):
    output_l = [x.strip() for x in input_l if x.strip()]
    return output_l


def update_moa():
    for x in input_coll.find():
        moa = clean_data(x['MOA'].split(';'))
        i_name = x['intervention_name']
        new_synonyms = clean_data(x['Synonyms'].split(';'))
        new_synonyms_lower = [i.lower() for i in new_synonyms]
        company = x['Company']
        drug_types = clean_data(x['Class'].split(';'))
        category = "Diabetes"

        if new_coll.find_one({'intervention_name': i_name.strip()}):
            new_coll.insert({
                'intervention_name': i_name.strip(),
                'new_synonyms': new_synonyms,
                'new_synonyms_lower': new_synonyms_lower,
                'company': company,
                'drug_type_standard': drug_types,
                'target_tags': moa,
                'category': category.strip()
            })
        else:
            print i_name


if __name__ == "__main__":

    update_moa()
