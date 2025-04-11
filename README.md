# TAC-using-3D-array
💡 Project Description: Three Address Code Generator for 3D Arrays
This project provides an interactive web interface using Streamlit to generate Three Address Code (TAC) for expressions involving three-dimensional arrays. Users can input the names, dimensions, and index variables for a left-hand side (LHS) array and two right-hand side (RHS) arrays, along with an arithmetic operation.

The tool computes the memory offsets of each array element using the standard row-major formula and generates step-by-step TAC that:

Calculates effective addresses for LHS and RHS arrays

Loads the values from RHS arrays

Applies the selected arithmetic operation (+, -, *, /)

Stores the result back to the LHS array location

This helps visualize how high-level 3D array operations get converted into low-level code that a compiler might generate.


