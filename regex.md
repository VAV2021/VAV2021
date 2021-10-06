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

Match: `word: number`    
and tell use the word and number that was matched.

Pattern: `(\w+):\s+(\d+)\n`    
More general: `(\w+):\s+(\d+)\s*`    

```java
import java.util.regex.*;

// test string to match
String inventory = "Coffee: 12\nMilk: 15\nSugar: 8\nChocolate: 0\n";

Pattern pattern = Pattern.compile("(\\w+):\\s+(\\d+)\\s*");

Matcher matcher = pattern.matcher( inventory );

// look for the pattern
if (matcher.find()) {
   System.out.println("Found some ingredient");
   var ingredient = matcher.group(1);
   var amount = matcher.group(2);
   System.out.printf("%s units of %s\n", amount, ingredient);
}

// Now, can you find another match?
```


Pattern:


