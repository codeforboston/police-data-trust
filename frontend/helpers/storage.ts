export function setItem(key: string, value: any) {
  localStorage.setItem(key, JSON.stringify({ value }))
}

export function getItem(key: string): any {
  try {
    return JSON.parse(localStorage.getItem(key)).value
  } catch (e) {
    return null
  }
}

export function removeItem(key: string) {
  localStorage.removeItem(key)
}
