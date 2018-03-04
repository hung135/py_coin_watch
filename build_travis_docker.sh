#!/usr/bin/env bash
docker-machine start default
docker-machine env
eval $(docker-machine env)

docker rm travis-debug -f
docker run --name travis-debug -dit travisci/ci-garnet:packer-1512502276-986baf0 /sbin/init

docker exec --user travis travis-debug /bin/bash -c "
export BRANCH=master;
export PROJECT_PATH=hung135/py_coin_watch;
source ~/.bash_profile; env;
cd /home/travis/builds/;
git clone https://github.com/travis-ci/travis-build;
mkdir ~/.travis/;
cd travis-build;
ln -s /home/travis/builds/travis-build ~/.travis/travis-build;
gem install bundler;
bundle install --gemfile /home/travis/builds/travis-build/Gemfile;
echo bundle installed;
bundler binstubs travis;
cd /home/travis/builds/;
git clone --depth=50 --branch='master' https://github.com/\$PROJECT_PATH \$PROJECT_PATH;
cd \$PROJECT_PATH;
pwd
~/.travis/travis-build/bin/travis compile >run_ci.sh;

sed -i \"s/branch.*https/branch\\\\\\=\\\\\\'\$BRANCH\\\\\\'\\\\\\ https/g\" run_ci.sh | grep https://github;
chmod +x run_ci.sh;
./run_ci.sh;

"
#chmod +x run_ci.sh
#./run_ci.sh
