# Configuration

Canvas delivery is configured in `<course>/manifests/production.json`. These manifests hold the target instance and hosted-output settings. Mutable IDs and fingerprints for GitOps deployments live on the `canvas-state` branch. Credentials come from environment variables or the protected GitHub environment.

This folder is reserved for future shared configuration. It is not a second runtime configuration source. See [README-BUILDER.md](../README-BUILDER.md) and [cloud setup](../docs/CLOUD_SETUP.md).
