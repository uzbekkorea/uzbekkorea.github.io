#!/bin/bash
# Run the site locally.
#   tools/serve.sh          serve at http://localhost:4000 with live reload
#   tools/serve.sh build    build once into _site and exit (verify the build)

set -e

cd "$(dirname "$0")/.."

# Prefer Homebrew Ruby, macOS system Ruby is too old
if [ -x /opt/homebrew/opt/ruby/bin/ruby ]; then
    export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
elif [ -x /usr/local/opt/ruby/bin/ruby ]; then
    export PATH="/usr/local/opt/ruby/bin:$PATH"
fi

if ! ruby -e 'exit Gem::Version.new(RUBY_VERSION) >= Gem::Version.new("3.0")' 2>/dev/null; then
    echo "Ruby 3.0 or newer is required (found: $(ruby -v 2>/dev/null || echo none))"
    echo "Install it with: brew install ruby"
    exit 1
fi

# Keep gems inside the project (vendor/ is gitignored)
bundle config set --local path vendor/bundle
bundle check > /dev/null 2>&1 || bundle install

case "$1" in
    build)
        JEKYLL_ENV=production bundle exec jekyll build
        ;;
    "")
        bundle exec jekyll serve --livereload
        ;;
    *)
        echo "Usage: $0 [build]"
        exit 127
        ;;
esac
