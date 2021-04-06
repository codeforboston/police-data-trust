# Contributing to Police Misconduct Data Collaborative

- [Contributing to Police Misconduct Data Collaborative](#contributing-to-police-misconduct-data-collaborative)
  - [Code of Conduct](#code-of-conduct)
  - [Issues and Feature Requests](#issues-and-feature-requests)
  - [If You're New to Open Source](#if-youre-new-to-open-source)
  - [Git Flow](#git-flow)
  - [Making Pull Requests](#making-pull-requests)
  - [Python Code Contributions](#python-code-contributions)
    - [Style guide:](#style-guide)
    - [Before you submit a pull request:](#before-you-submit-a-pull-request)

## [Code of Conduct](https://github.com/codeforboston/codeforboston.org/blob/master/code-of-conduct.md)

The Police Misconduct Data Collaborative project has a [Code of Conduct](https://github.com/codeforboston/codeforboston.org/blob/master/code-of-conduct.md)
to which all contributors must adhere.

## [Issues and Feature Requests](https://github.com/codeforboston/police-data-trust/issues)

- If you have a feature request or but report, our [issues page](https://github.com/codeforboston/police-data-trust/issues) is where to go to place those.
- If you think that you've found a bug in the application, first be certain that you're testing against the most recent version of the application available on the main repo. If not, search our [issues list](https://github.com/codeforboston/police-data-trust/issues) on GitHub in case a similar issue has already been opened.

## If You're New to Open Source

If you're brand new to Git and/or GitHub, you'll want to familiarize yourself with the basics of version control, which you can do with Github's [Hello World tutorial](https://guides.github.com/activities/hello-world/).

## Git Flow

Project flow will work like this:

1. You'll make a clone of the `main` branch of the repo on your local machine, and [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) a copy of the main repo to your GitHub account. 

2. You'll push any changes made on your local project to the forked version on your GitHub account, and then open a [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) from your forked repo to the main repo.

## [Making Pull Requests]()

Pull requests are merged into our main branch. This makes main our main development branch. You'll want to keep your fork and local repo current with this branch so you're always working off the latest code. To do so, run these commands:

```
git checkout main
git pull upstream main
git push origin main
```
## Python Code Contributions

### Style guide:

- Use [PEP-8](https://www.python.org/dev/peps/pep-0008/) above everything. We adhere to 80 line limits and 4 space indents.
- Also use the [Google Style Guide](https://google.github.io/styleguide/pyguide.html).

### Before you submit a [pull request](https://github.com/codeforboston/police-data-trust/pulls):

- Run backend tests with `python -m pytest`
- Run flake8 with `flake8 backend/`. If flake8 gives you any trouble, you can run `black backend/` to prettify your code automatically or use `# noqa` comments _sparingly_ if you are absolutely sure a line of code is fine.

