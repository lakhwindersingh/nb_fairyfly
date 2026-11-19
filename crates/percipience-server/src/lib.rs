use axum::{
    routing::get,
    Json, Router,
};
use serde_json::{json, Value};

pub fn create_router() -> Router {
    Router::new()
        .route("/health", get(health_handler))
        .route("/api/commercial/tiers", get(tiers_handler))
        .route("/api/observability/workflows", get(workflows_handler))
}

async fn health_handler() -> Json<Value> {
    Json(json!({
        "status": "UP",
        "engine": "percipience-server (Axum/Tokio)",
        "version": "3.0.0"
    }))
}

async fn tiers_handler() -> Json<Value> {
    Json(json!({
        "tiers": [
            { "name": "Free Community", "tier": "plan_free", "seats": 1, "price_usd": 0 },
            { "name": "Team", "tier": "plan_team", "seats": 15, "price_usd": 1499 },
            { "name": "Business", "tier": "plan_business", "seats": 50, "price_usd": 4499 },
            { "name": "Enterprise Dedicated", "tier": "plan_enterprise", "seats": "unlimited", "price_usd": 9999 }
        ]
    }))
}

async fn workflows_handler() -> Json<Value> {
    Json(json!({
        "workflows": [
            "pr_gatekeeper",
            "sequential_plan_orchestrator",
            "saas_portal_delivery_flow",
            "commercial_packaging_provisioning_flow"
        ]
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::body::Body;
    use axum::http::{Request, StatusCode};
    use tower::ServiceExt;

    #[tokio::test]
    async fn test_health_endpoint() {
        let app = create_router();
        let response = app
            .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_tiers_endpoint() {
        let app = create_router();
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/commercial/tiers")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }
}
