# podiff.py
compare two .po/gettext files for differences

This program can be used to see added, deleted, changed, header messages.
It also has an option to display statistics, to show only the number of differences.

## How to use:
* `podiff.py first.po second.po -s`

It only displays statistics

* `podiff.py first.po second.po -a`

It only displays added messages

* `podiff.py first.po second.po -d`

It only displays deleted messages

* `podiff.py first.po second.po -adgs`

Displays these messages added, deleted, changed, and statistics

Enter the command `podiff.py -h` to see all options

This app is based on https://github.com/amandasaurus/podiff
