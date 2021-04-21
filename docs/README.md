# Documentation

The full docs are available at: https://codeforboston.github.io/police-data-trust/

### Info

The docs were made with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

There are a lot of extensions included in this documentation in addition to Material:

- Most of the extensions come from [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).
- We use a tool called [Mermaid](https://mermaid-js.github.io/mermaid-live-editor/) for our flow charts.

All of these tools are added and configured inside `mkdocs.yml`. Note you need to pip install them for them to work when you deploy; see deployment script below.

### Deploying / Refreshing the Docs

If you have write permission to the upstream repository (i.e. you are a project manager), run the following:

```shell script
cd docs
mkdocs gh-deploy --remote-name upstream
```

If you do not have write permission to the upstream repository, you can do one of the following:
 
 1. (Preferred) Ask a project manager to refresh the pages after you've made changes to the docs.
 2. Run `mkdocs gh-deploy` on your own fork, and then do a pull request to `codeforboston:gh-pages`:
 
```shell script
mkdocs gh-deploy
git checkout gh-pages
git push origin gh-pages
```
