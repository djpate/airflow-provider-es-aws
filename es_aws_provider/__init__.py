def get_provider_info():
    return {
        "package-name": "airflow-provider-es-aws",
        "name": "Elasticsearch AWS Provider",
        "description": "A provider for Elasticsearch that supports AWS V4 signature as auth.", # Required
        "hook-class-names": ["es_aws_provider.hooks.es_aws_hook.EsAWSHook"],
        "versions": ["0.0.1"]
    }