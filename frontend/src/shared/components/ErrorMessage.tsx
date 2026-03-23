export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="card">
      <p style={{ color: "#b42318", margin: 0 }}>{message}</p>
    </div>
  );
}
