"""
Tools for destroying clusters.
"""

from typing import List

import click
import click_spinner

from cli.common.options import existing_cluster_id_option
from cli.common.utils import check_cluster_id_exists

from ._common import ClusterInstances, existing_cluster_ids
from ._options import aws_region_option


@click.command('destroy-list')
@click.argument(
    'cluster_ids',
    nargs=-1,
    type=str,
)
@aws_region_option
@click.pass_context
def destroy_list(
    ctx: click.core.Context,
    cluster_ids: List[str],
    aws_region: str,
) -> None:
    """
    Destroy clusters.

    To destroy all clusters, run ``dcos-vagrant destroy $(dcos-vagrant list)``.
    """
    for cluster_id in cluster_ids:
        if cluster_id not in existing_cluster_ids(aws_region=aws_region):
            warning = 'Cluster "{cluster_id}" does not exist'.format(
                cluster_id=cluster_id,
            )
            click.echo(warning, err=True)
            continue

        ctx.invoke(
            destroy,
            cluster_id=cluster_id,
            aws_region=aws_region,
        )


@click.command('destroy')
@existing_cluster_id_option
@aws_region_option
def destroy(cluster_id: str, aws_region: str) -> None:
    """
    Destroy a cluster.
    """
    check_cluster_id_exists(
        new_cluster_id=cluster_id,
        existing_cluster_ids=existing_cluster_ids(aws_region=aws_region),
    )
    cluster_instances = ClusterInstances(
        cluster_id=cluster_id,
        aws_region=aws_region,
    )
    with click_spinner.spinner():
        cluster_instances.destroy()
    click.echo(cluster_id)
