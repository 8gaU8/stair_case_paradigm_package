from typing import Final, Literal, Protocol

from numpy import mean

Choices = Literal["up", "down", "keep"]


class ParamUpdate(Protocol):
    def __call__(self, param: float, choice: Choices) -> float:
        ...


class StairCaseUpdater:
    def __init__(self, initial_param: float, update_fn: ParamUpdate) -> None:
        self.update_fn: ParamUpdate = update_fn

        self.answers: list[bool] = []
        self.params: list[float] = []
        self.turn_arounds: list[float] = []
        self.corrected_count = 0
        self.prev_corr = True
        self.param = initial_param

    def step(self, answer: bool) -> bool:
        self.params.append(self.param)
        self.answers.append(answer)

        if answer:
            self.corrected_count += 1
            if self.corrected_count == 2:
                self.corrected_count = 0
                self.param = self.update_fn(self.param, "down")
            if not self.prev_corr:
                self.turn_arounds.append(self.param)
            self.prev_corr = True

        else:
            self.corrected_count = 0
            if self.prev_corr:
                self.turn_arounds.append(self.param)
            self.param = self.update_fn(self.param, "up")
            self.prev_corr = False

        if len(self.turn_arounds) == 6:
            return False

        return True

    def result(self) -> float:
        return float(mean(self.turn_arounds))


def main():
    def update_fn(param: float, choice: Choices) -> float:
        if choice == "down":
            return param / 2
        elif choice == "up":
            return param * 2
        return param

    sc = StairCaseUpdater(20.0, update_fn)
    answers = (
        [True] * 10
        + [False, False]
        + [True, True]
        + [False]
        + [True, True, True]
        + [False]
        + [True]
    )
    for answer in answers:
        sc.step(answer)
    return sc


if __name__ == "__main__":
    import os
    from pathlib import Path

    os.chdir(Path(__file__).parent)
    print(main())
