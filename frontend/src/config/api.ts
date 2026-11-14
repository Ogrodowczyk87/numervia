export function apiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE_URL ?? "").trim().replace(/\/+$/, "");
  if (!base) return path;
  const url = new URL(base);
  if ((url.protocol !== "https:" && !(url.protocol === "http:" && ["localhost", "127.0.0.1"].includes(url.hostname)))
    || url.username || url.password || url.search || url.hash || url.pathname !== "/") {
    throw new Error("Invalid API base URL configuration.");
  }
  return `${base}${path}`;
}
