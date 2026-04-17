# I. Core Mathematical Definitions

## Functions & Equations

* **Function (f(x)):** A mathematical rule that takes an input and gives you a specific output.  
* **Independent Variable (x):** Also known as the pre-image.  
* **Image (f(x)):** The specific output of x under the function f.  
* **Domain (Df):** The set of all possible "legal" input values for which the function is defined.  
* **Range:** The set of all actual output values (f(x)).

[https://www.geogebra.org/m/NCAjb5Q9](https://www.geogebra.org/m/NCAjb5Q9)

Consider the function f(x) \= x^2 \+ 1\. Find the images for x \= 3 and x \= \-3. Can the image contain more than one value for a variable? Can the pre-image? If the Domain is "all real numbers," can the image f(x) ever be a number less than 1?

* **Cartesian Coordinate System (Cf):** The graph consisting of all points with coordinates (x, f(x)) where x belongs to the Domain Df.  
* **Vertical Line Test:** A rule stating a curve in the plane is a function if and only if no vertical line intersects it more than once.

[https://www.geogebra.org/m/kmZFpuv3](https://www.geogebra.org/m/kmZFpuv3)

Based on the Vertical Line Test, is the relationship x \= y^2 a function? Why or why not If an ML model for "Expected Stock Price" behaved like this curve, why would it be a problem for a trader?

* **Domain Constraints:** Rules defining which inputs (x) are "legal" (e.g., prohibition of division by zero).  
* **Monotonicity:**  
  * **Increasing:** As x gets larger, f(x) also gets larger (uphill).  
  * **Decreasing:** As x gets larger, f(x) gets smaller (downhill).  
* **Extrema:**  
  * **Local Maximum:** A point higher than those immediately around it.  
  * **Local Minimum:** A point lower than those immediately around it.

[https://www.geogebra.org/m/XXPAGxeU](https://www.geogebra.org/m/XXPAGxeU)

Consider the function f(x) \= 10 / x , for x \> 0\. If the range is only natural numbers, what would be the Domain Constraint for this function? Pick two numbers, x=2 and x=5. Calculate their images. Is the function increasing or decreasing between these two points?

* **Linear Function:** A function of the form f(x) \= ax. Its graph is a straight line passing through the origin (0,0).  
* **Affine Function:** A function of the form f(x) \= ax \+ b. Its graph is a straight line shifted vertically by b.  
* **Slope (a):** Represents the rate of change and determines the "steepness" of the line.  
* **Intercept (b):** The value of the function when x=0; where the line crosses the vertical y-axis.

[https://www.geogebra.org/m/j3sPyXGQ](https://www.geogebra.org/m/j3sPyXGQ)

You are building a simple ML model to predict the total cost of a cloud server. There is a fixed setup fee of 50, and then it costs 0.10 per hour of use Write the function f(x) for the total cost, where x is the number of hours Is this function Linear or Affine? Why? What is the slope (a)?

* **Quadratic Function:** A non-linear function f(x) \= ax^2 \+ bx \+ c (a ≠ 0\) forming a symmetrical U-shaped parabola.  
* **Vertex Form:** f(x) \= a(x \- X)^2 \+ Y (Vertex at (X,Y)).  
* **Factored Form:** f(x) \= a(x \- x1)(x \- x2) (Roots at x1 and x2).

[https://www.geogebra.org/m/qd6zb3cb](https://www.geogebra.org/m/qd6zb3cb)

An ML model's error is defined by the function E(w) \= 3(w \- 10)^2 \+ 450 Without graphing, identify the "Weight" (w) that results in the lowest possible error. What is that minimum error value? Does this error function ever hit zero?

* **Convexity:**  
  * **Convex (a \> 0):** Parabola opens upward (U-shape); vertex is the Global Minimum.  
  * **Concave (a \< 0):** Parabola opens downward (cap-shape); vertex is the Global Maximum.  
* The **Root Count (Discriminant)** is defined as D \= b^2 \- 4ac, where D \> 0 yields two real roots (crosses x-axis), D \= 0 yields one real root (touches at vertex), and D \< 0 results in zero real roots.   
* Key **Algebraic Identities** include the Perfect Square Trinomials, x^2 \+/- 2xy \+ y^2 \= (x \+/- y)^2, and the Difference of Squares, x^2 \- y^2 \= (x \+ y)(x \- y).   
* For **Form Conversions**, the Vertex Form is a(x \- X)^2 \+ Y (where X \= \-b/2a and Y \= f(X)), while the Factored Form is a(x \- x1)(x \- x2), with roots found via the quadratic formula: x \= (-b \+/- sqrt(D)) / 2a

[https://www.geogebra.org/m/jtkhuquv](https://www.geogebra.org/m/jtkhuquv)

Convert x^2 \+ 6x \+ 5 into a factored form a(x \- x1)(x \- x2)

* **Equation:** A statement asserting two expressions are equal (A \= B).  
* **Inequality:** A statement comparing the relative size or order (A \< B, A \> B, A ≤ B, A ≥ B).  
* **Logical Connectivity:**  
  * **Conjunction (AND):** Solution must satisfy all conditions simultaneously.  
  * **Disjunction (OR):** Solution satisfies at least one condition.

[https://www.geogebra.org/m/bmm9dwqz](https://www.geogebra.org/m/bmm9dwqz)

Solve the linear equation: 4x \- 8 \= 2x \+ 2 Solve the linear inequations: −3x \< 12 7 \- 2(x \+ 4\) \<= 10 \- 5x (5 \- 3x)/2 \> x \+ 10

* **Sign Analysis:** A method to determine where an expression is positive, negative, or zero using a Sign Table.

[https://www.geogebra.org/m/eGNywCa7](https://www.geogebra.org/m/eGNywCa7)

You are filtering data for a recommendation engine using the following system: A: 2x \- 6 \> 0 B: \-x \+ 5 \> 0 Solve the system to find the values of x Build the sign table

* The **General Form** of a quadratic equation occurs when a quadratic function Q(x) is set equal to another quadratic or linear function P(x), which can always be rewritten into the   
* **Standard Form**: ax^2 \+ bx \+ c \= 0\. To find the "roots" (the x-values that satisfy the equation),   
* the **Factoring Method** is used to convert the standard form into a product of linear parts: a(x \- x1)(x \- x2) \= 0\. This relies on the **Zero-Product Property**, which states that if a product equals zero, at least one factor must be zero, allowing you to solve for each root individually (e.g., x \- x1 \= 0).

https://www.geogebra.org/m/jKkjyQMh

A model's error threshold is defined by: 3x^2 \- 15x \+ 18 \= 0 Find the root(s) for x?

* To solve a **Quadratic Inequality** like ax^2 \+ bx \+ c \> 0, you must identify the intervals where the parabola sits above the x-axis.   
* This is governed by the **"a" Rule**: if a \> 0 (Cup-shape), the expression is positive on the outside of the roots and negative between them; if a \< 0 (Cap-shape), it is negative on the outside and positive between them.   
* In cases where there are **no roots**, the parabola never crosses the x-axis, meaning the expression is either always positive (if a \> 0\) or always negative (if a \< 0).

[https://www.geogebra.org/m/BU4x8ShK](https://www.geogebra.org/m/BU4x8ShK)

A model's "Stability Range" is defined by \-x^2 \+ 16 \> 0 Find the roots Determine the shape Find the intervals

* A **System of Quadratic Inequalities** is solved by finding the region on the number line where the solution sets of all individual inequalities overlap.   
* The **Resolution Method (Sign Table)** involves five steps: 1\) **Standardize** by setting each inequality against zero; 2\) **Find all Roots** for every expression in the system; 3\) **Construct the Table** with a row for each inequality and all roots ordered across the top; 4\) **Analyze Signs** to determine if each expression is positive (+) or negative (-) in the intervals between roots; and 5\) **Find the Overlap** by identifying the columns where every inequality simultaneously satisfies its condition.

[https://youtu.be/FUUKuZ4jv08](https://youtu.be/FUUKuZ4jv08)

Find the valid range for a model parameter x that satisfies this system: x^2 \- 4 \> 0 x^2 \- 9 \< 0

### Unit Exercise

A: Let f(x)=2x-2

1) Solve f(x)=0  
2) What is the f(x)’s slope? Is it increasing function or decreasing?  
3) Solve f(x)\>0

B: Let g1(x)=2x \+ 4

1) Will f(x) and g(x) intercept at a particular value of x? Why?  
2) Replace g1(x) by g2(x)=-x+4  
3) Solve f(x)=g2(x)   
4) Solve f(x)\<g2(x)

C: Let f(x)=x^2-2 and g(x)=x+1

1) Solve f(x)=g(x). How many solution do you find?  
2) Solve f(x)\<g(x)  
3) Plot the inequality solutions in Colab notebook

#### 

   ## Calculus

* The **Slope (gradient)** measures the "steepness" and direction of a line, representing a constant rate of change.   
* Using the **Linear Formula**, the slope "a" for any two points (x1, y1) and (x2, y2) is calculated as the ratio a \= (y2 \- y1) / (x2 \- x1).   
* This is often simplified through **Staircase Visualization**, where the slope remains consistent across the entire line; for every 1 unit moved to the right, you move "a" units vertically (up or down), forming a predictable pattern.

[https://www.geogebra.org/m/TzhXQqvu](https://www.geogebra.org/m/TzhXQqvu)

A linear model predicts the price of a data storage plan. At 2 terabytes (x1), the cost is $10 (y1). At 5 terabytes (x2), the cost is $25 (y2). Calculate the slope (a) using the Linear Formula. Using the Staircase Visualization, if you increase the storage by 1 more terabyte (to 6 total), how much will the price be?

* **Derivative:** The slope (gradient) of a function.  
* **Secant Line:** A line connecting two distinct points on a curve representing the average rate of change.  
* **Tangent Line:** A line touching a curve at exactly one point representing the instantaneous rate of change (the derivative).

[https://www.geogebra.org/m/U9gqRYyd](https://www.geogebra.org/m/U9gqRYyd)

Look at the function Q(x) \= x^2 Pick two points: x \= 1 and x \= 3\. Calculate the Secant Slope (Average Change) between them using the formula: (y2 \- y1) / (x2 \- x1)

* To analyze **Curves and Slopes**, we use a shortcut called the **Power Rule** to find the slope formula (derivative) of a function without drawing tangent lines.   
* For a basic **Quadratic Function** where f(x) \= x^2, the slope formula is f'(x) \= 2x, and for   
* the **General Quadratic Rule** where f(x) \= ax^2 \+ bx \+ c, the derivative is f'(x) \= 2ax \+ b.   
* Applying **General Polynomial Rules**, if the function is f(x) \= x^n, then the derivative is f'(x) \= nx^(n-1), allowing you to calculate the exact steepness at any point along the curve.

[https://www.geogebra.org/m/sncwbqfn](https://www.geogebra.org/m/sncwbqfn)

You are training a simple model where the error follows the formula: f(x) \= 2x^4 \+ 3x^2 \+ 8 Find the derivative formula f'(x) Calculate the exact slope when x \= 2

* **Integral:** The process of "putting things back together" to find a total amount; visually, the Area Under the Curve.  
* **Riemann Sum:** A method to compute an integral by dividing the area into many thin rectangles.

[https://www.geogebra.org/m/Bgst6SAB](https://www.geogebra.org/m/Bgst6SAB)

Estimate the area under f(x) \= x^2 from x=0 to x=4 using only 2 rectangles Which point of measurement can you take? Now try another reference point

* To calculate **Integrating Polynomials** in practice, we use the **Table of Usual Derivative Functions** in reverse to find the antiderivative.   
* A critical part of this process is the **\+C (Constant of Integration)**; because the derivative of any constant is zero, we must add "C" when integrating to account for the fact that we don't know if the original function had a vertical shift. For a general polynomial term, the Power Rule for integration is defined as: the integral of x^n dx \= (x^(n+1) / (n+1)) \+ C.

[https://www.geogebra.org/m/EsQnTHYC](https://www.geogebra.org/m/EsQnTHYC)

An AI’s "learning improvement" rate is given by the function: f'(x) \= 6x^2 \+ 2x What is the integral of f’(x)? If the AI started with an initial knowledge of 10, what is the value of C?

* **Optimization** is the branch of mathematics focused on finding the best possible solution—specifically, identifying the x-value that either **minimizes a cost/loss** or **maximizes a profit/efficiency**.   
* For **Convex Functions** (cup-shaped/U-shaped), the derivative f'(x) is always increasing, which ensures that any local minimum found is also the **Global Minimum**; since there is only one "bottom," finding the point where the slope is zero, f'(x) \= 0, guarantees the absolute best solution.   
* To **Optimize a Problem**, you follow three steps: 1\) **Modeling**, where you translate the scenario into a function f(x) and define the study interval; 2\) **Differentiation**, to calculate the derivative f'(x); and 3\) **Critical Point** analysis, where you solve f'(x) \= 0 to find the horizontal slope representing the potential optimum.

### Unit Exercise

**Part A: Finding the Optimum (The "Valley" or "Peak")**

Let f(x) \= (2x^2 \- 8)^2

1. **Differentiate**: Find f'(x)   
2. **Solve for Zero**: Solve f'(x) \= 0 to find the x-values where the slope is perfectly flat (there are 3 solutions).  
3. **Visual Verification**: Does the curve f(x) have a **Minimum** and/or a **Maximum**? Which ones?

**Part B: Accumulation (Area under the line)**

Let f(t) \= 3t^2 \+ 10

1. **Indefinite Integral**: Find  the integral of f(t). Remember to add the constant \+C.  
2. **Definite Integral**: Calculate the exact area from t \= 0 to t \= 2:  

   **Additional problem:** You have 40 meters of fencing to create a rectangular garden against a wall. What is the maximum area possible ? (Hint: You must cut the fencing into three parts, the fourth part is the wall…)

---

### **II. Tables & Properties**

**Fundamental Properties of Operations**

| Operation | Equations (A=B) | Inequalities (A\<B) |
| :---- | :---- | :---- |
| Addition / Subtraction | A \+ c \= B \+ c | A \+ c \< B \+ c |
| Multiplication by c \> 0 | Ac \= Bc | Ac \< Bc |
| Multiplication by c \< 0 | Ac \= Bc | Ac \> Bc |

**Algebraic Identities**

* x^2 \+ 2xy \+ y^2 \= (x \+ y)^2  
* x^2 \- 2xy \+ y^2 \= (x \- y)^2  
* x^2 \- y^2 \= (x \+ y)(x \- y)

**The Root Count (Discriminant)**

Calculated as **D \= b^2 \- 4ac** for f(x) \= ax^2 \+ bx \+ c:

* **D \> 0:** Two real roots (crosses x-axis twice).  
* **D \= 0:** One real root (touches x-axis at vertex).  
* **D \< 0:** Zero real roots (never touches x-axis).

**Useful Derivative Rules**

| Rule Name | Rule Formula | Example |
| :---- | :---- | :---- |
| **Sum** | (αf \+ βg)' \= αf' \+ βg' | (5x^3 \+ 2x)' \= (15x^2) \+ (2)  |
| **Product** | (fg)' \= f'g \+ fg' | ![][image1] |
| **Quotient** | ![][image2] | ![][image3] |
| **Chain** | For  ![][image4], ![][image5] | ![][image6] |

**Usual Derivative Functions**

| Function f(x) | Derivative f′(x) | Function f(x) | Derivative f′(x) |
| :---- | :---- | :---- | :---- |
| k (constant) | 0 | sin(x) | cos(x) |
| ax | a | cos(x) | \-sin(x) |
| ax^2 | 2ax | ![][image7] | ![][image8] |
| ax^2 | ![][image9] | ![][image10] | ![][image11] |
| ![][image12] | ![][image13] |  |  |

## Linear Algebra Basics

**Vectors & Vector Space**  
A **Vector** is an ordered array (a list) of N numbers. This means it contains N specific values, where each number has a fixed, known position. For example, if we have a vector U, we might write it as U \= (2,1). Here, the first number is 2 and the second is 1\.

A **Vector Space** is a collection or "set" of these vectors where we are allowed to perform mathematical operations, such as adding vectors together or multiplying them by a number.

**Math operations with vectors**

To make vectors useful, we perform two main actions:

* **Vector Addition:** You combine two vectors by adding the numbers in the same slots. If you have two lists, you add the 1st numbers together, then the 2nd numbers, and so on.  
  * *Example:* (1, 2\) \+ (3, 4\) \= (1+3, 2+4) \= (4, 6).  
* **Scalar Multiplication:** A **Scalar** is just a single "standalone" number. Multiplying a vector by a scalar means you "scale" the whole list by that amount.  
  * *Example:* 3 \* (1, 2\) \= (3, 6).

**Special Cases:**

* **The Null Vector (O):** A list of zeros (0, 0, …). Adding this to any vector changes nothing.  
* **The Negative (-U):** Multiplying a vector by the scalar \-1. This flips the direction of the vector.

[https://www.geogebra.org/m/BdujsZVSV4GMwdFF](https://www.geogebra.org/m/BdujsZVSV4GMwdFF)

Positions in a map: With a localisation system, I’m in the position U=(100, 250\) and I want to go to the position Q=(230, \-15) What is the vector V from U to Q?

**Dot Product**  
The **Dot Product** is a way of multiplying two vectors together to get a single, standalone number (a scalar) as the result.

**The Rules:**

* **Same Size:** You can only perform a dot product on two vectors if they have the same number of slots.  
* **The Process:** You multiply the numbers in the same positions (element-wise) and then **sum** all those results together.  
* **Notation:** The dot product of vector U and vector V is written as \<U, V\>.

**Dot Product Properties**  
T**he Angle Rule:** The dot product tells us if two vectors are pointing in the same general direction:

* **Positive (\> 0):** The vectors point in a **similar direction** (angle is less than 90°).  
  * **Zero (= 0):** The vectors are **perpendicular** (exactly 90°). In AI, this means the two vectors have nothing in common.  
  * **Negative (\< 0):** The vectors point in **opposite directions** (angle is greater than 90°).

**Vector Length:** The dot product of a vector with itself, \<U, U\>, gives the square of its length (||U||^2). Therefore, the **Length of U** is the square root of \<U, U\>.

**Cosine Similarity**

While the Dot Product is affected by the magnitude (length) of the vectors, **Cosine Similarity** "filters out" length to focus only on the angle.

* **The Formula:** It is calculated by dividing the Dot Product by the product of the two vectors' lengths: **Cosine Similarity \= \<U, V\> / (||U|| \* ||V||)**  
* **The Scale:** The result is always between **\-1** and **1**.  
  * **1**: The vectors point in the exact same direction (Angle \= 0°).  
  * **0**: The vectors are perfectly independent/orthogonal (Angle \= 90°).  
  * **\-1**: The vectors are diametrically opposed (Angle \= 180°).

[https://www.geogebra.org/m/N9pvSPf4](https://www.geogebra.org/m/N9pvSPf4)

Let U=(-1,2); V=(1.5, 1.9); W=(1, 1.75) Compute the similarities of these vectors in term of length and in term of direction (cosine similarity). Let P=(3, 1.5), what can we say about P compared to U, V or W? Let U \= (-1,2). How many vectors V have we for the equation U+V=0?

**Matrices and Matrix Space**  
A **Matrix** is a 2D grid or "table" of numbers arranged in **n rows** and **m columns** (referred to as an n \* m matrix).

* Think of it as an extension of a vector: while a vector is a single list, a matrix is a collection of lists stacked together.  
* If a matrix has only one column (m=1), it is simply a **Vector**.

The **Matrix Space** is the collection of all possible matrices of a certain size where we can perform mathematical operations.

**Matrix Operations**  
**Matrix Addition (+):** You add two matrices of the same size by adding the numbers in the same positions.  
**Scalar Multiplication:** You multiply every number in the grid by a single standalone number (the scalar).

* Identical to vector addition and scalar multiplication

**Element-wise Multiplication (     ):** You multiply numbers that occupy the exact same row and column in two different matrices.

**Matrix Product (  X  ):** A more complex "row-by-column" multiplication used to combine transformations. The number of columns of the first matrix must be equal to the number of rows of the second matrix.

**Functional Perspective**  
A matrix A of size n x m is not just a static table of data; it is a **linear function** that transforms vectors. It takes an input vector from a "source" space and moves it to a "target" space.

* **The Transformation:** If x is an m-dimensional vector, the function f is defined as f(x) \= A **X** x.  
* **The Dimension Rule:**  
  * **m columns:** Corresponds to the **input size**.  
  * **n rows:** Corresponds to the **output size**  
* **Example:** A 2 x 3 matrix is like a camera—it takes a 3D scene (input) and flattens it into a 2D photograph (output).

**Square Matrices & Inverses**  
When a matrix is square (n \= n), it might have an **Inverse Matrix** (A^{-1}).

* **The Identity Matrix (I):** This is the matrix version of the number "1." Multiplying any vector x by I leaves it unchanged (I **X** x \= x).  
* **The Undo Button:** Multiplying a matrix by its inverse "cancels it out" to create the identity:   
  * A **X** A^{-1} \= I.

**Matrix Properties & Chaining Functions**

Since matrices act as functions, they follow specific rules that allow us to combine them or break them apart. These properties are the foundation of how complex AI models are built.

* **Linearity:** Matrices are "predictable." If you multiply a vector by a number (k) or add two vectors (u+v) before applying the matrix, it is the same as applying the matrix first and then scaling or adding.  
  * *Formula:* A(k **X** (u \+ v)) \= k **X** (Au \+ Av)  
* **Chaining (Composition):** You can chain multiple transformations together. If matrix A transforms a vector, and then matrix B transforms that result, you can simplify the whole process into a single matrix (B **X** A).  
  * **Dimension Check:** If A is n x m and B is p x n, the resulting combined matrix is p x m.  
* **Non-Commutativity:** As mentioned before, the order of chaining matters. In most cases, A **X** B \\= B **X** A.

![][image14]

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPwAAAAPBAMAAAAyg7/jAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAZt2rELsiiUTvmVQyzXajcYypAAAAJklEQVR4XmP8zzCQgAldgL5g1PoBBKPWDyAYtX4Awaj1AwgG2HoA4AkBHSovNFIAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJ0AAAAxBAMAAAAy1rZwAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAZqu7iUTvEM0y3SJUmXZNph/XAAAAN0lEQVR4Xu3MoQHAIADAMOD/Z7kA/Gxwa2RF5xkv7fUtqJ/pZ/qZfqaf6Wf6mX6mn+ln+pm//S5fIgJSUw6tjgAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAO8AAAAqBAMAAACpexGNAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAZqu7iUTvEM0y3SJUmXZNph/XAAAAPElEQVR4Xu3NIQEAIADAMKB/WRKAJ8Awn7z5POOLvd6iNGYaM42ZxkxjpjHTmGnMNGYaM42Zxkxj5tv4AlxuAkRC3jmKAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHkAAAATBAMAAABGu79GAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAECJEVHaJmbvN3e9mMqv4CKprAAAAIUlEQVR4XmP8z0A++MiELkISGNVNDhjVTQ4Y1U0OGEjdAAyDAhbPddOnAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALcAAAATBAMAAAAgzYFUAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAECJEVHaJmbvN3e9mMqv4CKprAAAAKklEQVR4XmP8z0Az8JEJXYSaYNRwrGDUcKxg1HCsYNRwrGDUcKxg6BoOAJLEAhZ+xniHAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPwAAAAVBAMAAACQzp4eAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAZt2rELsiiUTvmVQyzXajcYypAAAALElEQVR4Xu3NoQEAIAzAMOD/n4fnAGIaWdM9Szpv+Ks91B5qD7WH2kPtIby/RW0BKcVSA/EAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAYBAMAAAAIZcBFAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAEklEQVR4XmP8zwADTHDWCGQCAB/QAS99L7hfAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAE0lEQVR4XmP8z4AATEjsUQ5eDgBUUAEv9uxP9AAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAUBAMAAADbzbjtAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAGUlEQVR4XmP8z4ATfGRCF0EGo5IMo5JgAAB4NQIYq4qIngAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAYBAMAAADjUntGAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAFklEQVR4XmP8zwAHH5kQbAaGUQ4+DgBuywIgpdm1bgAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADMAAAAYBAMAAACl5NjsAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAHElEQVR4XmP8z4ADfGRCF0GAUSlkMCqFDMiTAgANmgIgH+YQsQAAAABJRU5ErkJggg==>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAYBAMAAADwhTuyAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAZqt2ibsyIs1E3e8QmVS75V+sAAAAF0lEQVR4XmP8z4ACPjKh8hkYRgUGQgAALnYCILdmEhQAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAcBAMAAAAdLssvAAAAMFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAv3aB7AAAAD3RSTlMAEHar3e9mRLsyIpnNVIkRoUKfAAAAF0lEQVR4XmP8z4AKPjKhCTAwjIoMPxEA+MUCKN2eN5QAAAAASUVORK5CYII=>

[image14]: <data:image/png;base64,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>