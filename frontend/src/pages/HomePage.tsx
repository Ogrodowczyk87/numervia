import PlatformIntro from "../components/PlatformIntro";
import FinancialVideos from "../features/videos/FinancialVideos";
import FinancialNews from "../features/news/FinancialNews";
import PlannedModules from "../components/PlannedModules";

export default function HomePage() {
  return (
    <>
      <FinancialNews />
      <FinancialVideos />
      <PlatformIntro />

      <PlannedModules />
    </>
  );
}
