#!/usr/bin/python
import os
import sys
import ui

class log:

    def __init__(self):
        self.log_to_file = False
        self.log_file = 'ubifs_output.log'
        self.exit_on_except = False
        self.quiet = False

    def _out(self, s):
        if not self.quiet:
            if self.log_to_file:
                with open(os.path.join(ui.common.output_dir, self.log_file), 'a') as f:
                    f.write('%s\n' % s)
                f.close()
            else:
                print '%s' % s
        if self.exit_on_except:
            sys.exit()

    def write(self, s):
        self._out(s)

    def write_node(self, n):
        buf = '%s\n' % n
        for key, value in n:
            buf += '\t%s: %s\n' % (key, value)

        self._out(buf)