

class CommandHandler:
    def queueCommand(self, filters, width):
        user = filters['username']
        headers = filters['headers']

        flags = {
            '-S': 'i',
            '-u': user,
            '-O': ",".join([f'{h}:{width}' for h in headers]),
            '--noheader': ''
        }

        if user:
            cmd = " ".join([f'{key} {val}' for key, val in flags.items()])
        else:
            del flags['-u']
            cmd = " ".join([f'{key} {val}' for key, val in flags.items()])

        return ' '.join(['squeue', cmd])

    def historyCommand(self, filters):
        user = filters['username']
        headers = filters['headers']

        flags = {
            '-u': user,
            '--format': ",".join(headers),
            '--noheader': '',
            '-P': ''
        }

        cmd = " ".join([f'{key} {val}' for key, val in flags.items()])
        return ' '.join(['sacct', cmd, '| grep -v .batch | grep -v .exte'])

    def topCommand(self):
        return 'top -b -n1 | head -30 | tail -24'

    def killSelectedCommand(self, sel=None):
        if sel is None:
            sel = []
        return f'for PID in {" ".join(sel)}; do scancel $PID; done'

    def killAllCommand(self, username):
        return f'scancel -u {username}'
