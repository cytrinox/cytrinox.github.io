FROM debian:13.4-slim@sha256:26f98ccd92fd0a44d6928ce8ff8f4921b4d2f535bfa07555ee5d18f61429cf0c

RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby-full \
    ruby-dev \
    build-essential \
    libvips-dev \
    libvips-tools \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 jekyll

USER jekyll

ENV GEM_HOME=/home/jekyll/gems
ENV PATH=/home/jekyll/gems/bin:$PATH
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN gem install bundler --no-document

WORKDIR /src

COPY --chown=jekyll Gemfile Gemfile.lock ./

RUN bundle install --no-cache

COPY --chown=jekyll . .

VOLUME ["/app"]

CMD bundle exec jekyll build --disable-disk-cache --destination /app
