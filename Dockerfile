FROM debian:13.4-slim@sha256:26f98ccd92fd0a44d6928ce8ff8f4921b4d2f535bfa07555ee5d18f61429cf0c AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby-full \
    ruby-dev \
    build-essential \
    libvips-dev \
    libvips-tools \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 jekyll && mkdir /build && chown jekyll /build

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

RUN bundle exec jekyll build --disable-disk-cache --destination /build


FROM nginxinc/nginx-unprivileged:1.29.5-alpine3.23@sha256:f99cc61bf1719f30230602036314ff6ba5dcede8965c5ed3ded71b8bbced3723

COPY --from=builder /build /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
