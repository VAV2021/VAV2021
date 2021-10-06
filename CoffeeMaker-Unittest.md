Several statements will throw exception, hence **most of them are never executed**:

```java
    @Test(expected = RecipeException.class)
    public void testAmountAndPriceNotInInteger() throws RecipeException{
        Recipe testRecipe = new Recipe();
        testRecipe.setName("for test");
        testRecipe.setAmtChocolate("1.40");
        testRecipe.setAmtCoffee("3.00");     // not tested
        testRecipe.setAmtMilk("1.5");        // not tested
        testRecipe.setAmtSugar("1.0");       // not tested
        testRecipe.setPrice("50.0");         // not tested
    }
```

Same mistake, and largely redundant anyway:

```java
    @Test(expected = RecipeException.class)
    public void testAmountAndPriceMalformed() throws RecipeException{
        Recipe forTest = new Recipe();
        forTest.setName("for test");
        forTest.setAmtChocolate("ab");
        forTest.setAmtCoffee("-3");         // not tested
        forTest.setAmtMilk("a");            // not tested
        forTest.setAmtSugar("-1");          // not tested
        forTest.setPrice("-50");            // not tested
    }
```

Not a test:

```java
    @Test
    public void testAddRecipe() {
        coffeeMaker.addRecipe(recipe1);
    }

    @Test
    public void testWaitingState() {
    }

    @Test
    public void testDeleteRecipe() {
        coffeeMaker.addRecipe(recipe1);
        coffeeMaker.deleteRecipe(0);
    }

    @Test
    public void testEditRecipe() {
        coffeeMaker.addRecipe(recipe1);
        coffeeMaker.editRecipe(0,recipe2);
    }

    @Test
    public void testAddInventory() throws InventoryException {
        coffeeMaker.addInventory("4","7","0","9");
    }
```

Not a thorough test:
```java
    @Test
    public void testDeleteRecipe()  {
        coffeeMaker.addRecipe(recipe1);
        coffeeMaker.addRecipe(recipe2);
        coffeeMaker.addRecipe(recipe3);
        coffeeMaker.deleteRecipe(1);
        assertNotEquals(recipe2,coffeeMaker.getRecipes()[1]);
    }
```
this depends on 
1. Recipe.equals 
2. CoffeeMaker stores recipes as an array and does not shift recipes when one is deleted (implementation detail).


According to the Javadoc for `addRecipe`:
```java
   /**
     * Returns true if the recipe is added to the
     * list of recipes in the CoffeeMaker and false
     * otherwise.
     * @param r     a recipe to add
     * @return true if recipe successfully added
     */
    public boolean addRecipe(Recipe r) {
```

These tests are **not important**. In both cases you are just testing for index out of range:

```java
    @Test
    public void testDeleteRecipeNegativePosition()  {
        coffeeMaker.addRecipe(recipe1);
        coffeeMaker.addRecipe(recipe2);
        coffeeMaker.addRecipe(recipe3);
        assertEquals(coffeeMaker.deleteRecipe(-1),null);
    }
    @Test
    public void testDeleteRecipeNotInList()  {
        coffeeMaker.addRecipe(recipe1);
        coffeeMaker.addRecipe(recipe2);
        coffeeMaker.addRecipe(recipe3);
        assertEquals(coffeeMaker.deleteRecipe(4),null);
    }
```

OK but this test **ignores the return value** from addRecipe:
```java
    @Test
    public void testFourRecipe() {
        coffeeMaker.addRecipe(recipe4);
        coffeeMaker.addRecipe(recipe3);
        coffeeMaker.addRecipe(recipe2);
        // should not be added
        coffeeMaker.addRecipe(recipe1);
        assertFalse(
          Arrays.asList(coffeeMaker.getRecipes()).contains(recipe1));
    }
```

## Test Depends on a Bug

This test relies on a **bug** in Inventory that is corrected in 
later versions. Inventory uses static attributes but instance methods to access and update those attributes.

There is **no reason** to expect that creating a **new Inventory** would
have any effect on the inventory that **already exists** inside the CoffeeMaker.

```java
    @Ignore("this test ASSUMES that CoffeeMaker shares same buggy static inventory")
    @Test
    public void testInventoryQuantitySet(){
        Inventory inventory = new Inventory();
        inventory.setChocolate(5);
        inventory.setCoffee(6);
        inventory.setMilk(7);
        inventory.setSugar(8);
        String expectedOutput = "Coffee: 6\nMilk: 7\nSugar: 8\nChocolate: 5\n";
        assertEquals(expectedOutput, coffeeMaker.checkInventory());
    }
```

## Brittle Tests

Comparing strings like this is prone to failure.  A minor change
in `checkInventory` could change format of output. 

```java
   String expected = "Coffee: 6\nMilk: 7\nSugar: 8\nChocolate: 5\n";

   assertEquals(expectedOutput, coffeeMaker.checkInventory());
```

