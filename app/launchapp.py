import hashlib

import launch
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask('docker_launcher')
app.secret_key = '\xc8d\x19E}\xa5g\xbbC\xbd\xe2\x17\x83\xfa!>\xead\x07p\xbd\x92\xce\x85'


HISTORY = []
LAUNCHED_SESSIONS = []
FLASH_CLS = {
    'error': "alert alert-danger",
    'success': "alert alert-success",
}


@app.route('/', methods=['GET'])
def home():
    launched_sessions = launch.active_eri_images(ignore_other_images=True)

    return render_template(
        'index.html',
        launched_sessions=launched_sessions,
        sessoptions=sorted(launch.ERI_IMAGES.keys()),
        num_avail_gpus=list(range(len(launch.AVAIL_DEVICES) + 1))
    )


@app.route('/createSession', methods=['POST'])
def create_session():
    resp = launch.launch(
        username=request.form['username'],
        imagetype=request.form['imagetype'],
        jupyter_pwd=request.form['jupyter_pwd'],
        num_gpus=request.form['num_gpus']
    )
    HISTORY.append(resp)

    # handle errors
    if resp.get('error', False):
        flash(
            message=resp.get('message', 'unhandled error'),
            category=FLASH_CLS['error']
        )
        return redirect(url_for('home'))

    flash(
        message="docker container {} created successfully".format(
            resp['id'][:10]
        ),
        category=FLASH_CLS['success']
    )
    return redirect(url_for('home'))


@app.route('/killSession', methods=['POST'])
def kill_session():
    # verify that the password they provided hashes to the same value as the
    # known pw hash
    truehash = request.form['pwhash']
    newhash = hashlib.md5(request.form['jupyter_pwd'].encode()).hexdigest()
    if truehash != newhash:
        flash(
            message=(
                "unable to kill session - incorrect password. if this is"
                " your container and you have forgotten the password, contact"
                " admin for e"
            ),
            category=FLASH_CLS['error']
        )
        return redirect(url_for('home'))

    resp = launch.kill(docker_id=request.form['docker_id'])
    HISTORY.append(resp)

    # handle errors
    if resp.get('error', False):
        flash(
            message=resp.get('message', 'unhandled error'),
            category=FLASH_CLS['error']
        )
        return redirect(url_for('home'))

    flash(
        message="docker container {} killed successfully".format(
            request.form['docker_id'][:10]
        ),
        category=FLASH_CLS['success']
    )
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
