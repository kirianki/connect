import { Link } from "react-router-dom";

export default function SubcategoryCard({ subcategory }) {
  return (
    <Link to={`/subcategory/${subcategory.id}`} className="border p-4 rounded-lg shadow-md hover:shadow-lg transition">
      <h2 className="text-lg font-semibold">{subcategory.name}</h2>
    </Link>
  );
}
