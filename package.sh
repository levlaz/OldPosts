SITE_PACKAGES=$(pipenv --venv)/lib/python3.6/site-packages
DIR=$(pwd)

# Make sure pipenv is good to go
pipenv install

cd $SITE_PACKAGES
zip -r9 $DIR/OldPosts.zip *

cd $DIR
zip -g OldPosts.zip old_posts.py

