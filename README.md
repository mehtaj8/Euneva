# Euneva

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

1. Install Node v15.5.1
   - `node -v`
2. Install NPM 7.3.0
   - `npm -v`
3. Clone the repo

```sh
git clone https://gitlab.cas.mcmaster.ca/renx11/3xa3-project-l02-group9.git
```

4. Set-up Commitzen - OPTIONAL

```sh
cd 3xa3-project-l02-group9
npm i
cd .git/hooks
chmod +x prepare-commit-msg.sample
cd ../..
```

- This should allow you to commit nicely via `git commit`. You will be able to edit the commits one last time. Once you are satisfied with the commit execute `:wq` and then you are ready to push `git push`.
- You can still commit regularily via `git commit -m ` if you don't want to use commitzen
- Then just use `cntrl+c` to exit the commitizen flow and immediately commit your message without all this overhead

## Backend

1. Install NPM Dependencies

```sh
cd server
npm i
```

2. Set-up Python Virtual Environment

```sh
cd server/python_files
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
```

3. Install Python Dependencies

```sh
pip3 install -r requirements.txt
deactivate
```

## Frontend

1. Install NPM Dependencies

```sh
cd client
npm i
```

## TLDR Developing

- Get backend up and running locally first before running front-end.

1. Running Backend

```sh
npm run server
```

2. Formatting
   - There is already a command that formats everytime you save and/or commit `.ts .json .js .css` files for both the front-end and backend.
   - Format `.py` files before commits.
   ```sh
   cd server
   npm run format-py
   ```
3. Running Frontend

```sh
npm run start
```
