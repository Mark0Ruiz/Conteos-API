'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { FiSearch, FiMapPin, FiChevronRight, FiLogOut } from 'react-icons/fi'
import { useAuth } from '@/context/AuthContext'
import { conteosAPI } from '@/lib/api'
import { Sucursal } from '@/types/api'

export default function SeleccionarSucursal() {
  const { user, selectSucursal, logout, isLoading } = useAuth()
  const router = useRouter()

  const [sucursales, setSucursales] = useState<Sucursal[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login')
      return
    }
    if (user && user.NivelUsuario !== 4) {
      router.push('/dashboard')
      return
    }
    if (user) {
      loadSucursales()
    }
  }, [user, isLoading])

  const loadSucursales = async () => {
    try {
      const data = await conteosAPI.getSucursales()
      setSucursales(data)
    } catch {
      setError('Error al cargar las sucursales')
    } finally {
      setLoading(false)
    }
  }

  const handleSelect = (sucursal: Sucursal) => {
    selectSucursal(sucursal)
    router.push('/sucursal')
  }

  const filtered = sucursales.filter(s =>
    s.Sucursales.toLowerCase().includes(search.toLowerCase()) ||
    s.IdCentro.toLowerCase().includes(search.toLowerCase()) ||
    (s.Zona || '').toLowerCase().includes(search.toLowerCase())
  )

  // Agrupar por zona
  const porZona: Record<string, Sucursal[]> = {}
  filtered.forEach(s => {
    const zona = s.Zona || 'Sin zona'
    if (!porZona[zona]) porZona[zona] = []
    porZona[zona].push(s)
  })
  const zonas = Object.keys(porZona).sort()

  if (isLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Seleccionar Sucursal</h1>
            <p className="text-sm text-gray-500">
              {user?.NombreUsuario} — elige la sucursal de trabajo
            </p>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-1 text-sm text-gray-500 hover:text-red-600 transition-colors"
          >
            <FiLogOut className="w-4 h-4" />
            Salir
          </button>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-6 space-y-4">
        {/* Búsqueda */}
        <div className="relative">
          <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar por nombre, ID o zona..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="pl-10 w-full border border-gray-300 rounded-xl py-3 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {filtered.length === 0 && !loading && (
          <p className="text-center text-gray-500 py-12">No se encontraron sucursales</p>
        )}

        {/* Lista agrupada por zona */}
        {zonas.map(zona => (
          <div key={zona}>
            <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-1">
              {zona}
            </h2>
            <div className="bg-white rounded-xl shadow-sm divide-y divide-gray-100 overflow-hidden">
              {porZona[zona].map(sucursal => (
                <button
                  key={sucursal.IdCentro}
                  onClick={() => handleSelect(sucursal)}
                  className="w-full flex items-center gap-4 px-4 py-3 hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <FiMapPin className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{sucursal.Sucursales}</p>
                    <p className="text-sm text-gray-500">ID: {sucursal.IdCentro}</p>
                  </div>
                  <FiChevronRight className="w-5 h-5 text-gray-400 flex-shrink-0" />
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
