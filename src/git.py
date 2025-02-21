import os
import subprocess

def get_git_status(project_path):
    try:
        # Run the git status command with explicit UTF-8 encoding
        # todo git subprocess git status differ folder
        result = subprocess.run(
            ["git", "status","--",f"{project_path}"],
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding="utf-8"  # Explicitly set the encoding to UTF-8
        )
        print(result)
        # Ensure the result is not None and return the stripped output
        if result and result.stdout:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git status in {project_path}: {e}")
    return ""  # Return an empty string if no changes or error occurs

def commit_changes(project_path, project_name, changes):
    """Commit changes with a message that includes the project name and changes"""
    commit_message = f"Update project ({project_name}) changes: {changes}"
    subprocess.run(["git", "add", "."], cwd=project_path)  # Stage all changes
    subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path)  # Commit the changes
def commit_changes_without(project_path, project_name):
    """Commit changes with a message that includes the project name and changes"""
    commit_message = f"Update project ({project_name})"
    subprocess.run(["git", "add", "."], cwd=project_path)  # Stage all changes
    subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path)  # Commit the changes
def process_projects(base_path):
    """Traverse all projects in /002_Projects and commit changes if any"""
    projects_path = os.path.join(base_path, "002_Projects")  # Path to the projects folder
    if not os.path.exists(projects_path):  # Check if the directory exists
        print(f"Error: The directory {projects_path} does not exist.")
        return

    # Check if /.git/ exists in the base path
    if not os.path.exists(os.path.join(base_path, ".git")):
        print(f"Error: The /.git/ directory not exist in the base path.")
        return

    for project in os.listdir(projects_path):  # Loop through each project folder
        project_path = os.path.join(projects_path, project)
        if os.path.isdir(project_path):  # Only process directories
            commit_changes_without(project_path, project)
            # changes = get_git_status(project_path)  # Get the status of changes
            
            # if changes:  # If there are changes, commit them
            #     print(f"Detected changes in {project}, committing...")
            #     commit_changes(project_path, project, changes)
            #     print(f"Changes in {project} have been committed!")
            # else:
            #     print(f"{project} has no changes, skipping.")
def move_project_to(project_path,des_path):
    pass
if __name__ == "__main__":
    base_directory = r"C:\Users\shade\OneDrive\KG"  # Replace with your base directory path
    process_projects(base_directory)
#C:\\Users\\shade\\OneDrive\\KG\\002_Projects\\testxx