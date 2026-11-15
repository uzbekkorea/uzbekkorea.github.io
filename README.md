# Life in Korea : Experience of Uzbeks in Korea
This is static site based jekyll that contains information shared by Uzbekistan people living in Korea.

## How to add article
- `Fork` the repository
- Add new article with create file with a name `date-title.md` in `_posts`
- Test locally
- Push and create pull request

> :warning: Do NOT directly modify `gh-pages` branch, it is deployed when `main` branch is  modified.


## How to test locally
You need Ruby 3.0 or newer. On macOS, install it with Homebrew:
```sh
brew install ruby
```

Then run the site with live reload:
```sh
tools/serve.sh
```

To only check that the site builds (same as the PR build check):
```sh
tools/serve.sh build
```

The script installs gems into `vendor/bundle` on the first run.

### Verify changes

Visit http://localhost:4000 on your browser
