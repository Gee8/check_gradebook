# Import dependencies
import streamlit as st
import pandas as pd

from io import BytesIO

# Import helper function
from utils.clean_data import clean_data

# Create title for page
st.title('Checking Gradebook for Completion')

# Write instructions for the app in the sidebar
st.sidebar.markdown('<br>'.join([
                    '<h1>Instructions:</h1>',
                    '<h2>Download the gradebook</h2>',
                    '- Navigate to the gradebook',
                    '- Click the Actions dropdown',
                    '- Click "Export Current Gradebook View"',
                    '- Upload the exported gradebook by dragging and dropping, or browsing for the file',
                    '- Download the student results']), 
unsafe_allow_html = True)


# Create a box to upload the gradebook export
grades_export = st.file_uploader('Upload Gradebook')

# Wait for the grades export to be uploaded
if grades_export is not None:

    # Create teh student results dataframe
    student_results = clean_data(pd.read_csv(grades_export)) 

    # Return the student results in a download
    data = BytesIO()
    with pd.ExcelWriter(data) as writer:
        student_results.to_excel(writer, 
                                 sheet_name = 'Results', 
                                 index = False)

    # Create a download for the student results data  
    st.download_button(label = 'Download Student Results', 
                       data = data.getvalue(), 
                       file_name = 'Student Results.xlsx')
    