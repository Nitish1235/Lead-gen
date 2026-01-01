import axios from 'axios'

// Use relative path for unified deployment (nginx proxies /api to backend)
// In unified deployment, frontend and backend are served from same domain
const getApiBaseURL = () => {
  if (typeof window !== 'undefined') {
    // Browser environment - use relative path (nginx will proxy to backend)
    return '/api'
  }
  // Server-side - use environment variable or default
  return process.env.NEXT_PUBLIC_API_URL || '/api'
}

const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 30000,
})

export interface Lead {
  country: string
  city: string
  category: string
  business_name: string
  phone: string
  email: string
  website: string
  address: string
  rating: number | string
  review_count: number
  lead_score: number
  value_justification: string
  run_id: string
  timestamp: string
}

export interface DiscoveryStatus {
  is_running: boolean
  run_id: string | null
  current_country: string | null
  current_city: string | null
  current_category: string | null
}

export interface DiscoveryRequest {
  country: string
  city: string
  categories?: string[]
}

export const apiClient = {
  async getStatus(): Promise<DiscoveryStatus> {
    const response = await api.get('/status')
    return response.data
  },

  async startDiscovery(request: DiscoveryRequest): Promise<{ success: boolean; message?: string }> {
    const response = await api.post('/start', request)
    return response.data
  },

  async stopDiscovery(): Promise<{ success: boolean }> {
    const response = await api.post('/stop')
    return response.data
  },

  async getLeads(runId?: string): Promise<Lead[]> {
    const params = runId ? { run_id: runId } : {}
    const response = await api.get('/leads', { params })
    return response.data
  },

  async getCountries(): Promise<string[]> {
    const response = await api.get('/countries')
    return response.data
  },

  async getCategories(): Promise<string[]> {
    const response = await api.get('/categories')
    return response.data
  },

  async getStats(): Promise<{
    total_leads: number
    avg_score: number
    by_category: Record<string, number>
    by_country: Record<string, number>
  }> {
    const response = await api.get('/stats')
    return response.data
  },
}

