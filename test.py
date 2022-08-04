from core import CARLAgent, FakeCARLAEnvironment

agent = CARLAgent(FakeCARLAEnvironment(), batch_size=1, log_mode=None)
agent.summary()