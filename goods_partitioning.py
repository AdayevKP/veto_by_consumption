import collections as cl
import dataclasses as dc
import typing as tp
import string

import more_itertools as mit


@dc.dataclass
class Profile:
    capacity: tp.Dict[str, float]
    profile: tp.List[tp.List[str]]

    @staticmethod
    def from_profile(pref_profile: tp.List[tp.List[str]]):
        return Profile(
            capacity={
                c: 1.0
                for c in set(p for pref in pref_profile for p in pref)
            },
            profile=pref_profile
        )

    def __str__(self):
        p = '\n'.join(map(str, zip(*self.profile)))
        return f"{self.capacity}\n{p}\n"

    def cap_sum(self):
        return sum(self.capacity.values())

    def voters_num(self):
        return len(self.profile)


class ConsumingVeto:
    def __init__(self, profile: Profile):
        self.profile = profile

    def _update_profile(self, coefficient: float):
        last_positions = cl.Counter([pref[-1] for pref in self.profile.profile])

        new_capacities = {
            candidate_name: round(
                candidate_capacity - last_positions[candidate_name] * coefficient, 2 # noqa
            )
            for candidate_name, candidate_capacity
            in self.profile.capacity.items()
        }
        return Profile(
            capacity={n: c for n, c in new_capacities.items() if c},
            profile=[
                [p for p in prefs if new_capacities[p]]
                for prefs in self.profile.profile
            ]
        )

    def _eat_candidate(self):
        last_positions = cl.Counter([pref[-1] for pref in self.profile.profile])

        rk = min(
            candidate_capacity / last_positions[candidate_name]
            for candidate_name, candidate_capacity
            in self.profile.capacity.items()
            if last_positions[candidate_name]
        )
        return self._update_profile(rk)

    def _eat_to_capacity(self, capacity: int):
        n = self.profile.voters_num()
        sum_c = self.profile.cap_sum()

        rk = (sum_c - capacity) / n

        return self._update_profile(rk)

    def run(self):
        print(f"initial_profile {self.profile}")

        while sum(self.profile.capacity.values()) > 1:
            updated_profile = self._eat_candidate()

            if updated_profile.cap_sum() >= 1:
                self.profile = updated_profile
            else:
                self.profile = self._eat_to_capacity(1)

            print(self.profile)


def random_profile(voters_num: int, candidates_num: int):
    candidates = list(string.ascii_lowercase[:candidates_num])
    return [
        list(mit.random_permutation(candidates))
        for _ in range(voters_num)
    ]


if __name__ == "__main__":
    # pref_prof = [
    #     ['a', 'b', 'c'],
    #     ['c', 'b', 'a'],
    #     ['b', 'a', 'c'],
    # ]
    # pref_prof = [
    #     ['a', 'b', 'c', 'd', 'e'],
    #     ['a', 'b', 'c', 'd', 'e'],
    #     ['a', 'b', 'c', 'd', 'e'],
    #     ['e', 'b', 'c', 'd', 'a'],
    #     ['d', 'c', 'e', 'a', 'b'],
    # ]

    pref_prof = random_profile(voters_num=10, candidates_num=4)
    ConsumingVeto(Profile.from_profile(pref_prof)).run()


