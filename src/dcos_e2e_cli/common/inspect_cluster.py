"""
Helpers for showing details of a cluster.
"""

from typing import Any  # noqa: F401
from typing import Dict  # noqa: F401
from dcos_e2e_cli.common.base_classes import ClusterRepresentation
import json
import click
from dcos_e2e_cli.common.variants import get_cluster_variant

def show_cluster_details(
    cluster_id: str,
    cluster_representation: ClusterRepresentation,
) -> None:
    keys = {
        'masters': cluster_representation.masters,
        'agents': cluster_representation.agents,
        'public_agents': cluster_representation.public_agents,
    }

    nodes = {
        key: [
            cluster_representation.to_dict(node_representation=container)
            for container in representation
        ]
        for key, representation in keys.items()
    }

    cluster = cluster_representation.cluster
    dcos_variant = get_cluster_variant(cluster=cluster)
    variant_name = str(dcos_variant if dcos_variant else None)
    master = next(iter(cluster.masters))
    web_ui = 'http://' + str(master.public_ip_address)

    data = {
        'Cluster ID': cluster_id,
        'Web UI': web_ui,
        'Nodes': nodes,
        'SSH Default User': cluster_representation.ssh_default_user,
        'SSH key': str(cluster_representation.ssh_key_path),
        'DC/OS Variant': variant_name,
    }  # type: Dict[str, Any]
    click.echo(
        json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True),
    )
