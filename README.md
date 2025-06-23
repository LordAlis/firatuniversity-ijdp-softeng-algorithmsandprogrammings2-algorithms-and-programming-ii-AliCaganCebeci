[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/HuDt6KLx)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19223275&assignment_repo_type=AssignmentRepo)
# 🔤 Edit Distance (Levenshtein Distance) Visualizer

**Dynamic Programming Visualization for String Transformation**

## 🌐 Streamlit Web App
**Live Application URL:** [https://edit-distance-visualizer.streamlit.app](https://edit-distance-visualizer.streamlit.app)

## 📋 Project Description

This interactive web application implements and visualizes the **Edit Distance** (Levenshtein Distance) algorithm using Python and Streamlit. The application demonstrates how dynamic programming can efficiently calculate the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform one string into another.

**Developed by:** ALİ ÇAĞAN CEBECİ  
**Course:** Algorithms and Programming II - Semester Capstone Project  
**University:** Fırat University - Software Engineering Department  
**Instructor:** Assoc. Prof. Ferhat UÇAR  

## ✨ Features

- **Interactive String Input**: Enter custom strings or choose from predefined examples
- **Step-by-Step Visualization**: Watch the algorithm execute with detailed explanations
- **Dynamic Programming Table**: Visual heatmap showing the DP table construction
- **String Alignment**: Color-coded visualization of character matches and operations
- **Auto-Play Mode**: Automated step-through with adjustable speed
- **Complexity Analysis**: Visual comparison of time complexities
- **Operations Breakdown**: Detailed cost analysis of transformations
- **Responsive Design**: Modern, user-friendly interface

## 🚀 Installation and Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LordAlis/algorithms-and-programming-ii-semester-capstone-project-LordAlis.git
   cd algorithms-and-programming-ii-semester-capstone-project-LordAlis
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

### Usage Instructions

1. **Input Strings**: Enter two strings in the sidebar or select from sample pairs
2. **Visualization Options**: Toggle different visualization features
3. **Explore Tabs**:
   - **Visualization**: See the DP table heatmap and string alignment
   - **Step-by-Step**: Watch the algorithm execute with detailed steps
   - **Analysis**: View complexity analysis and performance metrics
   - **Algorithm Info**: Learn about the Edit Distance algorithm

## 📊 Algorithm Overview

### What is Edit Distance?

The **Edit Distance** between two strings is the minimum number of single-character edits needed to transform one string into another. The three allowed operations are:

- **Insertion**: Add a character (cost: 1)
- **Deletion**: Remove a character (cost: 1)  
- **Substitution**: Replace a character (cost: 1)
- **Match**: Characters are identical (cost: 0)

### Dynamic Programming Approach

The algorithm uses a bottom-up dynamic programming approach:

1. **Initialization**: Create an (m+1) × (n+1) DP table
2. **Base Cases**: Fill the first row and column
3. **Recurrence Relation**:
   ```
   If str1[i-1] == str2[j-1]:
       dp[i][j] = dp[i-1][j-1]  // No cost for match
   Else:
       dp[i][j] = 1 + min(
           dp[i-1][j],    // Deletion
           dp[i][j-1],    // Insertion
           dp[i-1][j-1]   // Substitution
       )
   ```
4. **Result**: The value at `dp[m][n]` gives the edit distance

## 📈 Complexity Analysis

### Time Complexity: **O(m × n)**
- **m**: Length of first string
- **n**: Length of second string
- **Explanation**: We fill each cell in the DP table exactly once

### Space Complexity: **O(m × n)**
- **Storage**: Required for the DP table
- **Optimization**: Can be reduced to O(min(m,n)) with space optimization

### Comparison with Naive Approach

| Approach | Time Complexity | Space Complexity |
|----------|----------------|------------------|
| **Dynamic Programming** | O(m × n) | O(m × n) |
| **Naive Recursive** | O(3^max(m,n)) | O(max(m,n)) |

The DP approach provides exponential speedup over the naive recursive solution.

## 🧪 Testing

Run the unit tests to verify algorithm correctness:

```bash
python test_algorithm.py
```

The test suite includes:
- Basic functionality tests
- Edge cases (empty strings, identical strings)
- Classic examples (kitten → sitting)
- Complex transformations
- Alignment path verification

## 📸 Screenshots

### Main Visualization Interface
![Main Interface](screenshots/main-interface.png)
*Interactive Edit Distance visualization showing DP table heatmap and string alignment for transforming "kitten" to "sitting"*

### Step-by-Step Algorithm Execution
![Step by Step Execution](screenshots/step-by-step.png)
*Algorithm execution with highlighted current step and detailed explanations*

### Complexity Analysis Dashboard
![Complexity Analysis](screenshots/complexity-analysis.png)
*Time and space complexity visualization with performance comparison charts*

### Algorithm Information Tab
![Algorithm Info](screenshots/algorithm-info.png)
*Comprehensive algorithm documentation and educational content*

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── algorithm.py           # Edit Distance implementation
├── utils.py              # Visualization and utility functions
├── test_algorithm.py     # Unit tests
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── data/                # Sample data directory
│   └── .gitkeep         # Keeps directory in git
└── screenshots/         # Application screenshots
    ├── main-interface.png
    ├── step-by-step.png
    ├── complexity-analysis.png
    └── algorithm-info.png
```



## 🎯 Applications

The Edit Distance algorithm has numerous real-world applications:

- **Spell Checkers**: Finding closest word matches
- **DNA Sequencing**: Comparing genetic sequences
- **Plagiarism Detection**: Measuring text similarity
- **Version Control**: Computing file differences (diff)
- **Natural Language Processing**: Text analysis and comparison
- **Autocomplete Systems**: Suggesting corrections
- **Data Deduplication**: Finding similar records

## 🔧 Technical Implementation

### Key Components

1. **algorithm.py**: Core edit distance implementation with step tracking
2. **utils.py**: Visualization functions using Plotly
3. **app.py**: Streamlit interface with interactive controls

### Libraries Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

## 🏆 Academic Context

This project was developed as part of the **Algorithms and Programming II** semester capstone project at Fırat University's Software Engineering Department. The assignment required implementing a unique algorithm with:

- ✅ Interactive web interface
- ✅ Step-by-step visualization
- ✅ Complexity analysis
- ✅ Comprehensive documentation
- ✅ Unit testing
- ✅ GitHub deployment

## 📚 References

1. **Levenshtein, V. I.** (1966). "Binary codes capable of correcting deletions, insertions, and reversals"
2. **Cormen, T. H., et al.** (2009). "Introduction to Algorithms" (3rd ed.)
3. **Skiena, S. S.** (2008). "The Algorithm Design Manual" (2nd ed.)
4. **Algorithm and Programming II Lecture Notes** - Fırat University CS Department (Prof. Ferhat Uçar)

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is developed for educational purposes as part of university coursework.

## 👨‍💻 Author

Name: Ali Çağan Cebeci
Student ID: 240543016   
GitHub: [@LordAlis](https://github.com/LordAlis)  

---

*Developed with ❤️ for Algorithms and Programming II - Semester Capstone Project 2025*
