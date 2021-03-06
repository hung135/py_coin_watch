#!/usr/bin/env bash
export MACHINE_NAME="default"
export VOL_DIR="_docker_travis"
export WORKDIR=$(basename "$VOL_DIR")
export VOL_DIR2="_docker_travis_deploy"
export WORKDIR2=$(basename "$VOL_DIR2")
export PROJECT_PATH=$(pwd)
export U=2000
export G=2000
diskutil unmount $PROJECT_PATH/$WORKDIR
diskutil unmount $PROJECT_PATH/$WORKDIR2


echo $PROJECT_PATH/$WORKDIR
rm $PROJECT_PATH/$WORKDIR
mkdir $PROJECT_PATH/$WORKDIR

docker-machine ssh default sudo rm foo -rf
docker-machine ssh default sudo rm foo2 -rf
docker-machine ssh default mkdir foo
docker-machine ssh default mkdir foo2

docker-machine ssh default chmod 777 foo -R
docker-machine ssh default chmod 777 foo2 -R


docker-machine mount default:/home/docker/foo $PROJECT_PATH/$WORKDIR
docker-machine mount default:/home/docker/foo2 $PROJECT_PATH/$WORKDIR2

#docker-machine ssh $MACHINE_NAME "sudo mkdir -p \"$VOL_DIR\""
#vboxmanage sharedfolder add "$MACHINE_NAME" --name "$WORKDIR" --hostpath "$VOL_DIR" --transient
#docker-machine ssh $MACHINE_NAME "sudo mount -t vboxsf -o uid=\"$U\",gid=\"$G\" \"$WORKDIR\" \"$VOL_DIR\""

docker-machine start $MACHINE_NAME
docker-machine env
eval $(docker-machine env)

docker rm travis-debug -f
# this is for a python build find yours Here: https://docs.travis-ci.com/user/common-build-problems/
# under Running a Container Based Docker Image Locally #
#docker run --name travis-debug -dit travisci/ci-garnet:packer-1512502276-986baf0 /sbin/init
#mount local dir
mkdir travis
pwd
docker run --name travis-debug -v /home/docker/foo/:/home/travis/builds/ -v /home/docker/foo2/:/home/travis/.travis/  -dit travisci/ci-garnet:packer-1512502276-986baf0 /sbin/init


docker exec --user travis travis-debug /bin/bash -c "
export BRANCH=master;
export PROJECT_PATH=hung135/py_coin_watch;
source ~/.bash_profile;
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
~/.travis/travis-build/bin/travis compile >run_ci.sh;

sed -i \"s/branch.*https/branch\\\\\\=\\\\\\'\$BRANCH\\\\\\'\\\\\\ https/g\" run_ci.sh | grep https://github;
chmod +x run_ci.sh;
./run_ci.sh"
