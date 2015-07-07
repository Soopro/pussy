#coding=utf-8
from __future__ import absolute_import

import os, sys, glob
import subprocess

from ..services import RenderHandler, MinifyHandler
from ..utlis import (now, gen_md5, copy_file, safe_path, 
                     ensure_dir, remove_dir, remove_file)
from .helpers import load_config, run_task


# variables
TEMP_FILE = '_construct_temp_.tmp'
DEFAULT_LIBS_DIR = 'src/libs/'
DEFAULT_SRC_DIR = 'src'
DEFAULT_BUILD_DIR = 'build'
DEFAULT_DIST_DIR = 'dist'


# helpers
def helper_find_path_list(src, cwd):
    if not isinstance(src, list):
        src = [src]
    
    cwd = safe_path(cwd)
    path_list = []
    for file in src:
        if file.startswith('!'):
            continue
        file = safe_path(file)        
        file_path_pattern = os.path.join(cwd, file)
        paths = glob.glob(file_path_pattern)

        for path in paths:
            if not os.path.exists(path):
                print "peon: Failed -> " + path + " (not exist)"
                continue
            if not path in path_list:
                path_list.append(path)
                
    for file in src:
        if not file.startswith('!'):
            continue
        file = safe_path(file[1:])
        file_path_pattern = os.path.join(cwd, file)
        paths = glob.glob(file_path_pattern)
        
        for path in paths:
            if path in path_list:
                path_list.remove(path)
                
    return path_list

# methods
def install(cfg):
    for c in cfg:
        if c == "bower":
            try:
                print "Bower installing......"
                subprocess.call(["bower", "update"])
                subprocess.call(["bower", "install"])
            except Exception as e:
                raise e

        elif c == "npm":
            try:
                print "Npm installing......"
                subprocess.call(["npm", "update"])
                subprocess.call(["npm", "install"])
            except Exception as e:
                raise e


def shell(cfg):
    for cmd in cfg:
        subprocess.call(cmd, shell=True)


def rev(cfg):
    if cfg.get('pattern'):
        pattern = str(cfg['pattern'])
        find = cfg.get('find')
        if find:
            find = str(find)
        else:
            find = pattern
        pattern = find.replace(pattern, gen_md5())
        replacements = {find: pattern}
    cwd = safe_path(cfg.get('cwd',''))
    files = cfg.get('src', []) 
    path_list = helper_find_path_list(files, cwd)

    for path in path_list:
        file = open(path)
        if os.path.isfile(TEMP_FILE):
            os.remove(TEMP_FILE)
        tmp = open(TEMP_FILE, 'w')
        for line in file:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            tmp.write(line)
        tmp.close()
        file.close()
        try:
            os.rename(TEMP_FILE, path)
            print "peon: MD5ify -> " + path
        except Exception as e:
            print('Error: %s' % e)
            raise e

    if os.path.isfile(TEMP_FILE):
        os.remove(TEMP_FILE)
        
    print "peon: Work work ...(rev)"


def copy(cfg):
    for key in cfg:
        rule = cfg[key]
        is_flatten = rule.get('flatten', False)
        force = rule.get('force', True)
        cwd, dest = safe_path(rule.get('cwd', ''),
                              rule.get('dest', DEFAULT_LIBS_DIR))
        
        files = rule.get('src', [])
        path_list = helper_find_path_list(files, cwd)
        
        for path in path_list:
            if is_flatten:
                dest_path = dest
                ensure_dir(dest_path)
            else:
                _path = safe_path(path.replace(cwd, '', 1))
                dest_path = safe_path(os.path.join(dest, _path))
                ensure_dir(dest_path, True)

            if os.path.isdir(path):
                ensure_dir(dest_path)
                continue
            
            if force or not os.path.isfile(dest_path):
                copy_file(path, dest_path)
            else:
                continue
    
    print "peon: Work work ...(copy)"


def render(cfg):
    render_opts = {
        "src": cfg.get('cwd', DEFAULT_SRC_DIR),
        "dest": cfg.get('dest', DEFAULT_BUILD_DIR)
    }
    render = RenderHandler(render_opts)
    if cfg.get('clean') is True:
        render.clean()
    render.render_all()
    print "peon: Work work ...(render)"

def clean(paths):
    cwd = ''
    path_list = helper_find_path_list(paths, cwd)
    for path in path_list:
        if os.path.isdir(path):
            remove_dir(path)
    print "peon: Work work ...(clean)"

def scrap(cfg):
    cwd = safe_path(cfg.get('cwd', ''))
    files = cfg.get('src', [])
    path_list = helper_find_path_list(files, cwd)
    for path in path_list:
        if os.path.isdir(path):
            remove_dir(path)
        elif os.path.isfile(path):
            remove_file(path)
    print "peon: Work work ...(scrap)"

def compress(cfg):
    cwd, dest = safe_path(cfg.get('cwd', DEFAULT_BUILD_DIR),
                          cfg.get('dest', DEFAULT_DIST_DIR))
    minify = MinifyHandler(cwd)
    files = cfg.get('src', [])
    path_list = helper_find_path_list(files, cwd)
    for path in path_list:
        minify.process_html(path)
    
    print "peon: Work work ...(compress)"


#-------------
# main
#-------------
DEFAULT_ACTION = 'release'
ALLOWED_ACTION_TYPES = ['release', 'init', 'build']

COMMANDS = {
    "install": install,
    "copy": copy,
    "clean": clean,
    "scrap": scrap,
    "render": render,
    "compress": compress,
    "rev": rev,
    "shell": shell
}

def construct(opts):
    config_type = opts.construct or DEFAULT_ACTION
    peon_config = load_config(config_type)

    run_task(peon_config, COMMANDS)
    
    print "peon: finish construct ..."



if __name__ == '__main__':
    import argparse
    # command line options
    parser = argparse.ArgumentParser(
                    description='Options of run Peon dev server.')

    parser.add_argument('-c', '--construct', 
                        dest='construct',
                        action='store',
                        nargs='?',
                        type=str,
                        const='release',
                        help='Run Peon construct to build files.')

    opts, unknown = parser.parse_known_args()
    
    construct(opts)