import os
import subprocess

def get_git_status(project_path):
    """获取 git status --short 的输出"""
    result = subprocess.run(["git", "status", "--short"], cwd=project_path, capture_output=True, text=True)
    return result.stdout.strip()

def commit_changes(project_path, project_name, changes):
    """提交 git 变更"""
    commit_message = f"更新 project ({project_name}) 改动文件为: {changes}"
    subprocess.run(["git", "add", "--all"], cwd=project_path)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path)

def process_projects(base_path):
    """遍历 /002_Projects 下的所有项目并提交变更"""
    projects_path = os.path.join(base_path, "002_Projects")
    if not os.path.exists(projects_path):
        print(f"错误: 目录 {projects_path} 不存在")
        return
    if os.path.exists(os.path.join(base_path, "/.git/")):
        print(f"错误: 目录 .git 不存在")
        return
    for project in os.listdir(projects_path):
        project_path = os.path.join(projects_path, project)
        if os.path.isdir(project_path) :
            changes = get_git_status(project_path)
            if changes:
                print(f"检测到 {project} 有变更，提交中...")
                commit_changes(project_path, project, changes)
                print(f"{project} 提交完成！")
            else:
                print(f"{project} 没有变更，跳过。")

if __name__ == "__main__":
    base_directory = r"C:\Users\shade\OneDrive\KG"
    process_projects(base_directory)