# CSVision 📊

### Automated CSV Data Analysis & Visualization Dashboard

CSVision is a Python-based data analysis dashboard that allows users to upload CSV files and automatically explore, analyze, and visualize their data through a simple and interactive Streamlit interface.

Instead of manually inspecting a dataset, CSVision performs automated data analysis and presents the results through visualizations, data-quality metrics, relationship analysis, outlier detection, and numerical insights.

---

## 🚀 Features

### 📂 CSV Upload
- Upload your own CSV dataset directly through the application.
- Automatically reads and processes the uploaded data using Pandas.

### 🔍 Automatic Column Analysis
CSVision automatically identifies different types of columns, including:
- Numerical columns
- Categorical columns
- Identifier columns

### 📊 Automatic Visualizations
The application automatically generates relevant visualizations for numerical data, helping users understand the distribution of their dataset quickly.

### 🔗 Relationship Analysis
CSVision analyzes relationships between numerical columns using scatter plots.

This helps identify possible relationships and patterns between variables.

### 📅 Trend Analysis
If the uploaded dataset contains date-based columns, CSVision can analyze numerical values over time.

### 🧹 Data Quality Analysis
The application checks the uploaded dataset for:
- Missing values
- Duplicate rows
- Rows containing missing values
- Columns containing missing values
- Overall data completeness

### 🚨 Outlier Detection
CSVision detects potential outliers in numerical columns using the **Interquartile Range (IQR)** method.

### 💡 Automated Insights
The application generates basic numerical insights such as:
- Average values
- Minimum values
- Maximum values

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualization |
| Streamlit | Web application interface |

---

## 📁 Project Structure
```text

CSV-Insight-Generator/
│
├── app.py                  # Main Streamlit application
├── analyser.py             # Data analysis and column classification
├── visualizer.py           # Visualization functions
├── insights.py             # Automated insight generation
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
├── assets/
│   └── background.png      # Application background
│
└── sample data/
    ├── students.csv        # Sample student dataset
    └── sales.csv           # Sample sales dataset
```
⚙️ How to Run Locally
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/CSVision.git
2. Navigate to the project directory
cd CSVision
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Git Bash
source venv/Scripts/activate
Windows PowerShell
venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Run the application
streamlit run app.py

The application will open in your browser.

🧪 Sample Datasets

CSVision includes sample datasets to demonstrate the application's functionality.

Students Dataset

Contains information such as:

Marks
Attendance
Study Hours
Department
Gender
Sales Dataset

Contains information such as:

Product
Category
Price
Quantity
Revenue
Region

You can also upload your own CSV files and analyze them using the application.
``` text

🔄 How CSVision Works
        CSV File
           ↓
      CSV Upload
           ↓
    Pandas DataFrame
           ↓
   Column Classification
           ↓
     Data Quality Check
           ↓
 ┌─────────┼──────────┐
 ↓         ↓          ↓
Charts  Relationships  Trends
 ↓         ↓          ↓
 └─────────┼──────────┘
           ↓
    Outlier Detection
           ↓
    Insight Generation
           ↓
      Data Dashboard
```
📈 Example Use Cases

CSVision can be useful for quickly exploring datasets such as:

Student performance data
Sales data
Business datasets
Survey datasets
Customer datasets
Experimental datasets
General tabular CSV data
🎯 Project Goals

The main goal of CSVision is to reduce the amount of manual work required for initial dataset exploration.

Instead of writing separate analysis code for every CSV file, the application attempts to automatically identify the structure of the dataset and provide useful analysis through a single interface.

🔮 Future Improvements

Planned improvements include:

More advanced automated insights
Improved identifier detection
Smarter categorical-data analysis
Additional visualization types
More advanced statistical analysis
Improved error handling
More intelligent dataset recommendations
Cloud Deployment
