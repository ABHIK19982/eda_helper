TOP_LEVEL_CELL = '''import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
'''
LOAD_MARKDOWN_CELL = '''# Load data from file'''
LOAD_DATA_CODE_DELL = '''df = pd.read_{FILE_TYPE}('{FILE_PATH}')'''
EDA_MKD_CELL = '''# Data Analysis'''
DESCRIBE_DATA_CODE_CELL = '''df.describe(include = 'all').T'''
ANALYSIS_MKD_CELL = '''## Analysis for {COL}'''
OBJECT_DATA_EDA_CODE_CELL = '''sns.set_style('darkgrid')
plt.figure(figsize = (10, 5))
ax = sns.countplot(data = df, x = '{COL}', stat = 'percent', hue = '{COL}')
ax.set_title('Countplot of {COL}')
ax.set_xlabel('{COL}')
ax.set_ylabel('Count')'''

NUMERICAL_DATA_EDA_CODE_CELL = '''sns.set_style('darkgrid')
plt.figure(figsize = (10, 5))
ax = sns.histplot(data = df, x = '{COL}', kde = True, fill = True)
ax.set_title('Histogram of {COL}')
ax.set_xlabel('{COL}')
ax.set_ylabel('Count')'''

CORRELATION_DATA_EDA_CODE_CELL = '''sns.set_style('darkgrid')
plt.figure(figsize = (10, 5))
ax = sns.heatmap(data = df.corr(), annot = True, cmap = 'coolwarm')
ax.set_title('Correlation Heatmap')'''

