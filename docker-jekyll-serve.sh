#!/bin/bash

docker run --rm \
    --volume="$PWD:/srv/jekyll" \
    -p 4000:4000 \
    jekyll/jekyll \
    jekyll serve