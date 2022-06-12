import os
import json
from araneae.wrapper import Araneae
from utils.spider_connectors import *
from configure import *
from dto.sample import *


CURRENT_TYPE = 'binary-gender'
BINARY_PATH = os.path.join(QUERY_TYPES_PATH, 'binary.json')
ANALYSIS_PATH = os.path.join(ROOT_PATH, 'resources', 'results', 'reports', 'binary', f"{CURRENT_TYPE}.txt")


with open(BINARY_PATH, "r", encoding='utf-8') as file_input:
    binary = json.load(file_input)


current_triples = []
ru_spider = RuSpiderDB()
for db, db_content in binary.items():
    for table, table_content in db_content.items():
        for column, column_content in table_content.items():
            if column_content["type"] == CURRENT_TYPE:
                current_triples.append(Triple(db, table, column))

with open(ANALYSIS_PATH, 'w', encoding='utf-8') as anf:
    for _triple in current_triples:
        values = ru_spider.get_values(_triple.db, _triple.table, _triple.column)
        values = list(set(values))
        anf.writelines(str(_triple))
        anf.write('\n')
        for _value in values:
            anf.writelines(f"    {_value}\n")

bad_triples = [
    Triple(db='customers_and_products_contacts', table='Customer_Orders', column='order_status_code'),
    Triple(db='voter_2', table='Voting_record', column='Election_Cycle'),
    Triple(db='medicine_enzyme_interaction', table='enzyme', column='Location'),
    Triple(db='driving_school', table='Lessons', column='lesson_status_code'),
    Triple(db='election_representative', table='representative', column='Party'),
    Triple(db='entertainment_awards', table='nomination', column='Result'),
    Triple(db='insurance_and_eClaims', table='Claims_Processing_Stages', column='Claim_Status_Name'),
    Triple(db='loan_1', table='customer', column='acc_type'),
    Triple(db='local_govt_and_lot', table='Things', column='service_details'),
    Triple(db='local_govt_in_alabama', table='Participants', column='Participant_Type_Code'),
    Triple(db='local_govt_in_alabama', table='Events', column='Event_Details'),
    Triple(db='musical', table='musical', column='Result')
]