# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "uzbekkorea"
  spec.version       = "1.0.0"
  spec.authors       = ["Elmurod Talipov"]
  spec.email         = ["elmurod.talipov@gmail.com"]

  spec.summary       = "Special Theme for uzbekkorea.com based on Chirpy 5.1.0."
  spec.homepage      = "https://uzbekkorea.com"
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0").select { |f|
    f.match(%r!^((_(includes|layouts|sass|data|tabs|plugins)|assets)\/|_config|README|LICENSE|index)!i)
  }

  spec.required_ruby_version = ">= 2.4"

  spec.add_runtime_dependency "jekyll", "~> 4.1"
  spec.add_runtime_dependency "jekyll-paginate", "~> 1.1"
  spec.add_runtime_dependency "jekyll-redirect-from", "~> 0.16"
  spec.add_runtime_dependency "jekyll-seo-tag", "~> 2.7"
  spec.add_runtime_dependency "jekyll-archives", "~> 2.2"
  spec.add_runtime_dependency "jekyll-sitemap", "~> 1.4"

  spec.post_install_message =  <<~MSG
                               Thanks for installing !
                               MSG

end
