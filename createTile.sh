#!/bin/sh

pushd releases
wget -O emc-persistence-release-3.tgz https://s3.amazonaws.com/emc-persistence-release/emc-persistence-release-3.tgz
wget -O libstorage-release-3.tgz https://s3.amazonaws.com/libstorage/libstorage-release-3.tgz
wget -O cf-routing-release-0.140.0.tgz https://bosh.io/d/github.com/cloudfoundry-incubator/cf-routing-release?v=0.140.0
popd

zip -r persistence-storage.pivotal metadata/ releases/
rm -rf releases/*
