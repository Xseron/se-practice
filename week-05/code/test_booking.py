import unittest
from booking import can_book


class BookingTests(unittest.TestCase):
    def test_touching_end_is_allowed(self):
        result = can_book(660, 720, 540, False, [(600, 660)])
        self.assertIs(result, True)

    # --- the six cases from the task table (base: now=540, blocked=False, existing=[(600, 660)]) ---

    def test_partial_overlap_is_rejected(self):
        # AC4: (630, 690) shares 630-660 with (600, 660)
        self.assertIs(can_book(630, 690, 540, False, [(600, 660)]), False)

    def test_blocked_room_is_rejected(self):
        # AC3: same request as the touching case, only blocked differs
        self.assertIs(can_book(660, 720, 540, True, [(600, 660)]), False)

    def test_exactly_two_hours_is_allowed(self):
        # AC2: 840 - 720 = 120, "at most 120"
        self.assertIs(can_book(720, 840, 540, False, [(600, 660)]), True)

    def test_over_two_hours_is_rejected(self):
        # AC2: 841 - 720 = 121
        self.assertIs(can_book(720, 841, 540, False, [(600, 660)]), False)

    def test_starting_now_is_rejected(self):
        # AC1: start > now is strict; 540 is not > 540
        self.assertIs(can_book(540, 570, 540, False, [(600, 660)]), False)


if __name__ == "__main__":
    unittest.main()
