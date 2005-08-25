from setuptools import Command
from distutils.errors import DistutilsOptionError
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

    _svn_url_re = re.compile(r'\bURL: (.*)')
    _setup_version_re = re.compile(r'(version\s+=\s+)([^ \n\r,)]*)')
    _egg_info_re = re.compile(r'^[egg_info]$')

    def run(self):
        ei_cmd = self.get_finalized_command("egg_info")
        path_item = normalize_path(ei_cmd.egg_base)
        metadata = PathMetadata(
            path_item, normalize_path(ei_cmd.egg_info)
        )
        proc = subprocess.Popen(
            ['svn', 'info', path_item],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            print 'Error from svn:'
            print stderr
        match = self._svn_url_re.search(stdout)
        if not match:
            print 'svn output did not contain "URL: ...":'
            print stdout
            assert 0
        svn_url = match.group(1)
        if not svn_url.endswith('/trunk'):
            print 'svn URL must end with "/trunk" (current: %r)' % svn_url
            assert 0
        package_url = svn_url.rsplit('/', 1)[0]
        tag_url = package_url + '/tags/' + self.version
        # @@: Should check svn status
        command = ['svn', 'cp', '--message', self.message,
                   svn_url, tag_url]
        print ' '.join(command)
        proc = subprocess.Popen(command)
        proc.communicate()
        tmpdir = tempfile.mkdtemp(prefix='tag_checkout_')
        command = ['svn', 'co', '--quiet', tag_url, tmpdir]
        print ' '.join(command)
        subprocess.Popen(command).communicate()
        self.update_setup_py(tmpdir)
        self.update_setup_cfg(tmpdir)
        print ' '.join(command)
        subprocess.Popen(command).communicate()
        command = ['svn', 'commit', '--message',
                   'Auto-update of version strings', tmpdir]
        print ' '.join(command)
        subprocess.Popen(command).communicate()
        print 'Removing %s' % tmpdir
        shutil.rmtree(tmpdir)

    def update_setup_py(self, tmpdir):
        setup_py = os.path.join(tmpdir, 'setup.py')
        if not os.path.exists(setup_py):
            print 'setup.py file cannot be found at %s' % setup_py
            return
        f = open(setup_py)
        content = f.read()
        f.close()
        match = self._setup_version_re.search(content)
        if not match:
            print 'Cannot find version info in %s' % setup_py
        else:
            new_content = (
                content[:match.start()]
                + match.group(1)
                + repr(self.version)
                + content[match.end():])
            if new_content == content:
                print 'Version string up-to-date (edit trunk yourself)'
            else:
                f = open(setup_py, 'w')
                f.write(new_content)
                f.close()
                print '%s version updated' % setup_py
        command = [sys.executable, setup_py, 'egg_info']

    def update_setup_cfg(self, tmpdir):
        setup_cfg = os.path.join(tmpdir, 'setup.cfg')
        if not os.path.exists(setup_cfg):
            print 'setup.cfg file cannot be found at %s' % setup_cfg
            return
        f = open(setup_cfg)
        content = f.readlines()
        f.close()
        new_content = []
        egg_info_content = []
        while content:
            line = content.pop(0)
            if line.strip() != '[egg_info]':
                new_content.append(line)
            else:
                egg_info_content.append(line)
                inner_line = None
                while content:
                    inner_line = content.pop(0)
                    if inner_line.strip().startswith('['):
                        break
                    if inner_line.strip().startswith('tag_build'):
                        continue
                    elif inner_line.strip().startswith('tag_svn_revision'):
                        continue
                    if line.strip():
                        egg_info_content.append(line)
                if len(egg_info_content) == 1:
                    egg_info_content = []
                else:
                    egg_info_content.append('\n')
                new_content.extend(egg_info_content)
                if inner_line:
                    new_content.append(inner_line)
        content = ''.join(content)
        if not content:
            command = ['svn', 'rm', setup_cfg]
            print ' '.join(command)
            subprocess.Popen(command).communicate()
            return
        if content != new_content:
            f = open(setup_cfg, 'w')
            f.write(new_content)
            f.close()
            print '%s updated' % setup_cfg
        
                    
                    
        
