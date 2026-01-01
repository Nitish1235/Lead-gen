'use client'

import { useEffect, useState } from 'react'
import { TrendingUp, Building2, MapPin, BarChart3, Award } from 'lucide-react'
import { apiClient } from '@/lib/api'

export function StatsDashboard() {
  const [stats, setStats] = useState<{
    total_leads: number
    avg_score: number
    by_category: Record<string, number>
    by_country: Record<string, number>
  } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiClient.getStats()
        setStats(data)
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
    const interval = setInterval(fetchStats, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-800">
        <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 dark:text-gray-400">No statistics available yet</p>
      </div>
    )
  }

  const topCategories = Object.entries(stats.by_category)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)

  const topCountries = Object.entries(stats.by_country)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Building2 className="h-8 w-8 opacity-90" />
            <TrendingUp className="h-6 w-6 opacity-75" />
          </div>
          <div className="text-3xl font-bold mb-1">{stats.total_leads}</div>
          <div className="text-sm opacity-90">Total Leads</div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-700 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Award className="h-8 w-8 opacity-90" />
            <TrendingUp className="h-6 w-6 opacity-75" />
          </div>
          <div className="text-3xl font-bold mb-1">{stats.avg_score.toFixed(1)}</div>
          <div className="text-sm opacity-90">Average Score</div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-700 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <BarChart3 className="h-8 w-8 opacity-90" />
            <TrendingUp className="h-6 w-6 opacity-75" />
          </div>
          <div className="text-3xl font-bold mb-1">{Object.keys(stats.by_category).length}</div>
          <div className="text-sm opacity-90">Categories</div>
        </div>
      </div>

      {/* Top Categories & Countries */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <h3 className="text-xl font-bold font-display mb-4 text-gray-900 dark:text-gray-100">
            Top Categories
          </h3>
          <div className="space-y-3">
            {topCategories.length > 0 ? (
              topCategories.map(([category, count]) => (
                <div key={category} className="flex items-center justify-between">
                  <span className="text-gray-700 dark:text-gray-300">{category}</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full"
                        style={{ width: `${(count / stats.total_leads) * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-900 dark:text-gray-100 w-8 text-right">
                      {count}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 dark:text-gray-400 text-sm">No data available</p>
            )}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <h3 className="text-xl font-bold font-display mb-4 text-gray-900 dark:text-gray-100">
            Top Countries
          </h3>
          <div className="space-y-3">
            {topCountries.length > 0 ? (
              topCountries.map(([country, count]) => (
                <div key={country} className="flex items-center justify-between">
                  <span className="flex items-center text-gray-700 dark:text-gray-300">
                    <MapPin className="h-4 w-4 mr-2" />
                    {country}
                  </span>
                  <div className="flex items-center space-x-2">
                    <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${(count / stats.total_leads) * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-900 dark:text-gray-100 w-8 text-right">
                      {count}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 dark:text-gray-400 text-sm">No data available</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

