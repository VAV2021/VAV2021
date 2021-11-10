## Evaluating the Appointment Booking System Tests

[Specification for the Appointment Booking Service][booking-service]

[booking-service]: https://docs.google.com/document/d/1WAaBFQ5lIB1Ms1rHlfZl3HnOqYhT0v3YKo6iTpyXFhY/

### How I Evaluated

I used a BookingSystem with 7 variants as listed below,
and ran each student's BookingSystemTest using the variants.

* Test V0: Correct BookingSystem. All tests should **pass**.
* Test V1: Correct BookingSystem but `findAppointmentsForDate` returns list of appointments in LIFO order (the specification states that the ordering is not guaranteed). All tests should **pass**.
* Ignore Invalid Tests: any tests that fail for V0 or don't contain valid tests (asserts or test for exception) are deactivated using `@org.junit.Ignore`.
* Test V2 - V7: each variant contains a defect. At least 1 of your tests should **fail**.
* Brittle Tests: I checked whether tests depend on the output of `Appointment::toString`. You should not do this. There is no reason for it, and it can cause your tests to fail due to a minor, unrelated change in toString.


### Target Code

The variations of the `BookingSystem` used as "code under test" were:


 Variant  | Description                                             
----------|:----------------------------------------------------
 0        | Same as BookingSystem code in exam. All tests should **pass**.
 1        | Same as above, but `findAppointmentsForDate` returns appointments in a different order. All tests should **pass**.
 2        | BookingSystem doesn't completely fill daily capacity (off by 1).
 3        | BookingSystem overbooks appointments (more than capacity per date).
 4        | A person can create more than one Appointment.
 5        | A person cannot cancel an appointment.
 6        | BookingSystem ignores the appointment request date and chooses the date itself.
 7        | A Person can create appointment up to 7 years in the future (programmer error).

- For variant 2 - 7 **at least one test should fail**.

V2 - V7 are all errors that a programmer might actually make,
and clearly violate the specification.

### Common Mistakes

1. Hard-coded dates as strings, such as "27/10/2021". This usually causes all tests to fail.

2. Using Appointment `toString` to compare actual and expected values, where you construct the expected string in code.  This is brittle and error-prone. You should compare the actual attributes of the Appointment.    
   - A good way would be to write your own helper method (such as `assertEqual(Appointment expected, Appointment actual)` and test each attribute using asserts.
   - If you **really** need to test by comparing strings, then instead of building the string yourlself, create an Appointment object with the data you expect and call that object's toString:
   ```java
   Appointment expected = new Appointment(expectedId, expectedName, date);
   Appointment actual = bs.findAppointmentForForId(expectedId);
   // try not to test this way:
   assertEquals(expected.toString(), actual.toString());
   // better: use your own helper method
   assertAppointmentsEqual(expected, actual);

   public void assertAppointmentsEqual(appt1, appt2) {
       // attributes are public final. Don't need getter method.
       assertEqual(appt1.personId, appt2.personId);
       assertEqual(appt1.personName, appt2.personName);
       assertEqual(appt1.date, appt2.date);
   }
   ```
