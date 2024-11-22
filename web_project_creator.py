import os
import datetime
import streamlit as st
import tempfile
import zipfile
import io

def sanitize_path(path):
    return path.strip('\'"')

def create_project_structure(project_name, directories, readme_content, config_content, script_content, author_name, additional_files):
    current_datetime = datetime.datetime.now()

    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        # update directories with full paths
        directories_full = {key: os.path.join(project_path, path) for key, path in directories.items()}

        # create subdirectories
        for dir_path in directories_full.values():
            os.makedirs(dir_path, exist_ok=True)

        # create requirements.txt
        requirements = '''pandas
matplotlib
datetime
os
pyyaml
'''
        with open(os.path.join(project_path, 'requirements.txt'), 'w') as file:
            file.write(requirements)

        # initialize config.yaml with content from user
        config_content_formatted = config_content.format(project_name=project_name)
        with open(os.path.join(directories_full.get('src', project_path), 'config.yaml'), 'w') as file:
            file.write(config_content_formatted)

        # create the main Python script
        script_content_formatted = script_content.format(project_name=project_name, author_name=author_name)
        script_path = os.path.join(directories_full.get('src', project_path), f'{project_name}.py')
        with open(script_path, 'w') as file:
            file.write(script_content_formatted)

        # create README.md with content from user
        readme_content_formatted = readme_content.format(project_name=project_name)
        with open(os.path.join(project_path, 'README.md'), 'w') as file:
            file.write(readme_content_formatted)

        # create additional files
        for file_info in additional_files:
            dir_key = file_info['directory']
            file_name = file_info['file_name']
            content = file_info['content']
            dir_path = directories_full.get(dir_key, project_path)
            file_path = os.path.join(dir_path, file_name)
            # ensure the directory exists
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(content)

        # create ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(project_path):
                # include the directory in the zip file
                arc_dir = os.path.relpath(root, start=project_path) + '/'
                zip_info = zipfile.ZipInfo(arc_dir)
                zip_file.writestr(zip_info, '')

                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=project_path)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

# Streamlit App

st.title("Project Initialization App")

# input fields
project_name = st.text_input('Enter the project name:', value='MyProject')

# initialize session state for directories
if 'directories' not in st.session_state:
    st.session_state.directories = [{'key': 'src', 'path': 'src'}]

st.header("Customize Directory Structure")

# button to add a new directory
if st.button('Add Directory'):
    st.session_state.directories.append({'key': '', 'path': ''})

# display directory inputs
remove_indices = []
for i, dir_entry in enumerate(st.session_state.directories):
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        dir_key = st.text_input(f'Directory Key {i+1}', value=dir_entry['key'], key=f'dir_key_{i}')
    with col2:
        dir_path = st.text_input(f'Directory Path {i+1}', value=dir_entry['path'], key=f'dir_path_{i}')
    with col3:
        remove = st.checkbox('Remove', key=f'remove_dir_{i}')
    st.session_state.directories[i]['key'] = dir_key
    st.session_state.directories[i]['path'] = dir_path
    if remove:
        remove_indices.append(i)

# remove directories that have been marked for removal
for idx in sorted(remove_indices, reverse=True):
    st.session_state.directories.pop(idx)

# build the directories dictionary
directories = {entry['key']: entry['path'] for entry in st.session_state.directories if entry['key'] and entry['path']}

# file content customization
st.header("Customize File Contents")

readme_content = st.text_area('README.md Content:', '''# {project_name}

## Introduction

*Provide an overview of the project here. Describe the purpose and scope of the project.*

## How to Use

*Explain how to set up and run the project. Include instructions on installation, configuration, and execution.*

## Conclusion

*Summarize the project and discuss any future developments or considerations.*
''')

config_content = st.text_area('config.yaml Content:', '''# configuration parameters
paths:
  data_raw: ../data/raw
  data_processed: ../data/processed
  images: ../images
  report: ../report
  addons: ../addons
''')

script_content = st.text_area('Main Script Content:', '''# made by {author_name}
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(script_dir, "config.yaml")

# load configuration
with open(config_dir, 'r') as config_file:
    config = yaml.safe_load(config_file)

# initialize paths from config
data_raw_path = os.path.join(script_dir, config['paths']['data_raw'])
data_processed_path = os.path.join(script_dir, config['paths']['data_processed'])
images_path = os.path.join(script_dir, config['paths']['images'])
report_path = os.path.join(script_dir, config['paths']['report'])
addons_path = os.path.join(script_dir, config['paths']['addons'])

# your code starts here

''')

author_name = st.text_input('Author Name:', 'Your Name')

# initialize session state for additional files
if 'additional_files' not in st.session_state:
    st.session_state.additional_files = []

st.header("Add Additional Files")

# button to add a new file
if st.button('Add File'):
    st.session_state.additional_files.append({'directory': '', 'file_name': '', 'content': ''})

# display additional file inputs
remove_file_indices = []
for i, file_entry in enumerate(st.session_state.additional_files):
    st.subheader(f"File {i+1}")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        directory = st.selectbox(f"Select Directory for File {i+1}", options=directories.keys(), key=f'file_dir_{i}')
    with col2:
        file_name = st.text_input(f"File Name {i+1} (e.g., script.py)", value=file_entry['file_name'], key=f'file_name_{i}')
    with col3:
        remove = st.checkbox('Remove', key=f'remove_file_{i}')
    content = st.text_area(f"Content for {file_name or 'File ' + str(i+1)}", value=file_entry.get('content', ''), key=f'file_content_{i}')

    # update session state
    st.session_state.additional_files[i]['directory'] = directory
    st.session_state.additional_files[i]['file_name'] = file_name
    st.session_state.additional_files[i]['content'] = content
    if remove:
        remove_file_indices.append(i)

# remove files that have been marked for removal
for idx in sorted(remove_file_indices, reverse=True):
    st.session_state.additional_files.pop(idx)

# button to generate the project
if st.button('Create Project'):
    if not project_name:
        st.error('Please enter a project name.')
    else:
        try:
            additional_files = st.session_state.additional_files
            zip_data = create_project_structure(project_name, directories, readme_content, config_content, script_content, author_name, additional_files)
            st.success(f'Project {project_name} has been created and is ready for download.')

            # provide download button
            st.download_button(
                label="Download Project ZIP",
                data=zip_data,
                file_name=f"{project_name}.zip",
                mime="application/zip"
            )
        except Exception as e:
            st.error(f'An error occurred: {e}')
