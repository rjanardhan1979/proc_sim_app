import numpy as np
import simpy
import random
import copy
import pandas as pd

np.random.seed(0)

SURG_TIME = 0.0

# consignment inventory object declaration
CONS_INV = [{'surg_type': 'primary knee', 'entitlement': 8, 'onHand': 8, 'openOrder': 0, 'orderQty': 0},
            {'surg_type': 'primary hip', 'entitlement': 5, 'onHand': 6, 'openOrder': 0, 'orderQty': 0}]

# object to keep track of orders placed and received by day
O_R = [{'surg_type': 'primary knee', 'orderDay': [], 'orderQty': [], 'receiptDay': [], 'receiptQty': []},
       {'surg_type': 'primary hip', 'orderDay': [], 'orderQty': [], 'receiptDay': [], 'receiptQty': []}]

SCHED = [] #surgery schedule
LT = [2, 3, 4, 5] # lead time for product received. 4 possible values in days/
LT_PROB = [0.45, 0.3, 0.2, 0.05] # probabbility for each LT value above
TIME_HIST = [] # list to store simulation time history output
INV_HIST = [] # list to store onHand inventory history
LT_HIST = [] # list to store LT history for each order placed
temp = []
surg_on_a_day = [np.random.randint(1, 6), np.random.randint(1, 4)] # probability for number of surgery by Surgeon A and Surgeon B. Surgeon A does higher volume
surg_type_ = ['primary knee', 'primary hip'] # types of surgeries
surg_type_weights = [0.6, 0.4] # probability of each type of surgery

def generate_samples():
    surgery_type = random.choices(surg_type_, weights=surg_type_weights, k=1)
    return surgery_type[0]


# generate a sample of surgeries by Surgeon A or B for 4 weeks by day.
pid = 0
wk = 0
day_of_week = 1
day = 7*wk + day_of_week
while wk < 4:
    # append surgeon A schedule on day
    if day_of_week == 1 or day_of_week == 2 or day_of_week == 5:
        for i in range(surg_on_a_day[0]):
            SCHED.append({'patient_id': pid, 'surgeon': 'A', 'surg_day': day,
                         'surg_type': generate_samples(), 'stockout_prob': 0.})
            pid += 1
        # append surgeon B schedule on day
    if day_of_week == 2 or day_of_week == 3:
        for i in range(surg_on_a_day[1]):
            SCHED.append({'patient_id': pid, 'surgeon': 'B', 'surg_day': day,
                         'surg_type': generate_samples(), 'stockout_prob': 0.})
            pid += 1
    day_of_week += 1
    day = 7*wk + day_of_week
    if day_of_week == 8:
        day_of_week = 1
        wk += 1
        day = 7*wk + day_of_week

# define surgery class and simulation start
class Surgery:
    def __init__(self, env, schedule, inv):
        self.env = env
        self.schedule = copy.deepcopy(SCHED)
        self.cons = copy.deepcopy(CONS_INV)
        self.order_receipts = copy.deepcopy(O_R)        
        self.surgery = env.event()
        env.process(self.sEvent(self.env, self.schedule))
    
    # describes surgery event
    def sEvent(self, env, schedule):
        for index, item in enumerate(schedule):
            if index == 0:
                yield env.timeout(self.schedule[0]['surg_day'])
            
            # checks if day has changed
            if item['surg_day'] == schedule[index-1]['surg_day']:
                day_change = False
            else:
                day_change = True
            if day_change == True and index != 0:
                yield env.timeout(item['surg_day'] - schedule[index-1]['surg_day']) #moves time forward by next surgery day
            if item['surg_type'] == 'primary knee':
                c_index = 0
            else:
                c_index = 1
            if self.cons[c_index]['onHand'] > 0:
                self.surgery.succeed()
                self.cons[c_index]['onHand'] -= 1 # decrease on hand inventory by 1 for each completed surgery
            self.surgery = self.env.event()
            env.process(self.replenishOrder(self.env, c_index, index))
            TIME_HIST.append(env.now) #append final event values to time and inventory history
            INV_HIST.append(copy.deepcopy(self.cons[c_index]))

    def replenishOrder(self, env, c, i): # describes inventory replenishment process
        if self.cons[c]['onHand'] < self.cons[c]['entitlement']:
            orderQuantity = max(self.cons[c]['entitlement'] - self.cons[c]['onHand'] - self.cons[c]['openOrder'], 0)
            self.cons[c]['orderQty'] = orderQuantity
            self.cons[c]['openOrder'] += orderQuantity
            self.order_receipts[c]['orderDay'].append(env.now)
            self.order_receipts[c]['orderQty'].append(orderQuantity)
            lead_time = self.getLT()
            yield env.timeout(lead_time)
            LT_HIST.append(lead_time)
            self.order_receipts[c]['receiptDay'].append(env.now)
            self.order_receipts[c]['receiptQty'].append(orderQuantity)
            self.cons[c]['onHand'] += orderQuantity
            self.cons[c]['openOrder'] -= orderQuantity

    def getLT(self): #generate Lead Time
        lead_time = random.choices(LT, weights=LT_PROB, k=1)
        return lead_time[0]


def run(SCHED, CONS_INV):
    env = simpy.Environment()
    s = Surgery(env, SCHED, CONS_INV)
    env.run()
    for index, item in enumerate(INV_HIST):
        item['time'] = TIME_HIST[index]
    df_orderlog = pd.DataFrame()
    df = pd.DataFrame(INV_HIST)
    df_sched = pd.DataFrame(s.schedule)

    for i in range(len(s.order_receipts)):
        mydict = s.order_receipts[i]
        df_temp = pd.DataFrame(dict(list(mydict.items())[1:]))
        df_temp['surg_type'] = mydict['surg_type']
        df_orderlog = pd.concat([df_orderlog, df_temp])

    return [df, df_orderlog, df_sched]

def runApp():
    return run(SCHED, CONS_INV)



