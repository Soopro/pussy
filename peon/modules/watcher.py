#coding=utf-8
from __future__ import absolute_import

import os, subprocess, time
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler

from ..services import RenderHandler
from .helpers import load_config

# variables
SLEEP_TIME = 1
DEFAULT_SRC_DIR = 'src'
DEFAULT_DEST_DIR = 'build'

# handlers
class WatchPatternsHandler(PatternMatchingEventHandler):
    
    def __init__(self, render_handler,
                       include_mark = None,
                       patterns = None,
                       ignore_patterns = None,
                       ignore_directories = False,
                       case_sensitive = False):

        super(PatternMatchingEventHandler, self).__init__()
        self._patterns = patterns
        self._ignore_patterns = ignore_patterns
        self._ignore_directories = ignore_directories
        self._case_sensitive = case_sensitive
        
        if isinstance(render_handler, RenderHandler):
            self.render = render_handler
        else:
            raise Exception("Render is invalid.")
        
        self.incl_mark = include_mark
    
    def _find_end_path(self, path):
        if not path:
            return None
        tmp_path_list = path.rsplit(os.path.sep,1)
        if len(tmp_path_list) > 0:
            return tmp_path_list[1]
        else:
            return None

    def on_created(self, event):
        self.render.render(event.src_path)
    
    def on_modified(self, event):
        self.render.render(event.src_path)
    
    def on_moved(self, event):
        end_src_path = self._find_end_path(event.src_path)
        end_dest_path = self._find_end_path(event.dest_path)
        if end_src_path != end_dest_path:
            self.render.move(event.src_path, event.dest_path)
    
    def on_deleted(self, event):
        self.render.delete(event.src_path)
    


#-------------
# main
#-------------
DEFAULT_ACTION = 'watch'


def watch(opts):
    peon_config = load_config(DEFAULT_ACTION, force=False, multiple=False)
    
    print "------------"
    print "Peon Wacther started"
    print "------------"

    if peon_config:
        src_dir = peon_config.get('src', DEFAULT_SRC_DIR)
        dest_dir = peon_config.get('dest', DEFAULT_DEST_DIR)
        skip_includes = peon_config.get('skip_includes', [])
        clean_dest = peon_config.get('clean', True)
        server = peon_config.get('server', False)
        server_port = peon_config.get('port', '')
        pyco_server = peon_config.get('pyco')
    else:
        src_dir = opts.src_dir or DEFAULT_SRC_DIR
        dest_dir = opts.dest_dir or DEFAULT_DEST_DIR
        skip_includes = opts.skip_includes or []
        clean_dest = opts.clean
        server = bool(opts.port)
        server_port = opts.port
        pyco_server = opts.pyco

    
    if dest_dir == DEFAULT_SRC_DIR:
        dest_dir = DEFAULT_DEST_DIR
    
    render_opts = {
        "src": src_dir,
        "dest": dest_dir,
        "skip_includes": skip_includes,
    }
    render = RenderHandler(render_opts)
    
    if clean_dest:
        render.clean()
        render.render_all()
    
    if server:
        if pyco_server:
            args = ['python', '{}{}pyco.py'.format(pyco_server, os.path.sep)]
            pyco_progress = subprocess.Popen(args)
            # args = 'cd '+pyco_server+' && python pyco.py'
            # pyco_progress = subprocess.Popen(args, shell=True)
        else:
            try:
                port = str(server_port)
            except:
                port = ''

            if port:
                args = ['peon', '-s', port, '--http', '--dir', dest_dir]
            else:
                args = ['peon', '-s', '--http', '--dir', dest_dir]

            server_progress = subprocess.Popen(args)
    
    
    observer = Observer()
    watcher = WatchPatternsHandler(render_handler = render,
                                   ignore_patterns = ['*/.*'])

    observer.schedule(watcher, src_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        observer.stop()
        print "------------"
        print "Peon Wacther stoped"
        print "------------"
        
    observer.join()
    


if __name__ == '__main__':
    import argparse
    # command line options
    parser = argparse.ArgumentParser(
                        description='Options of run Peon watcher.')
    
    parser.add_argument('--dest',
                        dest='dest_dir',
                        action='store',
                        nargs='?',
                        const='build',
                        help='Define operation dest dir.')
    
    parser.add_argument('--src', 
                        dest='src_dir',
                        action='store',
                        nargs='?',
                        const='src',
                        help='Define operation src dir.')
    
    parser.add_argument('--clean',
                        dest='clean',
                        action='store_const',
                        const=True,
                        help='Clean dest folder before take actions.')
    
    parser.add_argument('--skip',
                        dest='skip_includes',
                        action='append',
                        type=str,
                        help='Skip type of include files with rendering.')
    
    parser.add_argument('-w', '--watcher',
                        dest='watcher',
                        action='store_const',
                        const=True,
                        help='Run Peon watcher file changes.')

    opts, unknown = parser.parse_known_args()

    watch(opts)
