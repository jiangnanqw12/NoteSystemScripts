

### 🛠️ 个人自动化处理脚本（按操作对象模块化）

---

#### 1. 操作对象：Git

##### 1.1 Git 代码仓

- `git clone`
- `git pull`

##### 1.2 PARA 笔记仓

- 更新项目（update project）
- 移动文件夹（mv folder）

---

#### 2. 操作对象：Code（如 C / C++ / Python 等代码文本）

---

#### 3. 操作对象：Config（如 JSON / INI / XML 等配置文件）

---

#### 4. 操作对象：Markdown



### 📁 自动化脚本项目结构（模块化划分）

```
auto_scripts/
├── src/
│   ├── git_ops/
│   │   ├── code_repos/
│   │   └── para_notes/
│   ├── code_processing/
│   ├── config_handling/
│   ├── markdown_tools/
│   └── common/
├── config/
│   ├── git_ops/
│   │   ├── code_repos.yaml
│   │   └── para_notes.yaml
│   ├── code_processing.yaml
│   ├── config_handling.yaml
│   ├── markdown_tools.yaml
│   └── global.yaml                # 全局设置（如路径、日志等级）
├── logs/
│   ├── git_ops/
│   │   ├── code_repos.log
│   │   └── para_notes.log
│   ├── code_processing.log
│   ├── config_handling.log
│   ├── markdown_tools.log
│   └── main.log
├── data/
│   ├── git_ops/
│   │   ├── repo_list.json
│   │   └── para_index.csv
│   ├── code_processing/
│   ├── config_handling/
│   └── markdown_tools/
├── output/
│   ├── git_ops/
│   │   └── repo_status.md
│   ├── code_processing/
│   │   └── stats_summary.txt
│   ├── config_handling/
│   └── markdown_tools/
│       └── updated_docs/
└── main.py
```

---

### ✅ 优势

- 各模块拥有**独立配置、日志、数据与输出**，方便调试和复用。
- 保持 `src/` 与其他目录结构一一对应，便于导航与管理。
- 支持模块独立运行或集中调度。

### 自动脚本
以下是一个 Python 脚本，用于**自动创建上述模块化目录结构**：

```python
import os
import subprocess

def get_git_status(project_path):
    try:
        # Run the git status command with explicit UTF-8 encoding
        result = subprocess.run(
            ["git", "status", ".","--porcelain"],  # Use --porcelain for machine-readable output
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if result and result.stdout:
            status_lines = result.stdout.strip().split('\n')
            for line in status_lines:
                # Determine the state based on the git status output
                if line.startswith("??"):  # Untracked
                    print(f"Untracked: {line[3:]}")
                elif line.startswith(" M"):  # Modified
                    print(f"Modified: {line[3:]}")
                elif line.startswith("A "):  # Staged (Added)
                    print(f"Staged: {line[3:]}")
                elif line.startswith("D "):  # Deleted
                    print(f"Deleted: {line[3:]}")
                elif line.startswith("R "):  # Renamed
                    print(f"Renamed: {line[3:]}")
                elif line.startswith("C "):  # Conflicted
                    print(f"Conflicted: {line[3:]}")
                else:  # Committed (Nothing to show, as it's clean)
                    print(f"Committed: {line[3:]}")
            
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
            # get_git_status(project_path)
            changes = get_git_status(project_path)  # Get the status of changes
            
            if changes:  # If there are changes, commit them
                print(f"Detected changes in {project}, committing...")
                commit_changes(project_path, project, changes)
                print(f"Changes in {project} have been committed!")
            else:
                print(f"{project} has no changes, skipping.")
def move_project_to(project_path,des_path):
    pass
if __name__ == "__main__":
    base_directory = r"C:\Users\shade\OneDrive\KG"  # Replace with your base directory path
    process_projects(base_directory)
#C:\\Users\\shade\\OneDrive\\KG\\002_Projects\\testxx
```

---

### 📌 使用方式

1. 将以上脚本保存为 `init_structure.py`
2. 在终端运行：

```bash
python init_structure.py
```

这会在当前目录下创建完整的 `auto_scripts/` 结构。

需要我也提供一个 `.gitignore` 或 `Makefile` 示例配套使用吗？