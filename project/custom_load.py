from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import random

class UserTasks(TaskSet):
    @task
    def root(self):
        self.client.get("/")


class WebsiteUser(HttpUser):
    wait_time = constant(0.0)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 40, "users": 20, "spawn_rate": 1.0},
        {"duration": 70, "users": 60, "spawn_rate": 2.0},
        {"duration": 100, "users": 100, "spawn_rate": 4.0}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None