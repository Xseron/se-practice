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

    # --- AC1: zero-length and reversed times ---

    def test_zero_length_is_rejected(self):
        # AC1: start < end; 700 is after now, duration 0 <= 120, no overlap - only start < end decides
        self.assertIs(can_book(700, 700, 540, False, [(600, 660)]), False)

    def test_reversed_times_are_rejected(self):
        # AC1: start < end; duration -60 would pass "<= 120", 760 > now, and (760, 700) overlaps nothing
        self.assertIs(can_book(760, 700, 540, False, [(600, 660)]), False)

    # --- AC1: the day bounds and the start just after now ---

    def test_ending_at_midnight_is_allowed(self):
        # AC1: end <= 1440, so 1440 itself is allowed
        self.assertIs(can_book(1380, 1440, 540, False, [(600, 660)]), True)

    def test_ending_after_midnight_is_rejected(self):
        # AC1: end <= 1440; duration 61 and no overlap, so only the upper bound decides
        self.assertIs(can_book(1380, 1441, 540, False, [(600, 660)]), False)

    def test_one_minute_after_now_is_allowed(self):
        # AC1: start > now; 541 > 540
        self.assertIs(can_book(541, 571, 540, False, [(600, 660)]), True)

    def test_start_before_now_is_rejected(self):
        # AC1: start > now; 500 < 540, (500, 530) is inside the day and overlaps nothing
        self.assertIs(can_book(500, 530, 540, False, [(600, 660)]), False)

    # --- AC4: the other overlap relationships from the README table ---

    def test_inside_existing_is_rejected(self):
        self.assertIs(can_book(615, 645, 540, False, [(600, 660)]), False)

    def test_containing_existing_is_rejected(self):
        # (570, 690) is exactly 120 minutes, so AC2 does not reject it - only AC4 does
        self.assertIs(can_book(570, 690, 540, False, [(600, 660)]), False)

    def test_identical_to_existing_is_rejected(self):
        self.assertIs(can_book(600, 660, 540, False, [(600, 660)]), False)

    def test_overlapping_the_start_of_existing_is_rejected(self):
        # partial overlap from the left: shares 600-630
        self.assertIs(can_book(570, 630, 540, False, [(600, 660)]), False)

    def test_touching_start_is_allowed(self):
        # AC4: ends exactly where the existing booking starts
        self.assertIs(can_book(570, 600, 540, False, [(600, 660)]), True)

    def test_one_minute_overlap_at_the_end_is_rejected(self):
        self.assertIs(can_book(659, 700, 540, False, [(600, 660)]), False)

    # --- AC4: an empty existing, and an existing with several bookings ---

    def test_empty_existing_is_allowed(self):
        # the same request that overlaps in the base case is free in an empty room
        self.assertIs(can_book(630, 690, 540, False, []), True)

    def test_conflict_with_the_last_booking_only(self):
        existing = [(600, 660), (720, 780), (900, 960)]
        self.assertIs(can_book(930, 990, 540, False, existing), False)

    def test_conflict_with_the_first_of_unsorted_bookings(self):
        existing = [(900, 960), (600, 660)]
        self.assertIs(can_book(630, 690, 540, False, existing), False)

    def test_gap_exactly_between_two_bookings_is_allowed(self):
        existing = [(600, 660), (720, 780)]
        self.assertIs(can_book(660, 720, 540, False, existing), True)

    # --- AC5: inputs unchanged ---

    def test_existing_unchanged_after_true(self):
        existing = [(720, 780), (600, 660)]
        before = list(existing)
        result = can_book(660, 720, 540, False, existing)
        self.assertIs(result, True)
        self.assertEqual(existing, before)

    def test_existing_unchanged_after_false(self):
        existing = [(720, 780), (600, 660)]
        before = list(existing)
        result = can_book(630, 690, 540, False, existing)
        self.assertIs(result, False)
        self.assertEqual(existing, before)

    def test_existing_unchanged_when_rejected_before_the_loop(self):
        existing = [(720, 780), (600, 660)]
        before = list(existing)
        can_book(660, 720, 540, True, existing)
        self.assertEqual(existing, before)

    # --- outside the contract: documents my section 9.2 decision, does not count towards M ---

    def test_string_time_is_not_handled(self):
        # Decision: not-handled. The contract guarantees integers; a string start is a caller bug
        # and Python's own TypeError is allowed to surface.
        with self.assertRaises(TypeError):
            can_book("600", 660, 540, False, [])


if __name__ == "__main__":
    unittest.main()
