import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import HomePage from "./pages/HomePage";
import SectorPage from "./pages/SectorPage";
import SubcategoryPage from "./pages/SubcategoryPage";
import ProviderPage from "./pages/ProviderPage";
import ProviderDashboard from "./pages/ProviderDashboard";
import LoginPage from "./pages/LoginPage";
import EditProfilePage from "./pages/EditProfilePage";
import UploadPortfolioPage from "./pages/UploadPortfolioPage";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/sector/:sectorId" element={<SectorPage />} />
          <Route path="/subcategory/:subcategoryId" element={<SubcategoryPage />} />
          <Route path="/provider/:providerId" element={<ProviderPage />} />
          <Route path="/dashboard" element={<ProviderDashboard />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/edit-profile" element={<EditProfilePage />} />
          <Route path="/upload-portfolio" element={<UploadPortfolioPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
