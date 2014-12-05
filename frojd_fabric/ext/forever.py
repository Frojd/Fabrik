
# https://github.com/nodejitsu/forever

# forever start app.js
# forever stop app.js
# forever restart app.js


def restart():
    app = "app.js"
    env.run("forever restart %s" % app)

