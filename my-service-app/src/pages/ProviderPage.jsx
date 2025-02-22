import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchProviderDetails } from "../api/api";
import Navbar from "../components/Navbar";

export default function ProviderPage() {
  const { providerId } = useParams();
  const [provider, setProvider] = useState(null);

  useEffect(() => {
    fetchProviderDetails(providerId)
      .then(res => setProvider(res.data))
      .catch(console.error);
  }, [providerId]);

  if (!provider) return <p>Loading...</p>;

  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold">{provider.full_name}</h1>
        <p className="text-gray-600">{provider.service_area}</p>

        <h2 className="text-xl font-semibold mt-4">Portfolio</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {provider.portfolio_images?.map((img, index) => (
            <img key={index} src={img} alt="Portfolio" className="rounded-lg shadow-md" />
          ))}
        </div>

        <h2 className="text-xl font-semibold mt-4">Reviews</h2>
        <ul>
          {provider.reviews?.map((review, index) => (
            <li key={index} className="border-b p-2">{review.text}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
