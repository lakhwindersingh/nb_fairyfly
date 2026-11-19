use anyhow::{bail, Result};
use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug, Clone)]
pub struct PlanNode {
    pub id: String,
    pub dependencies: Vec<String>,
}

pub struct DagScheduler;

impl DagScheduler {
    /// Kahn's algorithm for resolving topological ordering and verifying acyclicity.
    pub fn resolve_execution_order(nodes: &[PlanNode]) -> Result<Vec<String>> {
        let mut in_degree: HashMap<String, usize> = HashMap::new();
        let mut adj: HashMap<String, Vec<String>> = HashMap::new();
        let all_ids: HashSet<String> = nodes.iter().map(|n| n.id.clone()).collect();

        for node in nodes {
            in_degree.entry(node.id.clone()).or_insert(0);
            for dep in &node.dependencies {
                if all_ids.contains(dep) {
                    adj.entry(dep.clone()).or_default().push(node.id.clone());
                    *in_degree.entry(node.id.clone()).or_insert(0) += 1;
                }
            }
        }

        let mut queue: VecDeque<String> = in_degree
            .iter()
            .filter(|&(_, &deg)| deg == 0)
            .map(|(id, _)| id.clone())
            .collect();

        let mut ordered = Vec::new();

        while let Some(current) = queue.pop_front() {
            ordered.push(current.clone());

            if let Some(neighbors) = adj.get(&current) {
                for neighbor in neighbors {
                    if let Some(deg) = in_degree.get_mut(neighbor) {
                        *deg -= 1;
                        if *deg == 0 {
                            queue.push_back(neighbor.clone());
                        }
                    }
                }
            }
        }

        if ordered.len() != nodes.len() {
            bail!("Circular dependency detected in plan execution DAG!");
        }

        Ok(ordered)
    }

    /// Partitions nodes into parallel execution waves
    pub fn partition_waves(nodes: &[PlanNode]) -> Result<Vec<Vec<String>>> {
        let mut in_degree: HashMap<String, usize> = HashMap::new();
        let mut adj: HashMap<String, Vec<String>> = HashMap::new();
        let all_ids: HashSet<String> = nodes.iter().map(|n| n.id.clone()).collect();

        for node in nodes {
            in_degree.entry(node.id.clone()).or_insert(0);
            for dep in &node.dependencies {
                if all_ids.contains(dep) {
                    adj.entry(dep.clone()).or_default().push(node.id.clone());
                    *in_degree.entry(node.id.clone()).or_insert(0) += 1;
                }
            }
        }

        let mut current_wave: Vec<String> = in_degree
            .iter()
            .filter(|&(_, &deg)| deg == 0)
            .map(|(id, _)| id.clone())
            .collect();

        let mut waves = Vec::new();
        let mut processed = 0;

        while !current_wave.is_empty() {
            processed += current_wave.len();
            let mut next_wave = Vec::new();

            for node_id in &current_wave {
                if let Some(neighbors) = adj.get(node_id) {
                    for neighbor in neighbors {
                        if let Some(deg) = in_degree.get_mut(neighbor) {
                            *deg -= 1;
                            if *deg == 0 {
                                next_wave.push(neighbor.clone());
                            }
                        }
                    }
                }
            }

            waves.push(current_wave);
            current_wave = next_wave;
        }

        if processed != nodes.len() {
            bail!("Circular dependency detected in plan waves!");
        }

        Ok(waves)
    }
}
