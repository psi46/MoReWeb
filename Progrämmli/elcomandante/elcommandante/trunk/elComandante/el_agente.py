# elCliente: Base class for all elComandante clients
#
# The class presents an interface to elComandante that all possible
# agents (el_agente) that supervise clients have to implement.

class el_agente():
    def __init__(self, timestamp, log, sclient):
        self.timestamp = timestamp
        self.log = log
        self.sclient = sclient
        self.active = 0
        self.pending = False
        self.agente_name = "el_agente"
        self.client_name = "client"
        self.subscription = "/el_agente"
        self.Directories={}
        self.test = None
    def setup_configuration(self, conf):
        return True
    def send(self,message):
        try:
            self.sclient.send(self.subscription,message)
        except:
            pass
    def setup_initialization(self, init):
        return True
    def setup_dir(self,Directories):
        self.Directories = Directories
    def check_logfiles_presence(self):
        # Returns a list of logfiles present in the filesystem
        return []
    def check_client_running(self):
        # Check whether a client process is running
        return False
    def start_client(self, timestamp):
        self.timestamp = timestamp
        # Start a client process
        return False
    def subscribe(self):
        if (self.active):
            self.sclient.subscribe(self.subscription)
    def check_subscription(self):
        # Verify the subsystem connection
        if (self.active):
            return self.sclient.checkSubscription(self.subscription)
        return True
    def request_client_exit(self):
        # Request the client to exit with a command
        # through subsystem
        return False
    def kill_client(self):
        # Kill a client with a SIGTERM signal
        return False
    def set_test(self, test):
        self.test = test
    def prepare_test(self, test, environment):
        # Run before a test is executed
        return False
    def execute_test(self):
        # Initiate a test
        return False
    def cleanup_test(self):
        # Run after a test has executed
        return False
    def final_test_cleanup(self):
        # Cleanup after all tests have finished to return
        # everything to the state before the test
        return False
    def check_finished(self):
        # Check whether the client has finished its task
        # but also check for errors and raise an exception
        # if one occurs.
        return not self.pending
