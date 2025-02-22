import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = "http://127.0.0.1:8000/api/providers/";

export default function EditProfilePage() {
  const { user, token } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || "",
    service_area: user?.service_area || "",
    profile_picture: null,
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, profile_picture: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = new FormData();
    form.append("full_name", formData.full_name);
    form.append("service_area", formData.service_area);
    if (formData.profile_picture) form.append("profile_picture", formData.profile_picture);

    try {
      await axios.patch(`${API_BASE_URL}${user.id}/`, form, {
        headers: { Authorization: `Token ${token}`, "Content-Type": "multipart/form-data" },
      });
      navigate("/dashboard");
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Edit Profile</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} placeholder="Full Name" className="border p-2 rounded w-full" />
        <input type="text" name="service_area" value={formData.service_area} onChange={handleChange} placeholder="Service Area" className="border p-2 rounded w-full" />
        <input type="file" onChange={handleFileChange} className="border p-2 rounded w-full" />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">Save Changes</button>
      </form>
    </div>
  );
}
