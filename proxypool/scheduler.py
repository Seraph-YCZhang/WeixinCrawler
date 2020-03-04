TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

API_PORT = 5555

from multiprocessing import Process
from api import app
from tester import Tester
from getter import Getter
import time
class Scheduler():
    def set_tester(self, cycle = TESTER_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)
    
    def set_getter(self, cycle = GETTER_CYCLE):
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)
    
    def set_api(self):
        app.run(port=API_PORT)
    
    def run(self):
        print("PROXY POOL IS RUNNING")
        if TESTER_ENABLED:
            tester_process = Process(target=self.set_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.set_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.set_api)
            api_process.start()

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()