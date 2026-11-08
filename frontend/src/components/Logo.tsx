import logo from "../assets/numervia-logo.png";

export default function Logo() {
  return (
    <span className="inline-flex shrink-0 items-center">
      {/* Frame the complete artwork without the PNG's large empty margins. */}
      <svg
        role="img"
        aria-label="Numervia"
        viewBox="60 385 1340 350"
        className="block h-10 w-auto sm:h-14"
      >
        <image href={logo} width="1448" height="1086" />
      </svg>
    </span>
  );
}
