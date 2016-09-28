import datetime
import os
import subprocess
import sys
import time

cmd = sys.argv[1:]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

anim_frames = [
    '[█         ]',
    '[▓█        ]',
    '[▒▓█       ]',
    '[░▒▓█      ]',
    '[░░▒▓█     ]',
    '[░░░▒▓█    ]',
    '[ ░░░▒▓█   ]',
    '[  ░░░▒▓█  ]',
    '[   ░░░▒▓█ ]',
    '[    ░░░▒▓█]',
    '[     ░░░▒█]',
    '[      ░░░█]',
    '[       ░░█]',
    '[        ░█]',
    '[         █]',
    '[        █▓]',
    '[       █▓▒]',
    '[      █▓▒░]',
    '[     █▓▒░░]',
    '[    █▓▒░░░]',
    '[   █▓▒░░░ ]',
    '[  █▓▒░░░  ]',
    '[ █▓▒░░░   ]',
    '[█▓▒░░░    ]',
    '[█▒░░░     ]',
    '[█░░░      ]',
    '[█░░       ]',
    '[█░        ]',
]
counter = 0

start = datetime.datetime.now()
last_check = start
command_str = " ".join(cmd)
while p.poll() is None:
    now = datetime.datetime.now()
    if last_check + datetime.timedelta(milliseconds=500) < now:
        print("\r'{}': {}".format(command_str, anim_frames[counter]), end='')
        counter += 1
        counter %= len(anim_frames)
        last_check = now
    time.sleep(0.1)

out, err = p.communicate()
if p.poll() > 0:
    sys.exit("\r'{}': {} ({})       \n{}".format(command_str, '✗', p.poll(), err.strip()))
else:
    print("\r'{}': {}           ".format(command_str, '✓'))
    if out:
        print(out)
