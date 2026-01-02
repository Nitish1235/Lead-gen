'use client'

import { useState } from 'react'
import { Building2, Phone, Mail, Globe, MapPin, Star, TrendingUp, Filter, Download } from 'lucide-react'
import { type Lead, type DiscoveryStatus } from '@/lib/api'
import { cn } from '@/lib/utils'

interface LeadsListProps {
  leads: Lead[]
  status: DiscoveryStatus
}

export function LeadsList({ leads, status }: LeadsListProps) {
  const [filterScore, setFilterScore] = useState<number | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedLead, setExpandedLead] = useState<string | null>(null)

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.business_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.city.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesScore = filterScore === null || lead.lead_score >= filterScore
    return matchesSearch && matchesScore
  })

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20'
    if (score >= 60) return 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20'
    if (score >= 40) return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20'
    return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800'
  }

  const exportToCSV = () => {
    const headers = ['Business Name', 'Category', 'City', 'Country', 'Phone', 'Email', 'Website', 'Address', 'Rating', 'Review Count', 'Lead Score']
    const rows = filteredLeads.map(lead => [
      lead.business_name,
      lead.category,
      lead.city,
      lead.country,
      lead.phone,
      lead.email,
      lead.website,
      lead.address,
      lead.rating,
      lead.review_count,
      lead.lead_score
    ])
    
    const csv = [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `leads-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Header & Filters */}
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold font-display text-gray-900 dark:text-gray-100">
              Discovered Leads
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {filteredLeads.length} of {leads.length} leads
            </p>
          </div>
          
          {leads.length > 0 && (
            <button
              onClick={exportToCSV}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Export CSV</span>
            </button>
          )}
        </div>

        <div className="mt-4 flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by business name, category, or city..."
              className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>
          
          <select
            value={filterScore || ''}
            onChange={(e) => setFilterScore(e.target.value ? Number(e.target.value) : null)}
            className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Scores</option>
            <option value="80">80+ (High Quality)</option>
            <option value="60">60+ (Good)</option>
            <option value="40">40+ (Fair)</option>
          </select>
        </div>
      </div>

      {/* Leads Grid */}
      {status.is_running && leads.length === 0 && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-blue-700 dark:text-blue-300 font-medium">Discovery in progress...</p>
          <p className="text-sm text-blue-600 dark:text-blue-400 mt-1">Leads will appear here as they are discovered</p>
        </div>
      )}

      {!status.is_running && leads.length === 0 && (
        <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-800">
          <Building2 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No leads found yet</p>
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">Start a discovery to find leads</p>
        </div>
      )}

      {filteredLeads.length > 0 && (
        <div className="grid grid-cols-1 gap-4">
          {filteredLeads.map((lead, index) => (
            <div
              key={`${lead.business_name}-${index}`}
              className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <Building2 className="h-5 w-5 text-primary-500" />
                      <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                        {lead.business_name}
                      </h3>
                    </div>
                    
                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-4">
                      <span className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        {lead.city}, {lead.country}
                      </span>
                      <span>{lead.category}</span>
                      {lead.rating && (
                        <span className="flex items-center">
                          <Star className="h-4 w-4 mr-1 text-yellow-500 fill-yellow-500" />
                          {lead.rating} ({lead.review_count} reviews)
                        </span>
                      )}
                    </div>

                    <div className="flex flex-wrap gap-3 mb-4">
                      {lead.phone && (
                        <a
                          href={`tel:${lead.phone}`}
                          className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                        >
                          <Phone className="h-4 w-4" />
                          <span>{lead.phone}</span>
                        </a>
                      )}
                      {lead.email && (
                        <a
                          href={`mailto:${lead.email}`}
                          className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                        >
                          <Mail className="h-4 w-4" />
                          <span>{lead.email}</span>
                        </a>
                      )}
                      {lead.website && (
                        <a
                          href={lead.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                        >
                          <Globe className="h-4 w-4" />
                          <span>Website</span>
                        </a>
                      )}
                    </div>
                  </div>

                  <div className="ml-4">
                    <div className={cn(
                      "px-4 py-2 rounded-lg font-bold text-lg text-center",
                      getScoreColor(lead.lead_score)
                    )}>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="h-5 w-5" />
                        <span>{lead.lead_score}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {lead.address && (
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                      <MapPin className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                      {lead.address}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

