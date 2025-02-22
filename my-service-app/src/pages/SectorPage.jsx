import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import SubcategoryCard from "../components/SubcategoryCard";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export default function SectorPage() {
  const { sectorId } = useParams();
  const [sector, setSector] = useState(null);
  const [subcategories, setSubcategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const sectorRes = await axios.get(`${API_BASE_URL}/listings/sectors/${sectorId}/`);
        setSector(sectorRes.data);

        const subcategoriesRes = await axios.get(`${API_BASE_URL}/listings/sectors/${sectorId}/subcategories/`);
        setSubcategories(subcategoriesRes.data);
      } catch (error) {
        console.error("Error fetching sector data:", error);
      }
    };
    fetchData();
  }, [sectorId]);

  if (!sector) return <p>Loading...</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">{sector.name}</h1>
      <p className="text-gray-600">{sector.description}</p>

      <h2 className="text-xl font-semibold mt-4">Subcategories</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {subcategories.map((subcategory) => (
          <SubcategoryCard key={subcategory.id} subcategory={subcategory} />
        ))}
      </div>
    </div>
  );
}
