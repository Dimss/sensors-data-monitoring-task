import unittest
from sensors import sensors, simulator
from config import config


class TestSensors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cfg = config.load_config()
        cls.simulator_socket = "/tmp/simulator.sock"
        cls.sim = simulator.MetricsSimulator(cls.simulator_socket)
        cls.sim.start()

    @classmethod
    def tearDownClass(cls):
        cls.sim.terminate()
        cls.sim.join()

    def test_is_metric_readable(self):
        s = sensors.BaseSensor("base-sensor", self.simulator_socket, self.cfg)
        self.assertIsNotNone(s.read_metrics())

    # more test to be added here ...


if __name__ == '__main__':
    unittest.main()
