#!/bin/bash

set -ev

# TRAVIS_PULL_REQUEST is either the PR number or "false"
if ([ "${TRAVIS_PULL_REQUEST}" != "false" ])
then
  echo 'Pull request, not deploying'
  exit 0
fi

if ([ "${TRAVIS_BRANCH}" == "development" ])
then
  echo 'Deploying development to AWS'
  TARGETAWSBUCKET="mendix-new-docs-site"
fi

if ([ "${TRAVIS_BRANCH}" == "master" ])
then
  echo 'Deploying master to AWS'
  TARGETAWSBUCKET="mendix-new-docs-site"
fi

echo "Deploying to AWS bucket $TARGETAWSBUCKET"

cd $TRAVIS_BUILD_DIR/public
aws --version

# This depends on the following (secret) Environment Variables being set up in Travis-CI
# AWS key needs to have appropriate access to the TARGETAWSBUCKET
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_DEFAULT_REGION
#
# HUGO creates new files with a newer timestamp except those in the /static folder 
# so this will always push all the html, but only changed /static files.
start=$SECONDS
echo "Starting sync to AWS"
# aws s3 sync . s3://$TARGETAWSBUCKET --delete
echo "Upload to AWS took $((SECONDS - start)) seconds"

exit 0