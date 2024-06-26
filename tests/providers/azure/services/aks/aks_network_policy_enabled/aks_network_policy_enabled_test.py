from unittest import mock
from uuid import uuid4

from tests.providers.azure.azure_fixtures import AZURE_SUBSCRIPTION


class Test_aks_network_policy_enabled:
    def test_aks_no_subscriptions(self):
        aks_client = mock.MagicMock

        with mock.patch(
            "prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled.aks_client",
            new=aks_client,
        ):
            from prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled import (
                aks_network_policy_enabled,
            )

            aks_client.clusters = {}

            check = aks_network_policy_enabled()
            result = check.execute()
            assert len(result) == 0

    def test_aks_subscription_empty(self):
        aks_client = mock.MagicMock

        with mock.patch(
            "prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled.aks_client",
            new=aks_client,
        ):
            from prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled import (
                aks_network_policy_enabled,
            )

            aks_client.clusters = {AZURE_SUBSCRIPTION: {}}

            check = aks_network_policy_enabled()
            result = check.execute()
            assert len(result) == 0

    def test_aks_network_policy_enabled(self):
        aks_client = mock.MagicMock
        cluster_id = str(uuid4())

        with mock.patch(
            "prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled.aks_client",
            new=aks_client,
        ):
            from prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled import (
                aks_network_policy_enabled,
            )
            from prowler.providers.azure.services.aks.aks_service import Cluster

            aks_client.clusters = {
                AZURE_SUBSCRIPTION: {
                    cluster_id: Cluster(
                        name="cluster_name",
                        public_fqdn="public_fqdn",
                        private_fqdn=None,
                        network_policy="network_policy",
                        agent_pool_profiles=[
                            mock.MagicMock(enable_node_public_ip=False)
                        ],
                        rbac_enabled=True,
                    )
                }
            }

            check = aks_network_policy_enabled()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"Network policy is enabled for cluster 'cluster_name' in subscription '{AZURE_SUBSCRIPTION}'."
            )
            assert result[0].resource_name == "cluster_name"
            assert result[0].resource_id == cluster_id
            assert result[0].subscription == AZURE_SUBSCRIPTION

    def test_aks_network_policy_disabled(self):
        aks_client = mock.MagicMock
        cluster_id = str(uuid4())

        with mock.patch(
            "prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled.aks_client",
            new=aks_client,
        ):
            from prowler.providers.azure.services.aks.aks_network_policy_enabled.aks_network_policy_enabled import (
                aks_network_policy_enabled,
            )
            from prowler.providers.azure.services.aks.aks_service import Cluster

            aks_client.clusters = {
                AZURE_SUBSCRIPTION: {
                    cluster_id: Cluster(
                        name="cluster_name",
                        public_fqdn="public_fqdn",
                        private_fqdn=None,
                        network_policy=None,
                        agent_pool_profiles=[
                            mock.MagicMock(enable_node_public_ip=False)
                        ],
                        rbac_enabled=True,
                    )
                }
            }

            check = aks_network_policy_enabled()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"Network policy is not enabled for cluster 'cluster_name' in subscription '{AZURE_SUBSCRIPTION}'."
            )
            assert result[0].resource_name == "cluster_name"
            assert result[0].resource_id == cluster_id
            assert result[0].subscription == AZURE_SUBSCRIPTION
