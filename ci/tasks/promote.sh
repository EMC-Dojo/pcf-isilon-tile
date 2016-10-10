#!/bin/bash
# vim: set ft=sh

set -e -x

export REPO_NAME=persistence-tile
export integer_version=`cut -d "." -f1 ${VERSION_FILE}`
echo ${integer_version} > promote/integer_version

cp -r ${REPO_NAME} promote/${REPO_NAME}
pushd promote/${REPO_NAME}
  ./ci/tasks/create_tile.py
  mv persistence-storage.pivotal ../persistence-storage-${integer_version}.pivotal

  git config --global user.email ${GITHUB_EMAIL}
  git config --global user.name ${GITHUB_USER}
  git config --global push.default simple

  echo "## v${integer_version}" >> CHANGELOG.md
  echo `git log -1 --abbrev-commit --pretty=oneline` >> CHANGELOG.md
  echo "${integer_version}.0.0" > ci/version
  git add CHANGELOG.md
  git add ci/version

  git commit -m ":airplane: New final release v${integer_version}" -m "[ci skip]"
popd
