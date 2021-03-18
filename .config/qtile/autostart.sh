#! /bin/bash
lxsession &
picom --experimental-backends &
nitrogen --restore &
/usr/bin/emacs --daemon &
