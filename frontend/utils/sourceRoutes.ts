import { Source } from "@/utils/api"

export const generateSourceSlug = (name: string): string =>
  name
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(".", "-")
    .replace(/[^a-z0-9-]/g, "")

export const getSourceIdentifier = (source: Pick<Source, "uid" | "slug" | "name">): string | null =>
  source.uid || source.slug || (source.name ? generateSourceSlug(source.name) : null)

export const getSourceHref = (source: Pick<Source, "uid" | "slug" | "name">): string | null => {
  const identifier = getSourceIdentifier(source)

  return identifier ? `/sources/${identifier}` : null
}
