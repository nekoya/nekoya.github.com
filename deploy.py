import datetime
import os
import shutil
import subprocess

from blog import logger

deploy_dir = '__dist'
repository = 'git@github.com:nekoya/nekoya.github.com.git'


def deploy() -> None:
    try:
        logger.info('prepare git repository')
        shutil.rmtree('.git', ignore_errors=True)

        execute('git init')
        execute('git add .')
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = 'Update at {} UTC'.format(now)
        logger.info('commit "{}"'.format(commit_message))
        execute('git commit -m "{}"'.format(commit_message))

        logger.info('Set remote repository: {}'.format(repository))
        execute('git remote add origin %s' % repository)
        logger.info('push to master branch')
        execute('git push -f origin master')
    except Exception as e:
        logger.error(str(e))


def execute(cmd: str) -> None:
    proc = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        logger.warn(out)
        raise Exception(err)


if __name__ == '__main__':
    pwd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(os.path.join(pwd, deploy_dir))
    deploy()
