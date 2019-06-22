from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def render_root():
    r = request
    # app.logger.warning("data: %s" % r.data)
    app.logger.warning("headers: %s " % r.headers)
    # app.logger.warning("view_args: %s " % r.view_args)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
