from stair_case_paradigm import Choices, StairCaseUpdater


def test_step():
    def update_fn(param: float, choice: Choices) -> float:
        if choice == "down":
            return param / 2
        elif choice == "up":
            return param * 2
        return param

    sc = StairCaseUpdater(20.0, update_fn, 6)
    answers = [True] * 10 + [False, False] + [True, True] + [False] + [True, True, True] + [False] + [True]
    for answer in answers:
        sc.step(answer)
    assert sc.result() == 1.7708333333333333
