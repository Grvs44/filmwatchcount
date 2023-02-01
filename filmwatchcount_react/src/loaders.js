import { apiRootPath } from "./constants"

export async function loadData(table, page=1) {
  const request = await fetch(apiRootPath + table)
  return await request.json()
}