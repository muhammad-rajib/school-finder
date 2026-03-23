type HeroProps = {
  mode: "home" | "results";
};

export function Hero({ mode }: HeroProps) {
  return (
    <section className={`hero hero-${mode}`}>
      <div className="hero-copy">
        <h1>Find Schools Near You</h1>
        <p>Explore detailed information about primary schools in your area</p>
      </div>
    </section>
  );
}
