import tester.*;
import javalib.worldimages.*;
import javalib.impworld.*;
import java.awt.Color;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

class Category {
  Color color;
  ArrayList<String> wordTexts;

  // Constructor for Category class
  Category(Color color, String... texts) {
    this.color = color;
    this.wordTexts = new ArrayList<>();
    for (String text : texts) {
      wordTexts.add(text);
    }
  }

  // Creates Word objects from the category's word texts
  ArrayList<Word> createWords() {
    ArrayList<Word> words = new ArrayList<>();
    for (String text : wordTexts) {
      words.add(new Word(text, color));
    }
    return words;
  }
}

class ConnectionsWorld extends World {
  int cellsize = 150;
  int gridsize = 4;
  int width = 600;
  int height = 750;
  int buttonheight = 30;
  int buttonwidth = 120;

  ArrayList<Group> foundGroups = new ArrayList<>();
  ArrayList<Word> words;
  int triesLeft;
  Random rand;
  boolean gameOver;
  boolean won;
  String feedbackMessage;
  int feedbackTimer;

  ArrayList<String> winMessages = new ArrayList<>();
  ArrayList<Category> allCategories = new ArrayList<>();

  // Constructor for ConnectionsWorld using a default random
  ConnectionsWorld() {
    this(new Random());
  }

  // Constructor for ConnectionsWorld with a specified random
  ConnectionsWorld(Random rand) {
    this.rand = rand;
    initializeWinMessages();
    initializeCategories();
    resetGame();
  }

  // Initializes the win messages
  void initializeWinMessages() {
    winMessages.add("Perfect! You solved it in 1 try!");
    winMessages.add("Great! You solved it in 2 tries!");
    winMessages.add("Good job! You solved it in 3 tries!");
    winMessages.add("You solved it in 4 tries!");
  }

  // Initializes all categories of words
  void initializeCategories() {
    // Yellow categories
    allCategories.add(new Category(Color.YELLOW, "AVERAGE", "MEAN", "NORM", "PAR"));
    allCategories.add(new Category(Color.YELLOW, "CHINA", "CRYSTAL", "LINEN", "SILVER"));
    allCategories.add(new Category(Color.YELLOW, "RAGAMUFFIN", "RUSSIAN", "SPHYNX", "TURKISH"));
    allCategories.add(new Category(Color.YELLOW, "BONUS", "INSURANCE", "SALARY", "VACATION"));
    allCategories.add(new Category(Color.YELLOW, "ABSORB", "ENGROSS", "HOLD", "RIVET"));
    allCategories.add(new Category(Color.YELLOW, "LION", "TIGER", "LEOPARD", "CHEETAH"));
    allCategories.add(new Category(Color.YELLOW, "APPLE", "BANANA", "ORANGE", "GRAPE"));
    allCategories.add(new Category(Color.YELLOW, "SUN", "MOON", "STAR", "COMET"));
    allCategories.add(new Category(Color.YELLOW, "RED", "BLUE", "GREEN", "YELLOW"));
    allCategories.add(new Category(Color.YELLOW, "EARTH", "MARS", "VENUS", "JUPITER"));

    // Green categories
    allCategories.add(new Category(Color.GREEN, "ARROWS", "EAGLE", "OLIVE", "SHIELD"));
    allCategories.add(new Category(Color.GREEN, "BERMUDA", "BIKE", "BOXER", "CARGO"));
    allCategories.add(new Category(Color.GREEN, "CHESHIRE", "COMEDY", "JOKER", "MONA"));
    allCategories.add(new Category(Color.GREEN, "FLAG", "GIVEAWAY", "SIGN", "TELL"));
    allCategories.add(new Category(Color.GREEN, "FILM", "RECORD", "SHOOT", "TAPE"));
    allCategories.add(new Category(Color.GREEN, "EMERALD", "RUBY", "SAPPHIRE", "DIAMOND"));
    allCategories.add(new Category(Color.GREEN, "NOVEL", "POEM", "PLAY", "ESSAY"));
    allCategories.add(new Category(Color.GREEN, "KNIFE", "FORK", "SPOON", "CHOPSTICKS"));
    allCategories.add(new Category(Color.GREEN, "WHEAT", "BARLEY", "OATS", "RYE"));
    allCategories.add(new Category(Color.GREEN, "TULIP", "ROSE", "DAISY", "LILY"));

    // Blue categories
    allCategories.add(new Category(Color.BLUE, "BIRDIE", "DOLLY", "KATE", "YANKEES"));
    allCategories.add(new Category(Color.BLUE, "CANAL", "MAN", "PANAMA", "PLAN"));
    allCategories.add(new Category(Color.BLUE, "LIBERTY", "STATUE", "TOWER", "VENUS"));
    allCategories.add(new Category(Color.BLUE, "CUT", "DEAL", "FAN", "SHUFFLE"));
    allCategories.add(new Category(Color.BLUE, "PASTEL", "PETALS", "PLEATS", "STAPLE"));
    allCategories.add(new Category(Color.BLUE, "HAMMER", "SAW", "DRILL", "WRENCH"));
    allCategories.add(new Category(Color.BLUE, "VOLCANO", "TSUNAMI", "EARTHQUAKE", "HURRICANE"));
    allCategories.add(new Category(Color.BLUE, "JAVA", "PYTHON", "RUBY", "SWIFT"));
    allCategories.add(new Category(Color.BLUE, "PLUTO", "GOOFY", "MICKEY", "DONALD"));
    allCategories.add(new Category(Color.BLUE, "PEN", "PENCIL", "MARKER", "CRAYON"));

    // Orange categories
    allCategories.add(new Category(Color.ORANGE, "BOGEY", "CRAFTS", "GENTLE", "SPOKES"));
    allCategories.add(new Category(Color.ORANGE, "BRAZIL", "CLUE", "COMMANDO", "WITNESS"));
    allCategories.add(new Category(Color.ORANGE, "BATHROBE", "BOWLING", "RUG", "WHITE"));
    allCategories.add(new Category(Color.ORANGE, "BANKNOTE", "BEAK", "INVOICE", "WILLIAM"));
    allCategories.add(new Category(Color.ORANGE, "GOOD", "PENNY", "PLEASE", "WOMAN"));
    allCategories.add(new Category(Color.ORANGE, "BASS", "FLUTE", "VIOLIN", "TRUMPET"));
    allCategories.add(new Category(Color.ORANGE, "PHOENIX", "DRAGON", "UNICORN", "GRIFFIN"));
    allCategories.add(new Category(Color.ORANGE, "RING", "HOOP", "LOOP", "CIRCLE"));
    allCategories.add(new Category(Color.ORANGE, "BOLT", "SOCKET", "WIRE", "SWITCH"));
    allCategories.add(new Category(Color.ORANGE, "BOW", "ARROW", "QUIVER", "TARGET"));
  }

  // Resets the game to its initial state
  void resetGame() {
    this.rand = new Random(System.nanoTime());
    Collections.shuffle(allCategories, rand);
    this.words = initializeWords();
    this.triesLeft = 4;
    this.gameOver = false;
    this.won = false;
    this.foundGroups.clear();
    this.feedbackMessage = "";
    this.feedbackTimer = 0;
    Collections.shuffle(words, rand);
  }

  // Initializes the words to be displayed in the game
  ArrayList<Word> initializeWords() {
    Collections.shuffle(allCategories, rand);
    ArrayList<Category> selectedCategories = new ArrayList<>();
    ArrayList<Color> selectedColors = new ArrayList<>();

    for (Category category : allCategories) {
      if (!selectedColors.contains(category.color)) {
        selectedCategories.add(category);
        selectedColors.add(category.color);
      }
      if (selectedCategories.size() == 4) {
        break;
      }
    }

    ArrayList<Word> words = new ArrayList<>();
    for (Category category : selectedCategories) {
      words.addAll(category.createWords());
    }
    return words;
  }

  // Creates the scene to be displayed
  public WorldScene makeScene() {
    WorldScene scene = this.getEmptyScene();

    for (int i = 0; i < words.size(); i++) {
      int row = i / gridsize;
      int col = i % gridsize;
      int x = col * cellsize + (cellsize / 2);
      int y = row * cellsize + (cellsize / 2);
      scene.placeImageXY(words.get(i).render(cellsize), x, y);
    }

    WorldImage triesText = new TextImage("Tries left: " + triesLeft, 24, Color.RED);
    scene.placeImageXY(triesText, width / 2, height - 120);

    WorldImage shuffleButton = new OverlayOffsetAlign(
        AlignModeX.CENTER,
        AlignModeY.MIDDLE,
        new TextImage("SHUFFLE", 18, Color.BLACK), 0, 0,
        new RectangleImage(buttonwidth, buttonheight, OutlineMode.SOLID, new Color(220, 220, 220)));
    scene.placeImageXY(shuffleButton, width / 4, height - 70);

    WorldImage deselectButton = new OverlayOffsetAlign(
        AlignModeX.CENTER,
        AlignModeY.MIDDLE,
        new TextImage("DESELECT ALL", 16, Color.BLACK), 0, 0,
        new RectangleImage(buttonwidth, buttonheight, OutlineMode.SOLID, new Color(220, 220, 220)));
    scene.placeImageXY(deselectButton, 3 * width / 4, height - 70);

    // Draw feedback message (position adjusted further down)
    if (feedbackTimer > 0) {
      WorldImage feedback = new TextImage(feedbackMessage, 20, Color.BLUE);
      scene.placeImageXY(feedback, width / 2, height - 40);
    }

    int yOffset = height - 180;
    for (Group group : foundGroups) {
      if (group.displayTimer > 0) {
        WorldImage label = new TextImage("Group Found!", 20, group.color);
        scene.placeImageXY(label, width / 2, yOffset);
        yOffset -= 30;
        group.displayTimer--;
      }
    }

    if (gameOver) {
      String message;
      if (won) {
        int triesUsed = 4 - triesLeft + 1;
        if (triesUsed > 0 && triesUsed <= winMessages.size()) {
          message = winMessages.get(triesUsed - 1);
        } else {
          message = "You solved it!";
        }
      } else {
        message = "Game Over! Try again!";
      }

      WorldImage resultText = new TextImage(message, 30, won ? Color.GREEN : Color.RED);
      scene.placeImageXY(resultText, width / 2, height / 2);

      WorldImage restartText = new TextImage("Press 'R' to restart", 20, Color.BLACK);
      scene.placeImageXY(restartText, width / 2, height / 2 + 40);
    }

    return scene;
  }

  // Handles mouse press events
  public void onMousePressed(Posn pos) {
    if (gameOver) {
      return;
    }

    if (pos.y >= height - 70 - buttonheight / 2 && pos.y <= height - 70 + buttonheight / 2) {
      if (pos.x >= width / 4 - buttonwidth / 2 && pos.x <= width / 4 + buttonwidth / 2) {
        shuffleWords();
        return;
      }
      else if (pos.x >= 3 * width / 4 - buttonwidth / 2 
          && pos.x <= 3 * width / 4 + buttonwidth / 2) {
        deselectAll();
        return;
      }
    }

    int col = pos.x / cellsize;
    int row = pos.y / cellsize;
    int index = row * gridsize + col;

    if (index >= 0 && index < words.size()) {
      Word word = words.get(index);
      if (!word.grouped) {
        word.selected = !word.selected;
        checkForGuess();
      }
    }
  }

  // Shuffles the words in the game
  void shuffleWords() {
    ArrayList<Word> ungrouped = new ArrayList<>();
    ArrayList<Word> grouped = new ArrayList<>();

    for (Word word : words) {
      if (word.grouped) {
        grouped.add(word);
      } else {
        ungrouped.add(word);
      }
    }

    Collections.shuffle(ungrouped, rand);
    words = new ArrayList<>();
    words.addAll(grouped);
    words.addAll(ungrouped);
    deselectAll();
  }

  // Deselects all selected words
  void deselectAll() {
    for (Word word : words) {
      word.selected = false;
    }
    feedbackMessage = "";
  }

  // Checks for a guess
  void checkForGuess() {
    ArrayList<Word> selected = new ArrayList<>();
    for (Word word : words) {
      if (word.selected) {
        selected.add(word);
      }
    }

    if (selected.size() == 4) {
      boolean correct = checkCategory(selected);
      processGuess(selected, correct);
    } else if (selected.size() == 3) {
      checkForPartialMatch(selected);
    } else {
      feedbackMessage = ""; // Clear message if less than 3 selected
      feedbackTimer = 0;
    }
  }

  // Checks for a partial match (3 of 4 words in a category)
  void checkForPartialMatch(ArrayList<Word> selected) {
    int yellow = 0;
    int green = 0;
    int blue = 0;
    int orange = 0;
    for (Word word : selected) {
      if (word.categoryColor == Color.YELLOW) {
        yellow++;
      }
      else if (word.categoryColor == Color.GREEN) {
        green++;
      }
      else if (word.categoryColor == Color.BLUE) {
        blue++;
      }
      else if (word.categoryColor == Color.ORANGE) {
        orange++;
      }
    }
    
    if (yellow == 3 || green == 3 || blue == 3 || orange == 3) {
      feedbackMessage = "Close! 3 of 4 words match a category";
      feedbackTimer = 60;
    }
  }

  // Checks if the selected words are in the same category
  boolean checkCategory(ArrayList<Word> selected) {
    if (selected.isEmpty()) {
      return false;
    }
    Color expected = selected.get(0).categoryColor;
    for (Word word : selected) {
      if (word.categoryColor != expected) {
        return false;
      }
    }
    return true;
  }

  // Processes the guess
  void processGuess(ArrayList<Word> selected, boolean correct) {
    if (correct) {
      Color groupColor = selected.get(0).categoryColor;
      foundGroups.add(new Group(selected, groupColor));
      
      for (Word word : selected) {
        word.grouped = true;
      }
      checkWinCondition();
    } else {
      triesLeft--;
      if (triesLeft <= 0) {
        endGame(false);
      }
    }

    words.forEach(word -> word.selected = false);
  }

  // Checks if the win condition is met
  void checkWinCondition() {
    for (Word word : words) {
      if (!word.grouped) {
        return;
      }
    }
    endGame(true);
  }

  // Ends the game
  void endGame(boolean won) {
    gameOver = true;
    this.won = won;
  }

  // Handles key events
  public void onKeyEvent(String key) {
    if (key.equals("r")) {
      resetGame();
    }
  }

  // Method to set words for testing purposes
  void testSetWords(ArrayList<Word> words) {
    this.words = words;
  }
}

class Word {
  String text;
  Color categoryColor;
  boolean selected;
  boolean grouped;

  // Constructor for Word class
  Word(String text, Color categoryColor) {
    this.text = text;
    this.categoryColor = categoryColor;
    this.selected = false;
    this.grouped = false;
  }

  // Renders the word as a WorldImage
  WorldImage render(int size) {
    Color bgColor = grouped ? categoryColor : 
        selected ? categoryColor.darker() : Color.WHITE;

    WorldImage cell = new RectangleImage(size, size, OutlineMode.SOLID, bgColor)
        .overlayImages(new RectangleImage(size, size, OutlineMode.OUTLINE, Color.BLACK));

    WorldImage wordText = new TextImage(text, 20, Color.BLACK);
    return new OverlayOffsetAlign(AlignModeX.CENTER, AlignModeY.MIDDLE, wordText, 0, 0, cell);
  }
}

class Group {
  ArrayList<Word> words;
  Color color;
  int displayTimer;

  // Constructor for Group class
  Group(ArrayList<Word> words, Color color) {
    this.words = new ArrayList<>(words);
    this.color = color;
    this.displayTimer = 60;
  }
}

class ExamplesConnections {
  // Test Category class
  void testCategoryCreation(Tester t) {
    // Tests the creation of a Category object
    Category cat = new Category(Color.YELLOW, "A", "B", "C", "D");
    t.checkExpect(cat.wordTexts.size(), 4);
    t.checkExpect(cat.color, Color.YELLOW);
  }

  void testCreateWords(Tester t) {
    // Tests the createWords method of the Category class
    Category cat = new Category(Color.GREEN, "X", "Y", "Z");
    ArrayList<Word> words = cat.createWords();
    t.checkExpect(words.size(), 3);
    t.checkExpect(words.get(0).categoryColor, Color.GREEN);
  }

  // Test Word class
  void testWordSelection(Tester t) {
    // Tests the selection functionality of the Word class
    Word word = new Word("TEST", Color.YELLOW);
    t.checkExpect(word.selected, false);
    word.selected = true;
    t.checkExpect(word.selected, true);
  }

  void testWordGrouped(Tester t) {
    // Tests the grouped functionality of the Word class
    Word word = new Word("TEST", Color.YELLOW);
    t.checkExpect(word.grouped, false);
    word.grouped = true;
    t.checkExpect(word.grouped, true);
  }

  void testWordRender(Tester t) {
    // Tests the render method of the Word class
    Word word = new Word("TEST", Color.YELLOW);
    WorldImage image = word.render(100);
    t.checkExpect(image instanceof WorldImage, true);
  }

  // Test Group class
  void testGroupCreation(Tester t) {
    // Tests the creation of a Group object
    ArrayList<Word> words = new ArrayList<>();
    words.add(new Word("A", Color.YELLOW));
    Group group = new Group(words, Color.YELLOW);
    t.checkExpect(group.words.size(), 1);
    t.checkExpect(group.displayTimer > 0, true);
  }

  void testGroupTimer(Tester t) {
    // Tests the displayTimer functionality of the Group class
    ArrayList<Word> words = new ArrayList<>();
    words.add(new Word("A", Color.YELLOW));
    Group group = new Group(words, Color.YELLOW);
    int initialTimer = group.displayTimer;
    group.displayTimer--;
    t.checkExpect(group.displayTimer, initialTimer - 1);
  }

  void testGroupColor(Tester t) {
    // Tests the color attribute of the Group class
    ArrayList<Word> words = new ArrayList<>();
    words.add(new Word("A", Color.YELLOW));
    Group group = new Group(words, Color.GREEN);
    t.checkExpect(group.color, Color.GREEN);
  }

  // Test ConnectionsWorld
  void testInitializeWordsSize(Tester t) {
    // Tests the size of the initialized words in ConnectionsWorld
    ConnectionsWorld world = new ConnectionsWorld();
    t.checkExpect(world.words.size(), 16);
  }

  void testCheckCategoryPositive(Tester t) {
    // Tests the checkCategory method with a correct category
    ConnectionsWorld world = new ConnectionsWorld();
    ArrayList<Word> testWords = new ArrayList<>();
    testWords.add(new Word("A", Color.YELLOW));
    testWords.add(new Word("B", Color.YELLOW));
    testWords.add(new Word("C", Color.YELLOW));
    testWords.add(new Word("D", Color.YELLOW));
    t.checkExpect(world.checkCategory(testWords), true);
  }

  void testCheckCategoryNegative(Tester t) {
    // Tests the checkCategory method with an incorrect category
    ConnectionsWorld world = new ConnectionsWorld();
    ArrayList<Word> testWords = new ArrayList<>();
    testWords.add(new Word("A", Color.YELLOW));
    testWords.add(new Word("B", Color.YELLOW));
    testWords.add(new Word("C", Color.YELLOW));
    testWords.add(new Word("D", Color.GREEN));
    t.checkExpect(world.checkCategory(testWords), false);
  }

  void testProcessGuessCorrect(Tester t) {
    // Tests the processGuess method with a correct guess
    ConnectionsWorld world = new ConnectionsWorld();
    ArrayList<Word> testWords = new ArrayList<>();
    testWords.add(new Word("A", Color.YELLOW));
    testWords.add(new Word("B", Color.YELLOW));
    testWords.add(new Word("C", Color.YELLOW));
    testWords.add(new Word("D", Color.YELLOW));
    world.testSetWords(testWords);

    world.processGuess(testWords, true);
    t.checkExpect(testWords.get(0).grouped, true);
    t.checkExpect(world.foundGroups.size(), 1);
  }

  void testDeselectAll(Tester t) {
    // Tests the deselectAll method
    ConnectionsWorld world = new ConnectionsWorld();
    world.words.get(0).selected = true;
    world.words.get(1).selected = true;
    world.deselectAll();
    t.checkExpect(world.words.get(0).selected, false);
    t.checkExpect(world.words.get(1).selected, false);
  }

  // Run the game
  void testGame(Tester t) {
    // Runs the game with a fixed random seed for consistent testing
    ConnectionsWorld world = new ConnectionsWorld(new Random(42));
    world.bigBang(world.width, world.height);
  }
}