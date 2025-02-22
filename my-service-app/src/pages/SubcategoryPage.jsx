import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchProviders } from "../api/api";
import Navbar from "../components/Navbar";
import ProviderCard from "../components/ProviderCard";

export default function SubcategoryPage() {
  const { subcategoryId } = useParams();
  const [providers, setProviders] = useState([]);

  useEffect(() => {
    fetchProviders(subcategoryId)
      .then(res => setProviders(res.data))
      .catch(console.error);
  }, [subcategoryId]);

  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold">Providers</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {providers.map(provider => <ProviderCard key={provider.id} provider={provider} />)}
        </div>
      </div>
    </div>
  );
}
