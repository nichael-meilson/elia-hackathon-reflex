from typing import Dict, List

import numpy as np
import pandas as pd
import reflex as rx

from .data_items import all_items
# from .player import Job
from .job import Job

dummy_data_json = "dummy_data.json"


class State(rx.State):
    """The app state."""

    jobs: list[Job] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    selected_items: Dict[str, List] = (
        all_items  # We add all items to the selected items by default
    )

    @rx.event
    def set_age(self, value: list[int | float]):
        self.age = (int(value[0]), int(value[1]))

    @rx.event
    def set_salary(self, value: list[int | float]):
        self.salary = (int(value[0]), int(value[1]))

    @rx.var(cache=True)
    def filtered_sorted_jobs(self) -> list[Job]:
        jobs = self.jobs

        # Filter players based on selected item
        if self.sort_value:
            if self.sort_value in ["date_utc", "scheduleid"]:
                jobs = sorted(
                    jobs,
                    key=lambda job: float(getattr(job, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                jobs = sorted(
                    jobs,
                    key=lambda job: str(getattr(job, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter players based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            jobs = [
                job
                for job in jobs
                if any(
                    search_value in str(getattr(job, attr)).lower()
                    for attr in [
                        "name",
                        "team",
                        "number",
                        "position",
                        "age",
                        "height",
                        "weight",
                        "college",
                        "salary",
                    ]
                )
            ]

        return jobs

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Job]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_jobs[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        df = pd.read_json(dummy_data_json)
        df = df.replace("", np.nan)  # Replace empty strings with NaN
        self.jobs = [Job(**row) for _, row in df.iterrows()]
        self.total_items = len(self.jobs)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    # @rx.var(cache=True)
    # def get_age_salary_chart_data(self) -> list[dict]:
    #     age_salary_data = {}
    #     age_count = {}

    #     for job in self.jobs:
    #         if (
    #             not pd.isna(job.scheduleid)
    #             and not pd.isna(job.version)
    #         ):
    #             version = job.scheduleid
    #             if version not in age_salary_data:
    #                 age_salary_data[version] = 0
    #                 age_count[version] = 0

    #             age_salary_data[version] += float(job.salary)
    #             age_count[version] += 1

    #     return [
    #         {
    #             "version": version,
    #             "average version": round(
    #                 age_salary_data.get(version, 0) / age_count.get(version, 1), 2
    #             ),
    #         }
    #         for version in range(self.[0], self.age[1] + 1)  # Ensure we include all ages
    #     ]

    # @rx.var(cache=True)
    # def get_position_salary_chart_data(self) -> list[dict]:
    #     position_salary_data = {}
    #     position_count = {}

    #     for player in self.players:
    #         if (
    #             not pd.isna(player.position)
    #             and not pd.isna(player.salary)
    #             and player.team in self.selected_items["teams"]
    #             and player.college in self.selected_items["colleges"]
    #             and player.position in self.selected_items["positions"]
    #             and self.age[0] <= player.age <= self.age[1]
    #             and self.salary[0] <= float(player.salary) <= self.salary[1]
    #         ):
    #             position = player.position
    #             if position not in position_salary_data:
    #                 position_salary_data[position] = 0
    #                 position_count[position] = 0

    #             position_salary_data[position] += float(player.salary)
    #             position_count[position] += 1

    #     return [
    #         {
    #             "position": position,
    #             "average salary": round(
    #                 position_salary_data[position] / position_count[position], 2
    #             ),
    #         }
    #         for position in position_salary_data
    #     ]

    # @rx.var(cache=True)
    # def get_team_salary_chart_data(self) -> list[dict]:
    #     team_salary_data = {}
    #     team_count = {}

    #     for player in self.players:
    #         if (
    #             not pd.isna(player.team)
    #             and not pd.isna(player.salary)
    #             and player.team in self.selected_items["teams"]
    #             and player.college in self.selected_items["colleges"]
    #             and player.position in self.selected_items["positions"]
    #             and self.age[0] <= player.age <= self.age[1]
    #             and self.salary[0] <= float(player.salary) <= self.salary[1]
    #         ):
    #             team = player.team
    #             if team not in team_salary_data:
    #                 team_salary_data[team] = 0
    #                 team_count[team] = 0

    #             team_salary_data[team] += float(player.salary)
    #             team_count[team] += 1

    #     return [
    #         {
    #             "team": team,
    #             "average salary": round(team_salary_data[team] / team_count[team], 2),
    #         }
    #         for team in team_salary_data
    #     ]

    # @rx.var(cache=True)
    # def get_college_salary_chart_data(self) -> list[dict]:
    #     college_salary_data = {}
    #     college_count = {}

    #     for player in self.players:
    #         if (
    #             not pd.isna(player.college)
    #             and not pd.isna(player.salary)
    #             and player.team in self.selected_items["teams"]
    #             and player.college in self.selected_items["colleges"]
    #             and player.position in self.selected_items["positions"]
    #             and self.age[0] <= player.age <= self.age[1]
    #             and self.salary[0] <= float(player.salary) <= self.salary[1]
    #         ):
    #             college = player.college
    #             if college not in college_salary_data:
    #                 college_salary_data[college] = 0
    #                 college_count[college] = 0

    #             college_salary_data[college] += float(player.salary)
    #             college_count[college] += 1

    #     return [
    #         {
    #             "college": college,
    #             "average salary": round(
    #                 college_salary_data[college] / college_count[college], 2
    #             ),
    #         }
    #         for college in college_salary_data
    #     ]

    # @rx.var(cache=True)
    # def get_team_age_average_data(self) -> list[dict]:
    #     team_age_data = {}
    #     team_count = {}

    #     for player in self.players:
    #         if (
    #             not pd.isna(player.team)
    #             and not pd.isna(player.age)
    #             and player.team in self.selected_items["teams"]
    #             and player.college in self.selected_items["colleges"]
    #             and player.position in self.selected_items["positions"]
    #             and self.age[0] <= player.age <= self.age[1]
    #             and self.salary[0] <= float(player.salary) <= self.salary[1]
    #         ):
    #             team = player.team
    #             if team not in team_age_data:
    #                 team_age_data[team] = []
    #                 team_count[team] = 0

    #             team_age_data[team].append(player.age)
    #             team_count[team] += 1

    #     return [
    #         {
    #             "team": team,
    #             "average age": round(sum(ages) / team_count[team], 2),
    #         }
    #         for team, ages in team_age_data.items()
    #     ]

    # @rx.var(cache=True)
    # def get_position_age_average_data(self) -> list[dict]:
    #     position_age_data = {}
    #     position_count = {}

    #     for player in self.players:
    #         if (
    #             not pd.isna(player.position)
    #             and not pd.isna(player.age)
    #             and player.team in self.selected_items["teams"]
    #             and player.college in self.selected_items["colleges"]
    #             and player.position in self.selected_items["positions"]
    #             and self.age[0] <= player.age <= self.age[1]
    #             and self.salary[0] <= float(player.salary) <= self.salary[1]
    #         ):
    #             position = player.position
    #             if position not in position_age_data:
    #                 position_age_data[position] = []
    #                 position_count[position] = 0

    #             position_age_data[position].append(player.age)
    #             position_count[position] += 1

    #     return [
    #         {
    #             "position": position,
    #             "average age": round(sum(ages) / position_count[position], 2),
    #         }
    #         for position, ages in position_age_data.items()
    #     ]

    def add_selected(self, list_name: str, item: str):
        self.selected_items[list_name].append(item)

    def remove_selected(self, list_name: str, item: str):
        self.selected_items[list_name].remove(item)

    def add_all_selected(self, list_name: str):
        self.selected_items[list_name] = list(all_items[list_name])

    def clear_selected(self, list_name: str):
        self.selected_items[list_name].clear()

    def random_selected(self, list_name: str):
        self.selected_items[list_name] = np.random.choice(
            all_items[list_name],
            size=np.random.randint(1, len(all_items[list_name]) + 1),
            replace=False,
        ).tolist()
