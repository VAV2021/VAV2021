## Thai Citizen ID Validation

[Thai Citizen ID Categories](#thai-citizen-id-categories) using first digit    
[Checksum Formula](#checksum-formula) to verify the id checksum (last digit)

### Checksum Formula

Javascript:

```javascript
export default function ThaiNationalID (id) {
  if (!/^[0-9]{13}$/g.test(id)) {
    return false
  }
  let i;
  let sum = 0;
  for (i = 0; i < 12; i++) {
    sum += Number.parseInt(id.charAt(i)) * (13 - i)
  }
  const checkSum = (11 - sum % 11) % 10
  return (checkSum === Number.parseInt(id.charAt(12))
}
```

Python:

```python
def valid_id(thai_id) -> bool:
    """Validate a 13-digit Thai National ID, given as a number or string."""
    if isinstance(thai_id, int):
        thai_id = str(thai_id)
    elif not isinstance(thai_id, str):
        return False
    if len(thai_id) != 13:
        return False
    try:
        digits = [int(d) for d in thai_id]
    except ValueError:
        return False
    # First digit is never 0; 0 is used for other IDs such as corporate tax ID
    if digits[0] == '0':
        return False
    # Apply checksum formula to first 12 digits
    sum = 0
    for i in range(0,12):
        sum += digits[i]*(13 - i)
    checksum = (11 - sum%11) % 10
    # last digit is checksum
    return checksum == digits[12]
```

- Checksum Formula: <https://mynoz.wordpress.com/2006/05/01/how-to-cal-the-last-digit-of-thai-citizen-id-card/>
- Validator in Javascript: <https://github.com/jukbot/thai-citizen-id-validator/>


### Thai Citizen ID Categories

Wikipedia describes how Thai Citizen IDs are numbered:
<https://en.wikipedia.org/wiki/Thai_identity_card#Identification_number>. 

The first digit indicates the category of id holder:

| First Digit  | Category   |
|--------------|------------|
| 0	           | Not found on national id cards but may be found on other issued identity cards |
| 1 | Thai nationals born after 1 Jan 1984 and their birth notified within 15 days |
| 2 | Thai nationals born after 1 Jan 1984 but their birth not notified within 15 days |
| 3 | Thai or foreign nationals with identification cards whose names were included in a house registration book before 1 Jan 1984 |
| 4 | Thai nationals born before 1 Jan 1984 but were not included in a house registration book at that time |
| 5 | Thai nationals with dual nationality and other special cases |
| 6 | Foreign nationals living in Thailand temporarily and illegal migrants |
| 7 | Children of people of category 6 who were born in Thailand |
| 8 | Foreign nationals living in Thailand permanently or Thai nationals by naturalization |
| 9 | Not used     |

