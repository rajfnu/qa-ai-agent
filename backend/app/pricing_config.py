"""
Pricing Configuration Loader

Loads pricing data from YAML configuration file and provides
helper functions to access pricing information.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from functools import lru_cache


class PricingConfig:
    """Load and manage pricing configuration from YAML file"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default path relative to this file
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "pricing.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load YAML configuration file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Pricing configuration file not found: {self.config_path}\n"
                f"Please ensure the config/pricing.yaml file exists."
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")

    def reload(self):
        """Reload configuration from file (useful for manual updates)"""
        self.config = self._load_config()

    @property
    def metadata(self) -> Dict:
        """Get metadata (version, last updated, etc.)"""
        return self.config.get('metadata', {})

    @property
    def exchange_rates(self) -> Dict:
        """Get currency exchange rates"""
        return self.config.get('metadata', {}).get('exchange_rates', {})

    def usd_to_aud(self, usd_amount: float) -> float:
        """Convert USD to AUD using configured exchange rate"""
        rate = self.exchange_rates.get('usd_to_aud', 1.54)
        return usd_amount * rate

    # ========== AZURE PRICING ==========

    def get_azure_vm(self, sku: str) -> Optional[Dict]:
        """Get Azure VM pricing by SKU"""
        vms = self.config.get('azure', {}).get('compute', {}).get('virtual_machines', [])
        for vm in vms:
            if vm.get('sku') == sku:
                return vm
        return None

    def get_azure_vm_hourly_cost(self, sku: str, use_reserved: bool = True) -> float:
        """Get hourly cost for Azure VM in AUD"""
        vm = self.get_azure_vm(sku)
        if not vm:
            return 0.0

        pricing = vm.get('pricing', {})
        if use_reserved:
            return pricing.get('reserved_1yr_per_hour_aud', 0.0)
        return pricing.get('payg_per_hour_aud', 0.0)

    def get_azure_storage_cost(self, storage_type: str, tier: str = 'hot') -> float:
        """Get Azure storage cost per GB/month in AUD"""
        storage = self.config.get('azure', {}).get('storage', {})

        if storage_type == 'adls_gen2':
            key = f"{tier}_per_gb_month_aud"
            return storage.get('adls_gen2', {}).get(key, 0.0)
        elif storage_type == 'blob':
            key = f"{tier}_per_gb_month_aud"
            return storage.get('blob_storage', {}).get(key, 0.0)

        return 0.0

    def get_azure_database_cost(self, db_type: str) -> Dict:
        """Get Azure database pricing"""
        databases = self.config.get('azure', {}).get('database', {})
        return databases.get(db_type, {})

    def get_aks_management_cost(self) -> float:
        """Get AKS management cost per hour in AUD"""
        return self.config.get('azure', {}).get('kubernetes', {}).get('aks_management_per_hour_aud', 0.15)

    def get_azure_monitoring_cost(self, service: str) -> float:
        """Get Azure monitoring cost per GB in AUD"""
        monitoring = self.config.get('azure', {}).get('monitoring', {})
        return monitoring.get(f"{service}_per_gb_aud", 0.0)

    # ========== AWS PRICING ==========

    def get_aws_ec2(self, instance_type: str) -> Optional[Dict]:
        """Get AWS EC2 pricing by instance type"""
        instances = self.config.get('aws', {}).get('compute', {}).get('ec2', [])
        for instance in instances:
            if instance.get('type') == instance_type:
                return instance
        return None

    def get_aws_s3_cost(self, storage_class: str = 'standard') -> float:
        """Get AWS S3 cost per GB/month in USD"""
        s3 = self.config.get('aws', {}).get('storage', {}).get('s3', {})
        key = f"{storage_class}_per_gb_month_usd"
        return s3.get(key, 0.0)

    # ========== GCP PRICING ==========

    def get_gcp_compute(self, instance_type: str) -> Optional[Dict]:
        """Get GCP Compute Engine pricing"""
        instances = self.config.get('gcp', {}).get('compute', {}).get('compute_engine', [])
        for instance in instances:
            if instance.get('type') == instance_type:
                return instance
        return None

    # ========== LLM PRICING ==========

    def get_llm_pricing(self, provider: str, model_name: str) -> Optional[Dict]:
        """Get LLM pricing for a specific model"""
        providers = self.config.get('llm_providers', {})
        provider_config = providers.get(provider, {})
        models = provider_config.get('models', [])

        for model in models:
            if model.get('name') == model_name:
                return model
        return None

    def get_llm_input_cost(self, provider: str, model_name: str) -> float:
        """Get LLM input cost per 1M tokens in USD"""
        model = self.get_llm_pricing(provider, model_name)
        if model:
            return model.get('input_per_1m_tokens_usd', 0.0)
        return 0.0

    def get_llm_output_cost(self, provider: str, model_name: str) -> float:
        """Get LLM output cost per 1M tokens in USD"""
        model = self.get_llm_pricing(provider, model_name)
        if model:
            return model.get('output_per_1m_tokens_usd', 0.0)
        return 0.0

    def get_llm_cache_cost(self, provider: str, model_name: str) -> float:
        """Get LLM cache read cost per 1M tokens in USD"""
        model = self.get_llm_pricing(provider, model_name)
        if model:
            return model.get('cache_read_per_1m_tokens_usd', 0.0)
        return 0.0

    def list_llm_models(self, provider: Optional[str] = None) -> List[Dict]:
        """List all LLM models, optionally filtered by provider"""
        providers = self.config.get('llm_providers', {})

        if provider:
            provider_config = providers.get(provider, {})
            return provider_config.get('models', [])

        # Return all models from all providers
        all_models = []
        for prov_name, prov_config in providers.items():
            models = prov_config.get('models', [])
            for model in models:
                model['_provider'] = prov_name
                all_models.append(model)
        return all_models

    # ========== MEMORY SYSTEMS PRICING ==========

    def get_memory_system_pricing(self, memory_type: str) -> Dict:
        """Get pricing for a memory system (redis, cosmos_db, neo4j, in_memory)"""
        memory_systems = self.config.get('memory_systems', {})
        return memory_systems.get(memory_type, {})

    def calculate_memory_cost(self, memory_type: str, capacity_gb: float = 6,
                               ru_per_second: int = 45000, nodes: int = 2) -> float:
        """
        Calculate monthly memory cost based on type and capacity

        Args:
            memory_type: 'redis', 'cosmos_db', 'neo4j', 'in_memory'
            capacity_gb: For Redis (ignored for others)
            ru_per_second: For Cosmos DB (ignored for others)
            nodes: For Neo4j (ignored for others)

        Returns:
            Monthly cost in AUD
        """
        if memory_type == 'in_memory':
            return 0.0

        memory_config = self.get_memory_system_pricing(memory_type)

        if memory_type == 'redis':
            # Find appropriate tier based on capacity
            tiers = memory_config.get('tiers', [])
            for tier in sorted(tiers, key=lambda t: t.get('capacity_gb', 0)):
                if capacity_gb <= tier.get('capacity_gb', 0):
                    return tier.get('cost_per_hour_aud', 0.0) * 730
            # If larger than all tiers, use the largest
            if tiers:
                return tiers[-1].get('cost_per_hour_aud', 0.0) * 730
            return 0.0

        elif memory_type == 'cosmos_db':
            pricing = memory_config.get('pricing', {})
            hourly_cost = (ru_per_second / 100) * pricing.get('ru_per_100_per_hour_aud', 0.012)
            return hourly_cost * 730

        elif memory_type == 'neo4j':
            pricing = memory_config.get('pricing', {})
            cost_per_node_hour = pricing.get('cost_per_node_per_hour_aud', 0.691)
            return cost_per_node_hour * nodes * 730

        return 0.0

    # ========== MCP TOOLS PRICING ==========

    def get_mcp_tool_pricing(self, tool_name: str) -> Optional[Dict]:
        """Get pricing for an MCP tool by name"""
        tools_config = self.config.get('mcp_tools', {})

        # Check servers
        servers = tools_config.get('servers', [])
        for server in servers:
            if server.get('name') == tool_name:
                return server

        # Check functions
        functions = tools_config.get('functions', [])
        for function in functions:
            if function.get('name') == tool_name:
                return function

        return None

    def calculate_mcp_tools_cost(self, selected_tools: List[str],
                                   num_assessments: int = 4000) -> float:
        """
        Calculate monthly cost for selected MCP tools

        Args:
            selected_tools: List of tool names
            num_assessments: Number of assessments per month

        Returns:
            Monthly cost in AUD
        """
        total_cost = 0.0

        for tool_name in selected_tools:
            tool_config = self.get_mcp_tool_pricing(tool_name)
            if not tool_config:
                continue

            if tool_config.get('type') == 'mcp_server':
                # Always-on server cost
                total_cost += tool_config.get('monthly_cost_aud', 0.0)

            elif tool_config.get('type') == 'function':
                # Pay per execution
                calls_per_assessment = tool_config.get('avg_calls_per_assessment', 1)
                total_calls = num_assessments * calls_per_assessment
                cost_per_1k = tool_config.get('cost_per_1k_calls_aud', 0.0)
                total_cost += (total_calls / 1000) * cost_per_1k

        return total_cost

    # ========== DATA SOURCES PRICING ==========

    def get_data_source_pricing(self, source_name: str) -> Optional[Dict]:
        """Get pricing for a data source by name"""
        sources = self.config.get('data_sources', [])
        for source in sources:
            if source.get('name').lower() == source_name.lower():
                return source
        return None

    def get_data_source_cost(self, source_name: str) -> float:
        """Get monthly cost for a data source in USD"""
        source = self.get_data_source_pricing(source_name)
        if source:
            return source.get('estimated_cost_usd_month', 0.0)
        return 0.0

    def list_data_sources(self) -> List[Dict]:
        """List all configured data sources"""
        return self.config.get('data_sources', [])

    # ========== MONITORING PRICING ==========

    def get_monitoring_service_pricing(self, service_name: str) -> Optional[Dict]:
        """Get pricing for a monitoring service"""
        monitoring = self.config.get('monitoring', {})

        # Check Azure Monitor services
        azure_monitor = monitoring.get('azure_monitor', [])
        for service in azure_monitor:
            if service.get('name').lower() == service_name.lower():
                return service

        # Check third-party services
        third_party = monitoring.get('third_party', [])
        for service in third_party:
            if service.get('name').lower() == service_name.lower():
                return service

        return None

    def list_monitoring_services(self) -> List[Dict]:
        """List all monitoring services"""
        monitoring = self.config.get('monitoring', {})
        all_services = []
        all_services.extend(monitoring.get('azure_monitor', []))
        all_services.extend(monitoring.get('third_party', []))
        return all_services


# Singleton instance
@lru_cache(maxsize=1)
def get_pricing_config() -> PricingConfig:
    """Get cached pricing configuration instance"""
    return PricingConfig()


# Convenience functions
def reload_pricing():
    """Reload pricing configuration from file"""
    get_pricing_config.cache_clear()
    return get_pricing_config()
