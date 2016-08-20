"""
Simple ZFS snapshot rotator thingamajig.


See https://bitbucket.org/mmichele/zfssnap for inspiration.
"""
import os
import sys
import subprocess
import datetime

import click


VERSION = '0.1'


class Snapper(object):
    def __init__(self):
        self.verbose = False
        self.dryrun = False

    def __repr__(self):
        return '<Snapper %r>' % self.pool

    def execute(self, args):
        output = ''
        if self.verbose:
            click.echo(' '.join(args))
        if not self.dryrun:
            output = subprocess.check_output(args)
        return output

    def create_snapshot(self, snapshot_path):
        args = ['/sbin/zfs', 'snapshot', snapshot_path]
        self.execute(args)

    def destroy_snapshot(self, snapshot_path):
        args = ['/sbin/zfs', 'destroy', snapshot_path]
        self.execute(args)

    def get_snapshots(self, dataset=None, tag=None):
        args = ['/sbin/zfs', 'list', '-t', 'snapshot']
        output = self.execute(args)
        snapshots = []
        for line in output.splitlines():
            name, _used, _avail, _refer, _mountpoint = line.split()
            if '@' not in name:
                continue
            if not dataset or dataset in name and not tag or tag in name:
                snapshots.append(name)
         return sorted(snapshots)


pass_snapper = click.make_pass_decorator(Snapper)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Increase verbosity')
@click.option('--dryrun', is_flag=True, help='Show what would happen if executed')
@click.version_option(VERSION)
@click.pass_context
def cli(ctx, verbose, dryrun):
    """Snapper is a command line tool that allows simple rotation of ZFS snapshots.

    This tool makes it easier to manage periodic snapshots for online and offline
    backup.
    """
    ctx.obj = Snapper()
    ctx.obj.verbose = verbose
    ctx.obj.dryrun = dryrun


@cli.command()
@click.argument('dataset', help='full dataset name (includes pool)')
@click.argument('tag', help='snapshot name (daily, hourly, etc)')
@click.argument('count', help='Number of snapshots to keep')
@pass_snapper
def snap(snapper, dataset, tag, count):
    """Make a snapshot.

    This will take a snapshot of the given zfs dataset.  If there are more than
    'count' snapshots, the oldest will be deleted.

    """
    now = datetime.datetime.now()
    snap_name = 'snapper-%s-%s' % (tag, now.isoformat())
    snapshot_path = '%s@%s' % (dataset, snap_name)
    click.echo('Snapshot %s' % snapshot_path)
    existing_snapshots = snapper.get_snapshots(dataset, tag)
    stale_snapshots = existing_snapshots[count-1:]
    for stale_snap in stale_snapshots:
        snapper.destroy_snapshot(stale_snap)
     snapper.create_snapshot(snapshot_path)


@cli.command()
@click.argument('dataset', help='full dataset name (includes pool)')
@click.argument('tag', help='tag to show')
@pass_snapper
def list(snapper, dataset, tag):
    """List current snapshots."""
    existing_snapshots = snapper.get_snapshots(dataset, tag)
    for snapshot in existing_snapshots:
        click.echo(snapshot)


if __name__ == '__main__':
    cli()
