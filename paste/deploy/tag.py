from setuptools import Command
from setuptools.command import setopt
from ConfigParser import NoSectionError
from distutils.errors import *
from distutils import log
from pkg_resources import *
import subprocess
import re
import sys
import os
import shutil
import tempfile

class tag(Command):

    description = "Tag for release"

    user_options = [
        ('version=', 'v', "Specify version"),
        ('message=', 'm', "Specify a log message"),
        ('build=', 'b', "Specify directory to build tag files in"),
        ]

    version = None
    message = None
    build = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        if self.version is None:
            raise DistutilsOptionError(
                "You must specify a version")
        if self.message is None:
            self.message = "Tagging %s version" % self.version
        if self.build and os.path.exists(self.build):
            raise DistutilsOptionError(
                "The build directory %s already exists" % self.build)
        if self.build is None:
            self.build = tempfile.mkdtemp(prefix='tag_checkout_')
            
    _svn_url_re = re.compile(r'\bURL: (.*)')
    _setup_version_re = re.compile(r'(version\s+=\s+)([^ \n\r,)]*)')
    _egg_info_re = re.compile(r'^[egg_info]$')

    def run(self):
        ei_cmd = self.get_finalized_command("egg_info")
        path_item = normalize_path(ei_cmd.egg_base)
        metadata = PathMetadata(
            path_item, normalize_path(ei_cmd.egg_info)
        )
        stdout = run_command(['svn', 'info', path_item])
        match = self._svn_url_re.search(stdout)
        if not match:
            raise DistutilsExecError(
                'svn output did not contain "URL: ...":\n' + stdout)
        svn_url = match.group(1)
        if not svn_url.endswith('/trunk'):
            raise DistutilsExecError(
                'svn URL must end with "/trunk" (current: %r)' % svn_url)
        package_url = svn_url.rsplit('/', 1)[0]
        tag_url = package_url + '/tags/' + self.version
        run_command(['svn', 'cp', '--message', self.message,
                     svn_url, tag_url])
        run_command(['svn', 'co', '--quiet', tag_url, self.build])
        self.update_setup_py()
        self.update_setup_cfg()
        run_command(['svn', 'commit', '--message',
                     'Auto-update of version strings', self.build])

    def update_setup_py(self):
        setup_py = os.path.join(self.build, 'setup.py')
        if not os.path.exists(setup_py):
            log.warn('setup.py file cannot be found at %s' % setup_py)
            return
        f = open(setup_py)
        content = f.read()
        f.close()
        match = self._setup_version_re.search(content)
        if not match:
            log.warn('Cannot find version info in %s' % setup_py)
        else:
            new_content = (
                content[:match.start()]
                + match.group(1)
                + repr(self.version)
                + content[match.end():])
            if new_content == content:
                log.info('Version string up-to-date (edit trunk yourself)')
            else:
                f = open(setup_py, 'w')
                f.write(new_content)
                f.close()
                log.info('%s version updated' % setup_py)
        command = [sys.executable, setup_py, 'egg_info']

    def update_setup_cfg(self):
        setup_cfg = os.path.join(self.build, 'setup.cfg')
        if not os.path.exists(setup_cfg):
            log.warn('setup.cfg file cannot be found at %s' % setup_cfg)
            return
        try:
            setopt.edit_config(
                setup_cfg,
                {'egg_info': {'tag_build': None,
                              'tag_svn_revision': None}})
        except NoSectionError:
            # No [egg_info]; that's okay
            pass
        f = open(setup_cfg)
        content = f.read()
        f.close()
        if not content.strip():
            log.info('%s empty; deleting' % setup_cfg)
            run_command(['svn', 'rm', '--force', setup_cfg])
                    
def run_command(command_list, stdin=None):
    log.info('Running %s', format_command(command_list))
    proc = subprocess.Popen(command_list,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(stdin)
    if stderr:
        log.warn('Ouput from %s:\n%s',
                 format_command(command_list),
                 stderr)
    returncode = proc.returncode
    if returncode:
        error = 'Exit code %s from %s' % (
            returncode, format_command(command_list))
        if stderr:
            error += '; stderr output:\n' + stderr
        raise DistutilsExecError(error)
    return stdout

def format_command(lst):
    return ' '.join(map(quote_command_item, lst))

def quote_command_item(item):
    if ' ' in item: # @@: Obvious I should check more characters
        for char in ('\\', '"', "'", '$'):
            item = item.replace(char, '\\' + char)
        item = '"%s"' % item
    return item

