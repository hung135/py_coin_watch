#!/usr/bin/env bash

docker run --name travis-debug -dit travisci/ci-garnet:packer-1512502276-986baf0 /sbin/init
docker exec -it travis-debug bash -l
su travis

cd /home/travis/builds/
git clone https://github.com/travis-ci/travis-build
mkdir ~/.travis/
cd travis-build
ln -s /home/travis/builds/travis-build ~/.travis/travis-build
gem install bundler
bundle install --gemfile ~/.travis/travis-build/Gemfile
bundler binstubs travis

cd /home/travis/builds/
git clone --depth=50 --branch='master' https://github.com/hung135/py_coin_watch hung135/py_coin_watch
cd hung135/py_coin_watch
~/.travis/travis-build/bin/travis compile >run_ci.sh
sed -i "s/branch.*https/branch\\\=\\\'master\\\'\\\ https/g" run_ci.sh
chmod +x run_ci.sh
./run_ci.sh
