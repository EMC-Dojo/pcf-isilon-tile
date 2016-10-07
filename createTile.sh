#!/bin/sh
RELEASE_TARFILE=dev_releases/*/*.tgz

function copy_release_tar_file {
  cp $RELEASE_TARFILE $1
}

function generate_private {
cat > config/private.yml << EOF
---
blobstore:
  s3:
    access_key_id: ${AWS_ACCESS_KEY}
    secret_access_key: ${AWS_SECRET_KEY}
EOF
}

mkdir releases/build
pushd releases/build
  git clone https://github.com/EMC-CMD/libstorage-release
  pushd libstorage-release
    generate_private
    bosh -n create release --force --with-tarball
    copy_release_tar_file ../../
  popd

  git clone https://github.com/EMC-CMD/emc-persistence-release
  pushd emc-persistence-release
    generate_private
    git submodule update --init --recursive
    bosh -n create release --force --with-tarball
    copy_release_tar_file ../../
  popd

  git clone https://github.com/cloudfoundry-incubator/routing-release
  pushd routing-release
    generate_private
    ./scripts/update
    bosh -n create release --force --with-tarball
    copy_release_tar_file ../../
  popd
popd

rm -rf releases/build

zip -r persistence-storage.pivotal metadata/ releases/
rm -rf releases/*
