# 17. Helm: Creating Charts & Templating

While consuming public charts is useful, you will quickly need to write your own charts for internal applications.

## Chart Structure

You can bootstrap a new chart using `helm create my-app`. This generates the following structure:

```
my-app/
  Chart.yaml          # A YAML file containing information about the chart
  values.yaml         # The default configuration values for this chart
  charts/             # A directory containing any charts upon which this chart depends
  templates/          # A directory of templates that, when combined with values,
                      # will generate valid Kubernetes manifest files.
```

## Templating in Action

Let's look at how a basic Deployment manifest is transformed into a Helm template.

**Standard K8s Manifest:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
...
```

**Helm Template (`templates/deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
...
```

Notice `{{ .Values.replicaCount }}`. When Helm renders this template, it looks at `values.yaml` to find `replicaCount` and injects it.

**`values.yaml`:**
```yaml
replicaCount: 1
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "latest"
```

## Dry Run & Debugging

Before actually pushing resources to Kubernetes, you should always render the templates locally to ensure the YAML is valid.

```bash
# Render templates locally and spit out YAML
helm template mycoolapp ./my-app

# Connect to K8s, simulate an install, but don't commit changes
helm install mycoolapp ./my-app --dry-run --debug
```

> [!TIP]
> Never hardcode environment-specific values in `templates/`. Always put them in `values.yaml` and override them during deployment (e.g., `values-prod.yaml`).
