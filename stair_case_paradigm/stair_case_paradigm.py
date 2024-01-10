from typing import Literal, Protocol

from numpy import mean

Choices = Literal["up", "down", "keep"]


class ParamUpdate(Protocol):
    """階段法で使用するパラメータ更新関数の型
    """
    def __call__(self, param: float, choice: Choices) -> float:
        ...


class StairCaseUpdater:
    """パラメータをupdate_fn関数に基づき階段法で制御する
    """

    def __init__(
        self, initial_param: float, update_fn: ParamUpdate, turn_arounds_count: int
    ) -> None:
        self.update_fn: ParamUpdate = update_fn
        self.turn_arounds_count = turn_arounds_count

        self.answers: "list[bool]" = []
        self.params: "list[float]" = []
        self.turn_arounds: "list[float]" = []
        self.corrected_count = 0
        self.prev_corr = True
        self.param = initial_param

    def step(self, answer: bool) -> "tuple[bool, float]":
        """正答か否かによりパラメータを制御

        Args:
            answer (bool): 正解の場合、True

        Returns:
            tuple[bool, float]: 指定のターンアラウンド数に達したかどうか、現在のパラメータ
        """
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

        if len(self.turn_arounds) == self.turn_arounds_count:
            return False, self.param

        return True, self.param

    def result(self) -> float:
        """ターンアラウンド値の平均を取る

        Returns:
            float: _description_
        """
        return float(mean(self.turn_arounds))


def main():
    def update_fn(param: float, choice: Choices) -> float:
        if choice == "down":
            return param / 2
        elif choice == "up":
            return param * 2
        return param

    sc = StairCaseUpdater(20.0, update_fn, 6)
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
