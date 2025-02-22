import { Link } from "react-router-dom";

export default function SectorCard({ sector }) {
  return (
    <Link to={`/sector/${sector.id}`} className="border p-4 rounded-lg shadow-md hover:shadow-lg transition">
      <h2 className="text-lg font-semibold">{sector.name}</h2>
    </Link>
  );
}
