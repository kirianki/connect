import { Link } from "react-router-dom";

export default function ProviderCard({ provider }) {
  return (
    <Link to={`/provider/${provider.id}`} className="border p-4 rounded-lg shadow-md hover:shadow-lg transition">
      <h2 className="text-lg font-semibold">{provider.full_name}</h2>
      <p className="text-gray-600">{provider.service_area}</p>
    </Link>
  );
}
