# Life in Korea : Experience of Uzbeks in Korea
This is static site based jekyll that contains information shared by Uzbekistan people living in Korea.

## How to add article
- `Fork` the repository
- Add new article with create file with a name `date-title.md` in `_posts`
- Test locally
- Push and create pull request

> :warning: Do NOT directly modify `gh-pages` branch, it is deployed when `main` branch is  modified.


## How to test locally
In order to test your changes locally you need to install jekyll, 
and run following command.
```sh
bundle exec jekyll serve
```

### Docker Environment
If you have docker, you may run jekyll in docker container. 
First you need to pull jekyll docker image.
```sh
docker pull jekyll/jekyll
```

Then, you may run following script
```sh
./docker-jekyll-serve.sh
```


### Verify changes

Visit http://localhost:4000 on your browser
