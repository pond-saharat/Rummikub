# Rummikub Coursework
## For team members
### Installation
**Step 1: Make sure you have install Python and PyGame on your local machine. If you have more than one version of Python on your local machine, please make sure you are using Python3.**<br>
Windows<br>
`python -m pip install --upgrade pip`<br>
`py -m pip install -U pygame` or `pip3 install pygame`<br> 
MacOS<br>
`python3 -m pip install -U pygame`<br>
Debain-based OS<br>
`sudo apt-get install python3-pygame`<br><br>

**Step 2: Make sure you have install Git on your local machine.**<br>
-> If not, [download Git](https://git-scm.com/downloads).<br>
Do not forget to set your name and email in Git.<br>
`git config --global user.name "firstname lastname"`
`git config --global user.email "youremail"`
<br><br>


**Step 3: Locate your directory.**<br>
`cd your-directory`<br>
`git clone https://github.com/pondsaharat/rummikub-coursework.git`<br><br>

### Useful commands
1. Retrive updates from the online repository <br>
`git fetch origin main` to your local repository<br>
`git pull origin main` to your workspace<br>

> [!IMPORTANT]
> Make sure you have fetched or pulled from the online repository every time you are working. Otherwise, you will be working on the outdated repo.<br>

2. Add or remove the files to be tracked by Git<br>
`git add yourfile` or `git add -A` to add all files<br>
`git rm yourfile`<br>
3. Commit changes to your local repository<br>
`git commit`<br>
### Naming conventions<br>
1. snake_case for naming functions, variables and filenames<br>
2. PascalCase for naming classes<br>
Read [PEP8 Python naming conventions](https://peps.python.org/pep-0008/#prescriptive-naming-conventions)<br>
### Guidelines<br>
You may need to create a branch to work on then create a pull request.<br>
`git branch` -> show how many branches are there right now.<br>
`git checkout -b yourbranch` -> create a new branch<br>
`git fetch origin main` -> fetch changes from a main branch to a local repository and `git merge` to merge<br>
`git pull origin main` -> fetch changes from a main branch to a workspace<br>
`git add -A` -> add all files you have<br>
`git push origin yourbranch` -> update your branch<br>
`git push origin main` -> create a pull request<br>

> [!WARNING]
> Make sure your code can run perfectly before creating a pull request<br>
