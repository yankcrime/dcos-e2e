class TestNodeUpgrade:

    def test_node_upgrade(
        self,
        oss_1_11_installer: Path,
        oss_1_12_installer: Path,
    ) -> None:
        # We use a specific version of Docker on the nodes because else we may
        # hit https://github.com/opencontainers/runc/issues/1175.
        cluster_backend = Docker(docker_version=DockerVersion.v17_12_1_ce)
        with Cluster(cluster_backend=cluster_backend) as cluster:
            cluster.install_dcos_from_path(
                dcos_installer=oss_1_11_installer,
                dcos_config=cluster.base_config,
                ip_detect_path=cluster_backend.ip_detect_path,
            )
            cluster.wait_for_dcos_oss()

            for nodes, role in (
                (cluster.masters, Role.MASTER),
                (cluster.agents, Role.AGENT),
                (cluster.public_agents, Role.PUBLIC_AGENT),
            ):
                for node in nodes:
                    node.upgrade_from_dcos_path(
                        dcos_installer=oss_installer,
                        dcos_config=cluster.base_config,
                        ip_detect_path=cluster_backend.ip_detect_path,
                        role=role,
                    )

            for node in nodes:
                pass
