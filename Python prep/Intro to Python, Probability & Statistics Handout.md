

### **Unit 1: Intro to Python, Probability & Statistics**

* **Jupyter Notebook:** An interactive web-based document combining live code, explanatory text, and visualizations in one place.  
* **Cells:** \* **Code Cells:** Areas for writing and running programming instructions.  
  * **Text Cells:** Areas used for notes, instructions, or explanations.  
* **Execution:**   
  * **The Kernel:** The background "brain" that performs calculations and runs code.  
  * **Errors:** Displays a "traceback" message explaining what went wrong and where.  
* **Numbers:** Python handles numbers as **integers** (whole) or **floats** (decimals).  
* **Variables:** A name that "binds" to a specific value, serving as a label for data.  
* **Assignment:** Uses the \= symbol to evaluate the expression on the right and bind the result to the name on the left.  
* **Nested Expressions:** You can use existing variable names or smaller calculations inside larger ones; Python evaluates the innermost parts first.  
* **Function Calls:** A "Call Expression" runs pre-made code called a Function.  
* **Name and Arguments:** You write the Function Name, then put inputs (Arguments) inside parentheses, separated by commas if multiple.  
* **Function Body & Return:** Inside a function is a sequence of stored statements (Body); it "gives back" a result known as the **Return Value**.

**Exercise:** unit1 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit1))

---

### **Unit 2: Tables**

* **Importing Modules:** Opening a "toolbox" using import to bring in specific tools like datascience for tables or numpy for math.  
* **Tables:** A sequence of labeled columns.  
  * **Rows:** Each represents a single individual.  
  * **Columns:** Each represents a specific attribute.  
  * **Labels:** Unique names identifying the attributes.  
* **Table Selection & Dropping:** \* t.select(label): Creates a new table with only specified columns.  
  * t.drop(label): Creates a new table where specified columns are removed.  
* **Table Sorting & Filtering:** \* t.sort(label): Rearranges rows based on values in a specific column.  
  * t.where(label, condition): Keeps only rows satisfying a specific rule.  
* **Why datascience.Table?**: It is a high-level wrapper designed for learning.  
  * **Human-Readable Syntax:** Uses descriptive verbs like .with\_column and .where.  
  * **Logic First:** Focuses on underlying logic identical to SQL, Excel, and professional AI libraries.  
* **Transferable Skills:** \* **SQL Databases:** The logic of .join and .where is how professional databases are queried.  
  * **Pandas:** Table operations have direct counterparts in the industry-standard Pandas library.  
  * **Spark:** High-speed AI clusters use the same "chaining" method.

**Exercise:** unit2 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit2))

---

### **Unit 3: Data Types, Arrays & Ranges**

* **Fundamental Data Types:** \* int: Integers/whole numbers (e.g., 2, \-500).  
  * float: Decimal numbers (e.g., 2.2, 1.0) with limited precision (15-16 places).  
  * str: "Strings" of text enclosed in quotes (e.g., 'Red fish', "12").  
* **Arrays & Ranges:** \* **Array:** A sequence where all elements should be the same type.  
  * **Element-wise Math:** Arithmetic applies to every element individually (e.g., array \* 2 doubles every entry).  
  * **Ranges:** np.arange(start, end, step) creates consecutive numbers, including the start but excluding the end.  
* **Creating Tables:** \* Table(): Creates an empty table.  
  * .with\_columns('Label', array): Adds columns with a label and an array of values.  
  * Table.read\_table(filename): Loads data from files like CSVs.

**Exercise:** unit3 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit3))

---

### **Unit 4: Visualization and Distribution**

* **Categorical vs. Numerical Data:** \* **Categorical:** Fits into specific groups (e.g., Color, Zip Code).  
  * **Numerical:** Represents a quantity where math makes sense (e.g., Height, Speed).  
  * **Rule:** Just because it’s a number doesn’t mean it’s numerical (e.g., Area Code).  
* **Plots:**  
  * **Scatter Plot:** One dot per individual; used to see if two numerical variables relate. table.scatter(x\_axis, y\_1, y\_2, …)  
  * **Line Plot:** Connected dots; used when the horizontal axis has a logical order like Time. table.plot(x\_axis, y\_1, y\_2, …)  
* **Distributions & Bar Charts:** \* **Distribution:** Shows all possible values and their frequencies.  
  * **Bar Charts:** For categorical data; heights show how many individuals are in each category.  
  * table.bar(categories\_column)  
* **Binning (Grouping Numbers):** Turns a range of numbers into a single group.  
  * **Rule:** \[Start, End) means Start is included, End is not.  
  * bins \= np.make\_array(0,12,26,40)  
* **Histograms & Area:** A bar chart for numbers.  
  * **Area Principle:** The **Area** (not just height) represents the percentage.  
  * **Total Area:** Always equals 100%.  
  * table.select(numerical\_column).hist(bins=bins)

**Exercise:** unit4 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit4))

---

### **Unit 5: Functions and Applying to Tables**

* **Defining Functions:** \* def: Keyword to start a definition.  
  * **Name, Argument/Parameter, Body, Return:** Components that allow code reuse.  
  * **Simple Formula:** def name(input): return result\_expression.  
* **The apply Method:** \* Calls a function on every single element in a column.  
  * **Command:** table\_name.apply(function\_name, 'column\_label').  
  * **Integration:** Often used within .with\_column to add results back to the table.

**Exercise:** unit5 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit5))

---

### **Unit 6: Grouping and Joining**

* **Lists and Rows:** \* **List:** A container for mixed data types.  
  * **Usage:** Lists are best for representing a single **Row**.  
  * t.with\_row(\[val1, val2\]): Adds a list as a new entry at the bottom.  
* **Grouping (Summary Tables):** group collapses rows that share a value.  
  * **Counting:** Tells you how many rows are in each group.  
  * **Multi-Group:** Can group by multiple columns simultaneously (e.g., \['Year', 'City'\]).  
  * **Math:** You can choose a function (sum, mean) for the group.  
* **Pivot Tables:** A 2D grouping that creates a grid (Top Variable vs. Side Variable).  
* **Joining Tables:** Combines tables by matching a shared "Key" column.  
  * **Result:** A single wide row for matching values.  
  * **Warning:** Non-matching values usually disappear from the result.

**Exercise:** unit6 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit6))

---

### **Unit 7: Loops and Booleans**

* **Booleans and Comparisons:** Values that are either True or False.  
  * **Operators:** \==, \!=, \>, \<, \>=, \<=.  
* **Control Statements (if):** Allows code to branch based on a condition.  
* **Random Selection:** np.random.choice(my\_array, 5\).  
  * **Replacement:** By default, it can pick the same item twice.  
* **Iteration (Loops):** for loops repeat a task for every item in a sequence.  
* **Saving Results (Appending):** Using np.append to glue loop results into a new array.

**Exercise:** unit7 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit7))

---

### **Unit 8-9 (Part A): Probability & Randomness**

* **Probability:** A number between 0 and 1\.  
* **Equally Likely:** If there are 4 sides on a spinner, each has a 1/4 chance.  
* **The Complement:** [![][image1]](https://www.codecogs.com/eqnedit.php?latex=P\(%5Ctext%7BNot%20Happening%7D\)%20%3D%201%20-%20P\(%5Ctext%7BHappening%7D\)#0).  
* **Rules:**   
  * **Multiplication (AND):** [![][image2]](https://www.codecogs.com/eqnedit.php?latex=P\(A%20%5Ctext%7B%20then%20%7D%20B\)%20%3D%20P\(A\)%20%5Ctimes%20P\(B%20%5Ctext%7B%20given%20%7D%20A\)#0).  
  * **Addition (OR):** [![][image3]](https://www.codecogs.com/eqnedit.php?latex=P\(%5Ctext%7BWay%201%20OR%20Way%202%7D\)%20%3D%20P\(%5Ctext%7BWay%201%7D\)%20%2B%20P\(%5Ctext%7BWay%202%7D\)#0).  
* **Independence:** Whether one outcome changes the probability of another.  
  * **Independent AND:** [![][image4]](https://www.codecogs.com/eqnedit.php?latex=P\(A%20%5Ctext%7B%20and%20%7D%20B\)%20%3D%20P\(A\)%20%5Ctimes%20P\(B\)#0).  
  * **Sampling:** WITH replacement creates independent events; WITHOUT does not.  
* **Distributions:**   
  * **Probability Distribution:** The theoretical "Blueprint".  
  * **Empirical Distribution:** The observed "Reality" from a sample.  
  * **Law of Averages:** Large random samples will almost certainly result in an empirical distribution matching the probability distribution.

**Exercise:** Unit8-9 (Part A) ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/Unit8-9))

---

### **Unit 8-9 (Part B): Inference & Hypothesis Testing**

* **Inference & Estimation:** \* **Parameter:** Fixed, usually mysterious number for the entire Population.  
  * **Statistic:** Number calculated from a Sample.  
  * **Statistical Inference:** Using a Statistic to estimate an unknown Parameter.  
* **Assessing Models & Hypotheses:** \* **Null Hypothesis:** Status Quo; assumes patterns are due to chance.  
  * **Alternative Hypothesis:** Assumes a real effect or bias exists.  
  * **Test Statistic:** A single number calculated to decide between hypotheses; often the distance between observation and prediction.  
* **Simulation under Null:** Deciding if a statistic is "weird" by simulating the process thousands of times assuming the Null is true.  
* **Conclusion:** \* **Consistent:** Observed statistic is in the "middle" of the simulation histogram.  
  * **Inconsistent:** Observed statistic is far in the tail.

**Exercise:** Unit8-9 (Part B) ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/Unit8-9))

---

### **Unit 10: Center, Spread & The Bell Curve**

* **Center:** \* **Percentiles:** Ranking number showing the percentage of data falling below a value.  
  * **Median:** The 50th Percentile.  
  * **Mean:** The balance point; easily pulled by extreme values.  
* **Skewness:** **Right Skew** pulls the Mean right; **Left Skew** pulls it left.  
* **Spread:** \* **Standard Deviation (SD):** The typical distance from the average.  
  * **SD Recipe:** 1\. Average, 2\. Deviations, 3\. Square deviations, 4\. Average squares, 5\. Square root.  
  * **Standard Units (z-scores):** Normalizes values. Tells you how many SDs a value is from the average.  
  * **Formula:** [![][image5]](https://www.codecogs.com/eqnedit.php?latex=z%20%3D%20%5Cfrac%7B\(%5Ctext%7Bvalue%7D%20-%20%5Ctext%7Baverage%7D\)%7D%7B%5Ctext%7BSD%7D%7D#0).  
* **The Bell Curve (Normal Distribution):** Symmetric shape centered on the Mean/Median.  
  * **68-95-99.7 Rule:** 68% within 1 SD, 95% within 2 SDs, 99.7% within 3 SDs.  
* **Central Limit Theorem (CLT):** For large random samples with replacement, the sample average distribution is roughly a Bell Curve.  
* **Correlation Coefficient ([![][image6]](https://www.codecogs.com/eqnedit.php?latex=r#0)):** Measures strength/direction of linear association from \-1 to 1\.  
  * **Formula:** Average of the product of [![][image7]](https://www.codecogs.com/eqnedit.php?latex=x#0) and [![][image8]](https://www.codecogs.com/eqnedit.php?latex=y#0) in standard units.  
* **Correlation vs. Causation:** Correlation does NOT imply causation; lurking (confounding) variables may be responsible.

**Exercise:** unit10 ([https://colab.research.google.com/github/tomer-libal/dlh-24065](https://www.google.com/search?q=https://colab.research.google.com/github/tomer-libal/dlh-24065/unit10))

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQkAAAAQBAMAAAD36JewAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMAid3vzburmXZEVBBmMiJm6649AAAALUlEQVR4Xu3OMREAAAiAQLV/WRPoyJ0FXPiRiZz413XLCy/gBbyAF/ACXsALLEscAhCnFv1jAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMkAAAAQBAMAAABO2UbRAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMAid3vzburmXZEVBBmMiJm6649AAAAJklEQVR4XmP8z0B78JEJXYQmYNQWUsGoLaSCUVtIBaO2kAqGky0AZwACEJFstkUAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJgAAAAjBAMAAACa4d6kAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMAZqvd780Qu4mZMiJEdlTva7LgAAAAMElEQVR4Xu3MoREAAAiAQHX/nbXbOI18JJAdf2qHC2ecM84Z54xzxjnjnHHOuNfZAPcbAUWqcVZvAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAHBAMAAAA2fErgAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMAMonN792ZVES7Iqt2EGZy3n0PAAAAEklEQVR4XmP8z8DwkYkBCHASAEAlAf5K3ejTAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAHBAMAAADHdxFtAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMARIm73e92MmarzVQiEJktzfMGAAAAEUlEQVR4XmP8z8DAwMSAjwAAIvYBDazScAcAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAALBAMAAABBvoqbAAAAMFBMVEX///8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx9fPp3uAAAAD3RSTlMAEFSr3e/NiTJEIplmu3ak7QEkAAAAEklEQVR4XmP8z8DwkYkBCEgiAGhhAgZfdY9rAAAAAElFTkSuQmCC>