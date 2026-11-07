export default function Footer() {
  return (
    <footer className="mx-auto mt-10 flex max-w-7xl flex-col gap-3 border-t border-line px-4 py-8 text-sm sm:flex-row sm:items-center sm:justify-between sm:px-6">
      <a href="/" className="text-lg font-bold"><span aria-hidden="true" className="mr-2 text-brand">∿</span>Numervia</a>
      <p className="text-muted">Finance simulation & operations for a clearer financial future.</p>
      <p className="text-soft">Python · React · TypeScript</p>
    </footer>
  );
}
