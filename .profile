# heroku app .profile file https://devcenter.heroku.com/articles/dynos#the-profile-file
# add ffmpeg on path
export PATH="$(pwd)/vendor/ffmpeg/amd64:${PATH}"
export PATH="$(pwd)/vendor/youtube-dl/:${PATH}"
