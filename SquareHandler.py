#Spencer Oswald

from openpyxl.descriptors.base import DateTime
from square.client import Client

class SquareHandler:

    CREDS: str
    DATES = []
    BODIES = {} #Keys are dates, bodies are request bodies
    API = None
    ENVIROMENT = "production"
    
    def get_creds(self):
        with open("creds", "r") as creds:
            self.CREDS = creds.read()
    
    def __init__(self):
        self.get_creds()
        self.DATES = ["2021-09-02"]
    
    def __init__(self, DATES: list):
        self.get_creds()
        self.DATES = DATES
    
    def connect(self):
        client = Client(access_token=self.CREDS, environment=self.ENVIROMENT)
        self.API = client.orders
    
    def generate_bodies(self):
        for date in self.DATES:
            body = {
            "location_ids": [
            "L7CEV1BC6XAZT"
            ],
            "query": {
            "filter": {
                "state_filter": {
                "states": [
                    "COMPLETED"
                ]
                },
                "date_time_filter": {
                "closed_at": {
                    "start_at": date+"T00:00:00Z",
                    "end_at": date+"T23:59:59Z"
                }
                }
            },
            "sort": {
                "sort_field": "CLOSED_AT",
                "sort_order": "ASC"
            }
            },
            "return_entries": True
            }
            self.BODIES[date] = body
    
    def get_range_totals(self):
        #Step 0, get the api, if we haven't already
        if self.API == None:
            self.connect()
        #Step 1 get order ids for every order in a day
        order_ids = {} #Keys will be dates, bodies a list of IDS
        for date in self.BODIES:
            ids = []
            result_body = ""
            result = self.API.search_orders(self.BODIES[date])
            if result.is_success(): result_body = result.body
            elif result.is_error(): print("There was a problem getting the order ids\n"+str(result.errors)); input()
            for entry in result_body:
                for j in result_body[entry]:
                    ids.append(j['order_id'])
            order_ids[date] = ids
        #Step 2: Get net amounts for each day
        net_amounts = {} #keys being dates, bodies being net amounts
        for date in order_ids:
            ids = order_ids[date]
            daily_total = 0
            for id in ids:
                result = self.API.retrieve_order(id)
                if result.is_success():
                    result_body = result.body
                    tenders = result_body['order']['tenders']
                elif result.is_error(): 
                    print("There was an error in getting the daily totals")
                    print(str(result.errors))
                tender_total = 0
                for tender in tenders:
                    gain = int(tender['amount_money']['amount'])
                    loss = int(tender['processing_fee_money']['amount'])
                    net_total = gain - loss
                    tender_total += net_total
                daily_total += tender_total
            net_amounts[date] = daily_total
        return net_amounts



                

