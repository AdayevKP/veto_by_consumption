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

    def get_dist(self):
        sum_cap = sum(self.capacity.values())
        return {n: round(c/sum_cap, 2) for n, c in self.capacity.items()}

    def __str__(self):
        p = '\n'.join(map(str, zip(*self.profile)))
        return f"{self.capacity}\n{p}\n"


def _step(profile: Profile):
    counter = cl.Counter([pref[-1] for pref in profile.profile])

    rk = min(
        cap/counter[name]
        for name, cap in profile.capacity.items()
        if counter[name]
    )

    new_cap = {n: round(c - counter[n]*rk, 2) for n, c in profile.capacity.items()}
    return Profile(
        capacity={n: c for n, c in new_cap.items() if c},
        profile=[[p for p in prefs if new_cap[p]] for prefs in profile.profile]
    )


def consuming_veto(profile: Profile):
    print(f"initial_profile {profile}")

    prof = profile
    while sum(prof.capacity.values()) > 1:
        prof = _step(prof)
        print(prof)


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
    consuming_veto(Profile.from_profile(pref_prof))

