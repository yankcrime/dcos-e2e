"""
A command that performs a cluster upgrade.
"""

from pathlib import Path

import click

from dcos_e2e.node import Transport
from dcos_e2e_cli.common.options import (
    existing_cluster_id_option,
    verbosity_option,
)
from dcos_e2e_cli.common.arguments import installer_argument
from dcos_e2e_cli.common.upgrade import UPGRADE_HELP
from dcos_e2e_cli.common.utils import check_cluster_id_exists

from ._common import ClusterContainers, existing_cluster_ids
from ._options import node_transport_option


@click.command('upgrade', help=UPGRADE_HELP)
@installer_argument
@existing_cluster_id_option
@node_transport_option
@verbosity_option
def upgrade(
    installer: str,
    cluster_id: str,
    transport: Transport,
    verbose: int,
) -> None:
    installer_path = Path(installer).resolve()

    check_cluster_id_exists(
        new_cluster_id=cluster_id,
        existing_cluster_ids=existing_cluster_ids(),
    )
    cluster_containers = ClusterContainers(
        cluster_id=cluster_id,
        transport=transport,
    )
    cluster = cluster_containers.cluster
    cluster.upgrade_dcos_from_path(dcos_installer=installer_path)
