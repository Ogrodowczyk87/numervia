import type { NewsFeed } from "./newsApi";

export default function NewsMetadata({ snapshot, stale }: { snapshot: NewsFeed; stale: boolean }) {
  const updated = new Date(snapshot.fetched_at).toLocaleString();
  return (
    <p className="mt-3 text-sm text-muted" role="status">
      {snapshot.demo && <span className="mr-2 font-semibold text-brand">Demo news · Synthetic headlines.</span>}{" "}
      {stale && "Showing saved news. "}
      Last updated <time dateTime={snapshot.fetched_at}>{updated}</time>.
    </p>
  );
}
