'use client'

import { useState, useEffect } from 'react'
import { Play, Square, MapPin, Building2, Search } from 'lucide-react'
import { apiClient, type DiscoveryStatus } from '@/lib/api'

interface DiscoveryPanelProps {
  status: DiscoveryStatus
  onStart: (country: string, city: string, categories?: string[]) => void
  onStop: () => void
}

export function DiscoveryPanel({ status, onStart, onStop }: DiscoveryPanelProps) {
  const [countries, setCountries] = useState<string[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCountry, setSelectedCountry] = useState('')
  const [city, setCity] = useState('')
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    apiClient.getCountries().then(setCountries).catch(console.error)
    apiClient.getCategories().then(setCategories).catch(console.error)
  }, [])

  const filteredCategories = categories.filter(cat =>
    cat.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleStart = () => {
    if (!selectedCountry || !city) {
      alert('Please select a country and enter a city')
      return
    }
    const cats = selectedCategories.length > 0 ? selectedCategories : undefined
    onStart(selectedCountry, city, cats)
  }

  const toggleCategory = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category]
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Panel - Configuration */}
      <div className="lg:col-span-2 space-y-6">
        {/* Country & City Selection */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <h2 className="text-xl font-bold font-display mb-4 text-gray-900 dark:text-gray-100">
            Location Configuration
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <MapPin className="inline h-4 w-4 mr-1" />
                Country
              </label>
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                disabled={status.is_running}
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">Select a country...</option>
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Building2 className="inline h-4 w-4 mr-1" />
                City
              </label>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                disabled={status.is_running}
                placeholder="Enter city name..."
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>
          </div>
        </div>

        {/* Category Selection */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <h2 className="text-xl font-bold font-display mb-4 text-gray-900 dark:text-gray-100">
            Business Categories
          </h2>
          
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search categories..."
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            {selectedCategories.length > 0 
              ? `${selectedCategories.length} selected (leave empty for all)`
              : 'Leave empty to search all categories'
            }
          </div>

          <div className="max-h-96 overflow-y-auto space-y-2">
            {filteredCategories.map(category => (
              <label
                key={category}
                className="flex items-center p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors"
              >
                <input
                  type="checkbox"
                  checked={selectedCategories.includes(category)}
                  onChange={() => toggleCategory(category)}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500 rounded border-gray-300 dark:border-gray-600"
                />
                <span className="ml-3 text-sm text-gray-700 dark:text-gray-300">
                  {category}
                </span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel - Controls & Status */}
      <div className="space-y-6">
        {/* Control Panel */}
        <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl shadow-lg p-6 text-white">
          <h2 className="text-xl font-bold font-display mb-4">Discovery Control</h2>
          
          {status.is_running ? (
            <div className="space-y-4">
              <div className="bg-white/20 rounded-lg p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Status</span>
                  <span className="px-2 py-1 bg-green-500 rounded text-xs font-semibold animate-pulse">
                    Running
                  </span>
                </div>
                {status.current_category && (
                  <div className="text-sm opacity-90">
                    Category: {status.current_category}
                  </div>
                )}
              </div>
              
              <button
                onClick={onStop}
                className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-red-500 hover:bg-red-600 rounded-lg font-semibold transition-colors shadow-md"
              >
                <Square className="h-5 w-5" />
                <span>Stop Discovery</span>
              </button>
            </div>
          ) : (
            <button
              onClick={handleStart}
              disabled={!selectedCountry || !city}
              className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-white text-primary-700 hover:bg-gray-100 rounded-lg font-semibold transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Play className="h-5 w-5" />
              <span>Start Discovery</span>
            </button>
          )}
        </div>

        {/* Quick Stats */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
            Quick Info
          </h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Total Categories</span>
              <span className="font-semibold text-gray-900 dark:text-gray-100">
                {categories.length}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Selected Categories</span>
              <span className="font-semibold text-primary-600 dark:text-primary-400">
                {selectedCategories.length || 'All'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

