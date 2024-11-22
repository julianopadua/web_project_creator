# Project Initialization App

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [Inserting `web_projector.py`](#inserting-web_projectorpy)
- [Running the Application](#running-the-application)
- [How the Code Works](#how-the-code-works)
  - [Project Structure Creation](#project-structure-creation)
  - [Directory Management](#directory-management)
  - [File Content Customization](#file-content-customization)
  - [Adding Additional Files](#adding-additional-files)
  - [Project Generation and Download](#project-generation-and-download)
- [Conclusion](#conclusion)
- [References](#references)

---

## Introduction

The **Project Initialization App** is a Streamlit-based application designed to help users quickly generate custom project structures. It allows users to:

- Define custom directories and manage them dynamically.
- Customize the contents of essential files like `README.md`, `config.yaml`, and the main script file.
- Add additional files to specific directories with custom content.
- Generate a ZIP archive of the project structure for download.

This tool streamlines the initial setup process for new projects, saving time and ensuring consistency across different projects.

---

## Prerequisites

Before running the application, ensure you have the following installed on your system:

- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Virtualenv** (optional but recommended)
- **Git** (optional, if cloning the repository)

---

## Setup and Installation

### Setting Up a Virtual Environment

It's recommended to use a virtual environment to manage your project's dependencies without affecting the global Python installation.

1. **Install Virtualenv (if not already installed):**

   ```bash
   pip install virtualenv
   ```

2. **Create a Virtual Environment:**

   Navigate to your project directory and create a virtual environment named `venv`:

   ```bash
   virtualenv venv
   ```

3. **Activate the Virtual Environment:**

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

### Installing Dependencies

Install the required Python packages using `pip`:

```bash
pip install streamlit pandas matplotlib pyyaml
```

### Inserting `web_projector.py`

Assuming you have the `web_projector.py` script (which contains the code for the Project Initialization App), place it in your project directory—the same directory where your virtual environment resides.

---

## Running the Application

To run the Streamlit application, execute the following command in your terminal:

```bash
streamlit run web_projector.py
```

This command will start the application and open it in your default web browser. If it doesn't open automatically, you can access it by navigating to `http://localhost:8501` in your browser.

---

## How the Code Works

### Project Structure Creation

The core functionality of the application is handled by the `create_project_structure` function. This function is responsible for generating the project directories, files, and assembling them into a ZIP archive for download.

```python
def create_project_structure(project_name, directories, readme_content, config_content, script_content, author_name, additional_files):
    # Function implementation...
```

**Note:** This function is more thoroughly explained in the [Project Creator](https://github.com/julianopadua/project_creator) repository. However, in brief, it performs the following steps:

1. **Creates a Temporary Directory:** Uses `tempfile.TemporaryDirectory` to create a temporary workspace.
2. **Generates Project Directories:** Creates the specified directories within the project structure.
3. **Creates Essential Files:** Writes the customized contents to `README.md`, `config.yaml`, and the main script file.
4. **Adds Additional Files:** Incorporates any user-defined additional files into the appropriate directories.
5. **Assembles the ZIP Archive:** Uses `zipfile.ZipFile` to create an in-memory ZIP file containing the entire project structure.

### Directory Management

The application allows users to dynamically add or remove directories. This is achieved using Streamlit's session state to maintain the list of directories across user interactions.

**Adding a New Directory:**

```python
# Button to add a new directory
if st.button('Add Directory'):
    st.session_state.directories.append({'key': '', 'path': ''})
```

When the "Add Directory" button is clicked, a new dictionary with empty 'key' and 'path' is appended to `st.session_state.directories`.

**Displaying Directory Inputs:**

```python
# Display directory inputs
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
```

- **Columns Layout:** Uses `st.columns` to arrange inputs horizontally.
- **Directory Key and Path Inputs:** `st.text_input` widgets capture the directory key and path.
- **Remove Option:** A checkbox allows the user to mark a directory for removal.
- **Session State Update:** The directory information is updated in `st.session_state`.
- **Removal Handling:** Indices of directories marked for removal are collected.

**Removing Directories:**

```python
# Remove directories that have been marked for removal
for idx in sorted(remove_indices, reverse=True):
    st.session_state.directories.pop(idx)
```

Directories marked for removal are deleted from the session state, ensuring they are no longer displayed or included in the project structure.

**Building the Directories Dictionary:**

```python
# Build the directories dictionary
directories = {entry['key']: entry['path'] for entry in st.session_state.directories if entry['key'] and entry['path']}
```

This dictionary maps directory keys to their paths and is used by the `create_project_structure` function to create the actual directories.

### File Content Customization

Users can customize the contents of essential files like `README.md`, `config.yaml`, and the main script file through text areas.

```python
# File content customization
st.header("Customize File Contents")

readme_content = st.text_area('README.md Content:', '''# {project_name}

## Introduction

*Provide an overview of the project here. Describe the purpose and scope of the project.*

## How to Use

*Explain how to set up and run the project. Include instructions on installation, configuration, and execution.*

## Conclusion

*Summarize the project and discuss any future developments or considerations.*
''')

# Similar customization for config_content and script_content...
```

- **Placeholders and Formatting:** The placeholders like `{project_name}` and `{author_name}` are replaced with actual values during project creation.
- **User Input:** The text areas allow users to modify the default content or input entirely new content.

### Adding Additional Files

The application provides functionality for users to add custom files to their project, specifying the directory, file name, and content.

**Adding a New File:**

```python
# Button to add a new file
if st.button('Add File'):
    st.session_state.additional_files.append({'directory': '', 'file_name': '', 'content': ''})
```

Clicking "Add File" appends a new file entry to `st.session_state.additional_files`.

**Displaying Additional File Inputs:**

```python
# Display additional file inputs
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

    # Update session state
    st.session_state.additional_files[i]['directory'] = directory
    st.session_state.additional_files[i]['file_name'] = file_name
    st.session_state.additional_files[i]['content'] = content
    if remove:
        remove_file_indices.append(i)
```

- **Directory Selection:** Uses `st.selectbox` to allow users to choose the target directory from existing directory keys.
- **File Name Input:** A text input where users specify the file name and extension (e.g., "example.py").
- **Content Input:** A text area for the file's content.
- **Removal Option:** Users can mark files for removal.
- **Session State Update:** The additional file information is stored in `st.session_state.additional_files`.

**Updating with New Directories:**

When users add new directories, the directory selection drop-down for files is automatically updated because it references the current `directories.keys()`.

**Removing Files:**

```python
# Remove files that have been marked for removal
for idx in sorted(remove_file_indices, reverse=True):
    st.session_state.additional_files.pop(idx)
```

Files marked for removal are deleted from the session state, ensuring they are not included in the project.

### Project Generation and Download

Once all customizations are made, users can generate the project and download it as a ZIP file.

```python
# Button to generate the project
if st.button('Create Project'):
    if not project_name:
        st.error('Please enter a project name.')
    else:
        try:
            additional_files = st.session_state.additional_files
            zip_data = create_project_structure(project_name, directories, readme_content, config_content, script_content, author_name, additional_files)
            st.success(f'Project "{project_name}" has been created and is ready for download.')

            # Provide download button
            st.download_button(
                label="Download Project ZIP",
                data=zip_data,
                file_name=f"{project_name}.zip",
                mime="application/zip"
            )
        except Exception as e:
            st.error(f'An error occurred: {e}')
```

- **Project Creation:** When "Create Project" is clicked, the application calls `create_project_structure` with all the user-defined parameters.
- **Success Message:** Upon successful creation, a success message is displayed.
- **Download Button:** A `st.download_button` is provided for the user to download the ZIP file.
- **Error Handling:** Any exceptions are caught and displayed as error messages.

---

## Conclusion

The **Project Initialization App** is a versatile tool that simplifies the creation of customized project structures. By leveraging Streamlit's interactive features and Python's file handling capabilities, the app provides an intuitive interface for defining directories, customizing file contents, and adding additional files. The end result is a downloadable ZIP archive that reflects the user's specifications, ready to be extracted and used as the foundation for new projects.

---

## References

- **Project Creator Repository:** For a more in-depth explanation of the `create_project_structure` function and project initialization logic, refer to the [Project Creator](https://github.com/julianopadua/project_creator) repository.
- **Streamlit Documentation:** [https://docs.streamlit.io/](https://docs.streamlit.io/)
- **Python Official Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)
