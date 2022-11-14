import numpy as np
import matplotlib as plt
import pandas as pd

# dataset  of Faridabad CRS

# dataset = pd.read_csv("C:/Users/Dell/Downloads/FARIDABAD_NPR/FARIDABAD_NPR.csv",lineterminator='\n',error_bad_lines=False)
# dataset local copy
dataset = pd.read_csv("C:/Users/Dell/Downloads/FARIDABAD_NPR/FARIDABAD_NPR.csv", sep='|', on_bad_lines='skip')
Test = dataset.copy()

# Pandas options to display max columns and rows in console

pd.options.display.max_columns = None
pd.options.display.max_rows = None

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# using fuzzywuzzy, find bext match for each substring of given string, from the list of matching strings match_list(already given)

# separate list of target column 'relname'
list2 = dataset['relname']

# Below is the list of actual relations name that are set of valid relation names
# First ,I had created a list match_list manually with individual words from below list.This will help me first to correct the spellings of raw data
rel_df = pd.read_excel("C:/Users/Dell/Downloads/Relationship.xlsx", names=['first', 'second'])
rels1 = list(rel_df['first'])
rels2 = list(rel_df['second'])
rels = rels1 + rels2
rels_new = []
for i in rels:
    string = i.replace('  ', ' ')
    rels_new.append(string)

rels_new[0] = 'Husband'  # these 2 had some issue with extra padded spaces so just fixed manually
rels_new[1] = 'Head'

rels_new = ['Husband', 'Head', 'Father', 'Son', 'Daughter', 'Brother', "Father's father", "Husband's Father", 'Sister',
            "son's son", "son's daughter", "Daughter's son",
            "Daughter's daughter", "Mother's Father", "Wife's Mother", "Father's Brother", "Father's sister",
            "Mother's Brother", "Mother's sister", "Husband's Brother",
            "Husband's Sister", "Wife's Brother ", "Wife's Sister", "Brother's son", "Brother's daughter",
            "Sister's son", "Sister's daughter", 'Wife', 'Spouse', 'Mother',
            "Sons's Wife ", "Daughter's Husband", "Brother's Wife", "Father's Mother", "Husband's Mother",
            "Sister's Husband", "Son's Son's Wife", "Son's Daughter's Husband",
            "Daughter's Son's Wife", "Daughter's Daughter's Husband", "Mother's Mother", "Wife's Father ",
            "Father's Brother's Wife", "Father's Sister's Husband", "Mother's Brother's Wife",
            "Mother's Sister's Husband ", "Husband's Brother's wife", "Husband's Sister's Husband",
            "Wife's Brother's Wife", "Wife's Sister's Husband", "Brother's son's wife",
            "Brother's daughter's Husband", "Sister's son's wife", "Sister's daughter's Husband"]

match_list = ['Son', 'Daughter', 'Father', 'Mother', 'Grand', 'Head', 'Self', 'Wife', 'Husband',
              'Sister', 'Brother', 'in', 'law', 'Niece', 'Nephew', 'Relation', 'Relative', 'Partner', 'Neighbour',
              'of', "Daughter's", "Brother's", "Father's", "Husband's", "Sister's", "Son's", "Mother's", "Wife's"]

num1 = 0  # just to track the number of lines processed and will display for every 1 lakh rows processed
mat4 = []  # list of list mat2 where we have given scoring for matching word of each substring in original string
mat5 = []  # list of refined relation name column
for i in range(len(list2)):
    # if null value in column then set'nan'
    if pd.isnull(list2[i]) or list2[i] == '':
        mat4.append('nan')
        mat5.append('nan')

    num1 = num1 + 1
    if num1 % 100000 == 0:
        print(num1)
    try:
        # divide relation string  in column to substring then match each against match_list
        ls = list2[i].split()
        mat1 = ''
        mat3 = []
        for j in ls:
            mat2 = []
            # process.extract method returns the the one match(limit=1 highest percentage) for string in 'j' from the list match_list
            # it returns a list (in list variable mat2)with first value is the mathcing string from match_list and second value is percentage of match

            mat2.append(process.extract(j, match_list, limit=1))
            # mat1 is joint strings of all strings returned from process.extract and reconstruct the original string.It
            #may correct the spellings too
            mat1 = mat1 + '  ' + (mat2[0][0][0])
            mat3.append(mat2)
        mat4.append(mat3)
        mat5.append(mat1.lstrip())
    except:
         continue

# new column for new refined relation name
Test['relname_new'] = mat5

# Now we will get list of individual relations matching percentage for each substring of original string , to separate column for easy readability

length = len(Test['relname'])
mat6 = []  # list of first match relation name.It will give 'n' for already nan values.need to make 'n' to nan
for i in range(length):
    mat6.append(mat4[i][0][0][0][0].strip())

mat7 = []  # list of first match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat7.append(int(mat4[i][0][0][0][1]))
    except IndexError as I:
        mat7.append(int(0))

mat8 = []  # list of second match relation name.It will give 'a' for already nan values.need to make 'a to 'nan'
for i in range(length):
    try:
        mat8.append(mat4[i][1][0][0][0].strip())
    except IndexError as I:
        mat8.append('nan')

mat9 = []  # list of second match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat9.append(int(mat4[i][1][0][0][1]))
    except IndexError as I:
        mat9.append(int(0))

mat10 = []  # list of third match relation name.It will give 'n' for already nan values.need to make 'n' to 'nan'
for i in range(length):
    try:
        mat10.append(mat4[i][2][0][0][0].strip())
    except IndexError as I:
        mat10.append('nan')

mat11 = []  # list of third match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat11.append(int(mat4[i][2][0][0][1]))
    except IndexError as I:
        mat11.append(int(0))

mat12 = []  # list of fourth match relation name.It will give 'nan' for already nan values.
for i in range(length):
    try:
        mat12.append(mat4[i][3][0][0][0].strip())
    except IndexError as I:
        mat12.append('nan')

mat13 = []  # list of fourth match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat13.append(int(mat4[i][3][0][0][1]))
    except IndexError as I:
        mat13.append(int(0))

mat14 = []  # list of fifth match relation name.It will give 'nan' for already nan values.
for i in range(length):
    try:
        mat14.append(mat4[i][4][0][0][0].strip())
    except IndexError as I:
        mat14.append('nan')

mat15 = []  # list of fifth match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat15.append(int(mat4[i][4][0][0][1]))
    except IndexError as I:
        mat15.append(int(0))

mat16 = []  # list of sixth match relation name.It will give 'nan' for already nan values.
for i in range(length):
    try:
        mat16.append(mat4[i][5][0][0][0].strip())
    except IndexError as I:
        mat16.append('nan')

mat17 = []  # list of sixth match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat17.append(int(mat4[i][5][0][0][1]))
    except IndexError as I:
        mat17.append(int(0))

mat18 = []  # list of seventh match relation name.It will give 'nan' for already nan values.
for i in range(length):
    try:
        mat18.append(mat4[i][6][0][0][0].strip())
    except IndexError as I:
        mat18.append('nan')

mat19 = []  # list of seventh match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat19.append(int(mat4[i][6][0][0][1]))
    except IndexError as I:
        mat19.append(int(0))

mat20 = []  # list of eigth match relation name.It will give 'nan' for already nan values.
for i in range(length):
    try:
        mat20.append(mat4[i][7][0][0][0].strip())
    except IndexError as I:
        mat20.append('nan')

mat21 = []  # list of eigth match relation percentage.It will give '0' for already nan values
for i in range(length):
    try:
        mat21.append(int(mat4[i][7][0][0][1]))
    except IndexError as I:
        mat21.append(int(0))

# Now assign these lists to new column wise  'matchreln' is column name for relation names in orders those are matched to each string
# 'matchreln_prcntg' are columns for matching percentages for those relations

Test['matchrel1'] = mat6
Test['matchrel1_prcntg'] = mat7
Test['matchrel2'] = mat8
Test['matchrel2_prcntg'] = mat9
Test['matchrel3'] = mat10
Test['matchrel3_prcntg'] = mat11
Test['matchrel4'] = mat12
Test['matchrel4_prcntg'] = mat13
Test['matchrel5'] = mat14
Test['matchrel5_prcntg'] = mat15
Test['matchrel6'] = mat16
Test['matchrel6_prcntg'] = mat17
Test['matchrel7'] = mat18
Test['matchrel7_prcntg'] = mat19
Test['matchrel8'] = mat20
Test['matchrel8_prcntg'] = mat21

# reformat some values in these columns for singularity of values

Test.loc[(Test['matchrel1'] == 'n'), 'matchrel1'] = 'nan'
Test.loc[(Test['matchrel2'] == 'a'), 'matchrel2'] = 'nan'
Test.loc[(Test['matchrel3'] == 'n'), 'matchrel3'] = 'nan'

# again reformat some values in these columns for making'nan' to pandas 'None'

Test.loc[(Test['matchrel1'] == 'nan'), 'matchrel1'] = None
Test.loc[(Test['matchrel2'] == 'nan'), 'matchrel2'] = None
Test.loc[(Test['matchrel3'] == 'nan'), 'matchrel3'] = None
Test.loc[(Test['matchrel4'] == 'nan'), 'matchrel4'] = None
Test.loc[(Test['matchrel5'] == 'nan'), 'matchrel5'] = None
Test.loc[(Test['matchrel6'] == 'nan'), 'matchrel6'] = None
Test.loc[(Test['matchrel7'] == 'nan'), 'matchrel7'] = None
Test.loc[(Test['matchrel8'] == 'nan'), 'matchrel8'] = None

# now create a new column 'relname_new_given' and a percentage matching column to find put the matching percentage
# of new relname column with actual vlaid list of relatiosn given
# Phewwwww .... lots of data to handle
length = len(Test['relname_new'])
ls = Test['relname_new']
ls1 = []
ls2 = []
for i in range(length):
    try:
        l = str(ls[i].strip())
        mat1 = []
        mat1.append(process.extract(l, rels_new, limit=1))
        ls1.append(mat1[0][0][0])
        ls2.append(mat1[0][0][1])
    except:
        ls1.append(None)
        ls2.append(int(0))

Test['relname_new_given'] = ls1
Test['relname_new_given_prcntg'] = ls2

# write dataset to csv
# final set of data.Hope this will be of some use

Test.to_csv('Faridabad_newrels_given.csv')
