I'll work only from this scenario. These are the constraints I'll keep consistent across every diagram:

**Actors:** Student, Administrator.

**Stories (IDs fixed):**
- **US-01:** book a room (R1–R4)
- **US-02:** view free rooms
- **US-03:** cancel own booking (R2)
- **US-04:** block a room (R3)
- **US-05:** unblock a room (R3)
- **US-06:** review usage

**Rules as I'll model them:**
- **R1:** The start is in the future, and 0 < duration ≤ 2 h.
- **R2:** Active bookings for the same room don't overlap. A cancelled booking stops being active, so it no longer blocks the slot.
- **R3:** A blocked room rejects *new* bookings. I won't assume that blocking cancels existing bookings, since no rule says so.
- **R4:** Every successful booking produces a confirmation. This is the only notification.

**Excluded:** payments, equipment, recurring bookings, waiting lists, other notifications, registration.

If a diagram would need behaviour the scenario doesn't define, I'll point it out rather than invent it. One example is what happens to existing bookings when a room is blocked.

What's the first diagram?