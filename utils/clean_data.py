# Import dependencies
import pandas as pd

# Define function to clean the gradebook upload
def clean_data(gradebook):

    # Drop the top row containing total points possible
    gradebook.drop(index = 0, inplace = True)

    # Create lists to hold the homework assignment and assessment columns
    homework_cols = [col for col in gradebook.columns if 'Challenge' in col and 'Module' in col]
    assessment_cols = [col for col in gradebook.columns if 'Unit Assessment:' in col]

    # Loop through the dataframe to gather the info for each students' grades
    data = []
    for index, row in gradebook.iterrows():
        student_data = {}
        student_data['Student'] = row['Student']
        student_data['Student ID'] = row['ID']
        student_data['Number of Homeworks Completed'] = (gradebook.loc[index, homework_cols] > 0).sum()
        student_data['Missing Assignments'] = (gradebook.loc[index, homework_cols] == 0).sum()
        student_data['Completed Assessments'] = (gradebook.loc[index, assessment_cols] >= 0).sum()
        student_data['Missing Assessments'] = gradebook.loc[index, assessment_cols].isna().sum()
        student_data['Final Score'] = row['Final Score']
        if (student_data['Missing Assignments'] <= 2) and (student_data['Missing Assessments'] == 0):
            student_data['Pass/Fail'] = 'Pass'
        else:
            student_data['Pass/Fail'] = 'Fail'
        
        # Append the students data to the data list
        data.append(student_data)

    # Return the dataframe of the students' coursework results
    return pd.DataFrame(data)