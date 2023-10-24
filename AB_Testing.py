### AB Testing ###

# What is AB Testing?
# Fundamentally, an A/B test is the comparison of means and it compares two different groups. In concept,
# it is a user experience research methodology. "A" represents a group and "B" represents another group that includes
# same variable for comparison.

### AB Testing Process ###

# 1. Construct Hypotheses
# 2. Assumption Checking
#   - Normality Assumption (Shapiro-Wilk)
#   - Homogeneity of Variance (Levene)
# 3. Hypothesis Testing
# 4. Interpret Results Based on the p-value.

########################
### Business Problem ###
########################

# Facebook offers various bidding strategies, and X company is interested in comparing two different bidding methods.
# The company has two datasets that include variables such as "impression" "click" "purchase" and "earning".
# Target variable is "purchase" and it is company's success criterion.

### Variables ###
# Impression: The number of ad views.
# Click: The number of clicks on the displayed ad.
# Purchase: The number of products purchased after clicking on the ads.
# Earning: The revenue generated after the purchase of products.

# Packages-Libraries-Settings #


import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#################################################
### Task 1:  Data Understanding and Preparing ###
#################################################

### Step 1: Load Data ###

# We have two datesets in the xlsx file, which are "Control Group" and "Test Group"

dfc = pd.read_excel("AB_Testing/ab_testing.xlsx", sheet_name="Control Group")
dft = pd.read_excel("AB_Testing/ab_testing.xlsx", sheet_name="Test Group")
dfc.head()
dft.head()

### Step 2: Check Data ###

def check_df(dataframe, head=5):
    print(" SHAPE ".center(70, '-'))
    print('Rows: {}'.format(dataframe.shape[0]))
    print('Columns: {}'.format(dataframe.shape[1]))
    print(" TYPES ".center(70, '-'))
    print(dataframe.dtypes)
    print(" HEAD ".center(70, '-'))
    print(dataframe.head(head))
    print(" TAIL ".center(70, '-'))
    print(dataframe.tail(head))
    print(" MISSING VALUES ".center(70, '-'))
    print(dataframe.isnull().sum())
    print(" DESCRIBE ".center(70, '-'))
    print(dataframe.describe([0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]).T)

check_df(dfc)
check_df(dft)

### Step 3: Checking and Suppressing Outliers ###

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

dfc.describe().T
dft.describe().T
replace_with_thresholds(dfc, "Purchase")
replace_with_thresholds(dft, "Purchase")
dfc.describe().T
dft.describe().T

### Step 4: Concatenate Data ###

# Since we have two datasets, we will add another column called "Group",
# this way we will be able to separate the control and test groups each other.

dfc["Group"] = "C"
dft["Group"] = "T"

df = pd.concat([dfc, dft], axis=0, ignore_index=True)

########################
### Task 2: A/B Test ###
########################

### Step 1: Construct A/B Test Hypotheses ###

# H0 = df[df["Group"] == "C"] = df[df["Group"] == "T"] # Null hypothesis, which states that there is no difference between groups.
# H1 = df[df["Group"] == "C"] != df[df["Group"] == "T"] # Alternative hypothesis, which states that there is a difference between groups.

### Step 2: Assumption Checking ###

# We will check for two crucial assumptions out of four, to clarify, they are normality and homogeneity.
# For normality check we will perform Shapiro-Wilk Test.
# For homogeneity test we will perform Levene Test.

# Normality

statistic, p_value = shapiro(df.loc[df["Group"] == "C", "Purchase"])
alpha = 0.05
if p_value > alpha:
    print("Sample looks normal!")
else:
    print("Sample does not look normal!")

statistic, p_value = shapiro(df.loc[df["Group"] == "T", "Purchase"])
alpha = 0.05
if p_value > alpha:
    print("Sample looks normal!")
else:
    print("Sample does not look normal!")

# Both of our p values are greater than 0.05, in other words, both purchase values of the groups
# are normally distributed. Since our data normally distributed and we have two groups,
# we are able to perform one of the parametric tests, Independent Samples T-test.

# Homogeneity

statistic, p_value = levene(df.loc[df["Group"] == "C", "Purchase"], df.loc[df["Group"] == "T", "Purchase"])
alpha = 0.05
if p_value > alpha:
    print("Variances are homogene!")
else:
    print("Variances are not homogene!")

# P value for Levene Test is greater than 0.05 and according to this result we can conclude that variances are homogene,
# and homogeneity of variances assumption is met. If the homogeneity of variances assumption were not met,
# we would stated it in T-test.

### Step 3: Hypothesis Testing ###

test_stat, p_value = ttest_ind(df.loc[df["Group"] == "C", "Purchase"],
                              df.loc[df["Group"] == "T", "Purchase"],
                              equal_var=True)
if p_value > alpha:
    print("H0 can not be denied!")
    print(f"t statistic = {test_stat}")
    print(f"p value = {p_value}")
else:
    print("H0 can denied!")
    print(f"t statistic = {test_stat}")
    print(f"p value = {p_value}")

# Due to p value (0.349) is greater than 0.05 H0 hypothesis can not be denied, in simple terms, difference between
# means of the two groups occured due to chance, there is no statistically significant difference.

### Step 4: Summary of A/B Testing and Interpretation of Results ###

# The Shapiro-Wilk test was applied to check if the observations followed a normal distribution.
# Since the variables exhibited a normal distribution, it was decided to apply a parametric test,
# which is the T-test. The homogeneity of variances assumption was tested using the Levene test,
# and it was found that the variances were homogeneous, as stated within the relevant T-test.

# When the means of the control and test applications were compared,
# it was determined that the difference in means was due to chance, and therefore,
# there was no need for the new test application. #



