# Airflow AWS ES Provider

This aims to be a Provider for Airflow that supports AWS V4 Signature Backed Elasticsearch Auth

## Testing

* Install astro cli

then

```bash
python3 -m build
mv dist/airflow_provider_es_aws-0.0.1-py3-none-any.whl ./testing
cd testing
astro dev start
```