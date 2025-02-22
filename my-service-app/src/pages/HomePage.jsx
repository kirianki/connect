import { useEffect, useState } from "react";
import { fetchSectors, searchProviders } from "../api/api";
import SectorCard from "../components/SectorCard";
import SearchBar from "../components/SearchBar";
import Navbar from "../components/Navbar";

export default function HomePage() {
  const [sectors, setSectors] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    fetchSectors().then(res => setSectors(res.data)).catch(console.error);
  }, []);

  const handleSearch = (query) => {
    searchProviders(`search=${query}`)
      .then(res => setSearchResults(res.data))
      .catch(console.error);
  };

  return (
    <div>
      <Navbar />
      <SearchBar onSearch={handleSearch} />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Explore Sectors</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {sectors.map(sector => <SectorCard key={sector.id} sector={sector} />)}
        </div>
      </div>
    </div>
  );
}
