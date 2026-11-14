import { afterEach, expect, test, vi } from "vitest";
import { apiUrl } from "../src/config/api";

afterEach(() => vi.unstubAllEnvs());

test.each(["", "https://api.example.com", "https://api.example.com/"])("builds an API URL for base %s", (base) => {
  vi.stubEnv("VITE_API_BASE_URL", base);
  expect(apiUrl("/api/v1/news?feed=housing")).toBe(`${base.replace(/\/$/, "")}/api/v1/news?feed=housing`);
});

test.each(["http://api.example.com", "https://user:secret@example.com", "https://example.com/api", "https://example.com?key=secret"])("rejects invalid base %s", (base) => {
  vi.stubEnv("VITE_API_BASE_URL", base);
  expect(() => apiUrl("/api/v1/health")).toThrow();
});
