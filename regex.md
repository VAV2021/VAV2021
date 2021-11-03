## Regular Expressions in Java

The [Java Tutorial](https://docs.oracle.com/javase/tutorial/) 
[ReallyBigIndex](https://docs.oracle.com/javase/tutorial/reallybigindex.html) has an entire chapter on [Regular Expressions](https://docs.oracle.com/javase/tutorial/essential/regex/index.html).

The 2 classes for regular expressions are:

* **Pattern** in `java.util.regex` - define a pattern and pre-process it
* **Matcher** in `java.util.regex` - match a Pattern (regex) to a string


### CoffeeMaker Example

coffeeMaker.checkInventory() returns a String like:
```
Coffee: 15
Milk: 15
Sugar: 15
Chocolate: 15
```

There are 8 elements in this string, grouped into 4 pairs.
Each pair looks like `word: number`

Pattern to match a word: `\w+`    
Pattern to match digits: `\d+`

To tell a regex matcher to remember what it matched, you can define
**match groups** by putting some part inside parenthesis, e.g. '(\w+)`.

Pattern to match: (word):space(digits)\n`    

Regular expression: `(\w+):\s+(\d+)\s*`    

When we put this regex in a String, we must double each backslash
so that the regex contains a literal backslash.

```java
import java.util.regex.*;

// test string to match
String test_string = "Coffee: 12\nMilk: 15\nSugar: 8\nChocolate: 0\n";

Pattern pattern = Pattern.compile("(\\w+):\\s+(\\d+)\\s*");

Matcher matcher = pattern.matcher( test_string );

// look for the pattern
while (matcher.find()) {
    System.out.println("Found an ingredient");
    // get whatever was matched in the first two (...) parts of the pattern
    var ingredient = matcher.group(1);
    var amount = matcher.group(2);
    System.out.printf("%s units of %s\n", amount, ingredient);
}

```

