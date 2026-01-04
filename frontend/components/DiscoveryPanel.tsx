'use client'

import { useState, useEffect, useMemo } from 'react'
import { Play, Square, MapPin, Building2, Search, CheckSquare, X } from 'lucide-react'
import { apiClient, type DiscoveryStatus } from '@/lib/api'

interface DiscoveryPanelProps {
  status: DiscoveryStatus
  onStart: (country: string, city: string, categories?: string[]) => void
  onStop: () => void
}

// Category groups based on config.py structure
const CATEGORY_GROUPS = [
  {
    id: 'healthcare',
    name: 'Healthcare & Wellness',
    keywords: ['clinic', 'medical', 'doctor', 'hospital', 'veterinary', 'physiotherapy', 'chiropractic', 'orthopedic', 'skin', 'dermatology', 'cosmetic', 'aesthetic', 'fertility', 'ivf', 'diagnostic', 'pathology', 'radiology', 'imaging', 'mental health', 'psychology', 'counseling', 'psychiatry', 'nutritionist', 'dietitian', 'ayurveda', 'homeopathy', 'naturopathy']
  },
  {
    id: 'beauty',
    name: 'Beauty & Personal Care',
    keywords: ['beauty salon', 'hair salon', 'barber', 'nail salon', 'spa', 'massage spa', 'wellness spa', 'esthetician', 'makeup', 'bridal', 'tattoo', 'piercing', 'laser hair removal', 'skin care']
  },
  {
    id: 'fitness',
    name: 'Fitness, Sports & Lifestyle',
    keywords: ['fitness', 'gym', 'crossfit', 'yoga', 'pilates', 'martial arts', 'karate', 'taekwondo', 'dance', 'zumba', 'personal trainer', 'swimming', 'tennis', 'badminton', 'sports academy', 'golf']
  },
  {
    id: 'professional',
    name: 'Professional & Financial Services',
    keywords: ['law firm', 'law office', 'accounting', 'chartered accountant', 'bookkeeping', 'consulting', 'business consultant', 'financial advisor', 'investment advisor', 'insurance', 'tax consultant', 'audit', 'company registration']
  },
  {
    id: 'real-estate',
    name: 'Real Estate & Property',
    keywords: ['real estate', 'property consultant', 'property dealer', 'real estate broker', 'commercial real estate', 'property management', 'rental agency', 'vacation rental']
  },
  {
    id: 'education',
    name: 'Education & Training',
    keywords: ['coaching', 'tutoring', 'private tutor', 'driving school', 'music school', 'dance academy', 'language school', 'english academy', 'computer training', 'coding bootcamp', 'it training', 'exam coaching', 'study abroad', 'career counseling']
  },
  {
    id: 'home-services',
    name: 'Home & Local Services',
    keywords: ['plumber', 'electrician', 'hvac', 'air conditioning', 'handyman', 'carpenter', 'painter', 'interior designer', 'home renovation', 'contractor', 'construction', 'roofer', 'waterproofing', 'landscaping', 'lawn care', 'cleaning', 'house cleaning', 'office cleaning', 'pest control', 'moving', 'packers and movers']
  },
  {
    id: 'automotive',
    name: 'Automotive Services',
    keywords: ['auto repair', 'car mechanic', 'auto service', 'auto body', 'car detailing', 'car wash', 'tire shop', 'battery service', 'vehicle inspection', 'motorcycle repair']
  },
  {
    id: 'hospitality',
    name: 'Food, Hospitality & Travel',
    keywords: ['restaurant', 'fine dining', 'cafe', 'coffee shop', 'bakery', 'pizzeria', 'cloud kitchen', 'catering', 'food truck', 'hotel', 'boutique hotel', 'resort', 'guest house', 'hostel', 'travel agency', 'tour operator', 'tourism']
  },
  {
    id: 'events',
    name: 'Events, Media & Creative',
    keywords: ['photography', 'wedding photographer', 'videography', 'event planner', 'wedding planner', 'event management', 'dj service', 'sound system', 'party rental', 'florist', 'decoration']
  },
  {
    id: 'retail',
    name: 'Retail, D2C & Commerce',
    keywords: ['retail store', 'boutique', 'clothing store', 'fashion boutique', 'shoe store', 'jewelry store', 'optical store', 'furniture store', 'electronics store', 'mobile phone shop', 'computer store', 'pet store', 'organic food store', 'grocery store', 'e-commerce', 'online store']
  },
  {
    id: 'repair',
    name: 'Repair & Technical Services',
    keywords: ['computer repair', 'laptop repair', 'phone repair', 'mobile repair', 'appliance repair', 'ac repair', 'refrigerator repair', 'washing machine repair', 'it service', 'managed it']
  },
  {
    id: 'digital',
    name: 'Digital, Tech & Agencies',
    keywords: ['digital marketing', 'seo agency', 'social media agency', 'performance marketing', 'web design', 'web development', 'software development', 'it consulting', 'automation services', 'ai consulting']
  },
  {
    id: 'manufacturing',
    name: 'Manufacturing & B2B',
    keywords: ['manufacturer', 'manufacturing company', 'fabrication', 'machine shop', 'welding', 'cnc machining', 'industrial supplier', 'packaging', 'printing company']
  },
  {
    id: 'pet',
    name: 'Pet Services',
    keywords: ['pet grooming', 'dog grooming', 'dog daycare', 'pet boarding', 'pet training', 'pet clinic', 'animal hospital']
  }
]

export function DiscoveryPanel({ status, onStart, onStop }: DiscoveryPanelProps) {
  const [countries, setCountries] = useState<string[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCountry, setSelectedCountry] = useState('')
  const [city, setCity] = useState('')
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [activeTab, setActiveTab] = useState<string>('healthcare')
  const [loadingCountries, setLoadingCountries] = useState(true)
  const [countriesError, setCountriesError] = useState<string | null>(null)
  const [cities, setCities] = useState<{ "Tier 1": string[], "Tier 2": string[], "Tier 3": string[] } | null>(null)
  const [loadingCities, setLoadingCities] = useState(false)
  const [citiesError, setCitiesError] = useState<string | null>(null)

  useEffect(() => {
    setLoadingCountries(true)
    setCountriesError(null)
    apiClient.getCountries()
      .then((data) => {
        console.log('Countries loaded:', data, 'Count:', data?.length)
        if (Array.isArray(data) && data.length > 0) {
          setCountries(data)
        } else {
          console.warn('Countries API returned empty or invalid data:', data)
          setCountriesError('No countries available')
          setCountries([])
        }
        setLoadingCountries(false)
      })
      .catch((error) => {
        console.error('Failed to load countries:', error)
        console.error('Error details:', error.response?.data || error.message)
        setCountriesError(error.response?.data?.detail || error.message || 'Failed to load countries')
        setCountries([])
        setLoadingCountries(false)
      })
    
    apiClient.getCategories()
      .then((data) => {
        console.log('Categories loaded:', data)
        setCategories(data)
      })
      .catch((error) => {
        console.error('Failed to load categories:', error)
        setCategories([])
      })
  }, [])

  // Fetch cities when country is selected
  useEffect(() => {
    if (selectedCountry) {
      setLoadingCities(true)
      setCitiesError(null)
      setCity('') // Reset city when country changes
      setCities(null)
      
      apiClient.getCities(selectedCountry)
        .then((data) => {
          console.log('Cities loaded for', selectedCountry, ':', data)
          setCities(data)
          setLoadingCities(false)
        })
        .catch((error) => {
          console.error('Failed to load cities:', error)
          setCitiesError(error.response?.data?.detail || error.message || 'Failed to load cities')
          setCities(null)
          setLoadingCities(false)
        })
    } else {
      setCities(null)
      setCity('')
    }
  }, [selectedCountry])

  // Group categories by their group
  const groupedCategories = useMemo(() => {
    const groups: Record<string, string[]> = {}
    
    CATEGORY_GROUPS.forEach(group => {
      groups[group.id] = categories.filter(cat => 
        group.keywords.some(keyword => cat.toLowerCase().includes(keyword.toLowerCase()))
      )
    })
    
    // Add uncategorized items to a misc group
    const categorized = new Set(Object.values(groups).flat())
    const uncategorized = categories.filter(cat => !categorized.has(cat))
    if (uncategorized.length > 0) {
      groups['other'] = uncategorized
    }
    
    return groups
  }, [categories])

  // Get categories for active tab
  const activeTabCategories = useMemo(() => {
    const tabCats = groupedCategories[activeTab] || []
    if (searchTerm) {
      return tabCats.filter(cat =>
        cat.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }
    return tabCats
  }, [groupedCategories, activeTab, searchTerm])

  // Check if all categories in active tab are selected
  const allSelectedInTab = useMemo(() => {
    if (activeTabCategories.length === 0) return false
    return activeTabCategories.every(cat => selectedCategories.includes(cat))
  }, [activeTabCategories, selectedCategories])

  // Check if some (but not all) categories in active tab are selected
  const someSelectedInTab = useMemo(() => {
    if (activeTabCategories.length === 0) return false
    const selectedCount = activeTabCategories.filter(cat => selectedCategories.includes(cat)).length
    return selectedCount > 0 && selectedCount < activeTabCategories.length
  }, [activeTabCategories, selectedCategories])

  const handleStart = () => {
    if (!selectedCountry || !city) {
      alert('Please select a country and enter a city')
      return
    }
    // If no categories selected, pass undefined to fetch all
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

  const selectAllInTab = () => {
    setSelectedCategories(prev => {
      const newSelection = [...prev]
      activeTabCategories.forEach(cat => {
        if (!newSelection.includes(cat)) {
          newSelection.push(cat)
        }
      })
      return newSelection
    })
  }

  const deselectAllInTab = () => {
    setSelectedCategories(prev => 
      prev.filter(cat => !activeTabCategories.includes(cat))
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
                disabled={status.is_running || loadingCountries}
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">
                  {loadingCountries ? 'Loading countries...' : countriesError ? `Error: ${countriesError}` : 'Select a country...'}
                </option>
                {countries.length === 0 && !loadingCountries && !countriesError && (
                  <option value="" disabled>No countries available</option>
                )}
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              {countriesError && (
                <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                  {countriesError}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Building2 className="inline h-4 w-4 mr-1" />
                City
              </label>
              {!selectedCountry ? (
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  disabled={status.is_running || !selectedCountry}
                  placeholder="Select a country first..."
                  className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 placeholder-gray-400 cursor-not-allowed"
                />
              ) : loadingCities ? (
                <div className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                  Loading cities...
                </div>
              ) : citiesError ? (
                <div className="text-red-500 text-sm p-2 border border-red-300 rounded-lg bg-red-50 dark:bg-red-900/20">
                  Error: {citiesError}
                </div>
              ) : cities ? (
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  disabled={status.is_running}
                  className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="">Select a city...</option>
                  {cities["Tier 1"] && cities["Tier 1"].length > 0 && (
                    <optgroup label="Tier 1 - Major Cities">
                      {cities["Tier 1"].map(cityName => (
                        <option key={cityName} value={cityName}>{cityName}</option>
                      ))}
                    </optgroup>
                  )}
                  {cities["Tier 2"] && cities["Tier 2"].length > 0 && (
                    <optgroup label="Tier 2 - Secondary Cities">
                      {cities["Tier 2"].map(cityName => (
                        <option key={cityName} value={cityName}>{cityName}</option>
                      ))}
                    </optgroup>
                  )}
                  {cities["Tier 3"] && cities["Tier 3"].length > 0 && (
                    <optgroup label="Tier 3 - Smaller Cities">
                      {cities["Tier 3"].map(cityName => (
                        <option key={cityName} value={cityName}>{cityName}</option>
                      ))}
                    </optgroup>
                  )}
                </select>
              ) : (
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  disabled={status.is_running}
                  placeholder="Enter city name manually..."
                  className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              )}
            </div>
          </div>
        </div>

        {/* Category Selection */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold font-display text-gray-900 dark:text-gray-100">
              Business Categories
            </h2>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {selectedCategories.length > 0 
                ? `${selectedCategories.length} selected`
                : 'All categories (none selected)'
              }
            </div>
          </div>

          {/* Category Group Tabs */}
          <div className="mb-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex flex-wrap gap-2 overflow-x-auto pb-2">
              {CATEGORY_GROUPS.map(group => {
                const groupCount = groupedCategories[group.id]?.length || 0
                const selectedInGroup = groupedCategories[group.id]?.filter(cat => 
                  selectedCategories.includes(cat)
                ).length || 0
                const isActive = activeTab === group.id
                
                return (
                  <button
                    key={group.id}
                    onClick={() => {
                      setActiveTab(group.id)
                      setSearchTerm('') // Clear search when switching tabs
                    }}
                    className={`px-4 py-2 rounded-t-lg text-sm font-medium transition-colors whitespace-nowrap ${
                      isActive
                        ? 'bg-primary-500 text-white border-b-2 border-primary-500'
                        : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                    }`}
                  >
                    {group.name}
                    {selectedInGroup > 0 && (
                      <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                        isActive ? 'bg-white/20' : 'bg-primary-500 text-white'
                      }`}>
                        {selectedInGroup}/{groupCount}
                      </span>
                    )}
                  </button>
                )
              })}
              {groupedCategories['other'] && groupedCategories['other'].length > 0 && (
                <button
                  onClick={() => {
                    setActiveTab('other')
                    setSearchTerm('')
                  }}
                  className={`px-4 py-2 rounded-t-lg text-sm font-medium transition-colors whitespace-nowrap ${
                    activeTab === 'other'
                      ? 'bg-primary-500 text-white border-b-2 border-primary-500'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                  }`}
                >
                  Other
                  {groupedCategories['other'].filter(cat => selectedCategories.includes(cat)).length > 0 && (
                    <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                      activeTab === 'other' ? 'bg-white/20' : 'bg-primary-500 text-white'
                    }`}>
                      {groupedCategories['other'].filter(cat => selectedCategories.includes(cat)).length}/{groupedCategories['other'].length}
                    </span>
                  )}
                </button>
              )}
            </div>
          </div>

          {/* Search and Select All Controls */}
          <div className="mb-4 flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder={`Search ${CATEGORY_GROUPS.find(g => g.id === activeTab)?.name || 'categories'}...`}
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={selectAllInTab}
                disabled={allSelectedInTab || activeTabCategories.length === 0}
                className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 text-sm font-medium"
              >
                <CheckSquare className="h-4 w-4" />
                Select All
              </button>
              <button
                onClick={deselectAllInTab}
                disabled={!someSelectedInTab && !allSelectedInTab}
                className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 text-sm font-medium"
              >
                <X className="h-4 w-4" />
                Deselect All
              </button>
            </div>
          </div>

          {/* Category List */}
          <div className="max-h-96 overflow-y-auto space-y-2">
            {activeTabCategories.length === 0 ? (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                {searchTerm ? 'No categories found matching your search' : 'No categories in this group'}
              </div>
            ) : (
              activeTabCategories.map(category => (
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
              ))
            )}
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

