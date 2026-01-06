import axios from 'axios'

// Determine API base URL based on environment
// In development: point to backend server (usually localhost:8000/api)
// In production (unified deployment): use relative path /api
const getApiBaseURL = () => {
  if (typeof window !== 'undefined') {
    // Browser environment
    // Check if we're in development (Next.js dev server on localhost)
    const isDevelopment = window.location.hostname === 'localhost' || 
                          window.location.hostname === '127.0.0.1' ||
                          window.location.port === '3000'
    
    if (isDevelopment) {
      // Development: backend runs separately on port 8000, use full URL
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      // Ensure it ends with /api if not already
      return backendUrl.endsWith('/api') ? backendUrl : `${backendUrl}/api`
    } else {
      // Production: unified deployment, use relative path
      return '/api'
    }
  }
  // Server-side rendering: use environment variable or default
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  return backendUrl.endsWith('/api') ? backendUrl : `${backendUrl}/api`
}

const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 30000,
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`, config.params || '')
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response ${response.status} from ${response.config.url}:`, response.data)
    return response
  },
  (error) => {
    console.error(`[API] Error ${error.response?.status || 'NO_RESPONSE'} from ${error.config?.url}:`, error.response?.data || error.message)
    return Promise.reject(error)
  }
)

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
    try {
      console.log('[API] Calling getCountries, baseURL:', api.defaults.baseURL)
      const response = await api.get('/countries')
      console.log('[API] getCountries response:', response.data)
      return response.data
    } catch (error: any) {
      console.error('[API] getCountries error:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        fullURL: error.config?.baseURL + error.config?.url
      })
      throw error
    }
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

      async getCities(country: string): Promise<{
        "Tier 1": string[]
        "Tier 2": string[]
        "Tier 3": string[]
      }> {
        const response = await api.get('/cities', { params: { country } })
        return response.data
      },
    }

