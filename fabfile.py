from tempfile import NamedTemporaryFile
from invoke import task
import os


@task
def install(c):
    """
    Clone or pull latest changes from the repo
    """
    with c.cd("src/"):
        if not c.run("test -d stream-lnd-htlcs-bot", warn=True).ok:
            c.run("git clone https://github.com/routablespace/stream-lnd-htlcs-bot.git")
        with c.cd("stream-lnd-htlcs-bot"):
            c.run("git pull")


@task
def install_supervisord(c):
    """
    Install supervisord
    """
    c.sudo("apt-get install supervisor -y")


@task
def install_supervisord_conf(c, tg_token):
    """
    Install supervisord config
    """
    with open("confs/stream-lnd-htlcs-bot.conf") as f:
        conf = f.read()
        if tg_token:
            conf = conf.replace("{OPTIONS}", f"--tg-token={tg_token}")
        tf = NamedTemporaryFile(mode="w")
        tf.write(conf)
        tf.flush()
        c.put(tf.name, "/tmp/stream-lnd-htlcs-bot.conf")
        tf.close()
        c.sudo("cp /tmp/stream-lnd-htlcs-bot.conf /etc/supervisor/conf.d/")
        c.sudo("supervisorctl update all")


@task
def start(c):
    """
    Start the app
    """
    c.sudo("supervisorctl start stream-lnd-htlcs-bot")


@task
def stop(c):
    """
    Stop the app
    """
    c.sudo("supervisorctl stop stream-lnd-htlcs-bot")


@task
def restart(c):
    """
    Restart the app
    """
    stop(c)
    start(c)


@task
def clear_logs(c):
    """
    Clear the logs
    """
    c.run("rm /home/ubuntu/logs/stream-lnd-htlcs-bot.*")


@task
def logs(c):
    """
    Tail the logs
    """
    c.run("tail -f /home/ubuntu/logs/stream-lnd-htlcs-bot.*")


@task
def sync(c, env=dict(KEYPEM=os.environ["KEYPEM"])):
    """
    Perform an rsync to test latest changes
    """
    c.run(f"mkdir -p /home/{c.user}/src/stream-lnd-htlcs-bot/")
    cmd = f"""rsync -azv -e 'ssh -i {env["KEYPEM"]}' . {c.user}@{c.host}:/home/{c.user}/src/stream-lnd-htlcs-bot/"""
    c.run(f"mkdir -p /home/{c.user}/src/stream-lnd-htlcs-bot/")
    print(cmd)
    c.local(cmd)
    with c.cd(f"/home/{c.user}/src/stream-lnd-htlcs-bot/"):
        c.run("pip3 install -r requirements.txt")
