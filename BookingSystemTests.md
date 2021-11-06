## Evaluating the Appointment Booking System Tests

### How I Evaluated

I used a BookingSystem with 7 variants as listed below,
and ran each student's BookingSystemTest using the variants.

* Test V0: Correct BookingSystem. All tests should **pass**.
* Test V1: Correct BookingSystem but `findAppointmentsForDate` returns a list with different ordering of appointments (the specification states this is possible). All tests should **pass**.
* Remove Invalid Tests: any tests that fail for V0 or don't contain tests (asserts or test for exception) are removed using `@org.junit.Ignore`.
* Test V2 - V7: each contain a defect. At least 1 test should **fail**.
* Brittle Tests: I checked whether tests depend on the output of `Appointment::toString`. You should not use this for testing, as a minor, unrelated change in that method would cause tests to fail.


### Target Code

The variation of the `BookingSystem` used as 'code under test' were:


 Variant  | Description                                             
----------|:----------------------------------------------------
 0        | Same as BookingSystem code in exam. All tests should **pass**.
 1        | Same as above, but `findAppointmentsForDate` returns appointments in LIFO order. All tests should **pass**.
 2        | BookingSystem doesn't completely fill daily capacity (off by 1).
 3        | BookingSystem overbooks appointments (more than capacity per date).
 4        | A Person can create more than one Appointment.
 5        | Person cannot cancel an appointment. Appointment stays in system.
 6        | BookingSystem ignores the request date and chooses the date itself.
 7        | A Person can create appointment up to 7 years in the future.

- For variant 2 - 7 **at least one test should fail**.


