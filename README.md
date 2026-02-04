# data_analysis_and_ML_website
## Overview
This project is a web-based Data Analysis and Machine Learning application built using Python and Flask for the backend and HTML, CSS, and JavaScript for the frontend.

The application provides an interactive, no-code interface to upload datasets and perform:

- Exploratory Data Analysis (EDA)

- Data Visualization

- Data Cleaning & Preprocessing

- Machine Learning Model Building and Evaluation

The objective of this project is to simplify EDA, preprocessing, and model building without requiring users to write code manually.

## Application Structure

The application is divided into three main sections:

1) Basic Data Information

2) Data Visualization

3) Data Processing
   
4) Model Building (Machine Learning)

Each section performs a specific set of analytical and transformation tasks on the uploaded dataset.

### Section 1: Basic Data Information

This section focuses on understanding the structure and quality of the dataset.

#### Dataset Preview

- Display first 5 rows

- Display last 5 rows

- Display random 5 rows

#### Dataset Metadata

- Column names

- Data types

- Dataset shape

- Memory usage

#### Statistical Summary

- Descriptive statistics using Pandas describe()

- Overview of numerical feature distributions

- Data Quality Analysis

- Missing value count per column

- Duplicate record detection

- Unique value analysis

- Correlation between numerical features

### Section 2: Data Visualization

This section provides graphical insights into the dataset using various plot types.

#### Univariate Analysis

- Count plots

- Pie charts

- Histograms

- Kernel Density Estimation (KDE) plots

- Box plots

#### Bivariate Analysis

- Scatter plots

- Box plots

- Bar plots

- Line plots

- Heatmaps

- Pair plots

### Section 3: Data Processing

This section allows users to clean and transform data interactively.

#### Data Cleaning Operations

- Handling missing values using multiple strategies

- Removing duplicate records

- Outlier detection and removal

#### Data Transformation Operations

- Changing data types of selected columns

- Removing unwanted columns

- Modifying dataset structure

#### Dynamic Updates

- Real-time re-analysis after each operation

- Automatic refresh of statistics and visualizations

#### Export Functionality

- Download the processed and analyzed dataset

### section 4:Model Building
This section enables end-to-end machine learning workflows directly inside the web application.

#### Key Features Implemented

1) Target Variable Selection

- Choose the dependent (output) variable for modeling

2) Train-Test Split Configuration

- Adjustable test size

- Random state selection

- Shuffle option

3) Data Preprocessing & Pipelines

- Automatic pipeline creation

- Feature scaling

- Categorical encoding

4) Model Selection
Users can choose from multiple algorithms:

- Linear Regression

- Logistic Regression

- K-Nearest Neighbors (KNN)

- Support Vector Machine (SVM)

- Decision Tree

- Random Forest

5) Model Training

- Train selected models directly within the web interface

6) Model Evaluation

For Regression Models:

- R² Score

- Mean Squared Error (MSE)

- Mean Absolute Error (MAE)

- Root Mean Squared Error (RMSE)

- Predicted vs Actual table

- Best-fit line visualization

For Classification Models:

- Accuracy

- Precision

- Recall

- F1 Score

- Confusion Matrix

- Classification Report

7) Model Export

- Download trained models as .pkl files for future use
- 
## Technology Stack
### Frontend

- HTML

- CSS

- JavaScript

### Backend

- Python

- Flask

### Data Processing and Visualization

- Pandas

- NumPy

- Matplotlib

- Seaborn
  
- scikit-learn

## System Workflow

- User uploads a CSV or Excel file

- Backend loads dataset into memory

- four sections become available

- User explores data using Basic Data Information

- User visualizes data using Data Visualization

- User processes data using Data Processing
- User builds and evaluates models using Model Building

- Results update dynamically

- User downloads the final processed dataset and trained model

## Installation and Execution
### Prerequisites

- Python 3.x

- pip package manager

### Setup Steps

- Clone the repository

- Create a virtual environment

- Install required dependencies

- Run the Flask application

- Open the application in a web browser

- Upload a CSV or Excel file to start analysis

## Application Use Cases

- Exploratory Data Analysis (EDA)

- Data cleaning and preprocessing
- Machine learning model training

- Academic and research projects

- Business analytics

- Dataset validation and inspection

## Project Objectives

- Provide a no-code interface for data analysis and ML

- Automate repetitive data exploration tasks

- Improve productivity in preprocessing workflows

- Enable real-time feedback during transformations
- Make machine learning accessible to beginners

## Future Enhancements

- Performance optimization for large datasets

- Interactive plotting libraries integration

- Advanced preprocessing techniques

- Deep learning model integration

- User authentication and session management
- Model comparison and hyperparameter tuning

## Author

Developed by Shivansh Dhakad
