"""
Tools for destroying sidecar containers.
"""

import sys

import click
from halo import Halo

from dcos_e2e.docker_utils import DockerLoopbackVolume

from ._common import loopback_sidecars_by_name


@click.command('destroy-loopback-sidecar')
@click.argument('name', type=str)
@Halo(enabled=sys.stdout.isatty())
def destroy_loopback_sidecar(name: str) -> None:
    """
    Destroy a loopback sidecar.
    """
    loopback_sidecars = loopback_sidecars_by_name(name=name)

    if not loopback_sidecars:
        message = 'Loopback sidecar "{name}" does not exist'.format(
            name=name,
        )
        raise click.BadParameter(message)

    [loopback_sidecar] = loopback_sidecars
    DockerLoopbackVolume.destroy(container=loopback_sidecar)
