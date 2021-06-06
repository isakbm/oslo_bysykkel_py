#!/usr/bin/python

import json
from oslo_bysykkel import API

# feel free to change the client_identifier
api = API(client_identifier='OSLO-ORIGO-APPLICANT-CODE-CHALLENGE')

summary = api.get_summary_dict()

print(json.dumps(summary, indent='    ', ensure_ascii=False))





