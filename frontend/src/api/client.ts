export interface SystemStatusData {
  status: string;
  environment: string;
  timestamp: string;
  database: {
    connected: boolean;
    status: string;
    pool: {
      configured_pool_size: number;
      configured_max_overflow: number;
      current_pool_size: number;
    };
  };
  server: {
    configured_workers: number;
    per_worker_pool_max: number;
    aggregate_api_peak_ceiling: number;
  };
}

export async function fetchSystemStatus(): Promise<SystemStatusData | null> {
  try {
    const response = await fetch('/api/v1/system/status');
    if (!response.ok) return null;
    const json = await response.json();
    return json.data;
  } catch {
    return null;
  }
}

export async function fetchHealth(): Promise<boolean> {
  try {
    const response = await fetch('/api/v1/health');
    if (!response.ok) return false;
    const json = await response.json();
    return json.success === true && json.data.status === 'healthy';
  } catch {
    return false;
  }
}
