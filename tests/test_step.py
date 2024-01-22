from stair_case_paradigm import Choices, StairCaseUpdater


def test_step():
    def update_fn(param: float, choice: Choices) -> float:
        if choice == "down":
            return param / 2
        elif choice == "up":
            return param * 2
        return param

    sc = StairCaseUpdater(20.0, update_fn, 6)
    assert sc.step(True) == (True, 20.0)
    assert sc.step(True) == (True, 10.0)
    assert sc.step(True) == (True, 10.0)
    assert sc.step(True) == (True, 5.0)
    assert sc.step(True) == (True, 5.0)
    assert sc.step(True) == (True, 2.5)
    assert sc.step(True) == (True, 2.5)
    assert sc.step(True) == (True, 1.25)
    assert sc.step(True) == (True, 1.25)
    assert sc.step(True) == (True, 0.625)
    assert sc.step(False) == (True, 1.25)
    assert sc.step(False) == (True, 2.5)
    assert sc.step(True) == (True, 2.5)
    assert sc.step(True) == (True, 1.25)
    assert sc.step(False) == (True, 2.5)
    assert sc.step(True) == (True, 2.5)
    assert sc.step(True) == (True, 1.25)
    assert sc.step(True) == (True, 1.25)
    assert sc.step(False) == (True, 2.5)
    assert sc.step(True) == (False, 2.5)
