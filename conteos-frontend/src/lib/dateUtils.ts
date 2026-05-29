/**
 * Convierte una fecha del servidor a fecha local sin ajuste de zona horaria
 * Evita que las fechas se muestren con un día de diferencia
 * 
 * @param dateString - Fecha en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:mm:ss)
 * @returns Fecha formateada en español de México
 */
export const formatLocalDate = (dateString: string): string => {
  if (!dateString) return 'N/A'
  
  // Extraer solo la parte de la fecha (YYYY-MM-DD)
  const datePart = dateString.split('T')[0]
  const [year, month, day] = datePart.split('-').map(Number)
  
  // Crear fecha en zona horaria local (sin conversión UTC)
  const date = new Date(year, month - 1, day)
  
  return date.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * Extrae y formatea la hora de una cadena ISO (HH:MM)
 */
export const formatTime = (dateString: string | null | undefined): string => {
  if (!dateString) return ''
  // If it has a T part with time info
  const tIndex = dateString.indexOf('T')
  if (tIndex === -1) return ''
  const timePart = dateString.substring(tIndex + 1, tIndex + 6) // HH:MM
  return timePart
}

/**
 * Convierte una fecha del servidor a formato corto (DD/MM/YYYY)
 */
export const formatShortDate = (dateString: string): string => {
  if (!dateString) return 'N/A'
  
  const datePart = dateString.split('T')[0]
  const [year, month, day] = datePart.split('-').map(Number)
  const date = new Date(year, month - 1, day)
  
  return date.toLocaleDateString('es-MX')
}
