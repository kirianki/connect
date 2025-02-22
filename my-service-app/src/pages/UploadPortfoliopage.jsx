import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/providers/";

export default function UploadPortfolioPage() {
  const { user, token } = useContext(AuthContext);
  const [images, setImages] = useState([]);

  const handleFileChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleUpload = async () => {
    const form = new FormData();
    images.forEach((image) => form.append("portfolio_images", image));

    try {
      await axios.post(`${API_BASE_URL}${user.id}/portfolio-images/`, form, {
        headers: { Authorization: `Token ${token}`, "Content-Type": "multipart/form-data" },
      });
      alert("Images uploaded successfully!");
    } catch (error) {
      console.error("Error uploading images:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Upload Portfolio Images</h1>
      <input type="file" multiple onChange={handleFileChange} className="border p-2 rounded w-full" />
      <button onClick={handleUpload} className="bg-green-500 text-white p-2 rounded mt-4">Upload</button>
    </div>
  );
}
