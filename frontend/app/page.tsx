'use client'

import { Header } from '@/components/Header'
import { DiscoveryPanel } from '@/components/DiscoveryPanel'
import { LeadsList } from '@/components/LeadsList'
import { StatsDashboard } from '@/components/StatsDashboard'
import { useState, useEffect } from 'react'
import { apiClient, type Lead, type DiscoveryStatus } from '@/lib/api'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'discovery' | 'leads' | 'stats'>('discovery')
  const [status, setStatus] = useState<DiscoveryStatus>({
    is_running: false,
    run_id: null,
    current_country: null,
    current_city: null,
    current_category: null,
  })
  const [leads, setLeads] = useState<Lead[]>([])

  useEffect(() => {
    // Poll for status updates
    const pollInterval = status.is_running ? 3000 : 5000 // Poll every 3s when running, 5s when idle
    
    const statusInterval = setInterval(async () => {
      try {
        const newStatus = await apiClient.getStatus()
        setStatus(newStatus)
        
        // If running, fetch new leads
        if (newStatus.is_running && newStatus.run_id) {
          const newLeads = await apiClient.getLeads(newStatus.run_id)
          setLeads(newLeads)
        }
      } catch (error) {
        console.error('Error fetching status:', error)
      }
    }, pollInterval)

    // Initial fetch
    apiClient.getStatus().then(setStatus).catch(console.error)

    return () => clearInterval(statusInterval)
  }, [status.is_running]) // Re-create interval when running state changes

  const handleDiscoveryStart = async (country: string, city: string, categories?: string[]) => {
    try {
      await apiClient.startDiscovery({ country, city, categories })
      setStatus(prev => ({ ...prev, is_running: true }))
      setLeads([])
      setActiveTab('leads')
    } catch (error) {
      console.error('Error starting discovery:', error)
      alert('Failed to start discovery. Please check the backend API.')
    }
  }

  const handleDiscoveryStop = async () => {
    try {
      await apiClient.stopDiscovery()
      setStatus(prev => ({ ...prev, is_running: false }))
    } catch (error) {
      console.error('Error stopping discovery:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-white dark:bg-gray-900 rounded-lg p-1 shadow-sm border border-gray-200 dark:border-gray-800 w-fit">
            <button
              onClick={() => setActiveTab('discovery')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === 'discovery'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
            >
              Discovery
            </button>
            <button
              onClick={() => setActiveTab('leads')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === 'leads'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
            >
              Leads {leads.length > 0 && `(${leads.length})`}
            </button>
            <button
              onClick={() => setActiveTab('stats')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === 'stats'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
            >
              Statistics
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === 'discovery' && (
            <DiscoveryPanel
              status={status}
              onStart={handleDiscoveryStart}
              onStop={handleDiscoveryStop}
            />
          )}
          {activeTab === 'leads' && (
            <LeadsList leads={leads} status={status} />
          )}
          {activeTab === 'stats' && <StatsDashboard />}
        </div>
      </main>
    </div>
  )
}

