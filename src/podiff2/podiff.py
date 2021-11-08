#! /usr/bin/env python3

import argparse
import polib
from polib import escape

class podiff:
    """this class get tow po file, and return ..."""
    def __init__(self, old_file, new_file):
        self.old_pofile = polib.pofile(old_file)
        self.new_pofile = polib.pofile(new_file)

        self.old_msgs = dict(((entry.msgid, entry.msgid_plural), entry) for entry in self.old_pofile)
        self.new_msgs = dict(((entry.msgid, entry.msgid_plural), entry) for entry in self.new_pofile)

    def diff_add(self):
        added_msgs = set(self.new_msgs.keys()) - set(self.old_msgs.keys())
        return [self.new_msgs[x] for x in added_msgs]

    def diff_delete(self):
        deleted_msgs = set(self.old_msgs.keys()) - set(self.new_msgs.keys())
        return [self.old_msgs[x] for x in deleted_msgs]

    def diff_change(self):
        common_msgs = set(self.old_msgs.keys()) & set(self.new_msgs.keys())

        changed = []
        for common in common_msgs:
            old_msg = self.old_msgs[common]
            new_msg = self.new_msgs[common]

            identical = True
            for attr in ['msgstr', 'msgstr_plural']:
                if getattr(old_msg, attr) != getattr(new_msg, attr):
                    identical = False

            if set(old_msg.flags) != set(new_msg.flags):
                identical = False

            if not identical:
                changed.append({'old':old_msg, 'new':new_msg})
        
        return changed

    def diff_metadata(self):
        added_metadata_keys = set(self.new_pofile.metadata) - set(self.old_pofile.metadata)
        deleted_metadata_keys = set(self.old_pofile.metadata) - set(self.new_pofile.metadata)
        common_metadata_keys = set(self.old_pofile.metadata) & set(self.new_pofile.metadata)

        changed_metadata = []
        for common in common_metadata_keys:
            old_metadata = self.old_pofile.metadata[common]
            new_metadata = self.new_pofile.metadata[common]

            if old_metadata != new_metadata:
                changed_metadata.append({'key': common, 'old':old_metadata, 'new':new_metadata})

        return {
            'added_metadata_keys': [x for x in self.new_pofile.metadata.items() if x[0] in added_metadata_keys],
            'deleted_metadata_keys': [x for x in self.old_pofile.metadata.items() if x[0] in deleted_metadata_keys],
            'changed_metadata': changed_metadata,
        }

def _repr_msgstr_plural(msg):
    string = ""
    for plural in msg.msgstr_plural :
        string += "msgstr[%d]: ⁨%s⁩\n" % (plural, escape(msg.msgstr_plural[plural]))
    return string

def print_add(diff):
    for msg in diff:
        if msg.msgid_plural == '':
            print("Added msg: ⁨%s⁩\n"
                  "   msgstr: ⁨%s⁩\n" % (escape(msg.msgid), escape(msg.msgstr)))
        else:
            print("Added msg: ⁨%s⁩\n"
                  "   plural: ⁨%s⁩\n"
                  "⁨%s⁩\n" % (escape(msg.msgid), escape(msg.msgid_plural), _repr_msgstr_plural(msg)))

def print_delete(diff):
    for msg in diff:
        if msg.msgid_plural == '':
            print("Deleted msg: ⁨%s⁩\n"
                  "     msgstr: ⁨%s⁩\n" % (escape(msg.msgid), escape(msg.msgstr)))
        else:
            print("Deleted msg: ⁨%s⁩\n"
                  "     plural: ⁨%s⁩\n"
                  "⁨%s⁩\n" % (escape(msg.msgid), escape(msg.msgid_plural), _repr_msgstr_plural(msg)))

def print_change(diff):
    for msg in diff:
        old, new = msg['old'], msg['new']

        added_flags = set(new.flags) - set(old.flags)
        deleted_flags = set(old.flags) - set(new.flags)
        if len(added_flags) > 0:
            print("Added flags: ⁨%s⁩" % (",".join(sorted(added_flags))))
        if len(deleted_flags) > 0:
            print("Delete flags: ⁨%s⁩" % (",".join(sorted(deleted_flags))))

        print("Changed msg: ⁨%s⁩" % escape(old.msgid))
        if old.msgid_plural == '':
            if old.msgstr == new.msgstr:
                print("     msgstr: ⁨%s⁩\n" % escape(old.msgstr))
            else:
                print("msgstr  old: ⁨%s⁩\n"
                      "        new: ⁨%s⁩\n" % (escape(old.msgstr), escape(new.msgstr)))
        else:
            if old.msgstr_plural == new.msgstr_plural:
                print("⁨%s⁩\n" % _repr_msgstr_plural(old))
            else:
                print("plural  old:\n⁨%s⁩\n"
                "        new:\n⁨%s⁩\n" % (_repr_msgstr_plural(old), _repr_msgstr_plural(new)))

def print_metadata(diff):
    for key, value in diff['added_metadata_keys']:
        print("New metadata: ⁨%s⁩: ⁨%s⁩\n" % (key, value))

    for key, value in diff['deleted_metadata_keys']:
        print("Deleted metadata: ⁨%s⁩: ⁨%s⁩\n" % (key, value))

    for key in diff['changed_metadata']:
        print("Changed metadata: ⁨%s⁩" % key['key'])
        print("\told: ⁨%s⁩" % key['old'])
        print("\tnew: ⁨%s⁩\n" % key['new'])

def print_status(diff):
    keys = [len(diff.diff_add()), len(diff.diff_delete()), len(diff.diff_change())]
    if all(key == 0 for key in keys):
        print("po files are semantically identical")
    else :
        print("added: %d, deleted: %d, changed: %d" % (keys[0], keys[1], keys[2]))

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--no-ignore-comments')
    parser.add_argument('-a', '--add', action='store_true', help="")
    parser.add_argument('-d', '--delete', action='store_true', help="")
    parser.add_argument('-g', '--change', action='store_true', help="")
    parser.add_argument('-m', '--metadata', action='store_true', help="")
    parser.add_argument('-s', '--status', action='store_true', help="")
    #parser.add_argument('-c', '--color', action='store_true', help="")
    #parser.add_argument('-n', '--number', action='store_true', help="")
    #parser.add_argument('-f', '--fuzze', action='store_true', help="")
    #parser.add_argument('-o', '--obsolete', action='store_true', help="")

    parser.add_argument('old_file')
    parser.add_argument('new_file')
    args = parser.parse_args()

    old_file = args.old_file
    new_file = args.new_file
    diff = podiff(old_file, new_file)

    if args.add:
        print_add(diff.diff_add())

    if args.delete:
        print_delete(diff.diff_delete())

    if args.change:
        print_change(diff.diff_change())

    if args.metadata:
        print_metadata(diff.diff_metadata())

    if args.status:
        print_status(diff)

if __name__ == '__main__':
    main()
