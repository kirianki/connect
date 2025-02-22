import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SectorPage from "./pages/SectorPage";
import SubcategoryPage from "./pages/SubcategoryPage";
import ProviderPage from "./pages/ProviderPage";
import ProviderDashboard from "./pages/ProviderDashboard";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sector/:sectorId" element={<SectorPage />} />
        <Route path="/subcategory/:subcategoryId" element={<SubcategoryPage />} />
        <Route path="/provider/:providerId" element={<ProviderPage />} />
        <Route path="/dashboard" element={<ProviderDashboard />} />
      </Routes>
    </Router>
  );
}
