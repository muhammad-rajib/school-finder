export function LoadingBlock({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="card">
      <p className="muted">{label}</p>
    </div>
  );
}
