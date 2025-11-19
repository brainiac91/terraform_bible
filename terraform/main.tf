terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "app" {
  metadata {
    name = "devops-learning-app"
    labels = {
      app = "devops-learning-app"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "devops-learning-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "devops-learning-app"
        }
      }

      spec {
        container {
          image = var.container_image
          name  = "devops-learning-app"
          image_pull_policy = "Never" # Important for local Kind/Minikube usage without registry

          port {
            container_port = 8000
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 3
            period_seconds        = 3
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name = "devops-learning-app-service"
  }
  spec {
    selector = {
      app = kubernetes_deployment.app.metadata.0.labels.app
    }
    port {
      port        = 80
      target_port = 8000
    }
    type = "NodePort"
  }
}
